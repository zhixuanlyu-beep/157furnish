"""Shared mm geometry and source binding. No external project dependencies."""
import json,hashlib,math,itertools,copy,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/layout.json').read_text(encoding='utf-8'))
SHA=hashlib.sha256((ROOT/'data/layout.json').read_bytes()).hexdigest()
REV=D['revision']
FUEL=os.environ.get('FURNISH_FUEL','gas')
MODEL_STEM='157furnish_'+REV+'_'+FUEL
def model_dependencies():
 return {n:hashfile(ROOT/'scripts'/n) for n in ['build_model.py','common.py']}

def assert_projection_current(snapshot):
 assert snapshot['layout_sha256']==SHA,'拒绝过期模型投影'
 assert snapshot.get('dependencies')==model_dependencies(),'建模脚本或依赖已变更，拒绝过期投影'

def candidate_data(c,data=D):
 out=copy.deepcopy(data);changes=c['changes']
 for n in changes.get('remove_furniture',[]):
  out['furniture'].pop(n,None)
  out['operations']={k:v for k,v in out['operations'].items() if v['owner']!=n}
 for field in ['furniture','operations','routes']:
  for n,v in changes.get(field,{}).items():out[field][n]={**out[field].get(n,{}),**v}
 for n in changes.get('restore_original_edges',[]):out['edges'].append(copy.deepcopy(next(e for e in out['original']['edges'] if e['id']==n)))
 # Components must follow changed equipment envelopes; regenerate in a candidate, never reuse R1 positions.
 for n,v in out['operations'].items():
  if n in changes.get('operations',{}) and 'box' in changes['operations'][n]:v.pop('parts',None)
 return out
def dump(path,obj): (ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def bound(obj):return {'revision':REV,'layout_sha256':SHA,**obj}
def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rect(b):x,y,w,h=b;return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
def overlap(a,b,eps=0.1):return min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])>eps and min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1])>eps
def polyhit(a,b):
 for p in (a,b):
  for u,v in zip(p,p[1:]+p[:1]):
   nx,ny=-(v[1]-u[1]),v[0]-u[0];aa=[x*nx+y*ny for x,y in a];bb=[x*nx+y*ny for x,y in b]
   if min(max(aa),max(bb))-max(min(aa),min(bb))<=0.01:return False
 return True
def edge_box(e,start,length):
 x,y=e['a'];horizontal=e['a'][1]==e['b'][1];t=e['thickness']
 return [x+start,y-t/2,length,t] if horizontal else [x-t/2,y+start,t,length]
def walls(data=D):
 out={}
 for e in data['edges']:
  length=math.dist(e['a'],e['b']);at=0
  for i,o in enumerate(sorted(e['openings'],key=lambda o:o['start'])):
   start=o['start'];w=o['width']
   if start>at:out[e['id']+'_'+str(i)]=dict(box=edge_box(e,at,start-at),z=0,height=2700,edge=e['id'])
   if o['sill']:out[e['id']+'_'+str(i)+'_sill']=dict(box=edge_box(e,start,w),z=0,height=o['sill'],edge=e['id'])
   top=o['sill']+o['height']
   if top<2700:out[e['id']+'_'+str(i)+'_lintel']=dict(box=edge_box(e,start,w),z=top,height=2700-top,edge=e['id'])
   at=start+w
  if at<length:out[e['id']+'_end']=dict(box=edge_box(e,at,length-at),z=0,height=2700,edge=e['id'])
 return out
def openings(data=D):
 out={}
 for e in data['edges']:
  for o in e['openings']:
   horizontal=e['a'][1]==e['b'][1];x,y=e['a'];start=o['start']
   b=edge_box(e,start,o['width']);out[o['id']]={**o,'edge':e['id'],'box':b,'horizontal':horizontal,'origin':[x+start,y] if horizontal else [x,y+start]}
 return out
def door_poly(o,angle=90,handle=False):
 x,y=o['origin'];w=o['width']-60;hinge=o['hinge'];h=o['horizontal']
 x+= (30+hinge*w) if h else 0;y+=0 if h else (30+hinge*w)
 a=(0 if h else math.pi/2)+hinge*math.pi+math.radians(angle*o['sign'])
 ux,uy=math.cos(a),math.sin(a);vx,vy=-uy,ux
 s,t=(max(0,w-160),w-60) if handle else (0,w);lo,hi=(20,70) if handle else (-20,20)
 return [(x+ux*k+vx*j,y+uy*k+vy*j) for k,j in [(s,lo),(t,lo),(t,hi),(s,hi)]]
