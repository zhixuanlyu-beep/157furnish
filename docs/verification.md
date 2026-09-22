# R2 核验摘要

版本 `R2`；布局 SHA256 `d9b4359b2b866b116cf96863e3055fa512a87d94c43bcca20d89990c7ed41a96`。

**数据一致性、使用检查、现场条件分别报告。** 见[交付核验](../reports/delivery.json)及[校验清单](../reports/manifest.json)。

- 固定实体冲突：0 项，明细 `[]`。
- 坐便前距：wcB 903.0mm；wcA 1241.0mm（概念几何，目标750／底线600）。
- 房门把手采样命中：0 扇；推拉未通过：[]。
- 柜门／抽屉外部命中：{}。柜内真实五金仍须深化。
- 日常500基线：通过概念检查；全部状态及宽度：未全部通过。
- 两燃料 Blender／GLB 独立重开：True；实际世界网格误差阈值0.1mm。
- 现场条件：待核，两个燃料均未取得实施条件确认。

路线用50mm网格，检查500单人、600／620携篮和900目标，完整包络必须落入目标区域。窄缝可能受网格对齐影响，失败不等于连续空间不可达证明。400站位仅原地站立概念，不代替500通路。入户路线从玄关内起算；楼外搬入未核。

| 状态 | 包络mm | 功能 | 具体限制 | 目标附近实体 |
| --- | ---: | --- | --- | --- |
| normal4 | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| normal4 | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| normal4 | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| normal4 | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| normal4 | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| normal4 | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| normal4 | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| normal4 | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| normal4 | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill |
| normal4 | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| normal4 | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| normal4 | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| normal4 | 900 | 会客 | 起点包络受阻 | coffee_table |
| normal4 | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| normal4 | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| normal4 | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| normal4 | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| normal4 | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| normal4 | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| normal4 | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal4 | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, living_balcony_parked, living_balcony_fixed |
| normal4 | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| normal4 | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| normal4 | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| normal4 | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal4 | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| normal4 | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 500 | 就餐 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | store_e_0, store_e_end, table, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 500 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | store_e_0, store_e_end, table, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| normal6 | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| normal6 | 600 | 就餐 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| normal6 | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| normal6 | 600 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 600 | 储物取物 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| normal6 | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| normal6 | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| normal6 | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| normal6 | 620 | 就餐 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill |
| normal6 | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| normal6 | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| normal6 | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| normal6 | 620 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 620 | 储物取物 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 900 | 会客 | 起点包络受阻 | coffee_table |
| normal6 | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| normal6 | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| normal6 | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| normal6 | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| normal6 | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| normal6 | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| normal6 | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, living_balcony_parked, living_balcony_fixed |
| normal6 | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| normal6 | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| normal6 | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| normal6 | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| normal6 | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| normal6 | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, six_w, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| chairs_pulled | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| chairs_pulled | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| chairs_pulled | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| chairs_pulled | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| chairs_pulled | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| chairs_pulled | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| chairs_pulled | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| chairs_pulled | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| chairs_pulled | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill |
| chairs_pulled | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| chairs_pulled | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| chairs_pulled | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| chairs_pulled | 900 | 会客 | 起点包络受阻 | coffee_table |
| chairs_pulled | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| chairs_pulled | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| chairs_pulled | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| chairs_pulled | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| chairs_pulled | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| chairs_pulled | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| chairs_pulled | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| chairs_pulled | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, living_balcony_parked, living_balcony_fixed |
| chairs_pulled | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| chairs_pulled | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| chairs_pulled | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| chairs_pulled | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| chairs_pulled | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| chairs_pulled | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| laundry_open | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| laundry_open | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| laundry_open | 600 | 洗烘 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | north_balcony_0_sill, laundry_moving |
| laundry_open | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| laundry_open | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| laundry_open | 600 | 阳台烹饪 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked |
| laundry_open | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| laundry_open | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| laundry_open | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| laundry_open | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| laundry_open | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill, laundry_moving |
| laundry_open | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| laundry_open | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| laundry_open | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| laundry_open | 620 | 阳台烹饪 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked |
| laundry_open | 900 | 会客 | 起点包络受阻 | coffee_table |
| laundry_open | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| laundry_open | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| laundry_open | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| laundry_open | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| laundry_open | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| laundry_open | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| laundry_open | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| laundry_open | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, laundry_moving, living_balcony_parked, living_balcony_fixed |
| laundry_open | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| laundry_open | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| laundry_open | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| laundry_open | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| laundry_open | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| laundry_open | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| temporary_drying | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| temporary_drying | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| temporary_drying | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| temporary_drying | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| temporary_drying | 600 | 阳台烹饪 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked |
| temporary_drying | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| temporary_drying | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| temporary_drying | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| temporary_drying | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| temporary_drying | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill, drying |
| temporary_drying | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| temporary_drying | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| temporary_drying | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| temporary_drying | 620 | 阳台烹饪 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked |
| temporary_drying | 900 | 会客 | 起点包络受阻 | coffee_table |
| temporary_drying | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| temporary_drying | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| temporary_drying | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| temporary_drying | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| temporary_drying | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| temporary_drying | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| temporary_drying | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| temporary_drying | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, drying, living_balcony_parked, living_balcony_fixed |
| temporary_drying | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| temporary_drying | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| temporary_drying | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| temporary_drying | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| temporary_drying | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| temporary_drying | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| cooking | 500 | 阳台烹饪 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill, balcony_s_1, hob, cook, kitchen_balcony_jamb1 |
| cooking | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| cooking | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| cooking | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| cooking | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| cooking | 600 | 阳台烹饪 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, cook, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked |
| cooking | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| cooking | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| cooking | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| cooking | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| cooking | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill |
| cooking | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| cooking | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| cooking | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| cooking | 620 | 阳台烹饪 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, cook, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked |
| cooking | 900 | 会客 | 起点包络受阻 | coffee_table |
| cooking | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| cooking | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| cooking | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| cooking | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| cooking | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| cooking | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| cooking | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| cooking | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, living_balcony_parked, living_balcony_fixed |
| cooking | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| cooking | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| cooking | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| cooking | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| cooking | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, cook, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| cooking | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| luggage_open | 500 | 客房睡眠 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | C_east_end, bedC |
| luggage_open | 500 | 客房到窗 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC |
| luggage_open | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| luggage_open | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| luggage_open | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| luggage_open | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| luggage_open | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| luggage_open | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| luggage_open | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| luggage_open | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| luggage_open | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill |
| luggage_open | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| luggage_open | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| luggage_open | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| luggage_open | 900 | 会客 | 起点包络受阻 | coffee_table |
| luggage_open | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| luggage_open | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| luggage_open | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| luggage_open | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| luggage_open | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| luggage_open | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| luggage_open | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| luggage_open | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, living_balcony_parked, living_balcony_fixed |
| luggage_open | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| luggage_open | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| luggage_open | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| luggage_open | 900 | 岛台至餐桌 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| luggage_open | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| luggage_open | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| screen_lowered | 600 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| screen_lowered | 600 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| screen_lowered | 600 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| screen_lowered | 600 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| screen_lowered | 620 | 儿童睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | bedA, chairA |
| screen_lowered | 620 | 客房睡眠 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | C_east_end, bedC, sofa |
| screen_lowered | 620 | 主卫 | 目标区可站立但50mm网格路线受阻；非连续空间不可达证明 | AB_east_0, AB_east_1, wcB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked |
| screen_lowered | 620 | 公卫 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | wcA, basinA, glassA |
| screen_lowered | 620 | 洗烘 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | north_balcony_0_sill |
| screen_lowered | 620 | 儿童到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | west_AB_0_sill, bedA, toys |
| screen_lowered | 620 | 客房到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa |
| screen_lowered | 620 | 主卧到窗 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| screen_lowered | 620 | 岛台至餐桌 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| screen_lowered | 900 | 会客 | 起点包络受阻 | coffee_table, screen |
| screen_lowered | 900 | 儿童睡眠 | 起点包络受阻 | bedA, chairA |
| screen_lowered | 900 | 主卧睡眠 | 起点包络受阻 | AB_east_0, AB_east_1, bath_north_0, bedB, basinB, bathB_entry_jamb1, bathB_entry_jamb2, B_entry_jamb1 |
| screen_lowered | 900 | 客房睡眠 | 起点包络受阻 | C_east_end, bedC, sofa |
| screen_lowered | 900 | 主卫 | 起点包络受阻 | AB_east_0, AB_east_1, wcB, basinB, glassB, bathB_entry_jamb1, bathB_entry_jamb2, bathB_entry_parked, bathB_entry_handle |
| screen_lowered | 900 | 公卫 | 起点包络受阻 | wcA, basinA, glassA |
| screen_lowered | 900 | 备餐 | 起点包络受阻 | island, sink, dishwasher, prep, fridge |
| screen_lowered | 900 | 就餐 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| screen_lowered | 900 | 洗烘 | 起点包络受阻 | north_balcony_0_sill, living_balcony_parked, living_balcony_fixed |
| screen_lowered | 900 | 儿童到窗 | 起点包络受阻 | west_AB_0, west_AB_0_sill, A_south_0, bedA, toys |
| screen_lowered | 900 | 客房到窗 | 起点包络受阻 | balcony_w_0, balcony_w_0_sill, north_C_0_sill, north_C_end, C_east_end, balcony_s_0, bedC, sofa, laundry |
| screen_lowered | 900 | 主卧到窗 | 起点包络受阻 | south_B_0, south_B_0_sill, south_B_end, B_step_e_end, south_main_0, wardB |
| screen_lowered | 900 | 备餐至岛台 | 目标区域无完整可站立包络（含墙/家具/当前开启件） | island, screen |
| screen_lowered | 900 | 岛台至餐桌 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |
| screen_lowered | 900 | 阳台烹饪 | 起点包络受阻 | north_balcony_0_sill, balcony_s_1, balcony_s_end, hob, kitchen_balcony_jamb1, kitchen_balcony_jamb2, kitchen_balcony_parked, kitchen_balcony_handle |
| screen_lowered | 900 | 储物取物 | 起点包络受阻 | bath_north_end, store_e_0, store_e_end, table, dining1, dining3, storage, store_entry_jamb1, store_entry_jamb2, store_entry_parked, store_entry_handle |

## 操作与错时

固定实体命中：`{'bedA_west': ['west_AB_0_sill', 'west_AB_end']}`。儿童床西侧不是必要照护边，东侧为照护入口；其余必要操作命中不能用错时掩盖。

必要站位未通过：`[]`，见[功能站位表](../tables/功能站位.csv)。

共享包络需错时／避让：wardA_use / child_play；shoe_use / robot_use；shoe_use / robot_service；basinB_use / dryB；basinB_use / wcB_use；child_play / child_pull；child_play / bedA_east；dryA / wcA_use；dryB / wcB_use；bedsideB_use / bedB_west。同设备重复包络不算两人并用。

洗烘开启只把开启部件加入路线障碍；烹饪状态将灶前操作者加入障碍后核第二人。临时晾晒、行李展开、餐椅拉出、六人及幕布放下分别核验。设备动画是600服务空间示意，非真实厂家轨迹。

回归覆盖旧坐便、推拉越界、行李架堵床侧、成长床目标、洗烘误判及模型依赖过期。重复与独立重建见reports/repeatability.json和reports/clean_rebuild.json，不承诺模型二进制逐字节相同。
