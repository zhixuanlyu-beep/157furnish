# 接手与重建

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
