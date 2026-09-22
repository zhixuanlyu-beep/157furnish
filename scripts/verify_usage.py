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
  for n,v in data['operations'].items():
   if n.startswith('dining_pull'):obs[v['owner']]=v['box']
 if state=='laundry_open':obs['laundry_moving']=data['operations']['laundry_use'].get('parts',{}).get('moving',data['operations']['laundry_use']['box'])
 if state in ['temporary_drying','cooking','luggage_open','screen_lowered']:obs.update(data['states'][state])
 for n,o in openings(data).items():
  if o['kind']=='door':
   for suffix,poly in [('_leaf',door_poly(o)),('_handle',door_poly(o,handle=True))]:
    x=min(p[0] for p in poly);y=min(p[1] for p in poly);obs[n+suffix]=[x,y,max(p[0] for p in poly)-x,max(p[1] for p in poly)-y]
  if o['kind'] in ('door','sliding','passage'):
   b=o['box'];x,y,w,h=b
   if o['horizontal']:obs[n+'_jamb1']=[x,y,30,h];obs[n+'_jamb2']=[x+w-30,y,30,h]
   else:obs[n+'_jamb1']=[x,y,w,30];obs[n+'_jamb2']=[x,y+h-30,w,30]
  # Surface sliding leaves are parked on adjacent wall faces; wide balcony panel overlaps half the opening.
  if o['kind']=='sliding':
   obs[n+'_parked']=slide_box(o,True);obs[n+'_handle']=slide_handle_box(o,1)
   if slide_fixed_box(o):obs[n+'_fixed']=slide_fixed_box(o)
 for x,y,w,h in obs.values():free &= ~((xx>x-r+.01)&(xx<x+w+r-.01)&(yy>y-r+.01)&(yy<y+h+r-.01))
 return free,step,obs
def find_path(grid,step,start,end,target_box=None,width=0):
 s=(round(start[1]/step),round(start[0]/step));t=(round(end[1]/step),round(end[0]/step));ny,nx=grid.shape
 if not(0<=s[0]<ny and 0<=s[1]<nx) or not grid[s]:return [],'起点包络受阻'
 if target_box:
  x,y,w,h=target_box;r=width/2
  targets={(iy,ix) for iy in range(max(0,math.ceil((y+r)/step)),min(ny,math.floor((y+h-r)/step)+1)) for ix in range(max(0,math.ceil((x+r)/step)),min(nx,math.floor((x+w-r)/step)+1)) if grid[iy,ix]}
 else:targets={t} if 0<=t[0]<ny and 0<=t[1]<nx and grid[t] else set()
 if not targets:return [],'目标区域无完整可站立包络（含墙/家具/当前开启件）'
 q=collections.deque([s]);prev={s:None}
 while q:
  p=q.popleft()
  if p in targets:t=p;break
  for dy,dx in [(0,1),(1,0),(0,-1),(-1,0)]:
   v=(p[0]+dy,p[1]+dx)
   if 0<=v[0]<ny and 0<=v[1]<nx and grid[v] and v not in prev:prev[v]=p;q.append(v)
 else:return [],'目标区可站立但50mm网格路线受阻；非连续空间不可达证明'
 path=[];p=t
 while p is not None:path.append([p[1]*step,p[0]*step]);p=prev[p]
 path.reverse();simple=[path[0]]
 for i in range(1,len(path)-1):
  if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):simple.append(path[i])
 simple.append(path[-1]);return simple,'该方形包络可达；门全开，操作区另查'
