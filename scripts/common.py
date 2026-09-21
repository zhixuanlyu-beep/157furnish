"""Shared mm geometry and source binding. No external project dependencies."""
import json,hashlib,math,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/layout.json').read_text(encoding='utf-8'))
SHA=hashlib.sha256((ROOT/'data/layout.json').read_bytes()).hexdigest()
REV=D['revision']
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
 x,y=o['origin'];w=o['width'];shift=(w*.5 if w>1800 else w)*o.get('slide_dir',1)
 if o['horizontal']:return [x+(shift if opened else 0),y+80,w,35]
 return [x+80,y+(shift if opened else 0),35,w]
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
  net=width-36;rail=net*(2 if '双层' in use else 1) if '挂' in use else 0;drawers=3 if '三抽' in use else (2 if '抽屉' in use else 0)
  out.append(dict(cabinet=n,module=i+1,use=use,width=width,net_width=net,net_depth=depth-38,rail_mm=rail,drawers=drawers,shelf_litres=round(net*(depth-38)*max(0,v['height']-100)/1e6,1) if not rail else 0,note='容积为未扣活动层板的几何上限；非实际件数承诺'))
 return out
def cabinet_levels(height,use):
 """Shared interior heights, keeping fixed shelves out of drawer boxes."""
 drawers=[120+180*j for j in range(3 if '三抽' in use else 2 if '抽屉' in use else 0)]
 if '挂' in use:
  shelves=[height-140]+([height/2+20] if '双层' in use else [])
  rails=[height-180]+([height/2-60] if '双层' in use else [])
 else:
  base=max(100,drawers[-1]+200 if drawers else 100);available=height-120-base
  shelves=[base+available*j/3 for j in range(3)] if available>100 else []
  rails=[]
 return shelves,rails,drawers