def slide_box(o,opened=False):
 x,y=o['origin'];w=o.get('slide_panel_width',o['width']-60);shift=o.get('slide_shift',o['width']*o.get('slide_dir',1));offset=o.get('slide_offset',80)
 if o['horizontal']:return [x+30+shift*float(opened),y+offset,w,35]
 return [x+offset,y+30+shift*float(opened),35,w]

def slide_fixed_box(o):
 if not o.get('fixed_panel'):return None
 b=slide_box(o,True);b[1 if o['horizontal'] else 0]+=40;return b

def slide_handle_box(o,fraction):
 b=slide_box(o,fraction)
 off=-50 if o.get('slide_offset',80)<0 else 35
 return [b[0]+b[2]-100,b[1]+off,60,50] if o['horizontal'] else [b[0]+off,b[1]+b[3]-100,50,60]
def fixed(data=D):return {**{n:v for n,v in walls(data).items() if v['z']<1800},**{n:v for n,v in data['furniture'].items() if v['kind'] not in ('shower','screen') and v['z']<1800}}
def inside(x,y):
 return any(a<=x<=a+w and b<=y<=b+h for a,b,w,h in D['footprint_boxes'])
def furniture_hits(data=D):
 f=data['furniture'];w=walls(data);hits=[]
 for a,b in itertools.combinations(f,2):
  x,y=f[a],f[b]
  if min(x['z']+x['height'],y['z']+y['height'])<=max(x['z'],y['z']):continue
  if overlap(x['box'],y['box']):hits.append([a,b])
 for a,v in f.items():
  for b,u in w.items():
   if min(v['z']+v['height'],u['z']+u['height'])>max(v['z'],u['z']) and overlap(v['box'],u['box']):hits.append([a,b])
 return hits
def capacity(n,v):
 if v['kind']!='cabinet':return []
 out=[];depth=v['box'][3] if v['front'] in ('north','south') else v['box'][2]
 for i,(width,use) in enumerate(zip(v.get('modules',[]),v.get('contents',[]))):
  net=width-36;rail=net*(2 if '双层' in use else 1) if '挂' in use and depth>=550 and '挂钩' not in use else 0;drawers=3 if '三抽' in use else (2 if '抽屉' in use else 0)
  excluded=any(s in use for s in ['水槽','净水','灶下','蒸烤'])
  litres=round(net*(depth-38)*max(0,min(v['height'],1800)-100)/1e6,1) if not rail and not excluded else 0
  seasonal=round(net*(depth-38)*max(0,v['height']-1800)/1e6,1) if not excluded else 0
  levels=cabinet_levels(v['height'],use)[1] if rail else []
  daily=net*sum(z<=D['assumptions']['daily_rail_height_mm'] for z in levels)
  out.append(dict(cabinet=n,module=i+1,use=use,width=width,net_width=net,net_depth=depth-38,rail_mm=rail,daily_rail_mm=daily,high_rail_mm=rail-daily,rail_heights_mm=str(levels),drawers=drawers,shelf_litres=litres,seasonal_litres=seasonal,access='入口外正面浅取；深处未计' if n=='storage' else '挂杆1700为概念可达高度须试取；1800以上季节性',note='扣设备但未扣活动层板的几何上限；取物可达另查，不承诺实际件数'))
 return out
def cabinet_levels(height,use):
 """Shared interior heights, keeping fixed shelves out of drawer boxes."""
 drawers=[120+180*j for j in range(3 if '三抽' in use else 2 if '抽屉' in use else 0)]
 if '挂' in use:
  top=min(height-180,D['assumptions']['daily_rail_height_mm'])
  shelves=[height-140]+([top/2+50] if '双层' in use else [])
  rails=[top]+([top/2] if '双层' in use else [])
  if '挂钩' in use:rails=[]
 else:
  base=max(100,drawers[-1]+200 if drawers else 100);available=height-120-base
  shelves=[base+available*j/3 for j in range(3)] if available>100 else []
  rails=[]
 return shelves,rails,drawers
