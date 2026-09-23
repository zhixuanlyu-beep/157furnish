"""Independent candidate study; every layout coordinate comes from layout.json."""
from common import *

ID='single_bath_utility'

def review(c,data,result):
 from verify_usage import route_grid,find_path
 result['limitations']=[v for v in result['limitations'] if '800mm名义入口' not in v]
 result['limitations'].append('本候选淋浴名义入口650mm；扣框五金后实际净宽待核。')
 errors=[]
 ids=[e['id'] for e in data['edges']]
 if len(ids)!=len(set(ids)):errors.append('重复墙ID')
 for e in data['edges']:
  at=0
  for o in sorted(e['openings'],key=lambda v:v['start']):
   if not at<=o['start'] or o['start']+o['width']>math.dist(e['a'],e['b']):errors.append('洞口越界 '+o['id'])
   at=o['start']+o['width']
 for n,v in data['furniture'].items():
  if v['room'] not in data['rooms']:errors.append('旧房间引用 '+n)
 for n,v in data['operations'].items():
  if v['owner'] not in data['furniture']:errors.append('旧设备引用 '+n)
 for s in data['services']:
  if s['attached_to'] not in data['furniture']:errors.append('旧接口引用 '+s['id'])
  else:
   x,y,w,h=data['furniture'][s['attached_to']]['box']
   if math.hypot(max(x-s['x'],0,s['x']-x-w),max(y-s['y'],0,s['y']-y-h))>350:errors.append('接口未随设备移动 '+s['id'])
 if any(e['external'] and e not in D['edges'] for e in data['edges']):errors.append('外围边界被改动')
 moving=data['operations']['laundry_use']['parts']
 component_hits=[]
 for a,b in itertools.combinations(moving,2):
  if overlap(moving[a],moving[b]):component_hits.append([a,b])
 # Compare cabinet motion to both occupied operator and equipment door envelopes.
 cabinet_hits={}
 for n,v in data['furniture'].items():
  if v['room']!='utility' or v['kind']!='cabinet':continue
  x,y,w,h=v['box'];u=0;hits=set()
  for span in v['modules']:
   for angle in range(91):
    a=math.radians(angle);length=span-22
    poly=[(x+u+11+math.cos(a)*k-math.sin(a)*t,y+h-9+math.sin(a)*k+math.cos(a)*t) for k,t in [(0,-9),(length,-9),(length,9),(0,9)]]
    for part,b in moving.items():
     if polyhit(poly,rect(b)):hits.add(part)
   u+=span
  cabinet_hits[n]=sorted(hits)
 door_ops={}
 for n in ['utility_entry','wet_entry']:
  o=openings(data)[n];hits={}
  for angle in range(91):
   for part in ['leaf','handle']:
    poly=door_poly(o,angle,part=='handle')
    for k,v in data['operations'].items():
     if polyhit(poly,rect(v['box'])):hits.setdefault(k+'_'+part,[]).append(angle)
  door_ops[n]={k:[min(a),max(a)] for k,a in hits.items()}
 wash=data['rooms']['wash']['boxes'][0];stand=data['operations']['wash_use']['box']
 inside_wash=all(wash[0]<=x<=wash[0]+wash[2] and wash[1]<=y<=wash[1]+wash[3] for x,y in rect(stand))
 cooking={f:{'status':v['status'],'requirements':v['requirements'],'routes':[r for r in result['routes'] if r['name']=='阳台烹饪' and r['state'] in ['normal4','laundry_open','cooking','temporary_drying']]} for f,v in D['fuel_variants'].items()}
 shower=[];b=data['furniture']['single_shower']['box'];start=data['routes']['淋浴入口']['start']
 for width in [500,600,620,900]:
  grid,step,_=route_grid(data,width);path,status=find_path(grid,step,start,[b[0]+b[2]/2,b[1]+b[3]/2],b,width)
  shower.append(dict(width_mm=width,reachable=bool(path),status=status,path=path))
 return dict(data_consistency_passed=not errors,errors=errors,site_conditions_passed=False,site_status='待核；任一必要条件不成立则方案受阻',site_gates=c['study']['site_gates'],wash_standing_inside=inside_wash,laundry_component_hits=component_hits,cabinet_vs_laundry=cabinet_hits,door_vs_operations=door_ops,shower_interior_routes=shower,balcony_recheck=cooking,limitations=c['study']['usage_limits']+['家政门开启途中扫过装卸站位，进出与装卸需分时','新增淋浴名义侧入口650，五金后净宽及现场进入体验待核','柜门与人体按平面保守包络；上柜需另核高度及碰头','路线门全开；完整坐便站位要求关门，未认证动态进门关门过程'])

