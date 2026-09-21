"""Explicit fixed, sampled operation and grid reachability checks."""
import copy,math,itertools,collections
import numpy as np
from common import *
def route_grid(data,width,state='normal4'):
 step=50;r=width/2;boxes=data['footprint_boxes'];xs=np.arange(0,math.ceil(max(a+w for a,b,w,h in boxes)/step)*step+1,step);ys=np.arange(0,math.ceil(max(b+h for a,b,w,h in boxes)/step)*step+1,step);xx,yy=np.meshgrid(xs,ys)
 # Union should not shrink at internal seams: test four corners of the square against actual outline.
 free=np.ones(xx.shape,dtype=bool)
 for dx,dy in itertools.product([-r,r],repeat=2):
  x,y=xx+dx,yy+dy
  corner_inside=np.zeros(xx.shape,dtype=bool)
  for bx,by,bw,bh in boxes:corner_inside|=(x>=bx)&(x<=bx+bw)&(y>=by)&(y<=by+bh)
  free &= corner_inside
 obs={n:v['box'] for n,v in fixed(data).items()}
 if state=='normal6':obs.update(data['states']['six_extra'])
 if state=='chairs_pulled':
  for n,v in D['operations'].items():
   if n.startswith('dining_pull'):obs[v['owner']]=v['box']
 if state=='laundry_open':obs['laundry_operation']=D['operations']['laundry_use']['box']
 for n,o in openings(data).items():
  if o['kind']=='door':
   for suffix,poly in [('_leaf',door_poly(o)),('_handle',door_poly(o,handle=True))]:
    x=min(p[0] for p in poly);y=min(p[1] for p in poly);obs[n+suffix]=[x,y,max(p[0] for p in poly)-x,max(p[1] for p in poly)-y]
  if o['kind'] in ('door','sliding','passage'):
   b=o['box'];x,y,w,h=b
   if o['horizontal']:obs[n+'_jamb1']=[x,y,30,h];obs[n+'_jamb2']=[x+w-30,y,30,h]
   else:obs[n+'_jamb1']=[x,y,w,30];obs[n+'_jamb2']=[x,y+h-30,w,30]
  # Surface sliding leaves are parked on adjacent wall faces; wide balcony panel overlaps half the opening.
  if o['kind']=='sliding':obs[n+'_parked']=slide_box(o,True)
 for x,y,w,h in obs.values():free &= ~((xx>x-r+.01)&(xx<x+w+r-.01)&(yy>y-r+.01)&(yy<y+h+r-.01))
 return free,step,obs
def find_path(grid,step,start,end):
 s=(round(start[1]/step),round(start[0]/step));t=(round(end[1]/step),round(end[0]/step));ny,nx=grid.shape
 if not grid[s] or not grid[t]:return [],'端点包络受阻'
 q=collections.deque([s]);prev={s:None}
 while q:
  p=q.popleft()
  if p==t:break
  for dy,dx in [(0,1),(1,0),(0,-1),(-1,0)]:
   v=(p[0]+dy,p[1]+dx)
   if 0<=v[0]<ny and 0<=v[1]<nx and grid[v] and v not in prev:prev[v]=p;q.append(v)
 if t not in prev:return [],'50mm网格未找到路线；非连续空间不可达证明'
 path=[];p=t
 while p is not None:path.append([p[1]*step,p[0]*step]);p=prev[p]
 path.reverse();simple=[path[0]]
 for i in range(1,len(path)-1):
  if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):simple.append(path[i])
 simple.append(path[-1]);return simple,'该方形包络可达；门全开，操作区另查'
