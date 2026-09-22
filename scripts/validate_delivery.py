"""Fail closed on stale input, wrong geometry, missing assets or local links."""
import csv,re,collections,xml.etree.ElementTree as ET
from PIL import Image
from common import *
def main():
 errors=[];evidence={}
 def check(ok,label):
  if not ok:errors.append(label)
 dims={v['id']:v['value'] for v in D['dimensions']}
 check(sum(dims['chain_x_north'])==sum(dims['chain_x_south'])==15077,'X chain');check(sum(dims['chain_y_west'])==sum(dims['chain_y_east'])==10074,'Y chain')
 degree=collections.Counter(tuple(p) for e in D['edges'] if e['external'] for p in [e['a'],e['b']]);check(all(n==2 for n in degree.values()),'external boundary closed')
 openings_review=[]
 for e in D['edges']:
  total=math.dist(e['a'],e['b']);at=0;parts=0
  for o in sorted(e['openings'],key=lambda o:o['start']):
   check(o['start']>=at and o['start']+o['width']<=total,'opening range '+o['id']);parts+=o['start']-at+o['width'];at=o['start']+o['width'];openings_review.append([o['id'],o['width'],o['width']-60])
  parts+=total-at;check(abs(parts-total)<.001,'wall opening partition '+e['id'])
 evidence['boundary_closed']=all(n==2 for n in degree.values());evidence['openings_nominal_and_frame_deducted_mm']=openings_review
 service_offsets={}
 for v in D['services']:
  x,y,w,h=D['furniture'][v['attached_to']]['box'];distance=math.hypot(max(x-v['x'],0,v['x']-x-w),max(y-v['y'],0,v['y']-y-h));service_offsets[v['id']]=round(distance,1);check(distance<=350,'service detached from furniture '+v['id'])
 evidence['service_offsets_mm']=service_offsets;evidence['original_photo_sha256']=hashfile(ROOT/D['source_image'])
 for fuel in D['fuel_variants']:
  model=json.loads((ROOT/('reports/model_verification_'+fuel+'.json')).read_text(encoding='utf-8'));check(model['passed'],'model actual geometry '+fuel);check(model['layout_sha256']==SHA,'stale model '+fuel);check(model['dependencies']==model_dependencies(),'stale model dependencies '+fuel)
  for ext in ['blend','glb']:check(model[ext+'_sha256']==hashfile(ROOT/('model/157furnish_'+REV+'_'+fuel+'.'+ext)),ext+' changed '+fuel)
  assert_projection_current(json.loads((ROOT/('model/projection_snapshot_'+fuel+'.json')).read_text(encoding='utf-8')))
 for path in ['model/projection_snapshot.json','model/scene_config.json','reports/usage.json','reports/comparison.json','reports/solar.json','reports/onsite_conditions.json']:
  v=json.loads((ROOT/path).read_text(encoding='utf-8'));check(v['layout_sha256']==SHA,'stale '+path)
 idx=json.loads((ROOT/'reports/drawing_index.json').read_text(encoding='utf-8'));check(len(idx)==len(set(n for n,t in idx)),'duplicate sheet')
 png=json.loads((ROOT/'reports/png_state.json').read_text(encoding='utf-8'));check(png['layout_sha256']==SHA,'stale png report')
 footprint_count=0
 for n,t in idx:
  svg=ROOT/'drawings/svg'/n;image=ROOT/'drawings/png'/n.replace('.svg','.png');root=ET.parse(svg).getroot();check(root.attrib.get('data-layout-sha256')==SHA,'stale svg '+n)
  # Candidates intentionally differ; recommended and room sheets must equal current source.
  for r in root.iter():
   if 'data-object' in r.attrib and not n.startswith('06-'):
    object_id=r.attrib['data-object'];expected_box=D['furniture'][object_id]['box']
    if n=='03-chairs_pulled.svg' and object_id.startswith('dining'):expected_box=D['operations']['dining_pull'+object_id[-1]]['box']
    vals=list(map(float,r.attrib['data-mm'].split(',')));check(vals==expected_box,'svg object '+n);footprint_count+=1
    ox,oy,s,cx,top=map(float,r.attrib['data-transform'].split(','));x,y,w,h=vals;expected=[ox+(x-cx)*s,oy+(top-y-h)*s,w*s,h*s];actual=[float(r.attrib[k]) for k in ['x','y','width','height']];check(max(abs(a-b) for a,b in zip(expected,actual))<.001,'actual SVG geometry '+n)
  check(hashfile(svg)==png['assets'][n]['svg_sha256'],'png source '+n);check(hashfile(image)==png['assets'][n]['png_sha256'],'png bytes '+n)
  with Image.open(image) as im:check(im.size==(1800,1250),'png size '+n);im.verify()
 check(footprint_count>len(D['furniture']),'svg coverage')
 for p in (ROOT/'tables').glob('*.csv'):
  with p.open(encoding='utf-8-sig',newline='') as f:
   for row in csv.DictReader(f):check(row['revision']==REV and row['layout_sha256']==SHA,'stale CSV '+p.name)
 with (ROOT/'tables/家具尺寸.csv').open(encoding='utf-8-sig',newline='') as f:
  rows=list(csv.DictReader(f));check(len(rows)==len(D['furniture']),'furniture table count')
  for row in rows:check([float(row[k]) for k in ['X','Y','宽','深']]==D['furniture'][row['ID']]['box'],'furniture CSV '+row['ID'])
 links=0
 for p in [ROOT/'README.md',ROOT/'AGENTS.md',*(ROOT/'docs').glob('*.md'),*(ROOT/'docs').glob('*.html')]:
  content=p.read_text(encoding='utf-8');urls=re.findall(r'(?:href|src)="([^"]+)"',content) if p.suffix=='.html' else re.findall(r'\]\(([^)]+)\)',content)
  for url in urls:
   if url.startswith(('http:','https:','#','data:')):continue
   path=(p.parent/url.split('#')[0]).resolve();generated_here={(ROOT/'reports'/n).resolve() for n in ['delivery.json','manifest.json']};check(path.exists() or path in generated_here,'broken link '+str(p.name)+' '+url);links+=1
 evidence.update(drawings=len(idx),tables=len(list((ROOT/'tables').glob('*.csv'))),svg_footprints=footprint_count,local_links=links,model_reopened=True,rendered_3d=False)
 for name in ['repeatability','clean_rebuild']:
  p=ROOT/'reports'/(name+'.json');v=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {};evidence[name+'_passed']=v.get('passed',False) and v.get('layout_sha256')==SHA
 usage=json.loads((ROOT/'reports/usage.json').read_text(encoding='utf-8'))
 check(not usage['fixed_hits'],'recommended fixed conflicts must be resolved')
 check(all(v['passed'] and v['side_passed'] for v in usage['wc_clearances'].values()),'toilet front and side minimum')
 regression=json.loads((ROOT/'reports/regressions.json').read_text(encoding='utf-8'));check(regression['passed'] and regression['layout_sha256']==SHA,'regression checks')
 report=bound({'data_consistency_passed':not errors,'usage_all_states_passed':usage['usage_passed'],'routine_baseline_passed':usage['routine_baseline_passed'],'site_conditions_passed':False,'errors':errors,'evidence':evidence});dump('reports/delivery.json',report)
 manifest={str(p.relative_to(ROOT)).replace('\\','/'):hashfile(p) for folder in ['data','scripts','drawings','tables','model','docs'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in str(p) and not p.name.endswith('.blend1')}
 for n in ['README.md','AGENTS.md','requirements.txt',D['source_image']]:manifest[n]=hashfile(ROOT/n)
 dump('reports/manifest.json',bound({'sha256':manifest}));print(json.dumps(report,ensure_ascii=False))
 if errors:raise RuntimeError('Delivery failed')
if __name__=='__main__':main()