def verify(data=D,full=True):
 out=bound({'fixed_hits':furniture_hits(data),'door_sweep':{},'sliding_sweep':{},'operation_fixed_hits':{},'operation_components':{},'time_shared':[],'routes':[]})
 obs=fixed(data)
 for n,o in openings(data).items():
  if o['kind']=='sliding':
   hits={};outside=[]
   for fraction in range(101):
    for part,b in [('leaf',slide_box(o,fraction/100)),('handle',slide_handle_box(o,fraction/100))]:
     if not all(any(a<=x<=a+w and c<=y<=c+h for a,c,w,h in data['footprint_boxes']) for x,y in rect(b)):outside.append(fraction)
     for k,v in obs.items():
      if overlap(b,v['box']):hits.setdefault(k+'_'+part,[]).append(fraction)
   out['sliding_sweep'][n]={'hits':{k:[min(a),max(a)] for k,a in hits.items()},'outside_samples':sorted(set(outside)),'parked_box':slide_box(o,True),'sampling':'101 positions; leaf + 50mm handle; jamb allowance 30mm'}
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
  out['operation_components'][n]={part:{'box':b,'fixed_hits':[k for k,f in obs.items() if k not in excluded and overlap(b,f['box'])]} for part,b in v.get('parts',{'operator':v['box']}).items()}
 out['time_shared']=[[a,b] for a,b in itertools.combinations(data['operations'],2) if data['operations'][a]['owner']!=data['operations'][b]['owner'] and overlap(data['operations'][a]['box'],data['operations'][b]['box'])]
 states=['normal4','normal6','chairs_pulled','laundry_open','temporary_drying','cooking','luggage_open','screen_lowered']
 for state in (states if full else ['normal4']):
  for width in (500,600,620,900):
   grid,step,obstacles=route_grid(data,width,state)
   for name,v in data['routes'].items():
    path,status=find_path(grid,step,v['start'],v['end'],v.get('target_box'),width)
    target=v.get('target_box');near=[]
    if not path and target:
     x,y,w,h=target;near=[n for n,b in obstacles.items() if overlap([x-width/2,y-width/2,w+width,h+width],b)]
    out['routes'].append(dict(name=name,width_mm=width,state=state,reachable=bool(path),path=path,status=status,target_box=target,near_target_obstacles=near))
 out['function_access']={}
 approach,smallstep,_=route_grid(data,400)
 for n,v in data['operations'].items():
  b=v['box'];required=v.get('required',True)
  # Seated chair owns its occupied seat; approach region is the pulled position.
  if v.get('component')=='seated':b=data['operations']['dining_pull'+v['owner'][-1]]['box']
  path,status=find_path(approach,smallstep,[13900,1850],[b[0]+b[2]/2,b[1]+b[3]/2],b,400)
  out['function_access'][n]=dict(reachable=bool(path),required=required,status=status,box=b,path=path,standing_envelope_mm=400,note='400为原地站位概念，不代替500单人或600/620携篮路线')
 out['wc_clearances']={}
 for n,v in data['furniture'].items():
  if v['kind']!='wc':continue
  x,y,w,h=v['box'];front=v['front'];dist=[]
  for k,f in obs.items():
   if k==n:continue
   a,b,c,d=f['box']
   if front=='west' and min(y+h,b+d)>max(y,b) and a+c<=x:dist.append((x-a-c,k))
   if front=='south' and min(x+w,a+c)>max(x,a) and b+d<=y:dist.append((y-b-d,k))
  gap,limiter=min(dist) if dist else (None,None)
  south=[];north=[]
  for k,f in obs.items():
   if k==n:continue
   a,b,c,d=f['box']
   if min(x+w,a+c)>max(x,a):
    if b+d<=y:south.append((y-b-d,k))
    if b>=y+h:north.append((b-y-h,k))
  sides={'south':min(south) if south else None,'north':min(north) if north else None}
  out['wc_clearances'][n]=dict(front_mm=gap,limiter=limiter,minimum_mm=600,target_mm=750,passed=gap is not None and gap>=600,side_clearances_mm=sides,side_minimum_concept_mm=150,side_passed=all(v is None or v[0]>=150 for v in sides.values()),side_and_wipe='左右各150仅概念擦洗目标；产品侧向使用与排污迁移仍待核')
 # Cabinet leaves sampled at 1 degree; drawer swept rectangles include 450mm extension.
 out['cabinet_motion_hits']={}
 for n,v in data['furniture'].items():
  if v['kind']!='cabinet':continue
  x,y,w,h=v['box'];front=v['front'];span=w if front in ['north','south'] else h;u=0;hits=set()
  for ww,use in zip(v.get('modules',[]),v.get('contents',[])):
   if v.get('door_type')=='sliding':
    shift=ww*.5*(1 if u+ww*1.5<=span else -1)
    for fraction in range(101):
     off=u+2+shift*fraction/100
     b=[x+off,y,ww-4,18] if front=='south' else [x+off,y+h-18,ww-4,18] if front=='north' else [x,y+off,18,ww-4] if front=='west' else [x+w-18,y+off,18,ww-4]
     if off<0 or off+ww-4>span:hits.add('outside_cabinet_track')
     for k,f in obs.items():
      if k!=n and overlap(b,f['box']):hits.add(k+'_sliding')
   else:
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
 out['routine_baseline_passed']=not out['fixed_hits'] and not any(out['door_sweep'].values()) and not any(v['hits'] or v['outside_samples'] for v in out['sliding_sweep'].values()) and not any(out['cabinet_motion_hits'].values()) and all(r['reachable'] for r in out['routes'] if r['width_mm']==500 and r['state']=='normal4') and all(v['passed'] for v in out['wc_clearances'].values()) and all(not hits for n,hits in out['operation_fixed_hits'].items() if data['operations'][n].get('required',True)) and all(v['reachable'] for v in out['function_access'].values() if v['required'])
 out['usage_passed']=out['routine_baseline_passed'] and all(r['reachable'] for r in out['routes']) and not out['time_shared']
 out['limitations']=['墙、门、家具为概念包络；固定相交按三维高度过滤，床采用含外伸床架。','门扇与50mm把手按1°采样；非连续运动认证。推拉停放包络已计路线；真实轨道/叠片待核。','路线50mm网格、轴对齐方形包络，含门框及全开门；900为目标，不作为强制合格线。','矩形操作区包含人员和门抽屉行程；命中与共享分别披露，不能把所有命中自动当作错时可解。','玻璃隔断设800mm名义入口；扣框五金后的真实入口尚未核定。']
 return out
def main():
 out=verify();dump('reports/usage.json',out)
 comparison=[]
 for c in D['candidates']:
  data=candidate_data(c)
  result=verify(data,False) if c['id']!='recommended' else out
  comparison.append({**c,'fixed_hits':result['fixed_hits'],'single_routes_passed':sum(r['reachable'] for r in result['routes'] if r['width_mm']==500 and r['state']=='normal4'),'route_count':len(data['routes']),'storage_rail_mm':sum(v['rail_mm'] for n,f in data['furniture'].items() for v in capacity(n,f)),'operation_hits':{k:v for k,v in result['operation_fixed_hits'].items() if v},'function_access':result['function_access'],'routes':result['routes'],'note':'完整候选：家具、操作及目标区一起变更；不覆盖推荐'})
 dump('reports/comparison.json',bound({'priority':['固定实体','必要路线','操作','容量','拆改代价'],'candidates':comparison}))
 print(json.dumps({'fixed':out['fixed_hits'],'door':out['door_sweep'],'operations':{k:v for k,v in out['operation_fixed_hits'].items() if v},'normal500_fail':[r['name'] for r in out['routes'] if not r['reachable'] and r['width_mm']==500 and r['state']=='normal4']},ensure_ascii=False))
if __name__=='__main__':main()