def drawings(Sheet,table):
 c=next(c for c in D['candidates'] if c['id']==ID);data=candidate_data(c);study=c['study']
 result=json.loads((ROOT/('reports/usage_'+ID+'.json')).read_text(encoding='utf-8'))
 q=Sheet('单卫候选 / 整体拆改研究',['红色：两卫中隔墙及储物西墙拟拆。','绿色：新隔墙；蓝框：拟封旧门。','北侧新家政入口及洗漱入口待结构核实。','外围、梁柱和立管不默认改动。','原储物纳入湿区条件失败则受阻。']);q.plan(data=data,crop=study['crop'])
 for id in study['demolition_edges']:
  e=next(e for e in D['edges'] if e['id']==id);q.line([q.pt(*e['a']),q.pt(*e['b'])],'#ca5944',7)
 for id in study['new_edges']:
  for v in walls(data).values():
   if v['edge']==id and v['z']==0:q.rect(q.rb(v['box']),'none','#36765a',4)
 for id in study['sealed_openings']:q.rect(q.rb(openings()[id]['box']),'none','#286fa1',4)
 q.save('06-single-demolition.svg')
 dims=['外围净包络',' × '.join(map(str,study['envelope'][2:]))+' mm，未实测。']
 dims += [v['label']+'：'+'×'.join(map(str,v['boxes'][0][2:])) for n,v in data['rooms'].items() if n in ['utility','wash','wet']]
 q=Sheet('单卫候选 / 新分区与尺寸',dims+['新隔墙120已扣；台盆1100×450。','小水池500宽为默认概念项。','洗澡与如厕需错开。']);q.plan(data=data,crop=study['crop'])
 for n in ['utility','wash','wet']:
  v=data['rooms'][n];b=v['boxes'][0];q.rect(q.rb(b),'none','#36765a',3);q.text(*q.pt(b[0]+b[2]*.55 if n=='wash' else b[0]+50,b[1]+b[3]*.55 if n=='wash' else b[1]+b[3]-80),v['label'],18)
 q.save('06-single-zones.svg')
 q=Sheet('单卫候选 / 内开门与洗漱坐便',['湿区门名义760，扣框概念700。','湿区入口内开，锁具及应急开启待核。','橙框：使用区；蓝线：500单人路线。','门扇与坐便使用区共享，关门后使用。','淋浴侧入口650，实际净宽待核。','完整冲突与失败见候选核验。']);q.plan(data=data,crop=study['crop'],ops=True,opened=True,route=[r for r in result['routes'] if r['width_mm']==500 and r['state']=='normal4' and r['name'] in c['changes']['routes']]);q.save('06-single-doors.svg')
 q=Sheet('单卫候选 / 洗烘开启与装卸',['红框：600开启件概念服务空间。','绿框：650深操作者包络。','叠放锚固、排风噪声和检修待核。','设备门轨迹须替换为厂家数据。','柜门及携篮冲突分别记录。']);q.plan(data=data,crop=study['crop'],opened=True)
 for part,b in data['operations']['laundry_use']['parts'].items():q.rect(q.rb(b),'none','#ca5944' if part=='moving' else '#36765a',3)
 q.save('06-single-laundry.svg')
 q=Sheet('单卫候选 / 洗烘迁出后的阳台',['西端已撤洗烘，原设备接口不沿用。','晾晒保留独立状态；东端烹饪仍附条件。','燃气迁移许可／电灶配电分别核实。','两案都须合法排烟；不默认外墙直排。','重新计算烹饪及携篮路线，保留失败。']);q.plan(data=data,crop=D['balcony']['net_box'],opened=True);q.save('06-single-balcony.svg')
 table('单卫候选路线.csv',['路线','状态','宽mm','可达','原因'],[[r['name'],r['state'],r['width_mm'],r['reachable'],r['status']] for r in result['routes']])
 table('单卫淋浴内部路线.csv',['宽mm','可达','说明'],[[v['width_mm'],v['reachable'],v['status']] for v in result['study_review']['shower_interior_routes']])

