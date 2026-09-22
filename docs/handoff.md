# 接手与独立重建

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