def verify(data=D,full=True):
 out=bound({'fixed_hits':furniture_hits(data),'door_sweep':{},'operation_fixed_hits':{},'time_shared':[],'routes':[]})
 obs=fixed(data)
 for n,o in openings(data).items():
  if o['kind']!='door':continue
  hits={}
  for angle in range(91):
   for part in ['leaf','handle']:
    poly=door_poly(o,angle,part=='handle')
    for k,v in obs.items():
     if polyhit(poly,rect(v['box'])):hits.setdefault(k+'_'+part,[]).append(angle)
  out['door_sweep'][n]={k:[min(a),max(a)] for k,a in hits.items()}
 for n,v in data['operations'].items():
  excluded={v['owner']}
  if n=='child_pull':excluded.add('deskA')
  out['operation_fixed_hits'][n]=[k for k,f in obs.items() if k not in excluded and overlap(v['box'],f['box'])]
 out['time_shared']=[[a,b] for a,b in itertools.combinations(data['operations'],2) if overlap(data['operations'][a]['box'],data['operations'][b]['box'])]
 for state in (['normal4','normal6','chairs_pulled','laundry_open'] if full else ['normal4']):
  for width in (500,600,620,900):
   grid,step,obstacles=route_grid(data,width,state)
   for name,v in data['routes'].items():
    path,status=find_path(grid,step,v['start'],v['end'])
    out['routes'].append(dict(name=name,width_mm=width,state=state,reachable=bool(path),path=path,status=status))
 # Cabinet leaves sampled at 1 degree; drawer swept rectangles include 450mm extension.
 out['cabinet_motion_hits']={}
 for n,v in data['furniture'].items():
  if v['kind']!='cabinet':continue
  x,y,w,h=v['box'];front=v['front'];span=w if front in ['north','south'] else h;u=0;hits=set()
  for ww,use in zip(v.get('modules',[]),v.get('contents',[])):
   if v.get('door_type')!='sliding':
    leaves=2 if ww>650 else 1
    for j in range(leaves):
     start=u+j*ww/leaves+11;length=ww/leaves-22
     if front in ['south','north']:px,py=x+start,y+9 if front=='south' else y+h-9;a0=0;sgn=-1 if front=='south' else 1
     else:px,py=x+9 if front=='west' else x+w-9,y+start;a0=math.pi/2;sgn=1 if front=='west' else -1
     for angle in range(91):
      a=a0+math.radians(sgn*angle);ux,uy=math.cos(a),math.sin(a);vx,vy=-uy,ux;poly=[(px+ux*k+vx*t,py+uy*k+vy*t) for k,t in [(0,-9),(length,-9),(length,9),(0,9)]]
      for k,f in obs.items():
       if k!=n and f['z']<v['z']+v['height'] and f['z']+f['height']>v['z']+82 and polyhit(poly,rect(f['box'])):hits.add(k+'_door')
   if '三抽' in use or '抽屉' in use:
    b={'south':[x+u,y-450,ww,450],'north':[x+u,y+h,ww,450],'west':[x-450,y+u,450,ww],'east':[x+w,y+u,450,ww]}[front]
    for k,f in obs.items():
     if k!=n and f['z']<v['z']+650 and f['z']+f['height']>v['z']+120 and overlap(b,f['box']):hits.add(k+'_drawer')
   u+=ww
  out['cabinet_motion_hits'][n]=sorted(hits)
 out['routine_baseline_passed']=not out['fixed_hits'] and not any(out['door_sweep'].values()) and not any(out['cabinet_motion_hits'].values()) and all(r['reachable'] for r in out['routes'] if r['width_mm']==500 and r['state']=='normal4') and not any(out['operation_fixed_hits'].values())
 out['usage_passed']=out['routine_baseline_passed'] and all(r['reachable'] for r in out['routes']) and not out['time_shared']
 out['limitations']=['墙、门、家具为概念包络；固定相交按三维高度过滤，床采用含外伸床架。','门扇与50mm把手按1°采样；非连续运动认证。推拉停放包络已计路线；真实轨道/叠片待核。','路线50mm网格、轴对齐方形包络，含门框及全开门；900为目标，不作为强制合格线。','矩形操作区包含人员和门抽屉行程；命中与共享分别披露，不能把所有命中自动当作错时可解。','玻璃隔断设800mm名义入口；扣框五金后的真实入口尚未核定。']
 return out
def main():
 out=verify();dump('reports/usage.json',out)
 comparison=[]
 for c in D['candidates']:
  data=copy.deepcopy(D)
  for k,v in c['changes'].items():
   if k in data['furniture']:data['furniture'][k]['box']=v
   if k=='remove_edge':data['edges']=[e for e in data['edges'] if e['id']!=v]
  result=verify(data,False) if c['id']!='recommended' else out
  comparison.append({**c,'fixed_hits':result['fixed_hits'],'single_routes_passed':sum(r['reachable'] for r in result['routes'] if r['width_mm']==500 and r['state']=='normal4'),'route_count':len(D['routes']),'storage_rail_mm':sum(v['rail_mm'] for n,f in data['furniture'].items() for v in capacity(n,f)),'operation_hits':{k:v for k,v in result['operation_fixed_hits'].items() if v},'note':'候选操作区仍取基线；床候选只核实体/通路，安装及舒适性见方案说明' if c['changes'] else '推荐基线'})
 dump('reports/comparison.json',bound({'priority':['固定实体','必要路线','操作','容量','拆改代价'],'candidates':comparison}))
 print(json.dumps({'fixed':out['fixed_hits'],'door':out['door_sweep'],'operations':{k:v for k,v in out['operation_fixed_hits'].items() if v},'normal500_fail':[r['name'] for r in out['routes'] if not r['reachable'] and r['width_mm']==500 and r['state']=='normal4']},ensure_ascii=False))
if __name__=='__main__':main()