def docs():
 c=next(c for c in D['candidates'] if c['id']==ID);u=json.loads((ROOT/('reports/usage_'+ID+'.json')).read_text(encoding='utf-8'));r=u['study_review']
 rows=['# 单卫＋家政收纳：独立候选','', 'R2推荐及两燃料模型保留。本候选仅二维研究，不代表已选定或可施工。所有尺寸未实测，来源为用户方案及R2概念包络，唯一坐标源为data/layout.json。', '', '[新分区图](../drawings/svg/06-single-zones.svg) · [拆改图](../drawings/svg/06-single-demolition.svg) · [内开门图](../drawings/svg/06-single-doors.svg) · [洗烘装卸图](../drawings/svg/06-single-laundry.svg) · [阳台复核图](../drawings/svg/06-single-balcony.svg)', '', '外围4423×2489；西侧家政1800宽、新墙120、东侧2503宽。外置洗漱1050深、新墙120，南湿区1319深。家政南端叠放洗烘、500宽小水池默认项、封闭下柜和上柜；不设两侧深柜。洗漱台1100×450及镜柜，站位在区内。湿区淋浴900×1100，坐便朝西，门内开。原套卫门与储物侧门封闭。', '', '## 数据一致性', '', str(r['data_consistency_passed'])+'；'+str(r['errors']), '', '## 使用检查', '', '以下为候选自身结果；全屋继承限制仍保留，不能把数据一致性当作使用通过。', '', '固定实体命中：'+str(u['fixed_hits']), '','坐便前侧空间：'+str(u['wc_clearances']), '', '门扇固定命中：'+str({k:v for k,v in u['door_sweep'].items() if v}), '', '门扇与操作区：'+str(r['door_vs_operations']), '', '洗烘开启件／操作者互撞：'+str(r['laundry_component_hits'])+'；家政柜门对装卸包络：'+str(r['cabinet_vs_laundry']), '', '必要操作实体命中：'+str({k:v for k,v in u['operation_fixed_hits'].items() if v}), '', '洗漱站位完全在洗漱区：'+str(r['wash_standing_inside']), '', '| 候选路线 | 状态 | 500 | 600 | 620 | 900 |','| --- | --- | --- | --- | --- | --- |']
 for state in ['normal4','laundry_open','cooking','temporary_drying']:
  for name in list(c['changes']['routes'])+['阳台烹饪']:
   rr=[next(v for v in u['routes'] if v['name']==name and v['state']==state and v['width_mm']==w) for w in [500,600,620,900]]
   rows.append('| '+' | '.join([name,state]+['通过' if v['reachable'] else '失败' for v in rr])+' |')
 rows+=['','全部状态与失败原因见[路线表](../tables/单卫候选路线.csv)及[完整核验JSON](../reports/usage_single_bath_utility.json)。','']+r['limitations']+['', '## 专业与现场条件', '', r['site_status']]+['- '+v['requirement']+'；'+v['status']+'；失败则'+v['if_failed'] for v in r['site_gates']]+['','## 阳台迁灶复核','','洗烘和关联水电接口已迁入家政。迁出释放西端设备及装卸空间，东端烹饪与晾晒仍按各状态重新计算，结果见上表。端窗、合法排烟、燃气许可或电灶容量等既有条件仍未确认；不默认迁出洗烘即允许迁灶。','','布局 SHA256：'+SHA]
 wc=u['wc_clearances']['single_wc']
 summary=['','坐便前方概念净距 '+str(wc['front_mm'])+' mm（目标750、最低600）；固定实体命中 '+str(len(u['fixed_hits']))+' 项，门扇命中实体 '+str(sum(len(v) for v in u['door_sweep'].values()))+' 项。此为未实测几何结果。','', '淋浴内部路线：'+ '；'.join(str(v['width_mm'])+' mm '+('通过' if v['reachable'] else '失败：'+v['status']) for v in r['shower_interior_routes']), '', '家政门开启途中扫过装卸站位，需要先完成进出再装卸；湿区门与坐便前区共享，关门后使用。洗澡与如厕需错开。', '']
 rows[8:8]=summary
 (ROOT/'docs/single-bath.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
