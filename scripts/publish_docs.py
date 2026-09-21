"""Human-readable handoff and separate data / use / onsite decisions."""
import html,re
from common import *
from build_drawings import table
def write(n,s):(ROOT/n).write_text(s.strip()+'\n',encoding='utf-8')
def main():
 U=json.loads((ROOT/'reports/usage.json').read_text(encoding='utf-8'));M=json.loads((ROOT/'reports/model_verification.json').read_text(encoding='utf-8'));C=json.loads((ROOT/'reports/comparison.json').read_text(encoding='utf-8'));I=json.loads((ROOT/'reports/drawing_index.json').read_text(encoding='utf-8'))
 constraints=[('01','原始测绘','总宽/深来自标注链；链的定位面、3370卫生间上界、墙厚、凹凸角、门窗宽高全部复测','所有净距结论随实测更新'),('02','结构与拆改','厨房西墙、门洞及推拉挂轨基层性质；梁柱、烟道不得按图猜测','未确认前采用保留分隔方案'),('03','燃气','原东墙燃气/排烟区保留；实际立管、阀门、灶烟距离及开放厨房许可','未取得燃气及物业认可不实施开放'),('04','岛台辅助槽','污水立管位置、落差、管径、路线及检修尚未知','推荐无水岛台；不默认抬地或穿梁'),('05','两卫','两套淋浴均在原湿区；地漏、坐便坑距、坡度、防水、门槛、排风和隔断五金','800名义淋浴入口须扣五金；不作防水施工图'),('06','阳台家政','洗烘给排水、承载、防冻、防晒、防水、污水接驳与叠放套件','设备未选型；晾晒与携篮/装卸错时'),('07','门窗五金','门洞扣框每侧30、把手50、门板40是概念；推拉门轨道/叠片/隔音/应急开启','现场净宽决定携篮结论；固定开启门不代表可省略门'),('08','真实设备','冰箱、洗碗机、蒸烤、微波、净水、基站及洗烘安装图','核散热、开门、插座、水阀、维修和运输；不得下单'),('09','柜体及衣物','主卧移门与三抽柜；18板厚、挂杆、轨道、门缝均为概念','按实际衣物复核数量与挂衣高度；柜体防倾倒'),('10','空调新风','冷凝水、回风、排风、外机、穿梁及吊顶净高','风量仅讨论输入，未做冷热负荷/风阻/噪声计算'),('11','日照','北京纬经度继承、图示北向、窗台/窗高均待核，外遮挡未知','仅四季枕点射线，不作日照合规判断'),('12','预算及产品','未收到预算上限、品牌或安装资料','本轮不锁型号、不编造报价'),('13','收纳间','净宽约515、原图细长储物形状；当前深架为可抽出单元候选','须核抽出方向/重量/轨道；不把1350深架当日常可全深徒手够取'),('14','家庭照护','学龄前儿童需圆角、防夹、防坠和柜体锚固；可调桌高度按本人试坐','165cm主厨为继承参数；其他成员身高未核')]
 dump('reports/onsite_conditions.json',bound({'passed':False,'reason':'尚未实测及取得专业确认','items':[dict(id=a,topic=b,required=c,decision=d,status='待核') for a,b,c,d in constraints]}))
 table('现场待核.csv',['编号','专题','所需确认','条件不成立时'],constraints)
 lines=['# 现场条件与使用边界','','本交付为 R1 设计深化与概念图模，不作施工或柜体下单依据。','']
 for a,b,c,d in constraints:lines+=['## '+a+' '+b,'',c+'。'+d+'。','']
 write('docs/constraints.md','\n'.join(lines))
 failures=[]
 for state in ['normal4','normal6','chairs_pulled','laundry_open']:
  for width in [500,600,620,900]:
   rr=[r for r in U['routes'] if r['state']==state and r['width_mm']==width];bad=[r['name'] for r in rr if not r['reachable']]
   failures.append(f"| {state} | {width} | {len(rr)-len(bad)}/{len(rr)} | {'、'.join(bad) or '无'} |")
 motion={k:v for k,v in U['cabinet_motion_hits'].items() if v}
 write('docs/verification.md',f'''# R1 核验摘要

布局版本 `{REV}`，SHA256 `{SHA}`。

**数据一致性、使用状态、现场条件分别判断。** 最终文件清单及检查结果见 [delivery.json](../reports/delivery.json)。

- 固定家具与墙/家具实体相交：{len(U['fixed_hits'])} 项；含床架外伸与高度过滤。
- 房门及50mm把手0–90°每1°采样命中：{sum(bool(v) for v in U['door_sweep'].values())} 扇。
- 概念柜门及450抽屉运动外部命中：{motion or '无'}。移门为分轨/框内平移示意，真实五金未锁定。
- 基线操作包络与固定实体命中：{sum(bool(v) for v in U['operation_fixed_hits'].values())} 项。
- 日常四人500单人基线：{'通过概念检查' if U['routine_baseline_passed'] else '存在未通过项'}。
- 全状态/全宽度使用检查：**未全部通过**。900是通路目标，不能把500通过当作900通过。
- Blender与GLB均重新打开，按源家具逐项读取实际网格世界包围盒：{'通过' if M['passed'] else '失败'}；误差阈值0.1mm。检查包含隐藏层临时启用、帧90动画对象位移。
- 现场与专业条件：未通过/待核，见[条件清单](constraints.md)。

| 情景 | 方形宽mm | 可达条数 | 未找到路线/端点受阻 |
| --- | ---: | ---: | --- |
'''+ '\n'.join(failures)+'''

路线使用50mm正交网格、全开房门、门框及把手，宽度为轴对齐方形包络，不包含人转身、衣篮旋转及门的动态开关。找不到路线不是连续空间不可达证明。对应JSON保留路径和失败，不删除失败状态。入户路线从玄关内出发，另有入户门名义/扣框净宽及门扇检查；不声称对楼外电梯与公共走廊做过验证。

操作重叠采用错时/避让说明，见[usage.json](../reports/usage.json) `time_shared`：儿童活动与拉椅/开柜、共享学习与岛台、冰箱与灶/备餐、主卫洗面与更衣。基站两条包络属于同一设备的重复说明，不是两个人可并用。

设备开启、抽屉、拉椅和装卸为概念操作包络。设备前面板动画用于展示服务空间，不能当作真实型号铰链轨迹。楼外搬入、大件旋转及厂家检修拆件步骤未验证，保留在现场条件。

原图尺寸链与外边界闭合、洞口分段、SVG坐标/CSV、PNG来源、模型校验值、本地链接及重复构建由 `validate_delivery.py` 和 `rebuild.py --repeat` 检查。人工抽查二维PNG，不执行三维渲染。
''')
 caps=[a for n,v in D['furniture'].items() for a in capacity(n,v)];master=[a for a in caps if a['cabinet']=='wardB']
 desc=['# R1 设计取舍','','推荐三房两卫、可关闭厨房和无水岛台；局部开放及岛槽作为条件候选。保持燃气/主水槽的原东墙区域，不承诺接口不动即可安装。','','## 主卧 B 与套卫','','1900×2120床架容纳1800×2000床垫；北床头，床尾至衣柜620mm。衣柜2200×600，800双层短挂、700长挂、700床品模块；柜门取移门，三抽分离到400×400×700床头柜，避免床尾同时站人和拉抽。净挂杆长度 '+str(sum(a['rail_mm'] for a in master))+'mm。南侧衣柜西端让出凹凸窗边路径。另一侧床头灯与充电按墙面点位预留，未用柜子占掉入卫通路。','','## 儿童房 A','','1200床垫、独立1200×600书桌、1800衣柜与1500低柜；保留活动区和照护路径。1500成长床作为独立候选，需重整活动包络，不能只换床便宣称所有使用不变。儿童桌高700为占位，可调范围与椅高必须按孩子身高选择。','','## 客房 C','','1620×2120床架配1500床垫；床两侧名义间距约511/510mm，单人可达但携篮到窗受限。衣柜置南侧1300×600；400深窄行李台置西侧。横床候选两侧通行变窄，按路线及使用区结果取舍。','','## 客餐厨与玄关','','北段沙发投影，咖啡柜在北端；南段1500×750干岛、1600×850餐桌与共享学习桌。餐椅四人常态与两端加椅六人分图；临时六人需试坐，西端椅影响到桌端点，路线端点在端椅外侧定义。东南鞋衣柜与换鞋凳分段沿东墙布置。岛台与共享学习操作会重叠，需错时。厨房采用独立可关闭推拉入口，局部开放列候选。','','## 两卫与家政','','两卫各900深淋浴，固定半幅玻璃与800名义入口；卫生间B套内进入，A服务公共区。湿区范围保持概念原边界；排污与坡度未核。阳台洗烘叠放和基站为候选，晾晒要收起后通行/装卸。515宽储物间仅安排深抽出单元/清洁器具，轨道载荷须专门设计。','','## 候选的比较顺序','','先实体、必要路线，再操作、收纳和拆改。推荐不依赖开放厨房或岛槽排水许可。下表为独立几何计算，未将候选覆盖到主模型。','','| 候选 | 实体命中 | 500路线 | 拆改序 |','| --- | --- | ---: | ---: |']
 for c in C['candidates']:desc.append(f"| {c['label']} | {c['fixed_hits'] or '无'} | {c['single_routes_passed']}/{c['route_count']} | {c['cost_rank']} |")
 desc+=['','候选床向比较保留基线操作区，作为保守约束；舒适性与真实床头方向需进一步试摆。开放厨房比较采用整段西墙移除的上界情景；实际只能在结构许可范围局部开放，保留边柱/门垛后必须重算。','', '## 材质与照明','','暖白柜门、木色柜体/地板、少量绿色软装；模型有材质、灯光及7个新定位相机。光线未渲染、未测照度。全屋通照、床头、学习、台面任务照明为点位概念。新风为讨论预留，需独立专业计算。']
 write('docs/design.md','\n'.join(desc))
 write('README.md',f'''# 157furnish · R1

本户型独立的三房两卫方案。先打开 [离线方案册](docs/方案册.html)，查看 [设计取舍](docs/design.md)、[核验摘要](docs/verification.md)及[现场条件](docs/constraints.md)。

- {len(I)}张可编辑SVG及对应PNG，见 [图纸](drawings/svg)。
- [Blender](model/157furnish_R1.blend)与[GLB](model/157furnish_R1.glb)，包含概念家具、柜体、门窗；未生成三维效果图。
- [表格](tables)、[唯一布局源](data/layout.json)、[独立重建说明](docs/handoff.md)。

固定与单人基线检查不代表全部使用通过；携篮、900目标、设备开启及多人操作的限制公开保留。尺寸来自原图标注、推导及显式概念参数，不能用于施工或柜体下单。

布局校验值：`{SHA}`。参考项目保持原样，重建不读取参考项目。
''')
 write('docs/handoff.md','''# 接手与重建

数据唯一入口 `data/layout.json`：毫米，X东Y北Z上。`dimensions`记录尺寸链及假设；`footprint_boxes`定义地面分区和路线外边界，房间盒仅作功能底图，并非产权/套内面积。墙/洞口由edges重建，实体由furniture，操作由operations，路线端点由routes，六人加椅由states，水电/空调/候选均在同文件。模型统一除1000换算米。

## 环境与命令

Python 3.13（本机），依赖见requirements.txt：Pillow、NumPy。Blender 5.2.1 LTS（本机已验证）。Windows中文字体默认msyh.ttc；其他系统需安装兼容字体并修改build_drawings.py字体入口。首次可 `python -m pip install -r requirements.txt`。重建不需要网络或176furnish目录。

```powershell
python scripts/rebuild.py --blender D:/Users/11171344/blender/blender.exe --repeat
```

其他机器传自己的Blender路径。顺序：使用核验→建模→重新打开blend/GLB→二维图表→文档→交付核验。默认绝不渲染。`--repeat`重复整个生成过程，比较SVG/PNG/CSV/文档/布局及模型几何快照的校验值；Blender/GLB二进制不承诺逐字节一致，改用重新打开的实际网格核验。

另外可执行 `python scripts/verify_clean_rebuild.py --blender <Blender路径>`：只复制scripts、data、requirements及原始照片到新的临时目录，从空输出目录重建，逐项比较图表/文档/几何快照；临时目录经绝对路径检查后清理。证明生成不依赖已有模型或参考项目。结果保存在reports/clean_rebuild.json。

只改文字/二维排版可用 `python scripts/build_drawings.py` 和 `python scripts/publish_docs.py`，前提是布局和模型脚本校验值没有变化；过期模型快照会被拒绝。修改布局、模型代码后必须全量重建。生成产物中的手工修改会被覆盖，应回写源数据/脚本。

## 模型

帧1关闭、帧90开启。普通柜门90度概念铰链、主/客衣柜分轨移门、抽屉450mm平移；设备面板平移600展示服务空间，不等同厂家开门轨迹。检查只排除与其他实体冲突，柜内真实滑轨/铰链与板件干涉仍需厂家深化。所有门同时播放仅作运动演示。

`Inspection_Envelopes`、`Ceilings`、`Dining_6_extra`默认隐藏。六人组只是加两端椅，启用时保留四人基础组。GLB导出静态帧1的推荐四人实体，不带检查包络/顶棚/六人加椅；Blender保留编辑层、动画、材质、灯光和7相机。当前构件为概念尺寸建模，不是品牌产品或五金加工模型。

模型验证临时启用隐藏层读取世界坐标，但不另存；避免隐藏层未求值造成假尺寸异常。`projection_snapshot.json`由真实家具网格的世界包围盒生成，不把源JSON简单复制冒充模型核验。

## 继承与独立性

参考项目仅用于学习统一坐标、状态分图、门扇采样、50mm网格路线、模型重开和离线交付机制；其脚本高度绑定旧房，未复制旧坐标/房号。所有本项目生成器在scripts内自包含。明确继承的生活参数是165cm主厨、暖白木色少量绿色和北京气候假设；未找到的家庭成员身高没有补造。

核验摘要三分：数据交付可通过；使用可部分通过；现场条件保持待核。不要用交付通过覆盖路线失败，也不要用本项目名称推算面积。
''')
 write('AGENTS.md','''# 接手约定

先读README.md、docs/handoff.md及docs/constraints.md。唯一布局坐标源data/layout.json，所有生成毫米转米。不得修改兄弟参考项目。不得执行三维渲染。原始照片保持原样。

所有未实测尺寸须标明来源与状态；禁止按照片像素冒充实测或按项目名推算面积。候选不得覆盖推荐状态，过期模型投影必须拒绝。

修改后运行scripts/rebuild.py全量核验。保留失败与现场条件；数据一致性、使用检查和专业/现场核实分别报告。读图与操作演示仅概念，不生成施工或下单承诺。
''')
 write('docs/drawing-visual-review.md','''# 二维图纸人工抽查

检查推荐总图、主卧局部、柜体立面和水电图的中文、框线、比例与注释。初次抽查发现局部图未裁剪、邻室绘制压到标题和右侧说明，已增加同范围SVG裁剪和PNG图层裁剪，重建后复查。总图以对象编号为索引，中文逐室图及家具尺寸表对应；图纸不承诺屏幕显示的物理打印比例，请使用1000mm比例尺。

所有图纸为二维矢量表达及其同源PNG，没有运行三维渲染。PNG与SVG使用同一绘图原语；字体基线在两种引擎间可能有像素差异，不作逐像素相同声明。
 ''')
 # This table is generated here, after drawings; refresh booklet links even on a completely clean first build.
 booklet=ROOT/'docs/方案册.html';page=booklet.read_text(encoding='utf-8');links=''.join(f'<li><a href="../tables/{html.escape(p.name)}">{html.escape(p.name)}</a></li>' for p in sorted((ROOT/'tables').glob('*.csv')));page=re.sub(r'<h2>表格</h2><ul>.*?</ul>','<h2>表格</h2><ul>'+links+'</ul>',page,flags=re.S);booklet.write_text(page,encoding='utf-8')
 print('DOCS_COMPLETE')
if __name__=='__main__':main()
