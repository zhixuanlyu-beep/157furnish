"""R2 documentation: data, usage and onsite outcomes are separate."""
import html,re
from common import *
from build_drawings import table
def write(n,s):(ROOT/n).write_text(s.strip()+'\n',encoding='utf-8')
def main():
 from single_bath import docs
 docs()
 U=json.loads((ROOT/'reports/usage.json').read_text(encoding='utf-8'));I=json.loads((ROOT/'reports/drawing_index.json').read_text(encoding='utf-8'));C=json.loads((ROOT/'reports/comparison.json').read_text(encoding='utf-8'))['candidates']
 models={f:json.loads((ROOT/('reports/model_verification_'+f+'.json')).read_text(encoding='utf-8')) for f in D['fuel_variants']}
 conditions=[
 ('01','实测与原始边界','尺寸链参考面、墙厚、梁柱、凹凸角、门窗标高及北向复测','未作现场实测；不得按项目名或照片像素推算面积'),
 ('02','拟拆改','厨房西侧与南入口隔墙及旧门，结构性质书面核实','梁柱、阳台分界墙、外墙和烟道保留；不允许拆则回退原厨房'),
 ('03','阳台燃气','迁移许可、管阀路径、可关闭空间、通风、灶后不燃材料','未落实则燃气迁灶受阻；不自动改选电灶'),
 ('04','阳台电灶','总配电容量、专用回路、散热、接地及设备防护','未落实则电灶迁灶受阻；电灶也须排烟'),
 ('05','排烟与端窗','合法烟道接入、压损、防火止回与检修；端窗开启、窗台、防水保温、支承和窗厂家节点','不默认外立面直排；条件不成立则阳台主案受阻，回退单列'),
 ('06','洗烘','叠放套件、荷载、防倾倒、污水接管、防冻防晒和独立电源','装卸、晾晒与携篮分状态；洗衣路线不穿灶前'),
 ('07','两卫','坐便朝西的坑距及排污迁移、地漏坡度、防水、隔断入口和擦洗','750目标／600底线须实测；保持原湿区，不作防水施工图'),
 ('08','门窗五金','推拉轨道、框、把手、固定扇、停放、密封与应急开启','房门1度、推拉101位置采样不等于连续运动认证'),
 ('09','岛槽与主槽','主槽留原厨房东侧；岛槽排水坡度、污水接管和检修未知','推荐干岛，不默认抬地、穿梁或接雨水'),
 ('10','设备','冰箱、洗碗、蒸烤、微波及基站安装图、散热、门、检修和搬入','600开启件加450人员为概念，须厂家替换；不锁型号'),
 ('11','衣柜与鞋衣','床架头板、踢脚线、衣物高度、挂杆、抽屉与板件五金','400深鞋柜仅正面挂钩；1800以上季节性，不计普通横挂'),
 ('12','储物间','入口外正面取物、300深单元、门净宽及伸手试验','深处不计容量；扩大侧开口仅结构条件候选'),
 ('13','空调新风','负荷、回风、冷凝水、排风、外机、穿梁、吊顶净高及噪声','风量仅讨论值，厨房排烟不接新风'),
 ('14','日照与投影','北京气候假设、图示北向、外遮挡、窗帘、投射比及眼点','二维点射线非日照合规、照度或投影选型承诺'),
 ('15','家庭与预算','儿童防夹防坠、锚固圆角及桌椅试坐；165cm主厨为继承参数','其他身高、预算及产品型号未核，不补造'),
 ('16','独立单卫候选','三空间整体重分；拟拆两卫中隔墙与储物西墙、新家政入口、套卫及储物侧门封闭；排污立管、洗烘接口排风噪声检修待核','原储物纳入湿区须确认防水、楼板和楼下条件；任一必要条件不成立则方案受阻；R2推荐保持不变，详见single-bath.md')]
 dump('reports/onsite_conditions.json',bound({'passed':False,'reason':'两个燃料案均未实测及取得专业确认','items':[dict(id=a,topic=b,required=c,decision=e,status='待核') for a,b,c,e in conditions]}))
 table('现场待核.csv',['编号','专题','所需确认','条件不成立时'],conditions)
 write('docs/constraints.md','# R2 现场条件与使用边界\n\n用于设计深化，不作施工、拆墙或柜体下单依据。\n\n'+'\n\n'.join('## '+a+' '+b+'\n\n'+c+'。'+e+'。' for a,b,c,e in conditions))
 improvements=[('客餐厨','独立厨房、共享桌挤岛前','拟拆两隔墙；干岛＋常规餐桌兼学习'),('阳台','标签框深1243、设备中置','墙内侧1143；两端设备、两入口、可关闭分隔'),('坐便','南向前距370／180','朝西；750前方目标、侧向和擦洗另核'),('主卧','床尾620','床北移100，含头板床架，床尾720'),('客房','固定行李架令西床侧70','撤架；床下收起与床尾展开分状态'),('储物间','1350深架容量误导','入口300深浅储物；深处不计容量'),('儿童成长','换床后旧终点失效','床、桌椅、活动及目标区一起变更'),('检查','单点路线、推拉只核停放','目标区域、坐便前距、推拉全过程、设备与人员分开')]
 table('R1到R2改进.csv',['专题','R1','R2'],improvements)
 table('燃料条件.csv',['变体','状态','条件'],[[v['label'],v['status'],'；'.join(v['requirements'])] for v in D['fuel_variants'].values()])
 table('功能站位.csv',['操作','必要','400站位可达','状态','目标区'],[[n,v['required'],v['reachable'],v['status'],str(v['box'])] for n,v in U['function_access'].items()])
 table('坐便前距.csv',['坐便','前距mm','最低mm','目标mm','限制实体','达到最低'],[[n,v['front_mm'],600,750,v['limiter'],v['passed']] for n,v in U['wc_clearances'].items()])
 table('推拉全过程.csv',['门','实体命中','越界样本','停放框'],[[n,str(v['hits']),str(v['outside_samples']),str(v['parked_box'])] for n,v in U['sliding_sweep'].items()])
 table('操作分解.csv',['操作','分量','范围','固定命中'],[[n,p,str(v['box']),str(v['fixed_hits'])] for n,parts in U['operation_components'].items() for p,v in parts.items()])
 table('具体路线限制.csv',['状态','宽mm','功能','失败原因','目标附近障碍'],[[r['state'],r['width_mm'],r['name'],r['status'],'、'.join(r['near_target_obstacles'])] for r in U['routes'] if not r['reachable']])
 details=['# R2 核验摘要','',f'版本 `{REV}`；布局 SHA256 `{SHA}`。','', '**数据一致性、使用检查、现场条件分别报告。** 见[交付核验](../reports/delivery.json)及[校验清单](../reports/manifest.json)。','',
 f'- 固定实体冲突：{len(U["fixed_hits"])} 项，明细 `{U["fixed_hits"]}`。',
 '- 坐便前距：'+'；'.join(n+' '+str(v['front_mm'])+'mm' for n,v in U['wc_clearances'].items())+'（概念几何，目标750／底线600）。',
 f'- 房门把手采样命中：{sum(bool(v) for v in U["door_sweep"].values())} 扇；推拉未通过：{[n for n,v in U["sliding_sweep"].items() if v["hits"] or v["outside_samples"]]}。',
 f'- 柜门／抽屉外部命中：{ {n:v for n,v in U["cabinet_motion_hits"].items() if v} }。柜内真实五金仍须深化。',
 f'- 日常500基线：{"通过概念检查" if U["routine_baseline_passed"] else "存在未通过项"}；全部状态及宽度：{"通过" if U["usage_passed"] else "未全部通过"}。',
 f'- 两燃料 Blender／GLB 独立重开：{all(v["passed"] for v in models.values())}；实际世界网格误差阈值0.1mm。',
 '- 现场条件：待核，两个燃料均未取得实施条件确认。','',
 '路线用50mm网格，检查500单人、600／620携篮和900目标，完整包络必须落入目标区域。窄缝可能受网格对齐影响，失败不等于连续空间不可达证明。400站位仅原地站立概念，不代替500通路。入户路线从玄关内起算；楼外搬入未核。','',
 '| 状态 | 包络mm | 功能 | 具体限制 | 目标附近实体 |','| --- | ---: | --- | --- | --- |']
 for r in U['routes']:
  if not r['reachable']:details.append(f'| {r["state"]} | {r["width_mm"]} | {r["name"]} | {r["status"]} | {", ".join(r["near_target_obstacles"])} |')
 details+=['','## 操作与错时','','固定实体命中：`'+str({n:h for n,h in U['operation_fixed_hits'].items() if h})+'`。儿童床西侧不是必要照护边，东侧为照护入口；其余必要操作命中不能用错时掩盖。','', '必要站位未通过：`'+str([n for n,v in U['function_access'].items() if not v['reachable'] and v['required']])+'`，见[功能站位表](../tables/功能站位.csv)。','', '共享包络需错时／避让：'+'；'.join(' / '.join(p) for p in U['time_shared'])+'。同设备重复包络不算两人并用。','', '洗烘开启只把开启部件加入路线障碍；烹饪状态将灶前操作者加入障碍后核第二人。临时晾晒、行李展开、餐椅拉出、六人及幕布放下分别核验。设备动画是600服务空间示意，非真实厂家轨迹。','', '回归覆盖旧坐便、推拉越界、行李架堵床侧、成长床目标、洗烘误判及模型依赖过期。重复与独立重建见reports/repeatability.json和reports/clean_rebuild.json，不承诺模型二进制逐字节相同。']
 write('docs/verification.md','\n'.join(details))
 design=['# R2 设计取舍','','推荐研究：干岛＋独立750高餐桌兼学习，原厨房西隔墙、南入口墙及旧门拟拆。阳台净深1143，东端烹饪朝西、西端洗烘朝东，分隔及两入口可关闭；燃气、电灶并列。结构、端窗、排烟与安装条件未落实时主案受阻。','','## R1 → R2','','| 专题 | 原问题 | 改进 |','| --- | --- | --- |']+['| '+' | '.join(row)+' |' for row in improvements]
 design+=['','## 完整布局比较','','干岛750×1500、850高，台面1.125㎡；靠南墙方案2000×450、850高，台面0.90㎡，与南餐椅就座重叠。两案均保留餐桌、东侧主槽／冰箱／蒸烤、玄关及阳台主研究条件。按固定冲突、必要通路、操作、收纳、拆改依次比较，保留干岛；辅助槽仅排水落实后可选。','','| 方案 | 固定冲突 | 操作命中 | 500路线 | 拆改序 |','| --- | --- | --- | ---: | ---: |']
 for c in C:design.append(f'| {c["label"]} | {c["fixed_hits"]} | {c["operation_hits"]} | {c["single_routes_passed"]}/{c["route_count"]} | {c["cost_rank"]} |')
 design+=['','## 逐室使用','','B保留1800×2000床垫，1900×2120床架包含头板及外伸，床尾720，北侧余80可容概念20踢脚线，仍须实测。2200×600衣柜日常双短挂／长挂、床品及1800以上季节性容量分列；床头抽屉单列。','','A保留1200床垫、独立桌、衣柜和低位书玩。1500成长床候选将桌缩至1000并平移桌椅，照护、拉椅、活动与窗路一起核；西床侧不作为必要照护边。','','C保留1500床垫，两侧概念净距511／510；固定行李架撤除，床下收起、床尾展开分状态，与取衣和床尾操作错时。500网格对511窄道敏感，站位与通路结论分别报告。','','两卫均有900深淋浴及800名义入口，坐便东墙朝西，前方750操作目标、侧向及擦洗另查；坑距、排污迁移、地漏、防水和隔断五金仍待核。','','储物间保墙，入口仅300深／1800高单元，从入口外取物，深处不可达空间不计容量；扩大侧开口仅结构条件候选。400深鞋柜按鞋层板和正面挂钩，普通横挂容量不计。','','西北会客与卷幕平面间距约2150，眼点、投射比及视角须试验；卷幕收起／放下分状态，北侧阳台路径须保持。咖啡柜收学习用品，餐桌兼共享学习，电源线不跨主要通路。','','## 阳台及回退','','长边连续600柜只余543通道，不采用。原窗台100与850灶台、1950洗烘不相容，需端窗固定不燃内衬、可检修支承及防水保温专项，保留可开启通风扇。两燃料均核合法烟道接入，不默认向外立面直排。','','燃气核迁移许可、管阀、关闭空间及通风；电灶核配电、专线及散热，均核灶后不燃材料与排烟。回退图保留原厨房附近灶和关闭隔墙，撤岛、冰箱／高柜回原区；回退也有错时及专业条件，不替代阳台主方向。','','暖白、木色、少量绿色，沿用北京气候研究。模型保留材质灯光相机与动画，无三维渲染，无预算／型号报价，不供施工或下单。']
 write('docs/design.md','\n'.join(design))
 ml=' · '.join(f'[{v["label"]} Blender](model/157furnish_R2_{f}.blend) / [GLB](model/157furnish_R2_{f}.glb)' for f,v in D['fuel_variants'].items())
 write('README.md',f'''# 157furnish · R2

三房两卫、客餐厨一体化及阳台迁灶条件研究。新增[单卫＋家政整体重分候选](docs/single-bath.md)，保留R2对比。先打开[离线方案册](docs/方案册.html)、[设计取舍](docs/design.md)、[核验摘要](docs/verification.md)及[现场条件](docs/constraints.md)。

- {len(I)}张可编辑SVG及同源PNG：[图纸](drawings/svg)，按实际内容编索引。
- {ml}。
- [表格](tables)、[唯一布局源](data/layout.json)、[接手重建](docs/handoff.md)。R1保留于Git历史，原始概念边界存layout.original。

数据一致性、使用检查与现场条件分别判断。500单人、600/620携篮和900目标逐项披露失败；两个燃料均附条件，未锁定。未实测参数明确来源及状态，不供施工或下单。未执行三维渲染，原照片和参考项目保持原样。

布局 SHA256：`{SHA}`。
''')
 write('docs/handoff.md','''# 接手与独立重建

唯一坐标源data/layout.json，毫米、X东Y北Z上，模型除1000转米。original保留R1原始概念边界，edges/furniture为R2，fuel_variants并列燃料；candidates补丁同时变更家具、操作和目标区域，states为使用状态。候选不能覆盖推荐。

```powershell
python scripts/rebuild.py --blender D:/Users/11171344/blender/blender.exe --repeat
python scripts/verify_clean_rebuild.py --blender D:/Users/11171344/blender/blender.exe
python scripts/validate_delivery.py
```

依赖Python、requirements.txt内Pillow/NumPy、Blender及中文msyh.ttc。无网络与兄弟参考项目依赖。顺序：回归、使用检查、两燃料模型及独立重开Blender/GLB、二维图表、文档、交付核验。clean_rebuild仅复制scripts、data、requirements及原照片至本项目reports隔离目录，检查绝对路径后清理。

重复构建比较SVG/PNG/CSV/文档及实际模型投影快照，不承诺二进制逐字节相同。投影校验包含build_model.py及common.py依赖，过期拒绝。所有修改后须全量rebuild；不手改生成产物。保留使用失败与现场条件，不能用一致性通过覆盖使用失败。

FURNISH_FUEL选择燃料，正常重建自动生成两套。Blender保留材质、灯光、7相机、动画及隐藏Inspection_Envelopes/Ceilings/Dining_6_extra。帧1关闭、90开启，柜门转动、推拉分轨、抽屉450、设备面板600为概念服务空间，非厂家轨迹。GLB四人静态实体不含六人加椅、检查层和顶棚。模型验证临时启用隐藏层，不另存；读取实际网格世界包围盒，不复制JSON冒充验证。

禁止三维渲染。门窗五金、柜内板件、支承节点需厂家深化。原图只用于尺寸链与拓扑，照片不加工，不以像素冒充实测。北京40N/116.5E、图示北仅研究假设；165cm主厨为继承参数。没有其他可靠身高、预算或产品型号。模型与操作演示均不供施工或下单。
''')
 write('AGENTS.md','''# 接手约定

先读README.md、docs/handoff.md及docs/constraints.md。唯一布局坐标源data/layout.json，所有生成毫米转米。不得修改兄弟参考项目。不得执行三维渲染。原始照片保持原样。

所有未实测尺寸须标明来源与状态；禁止按照片像素冒充实测或按项目名推算面积。候选不得覆盖推荐状态，过期模型投影必须拒绝。

修改后运行scripts/rebuild.py全量核验。保留失败与现场条件；数据一致性、使用检查和专业/现场核实分别报告。读图与操作演示仅概念，不生成施工或下单承诺。
''')
 write('docs/drawing-visual-review.md','''# 二维图面复核

R2使用中文微软雅黑，SVG/PNG共用二维原语与裁剪范围。总图编号、逐室中文名称对应家具表；使用1000mm比例尺，不能按屏幕物理尺寸下单。

重点抽查推荐总图、两卫、阳台燃料、端窗高度关系、拆改、柜体和水电，检查中文、说明边界和标注避让。本地链接和SVG实际坐标由交付核验检查。两引擎字体基线可能不同，不作逐像素相同声明。没有执行三维渲染。
''')
 page=(ROOT/'docs/方案册.html').read_text(encoding='utf-8');links=''.join(f'<li><a href="../tables/{html.escape(p.name)}">{html.escape(p.name)}</a></li>' for p in sorted((ROOT/'tables').glob('*.csv')))
 page=re.sub(r'<h2>表格</h2><ul>.*?</ul>','<h2>表格</h2><ul>'+links+'</ul>',page,flags=re.S).replace('三房两卫 · 可关闭厨房 · 无水岛台 · 两处淋浴','三房两卫 · 客餐厨一体 · 阳台两燃料并列条件案').replace('固定实体及500单人基线通过不等于全部使用通过','数据一致性通过不等于使用通过')
 intro='<section><p><a href="single-bath.md">新增单卫＋家政整体重分候选：二维图、使用核验及现场条件</a>；R2推荐与模型保持独立。</p><h2>R1 → R2 改进</h2><table><tr><th>专题</th><th>R1</th><th>R2</th></tr>'+''.join('<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in row)+'</tr>' for row in improvements)+'</table><p>固定实体冲突 '+str(len(U['fixed_hits']))+' 项；全状态使用未全部通过；现场条件待核，详见核验摘要和失败表。</p>'
 intro+=''.join(f'<p>{v["label"]}：<a href="../model/157furnish_R2_{f}.blend">Blender</a> · <a href="../model/157furnish_R2_{f}.glb">GLB</a>；'+html.escape('、'.join(v['requirements']))+'</p>' for f,v in D['fuel_variants'].items())+'</section>'
 page=page.replace('<details>',intro+'<details>',1).replace('li{margin:5px}','li{margin:5px}td,th{border:1px solid #bbc7b8;padding:10px;text-align:left}table{border-collapse:collapse;width:100%}')
 (ROOT/'docs/方案册.html').write_text(page,encoding='utf-8');print('DOCS_COMPLETE')
if __name__=='__main__':main()
