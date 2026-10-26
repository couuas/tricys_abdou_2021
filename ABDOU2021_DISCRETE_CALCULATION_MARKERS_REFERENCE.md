# Abdou 2021 原始文献离散计算点真值数据库与永久基准档案
# (Abdou 2021 Discrete Calculation Markers Reference Database)

> **权威文献来源**：  
> **M. Abdou, M. Riva, A. Ying, C. Day, A. Loarte, L. R. Baylor, P. Humrickhouse, T. F. Fuerst, S. Cho**  
> *"Physics and technology considerations for the deuterium–tritium fuel cycle and conditions for tritium fuel self sufficiency"*  
> **Nuclear Fusion**, Vol. 61, No. 1, 013001 (2021). [DOI: 10.1088/1741-4326/abbf35](https://doi.org/10.1088/1741-4326/abbf35)  
>
> **本档案定位与用途**：  
> 本文档是 TRICYS 验证与对标套件（V&V）的**永久离散真值基准数据归档**。  
> 针对原文献中未公布完整数值表格的 Figures 4 ~ 15，采用**亚像素计算机视觉（Sub-pixel Computer Vision）与加权双向质心定位技术**，从原版高分辨率矢量光栅图像中严格提取了文献作者的所有**离散数值模拟计算点（Discrete Calculation Markers）**，并通过像素级图形重合叠加（Pixel Overlay）严格自检。  
> **总共提取 11 幅图表、共计 292 组离散计算真值点**。

---

## 目录
1. [总览与图表标定参数映射表](#1-总览与图表标定参数映射表)
2. [Fig 04: 所需 TBR vs 核心乘积 (Required TBR vs Core Product)](#fig-04-文献离散计算真值表)
3. [Fig 05: 所需 TBR vs 反应堆可用率 (Required TBR vs Availability Factor)](#fig-05-文献离散计算真值表)
4. [Fig 06: 所需 TBR 削减 vs DIR 旁路比 (Mitigation of Required TBR via DIR)](#fig-06-文献离散计算真值表)
5. [Fig 07: 近期装置 TBR vs 核心乘积与倍增时间 (Near-Term FNSF TBR vs Doubling Time, AF=30%)](#fig-07-文献离散计算真值表)
6. [Fig 08: 商业电站 TBR vs 核心乘积与倍增时间 (Commercial TBR vs Doubling Time, AF=80%)](#fig-08-文献离散计算真值表)
7. [Fig 10: 启动氚库存塌陷 vs 核心乘积 (Start-up Tritium Inventory vs Core Product)](#fig-10-文献离散计算真值表)
8. [Fig 11: 启动库存削减 vs DIR 旁路比 (Start-up Inventory Reduction via DIR)](#fig-11-文献离散计算真值表)
9. [Fig 12: 启动库存 vs 应急储备时间 (Start-up Inventory vs Reserve Time)](#fig-12-文献离散计算真值表)
10. [Fig 13: 储备库存 vs 应急储备时间 (Reserve Inventory vs Reserve Time)](#fig-13-文献离散计算真值表)
11. [Fig 14: 所需 TBR vs 应急储备时间 (Required TBR vs Reserve Time)](#fig-14-文献离散计算真值表)
12. [Fig 15: 启动库存线性标度律 vs 聚变热功率 (Start-up Inventory Linear Scaling with Fusion Power)](#fig-15-文献离散计算真值表)
13. [产物文件清单与数据调用指引](#13-产物文件清单与数据调用指引)

---

## 1. 总览与图表标定参数映射表

| 图号 | 物理主题 | 自变量 (X) | 因变量 (Y) | 曲线组 | 数据点数 | 验证叠加图 |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **Fig 04** | 所需 TBR vs 核心乘积 | eta_f*fb in [0.3%, 5.0%] | TBR_R in [1.00, 1.30] | tp = 1, 4, 12 h | 27 | [Fig04_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig04_digitization_overlay.png) |
| **Fig 05** | 所需 TBR vs 可用率 | AF in [6.5%, 100%] | TBR_R in [1.00, 1.30] | eta_f*fb = 0.5, 1, 2, 3% | 22 | [Fig05_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig05_digitization_overlay.png) |
| **Fig 06** | 所需 TBR vs DIR 旁路比 | f_DIR in [10%, 90%] | TBR_R in [1.00, 1.25] | eta_f*fb = 0.5, 1, 2, 3% | 20 | [Fig06_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig06_digitization_overlay.png) |
| **Fig 07** | 近期装置 TBR vs 倍增时间 | eta_f*fb in [0.5%, 5.0%] | TBR_R in [1.00, 1.30] | td = 1, 3, 5, 7 yr (AF=30%) | 29 | [Fig07_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig07_digitization_overlay.png) |
| **Fig 08** | 商业电站 TBR vs 倍增时间 | eta_f*fb in [0.5%, 5.0%] | TBR_R in [1.00, 1.25] | td = 1, 3, 5, 7 yr (AF=80%) | 32 | [Fig08_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig08_digitization_overlay.png) |
| **Fig 10** | 启动库存 vs 核心乘积 | eta_f*fb in [0.5%, 5.0%] | I_S^0 in [0, 40] kg | tp = 1, 4, 12 h | 24 | [Fig10_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig10_digitization_overlay.png) |
| **Fig 11** | 启动库存 vs DIR 旁路比 | f_DIR in [10%, 90%] | I_S^0 in [0, 45] kg | eta_f*fb = 0.5, 1, 2, 3% | 20 | [Fig11_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig11_digitization_overlay.png) |
| **Fig 12** | 启动库存 vs 储备时间 | tr in [0, 48] h | I_S^0 in [0, 50] kg | eta_f*fb = 0.5, 1, 2, 3, 5% | 30 | [Fig12_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig12_digitization_overlay.png) |
| **Fig 13** | 储备库存 vs 储备时间 | tr in [0, 48] h | Ir in [0, 50] kg | eta_f*fb = 0.5, 1, 2, 3, 5% | 30 | [Fig13_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig13_digitization_overlay.png) |
| **Fig 14** | 所需 TBR vs 储备时间 | tr in [0, 48] h | TBR_R in [1.00, 1.30] | eta_f*fb = 0.5, 1, 2, 3, 5% | 30 | [Fig14_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig14_digitization_overlay.png) |
| **Fig 15** | 启动库存 vs 聚变功率 | Pfus in [0, 3000] MW | I_S^0 in [0, 45] kg | eta_f*fb=0.5, 5.0% (tr=6, 24h) | 28 | [Fig15_overlay](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig15_digitization_overlay.png) |
| **合计** | - | - | - | **41 条物理曲线** | **292 组真值点** | - |

---

## Fig04: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig04.png`
* **像素重合验证图**：[Fig04_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig04_digitization_overlay.png)
* **独立 CSV 文件**：[Fig04_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig04_literature_markers.csv)

| figure   | curve   |   tp_hours | marker_symbol   |   eta_f_fb_nominal_pct |   eta_f_fb_detected_pct |   required_tbr |   pixel_x |   pixel_y |
|:---------|:--------|-----------:|:----------------|-----------------------:|------------------------:|---------------:|----------:|----------:|
| Fig04    | tp_1h   |          1 | circle          |                    0.3 |                  0.2974 |         1.2794 |    327.91 |    114.63 |
| Fig04    | tp_1h   |          1 | circle          |                    0.5 |                  0.4952 |         1.1687 |    396.34 |    617.36 |
| Fig04    | tp_1h   |          1 | circle          |                    0.8 |                  0.7961 |         1.1066 |    500.46 |    899.18 |
| Fig04    | tp_1h   |          1 | circle          |                    1   |                  0.9929 |         1.0864 |    568.53 |    991.72 |
| Fig04    | tp_1h   |          1 | circle          |                    1.5 |                  1.4966 |         1.0595 |    742.81 |   1119.07 |
| Fig04    | tp_1h   |          1 | circle          |                    2   |                  1.9913 |         1.045  |    914.01 |   1182.18 |
| Fig04    | tp_1h   |          1 | circle          |                    2.5 |                  2.498  |         1.0369 |   1089.33 |   1219.44 |
| Fig04    | tp_1h   |          1 | circle          |                    3   |                  2.9987 |         1.0316 |   1262.55 |   1244.56 |
| Fig04    | tp_1h   |          1 | circle          |                    4   |                  3.9996 |         1.0244 |   1608.87 |   1276.25 |
| Fig04    | tp_1h   |          1 | circle          |                    5   |                  4.975  |         1.0208 |   1946.34 |   1295.63 |
| Fig04    | tp_4h   |          4 | square          |                    0.5 |                  0.4943 |         1.2116 |    396.02 |    418.43 |
| Fig04    | tp_4h   |          4 | square          |                    0.8 |                  0.7937 |         1.1347 |    499.61 |    775.18 |
| Fig04    | tp_4h   |          4 | square          |                    1   |                  0.9917 |         1.1075 |    568.12 |    894.44 |
| Fig04    | tp_4h   |          4 | square          |                    1.5 |                  1.4924 |         1.0729 |    741.38 |   1051.74 |
| Fig04    | tp_4h   |          4 | square          |                    2   |                  1.9913 |         1.0549 |    913.99 |   1133.15 |
| Fig04    | tp_4h   |          4 | square          |                    2.5 |                  2.4926 |         1.0448 |   1087.45 |   1179.48 |
| Fig04    | tp_4h   |          4 | square          |                    3   |                  2.9991 |         1.0389 |   1262.67 |   1211.84 |
| Fig04    | tp_4h   |          4 | square          |                    4   |                  3.9944 |         1.0308 |   1607.08 |   1250.2  |
| Fig04    | tp_4h   |          4 | square          |                    5   |                  4.9823 |         1.0239 |   1948.89 |   1274.63 |
| Fig04    | tp_12h  |         12 | triangle        |                    0.8 |                  0.7954 |         1.2062 |    500.19 |    445.02 |
| Fig04    | tp_12h  |         12 | triangle        |                    1   |                  0.994  |         1.1655 |    568.93 |    631.43 |
| Fig04    | tp_12h  |         12 | triangle        |                    1.5 |                  1.4956 |         1.1119 |    742.49 |    877.59 |
| Fig04    | tp_12h  |         12 | triangle        |                    2   |                  1.9923 |         1.0843 |    914.35 |   1000.76 |
| Fig04    | tp_12h  |         12 | triangle        |                    2.5 |                  2.4957 |         1.0694 |   1088.52 |   1074.2  |
| Fig04    | tp_12h  |         12 | triangle        |                    3   |                  2.9999 |         1.0579 |   1262.96 |   1123.43 |
| Fig04    | tp_12h  |         12 | triangle        |                    4   |                  3.9935 |         1.0441 |   1606.75 |   1184.12 |
| Fig04    | tp_12h  |         12 | triangle        |                    5   |                  4.9803 |         1.0368 |   1948.18 |   1221.65 |

---

## Fig05: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig05.png`
* **像素重合验证图**：[Fig05_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig05_digitization_overlay.png)
* **独立 CSV 文件**：[Fig05_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig05_literature_markers.csv)

| figure   | curve           |   eta_f_fb_pct | marker_symbol   |   AF_nominal_pct |   AF_detected_pct |   required_tbr |   pixel_x |   pixel_y |
|:---------|:----------------|---------------:|:----------------|-----------------:|------------------:|---------------:|----------:|----------:|
| Fig05    | eta_f_fb_0.5pct |            0.5 | diamond         |             31.8 |             31.84 |         1.2948 |    758.55 |     43.76 |
| Fig05    | eta_f_fb_0.5pct |            0.5 | diamond         |             50   |             49.96 |         1.2127 |   1047.85 |    420.55 |
| Fig05    | eta_f_fb_0.5pct |            0.5 | diamond         |             77.8 |             77.73 |         1.1952 |   1491.34 |    501.11 |
| Fig05    | eta_f_fb_0.5pct |            0.5 | diamond         |            100   |             99.82 |         1.1852 |   1844.16 |    547.09 |
| Fig05    | eta_f_fb_1.0pct |            1   | triangle        |             18.9 |             18.9  |         1.2263 |    551.84 |    358.32 |
| Fig05    | eta_f_fb_1.0pct |            1   | triangle        |             31.8 |             31.77 |         1.1505 |    757.42 |    706.4  |
| Fig05    | eta_f_fb_1.0pct |            1   | triangle        |             50   |             49.94 |         1.1082 |   1047.52 |    900.24 |
| Fig05    | eta_f_fb_1.0pct |            1   | triangle        |             77.8 |             77.74 |         1.1    |   1491.48 |    937.84 |
| Fig05    | eta_f_fb_1.0pct |            1   | triangle        |            100   |             99.85 |         1.0951 |   1844.57 |    960.45 |
| Fig05    | eta_f_fb_2.0pct |            2   | square          |             10.4 |             10.37 |         1.1948 |    415.66 |    503.07 |
| Fig05    | eta_f_fb_2.0pct |            2   | square          |             18.9 |             18.88 |         1.1175 |    551.47 |    857.67 |
| Fig05    | eta_f_fb_2.0pct |            2   | square          |             31.8 |             31.78 |         1.0782 |    757.55 |   1038.11 |
| Fig05    | eta_f_fb_2.0pct |            2   | square          |             50   |             49.94 |         1.0561 |   1047.62 |   1139.43 |
| Fig05    | eta_f_fb_2.0pct |            2   | square          |             77.8 |             77.75 |         1.0522 |   1491.69 |   1157.24 |
| Fig05    | eta_f_fb_2.0pct |            2   | square          |            100   |             99.87 |         1.0493 |   1844.88 |   1170.67 |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |              6.5 |              6.53 |         1.2081 |    354.23 |    441.78 |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |             10.4 |             10.38 |         1.1344 |    415.81 |    779.91 |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |             18.9 |             18.92 |         1.0813 |    552.08 |   1023.8  |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |             31.8 |             31.78 |         1.0537 |    757.48 |   1150.36 |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |             50   |             49.97 |         1.0388 |   1047.98 |   1218.88 |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |             77.8 |             77.75 |         1.0354 |   1491.7  |   1234.42 |
| Fig05    | eta_f_fb_3.0pct |            3   | circle          |            100   |             99.85 |         1.0336 |   1844.64 |   1242.95 |

---

## Fig06: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig06.png`
* **像素重合验证图**：[Fig06_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig06_digitization_overlay.png)
* **独立 CSV 文件**：[Fig06_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig06_literature_markers.csv)

| figure   | curve           |   eta_f_fb_pct | marker_symbol   |   DIR_nominal_pct |   DIR_detected_pct |   required_tbr |   pixel_x |   pixel_y |
|:---------|:----------------|---------------:|:----------------|------------------:|-------------------:|---------------:|----------:|----------:|
| Fig06    | eta_f_fb_0.5pct |            0.5 | diamond         |                10 |                9.9 |         1.204  |    241.34 |    247.77 |
| Fig06    | eta_f_fb_0.5pct |            0.5 | diamond         |                30 |               30   |         1.1873 |    648.46 |    331.17 |
| Fig06    | eta_f_fb_0.5pct |            0.5 | diamond         |                50 |               50   |         1.171  |   1054.94 |    412.43 |
| Fig06    | eta_f_fb_0.5pct |            0.5 | diamond         |                70 |               69.9 |         1.154  |   1459.52 |    497.17 |
| Fig06    | eta_f_fb_0.5pct |            0.5 | diamond         |                90 |               90   |         1.1371 |   1866.3  |    581.58 |
| Fig06    | eta_f_fb_1.0pct |            1   | square          |                10 |                9.9 |         1.1039 |    241.28 |    747.29 |
| Fig06    | eta_f_fb_1.0pct |            1   | square          |                30 |               30   |         1.0958 |    648.08 |    788    |
| Fig06    | eta_f_fb_1.0pct |            1   | square          |                50 |               50   |         1.0875 |   1054.93 |    828.99 |
| Fig06    | eta_f_fb_1.0pct |            1   | square          |                70 |               69.9 |         1.0788 |   1459.49 |    872.71 |
| Fig06    | eta_f_fb_1.0pct |            1   | square          |                90 |               90   |         1.0706 |   1866.63 |    913.32 |
| Fig06    | eta_f_fb_2.0pct |            2   | circle          |                10 |                9.9 |         1.0537 |    241.64 |    998.17 |
| Fig06    | eta_f_fb_2.0pct |            2   | circle          |                30 |               30   |         1.0498 |    648.43 |   1017.39 |
| Fig06    | eta_f_fb_2.0pct |            2   | circle          |                50 |               50   |         1.0456 |   1054.95 |   1038.51 |
| Fig06    | eta_f_fb_2.0pct |            2   | circle          |                70 |               70   |         1.0417 |   1460.05 |   1058.06 |
| Fig06    | eta_f_fb_2.0pct |            2   | circle          |                90 |               90   |         1.0374 |   1866.9  |   1079.21 |
| Fig06    | eta_f_fb_3.0pct |            3   | cross           |                10 |               10   |         1.0377 |    242.11 |   1077.64 |
| Fig06    | eta_f_fb_3.0pct |            3   | cross           |                30 |               29.9 |         1.035  |    646.21 |   1091.49 |
| Fig06    | eta_f_fb_3.0pct |            3   | cross           |                50 |               50   |         1.0319 |   1055.97 |   1106.55 |
| Fig06    | eta_f_fb_3.0pct |            3   | cross           |                70 |               69.9 |         1.029  |   1459.45 |   1121.01 |
| Fig06    | eta_f_fb_3.0pct |            3   | cross           |                90 |               90   |         1.0269 |   1866.85 |   1131.87 |

---

## Fig07: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig07.png`
* **像素重合验证图**：[Fig07_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig07_digitization_overlay.png)
* **独立 CSV 文件**：[Fig07_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig07_literature_markers.csv)

| figure   | curve   |   td_years | marker_symbol   |   eta_f_fb_nominal_pct |   eta_f_fb_detected_pct |   required_tbr |   pixel_x |   pixel_y |
|:---------|:--------|-----------:|:----------------|-----------------------:|------------------------:|---------------:|----------:|----------:|
| Fig07    | td_1yr  |          1 | circle          |                    2   |                   2     |         1.278  |    943.8  |    118.65 |
| Fig07    | td_1yr  |          1 | circle          |                    3   |                   2.999 |         1.2361 |   1252.88 |    297.06 |
| Fig07    | td_1yr  |          1 | circle          |                    4   |                   3.998 |         1.1861 |   1561.96 |    510.04 |
| Fig07    | td_1yr  |          1 | circle          |                    5   |                   5     |         1.1562 |   1871.92 |    637.07 |
| Fig07    | td_3yr  |          3 | square          |                    0.8 |                   0.798 |         1.2521 |    571.97 |    228.96 |
| Fig07    | td_3yr  |          3 | square          |                    1   |                   0.998 |         1.2048 |    633.84 |    430.07 |
| Fig07    | td_3yr  |          3 | square          |                    1.5 |                   1.5   |         1.1376 |    789.02 |    716.36 |
| Fig07    | td_3yr  |          3 | square          |                    2   |                   1.997 |         1.1062 |    942.98 |    850.1  |
| Fig07    | td_3yr  |          3 | square          |                    2.5 |                   2.498 |         1.0862 |   1098.01 |    934.97 |
| Fig07    | td_3yr  |          3 | square          |                    3   |                   2.999 |         1.0731 |   1252.98 |    991    |
| Fig07    | td_3yr  |          3 | square          |                    4   |                   3.998 |         1.0571 |   1562.07 |   1058.95 |
| Fig07    | td_3yr  |          3 | square          |                    5   |                   5     |         1.0475 |   1871.92 |   1099.91 |
| Fig07    | td_5yr  |          5 | triangle        |                    0.8 |                   0.811 |         1.1963 |    575.96 |    466.27 |
| Fig07    | td_5yr  |          5 | triangle        |                    1   |                   1.004 |         1.1581 |    635.7  |    628.85 |
| Fig07    | td_5yr  |          5 | triangle        |                    1.5 |                   1.498 |         1.1101 |    788.61 |    833.16 |
| Fig07    | td_5yr  |          5 | triangle        |                    2   |                   1.996 |         1.084  |    942.55 |    944.64 |
| Fig07    | td_5yr  |          5 | triangle        |                    2.5 |                   2.498 |         1.0693 |   1097.92 |   1006.96 |
| Fig07    | td_5yr  |          5 | triangle        |                    3   |                   3     |         1.0591 |   1253.26 |   1050.53 |
| Fig07    | td_5yr  |          5 | triangle        |                    4   |                   3.999 |         1.0467 |   1562.33 |   1103.02 |
| Fig07    | td_5yr  |          5 | triangle        |                    5   |                   5.004 |         1.0393 |   1873.19 |   1134.83 |
| Fig07    | td_7yr  |          7 | star            |                    0.5 |                   0.497 |         1.2933 |    478.75 |     53.41 |
| Fig07    | td_7yr  |          7 | star            |                    0.8 |                   0.798 |         1.1843 |    572.02 |    517.45 |
| Fig07    | td_7yr  |          7 | star            |                    1   |                   0.998 |         1.149  |    633.84 |    667.88 |
| Fig07    | td_7yr  |          7 | star            |                    1.5 |                   1.497 |         1.1018 |    788.19 |    868.73 |
| Fig07    | td_7yr  |          7 | star            |                    2   |                   1.998 |         1.0771 |    943.16 |    973.99 |
| Fig07    | td_7yr  |          7 | star            |                    2.5 |                   2.499 |         1.0629 |   1098.08 |   1034.08 |
| Fig07    | td_7yr  |          7 | star            |                    3   |                   3     |         1.0533 |   1253.07 |   1075.06 |
| Fig07    | td_7yr  |          7 | star            |                    4   |                   3.999 |         1.0416 |   1562.14 |   1124.76 |
| Fig07    | td_7yr  |          7 | star            |                    5   |                   5     |         1.0342 |   1872.14 |   1156.5  |

---

## Fig08: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig08.png`
* **像素重合验证图**：[Fig08_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig08_digitization_overlay.png)
* **独立 CSV 文件**：[Fig08_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig08_literature_markers.csv)

| figure   | curve   |   td_years | marker_symbol   |   eta_f_fb_nominal_pct |   eta_f_fb_detected_pct |   required_tbr |   pixel_x |   pixel_y |
|:---------|:--------|-----------:|:----------------|-----------------------:|------------------------:|---------------:|----------:|----------:|
| Fig08    | td_1yr  |          1 | circle          |                    1.5 |                   1.499 |         1.203  |    784.74 |    266.04 |
| Fig08    | td_1yr  |          1 | circle          |                    2   |                   1.998 |         1.1552 |    938.04 |    508.37 |
| Fig08    | td_1yr  |          1 | circle          |                    2.5 |                   2.498 |         1.1281 |   1091.84 |    645.99 |
| Fig08    | td_1yr  |          1 | circle          |                    3   |                   2.998 |         1.11   |   1245.67 |    737.29 |
| Fig08    | td_1yr  |          1 | circle          |                    4   |                   3.997 |         1.0853 |   1552.65 |    862.49 |
| Fig08    | td_1yr  |          1 | circle          |                    5   |                   4.999 |         1.0721 |   1860.7  |    929.7  |
| Fig08    | td_3yr  |          3 | square          |                    0.8 |                   0.797 |         1.1612 |    569.12 |    478.05 |
| Fig08    | td_3yr  |          3 | square          |                    1   |                   0.999 |         1.131  |    631.12 |    631.09 |
| Fig08    | td_3yr  |          3 | square          |                    1.5 |                   1.5   |         1.0892 |    785.03 |    842.97 |
| Fig08    | td_3yr  |          3 | square          |                    2   |                   1.997 |         1.069  |    937.85 |    945.12 |
| Fig08    | td_3yr  |          3 | square          |                    2.5 |                   2.498 |         1.0561 |   1092.04 |   1010.87 |
| Fig08    | td_3yr  |          3 | square          |                    3   |                   2.999 |         1.0481 |   1246.02 |   1051.1  |
| Fig08    | td_3yr  |          3 | square          |                    4   |                   3.998 |         1.0371 |   1552.96 |   1107.01 |
| Fig08    | td_3yr  |          3 | square          |                    5   |                   5     |         1.0312 |   1861.02 |   1136.97 |
| Fig08    | td_5yr  |          5 | triangle        |                    0.5 |                   0.496 |         1.1707 |    476.6  |    429.9  |
| Fig08    | td_5yr  |          5 | triangle        |                    0.8 |                   0.796 |         1.1085 |    568.83 |    745.27 |
| Fig08    | td_5yr  |          5 | triangle        |                    1   |                   0.997 |         1.0877 |    630.37 |    850.63 |
| Fig08    | td_5yr  |          5 | triangle        |                    1.5 |                   1.494 |         1.0598 |    783.31 |    991.8  |
| Fig08    | td_5yr  |          5 | triangle        |                    2   |                   1.996 |         1.0457 |    937.51 |   1063.55 |
| Fig08    | td_5yr  |          5 | triangle        |                    2.5 |                   2.496 |         1.0376 |   1091.42 |   1104.31 |
| Fig08    | td_5yr  |          5 | triangle        |                    3   |                   2.995 |         1.0317 |   1244.68 |   1134.28 |
| Fig08    | td_5yr  |          5 | triangle        |                    4   |                   3.994 |         1.0252 |   1551.87 |   1167.37 |
| Fig08    | td_5yr  |          5 | triangle        |                    5   |                   4.997 |         1.0219 |   1860.13 |   1183.79 |
| Fig08    | td_7yr  |          7 | star            |                    0.5 |                   0.498 |         1.1404 |    477.23 |    583.22 |
| Fig08    | td_7yr  |          7 | star            |                    0.8 |                   0.801 |         1.0884 |    570.16 |    846.99 |
| Fig08    | td_7yr  |          7 | star            |                    1   |                   0.999 |         1.0714 |    631.1  |    933.03 |
| Fig08    | td_7yr  |          7 | star            |                    1.5 |                   1.499 |         1.0489 |    784.77 |   1046.93 |
| Fig08    | td_7yr  |          7 | star            |                    2   |                   1.999 |         1.0378 |    938.35 |   1103.29 |
| Fig08    | td_7yr  |          7 | star            |                    2.5 |                   2.498 |         1.0306 |   1091.96 |   1139.91 |
| Fig08    | td_7yr  |          7 | star            |                    3   |                   2.999 |         1.0259 |   1245.98 |   1163.56 |
| Fig08    | td_7yr  |          7 | star            |                    4   |                   3.998 |         1.0205 |   1553.07 |   1191.31 |
| Fig08    | td_7yr  |          7 | star            |                    5   |                   4.999 |         1.0176 |   1860.72 |   1205.77 |

---

## Fig10: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig10.png`
* **像素重合验证图**：[Fig10_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig10_digitization_overlay.png)
* **独立 CSV 文件**：[Fig10_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig10_literature_markers.csv)

| figure   | curve   |   tp_hours | marker_symbol   |   eta_f_fb_nominal_pct |   eta_f_fb_detected_pct |   startup_inventory_IS0_kg |   pixel_x |   pixel_y |
|:---------|:--------|-----------:|:----------------|-----------------------:|------------------------:|---------------------------:|----------:|----------:|
| Fig10    | tp_1h   |          1 | circle          |                    0.5 |                   0.496 |                     29.6   |    383.77 |    351.83 |
| Fig10    | tp_1h   |          1 | circle          |                    0.8 |                   0.796 |                     18.942 |    483.12 |    686.76 |
| Fig10    | tp_1h   |          1 | circle          |                    1   |                   0.997 |                     15.286 |    549.35 |    801.64 |
| Fig10    | tp_1h   |          1 | circle          |                    1.5 |                   1.497 |                     10.462 |    714.55 |    953.22 |
| Fig10    | tp_1h   |          1 | circle          |                    2   |                   1.998 |                      8.062 |    880.07 |   1028.65 |
| Fig10    | tp_1h   |          1 | circle          |                    2.5 |                   2.5   |                      6.656 |   1045.91 |   1072.84 |
| Fig10    | tp_1h   |          1 | circle          |                    3   |                   2.996 |                      5.738 |   1209.86 |   1101.69 |
| Fig10    | tp_1h   |          1 | circle          |                    4   |                   3.997 |                      4.503 |   1540.53 |   1140.5  |
| Fig10    | tp_1h   |          1 | circle          |                    5   |                   4.999 |                      3.807 |   1871.68 |   1162.36 |
| Fig10    | tp_4h   |          4 | square          |                    0.8 |                   0.796 |                     26.794 |    482.94 |    440.01 |
| Fig10    | tp_4h   |          4 | square          |                    1   |                   0.995 |                     21.594 |    548.8  |    603.4  |
| Fig10    | tp_4h   |          4 | square          |                    1.5 |                   1.497 |                     14.663 |    714.66 |    821.2  |
| Fig10    | tp_4h   |          4 | square          |                    2   |                   1.997 |                     11.258 |    879.92 |    928.21 |
| Fig10    | tp_4h   |          4 | square          |                    2.5 |                   2.499 |                      9.244 |   1045.6  |    991.5  |
| Fig10    | tp_4h   |          4 | square          |                    3   |                   2.995 |                      7.841 |   1209.53 |   1035.58 |
| Fig10    | tp_4h   |          4 | square          |                    4   |                   3.997 |                      6.135 |   1540.65 |   1089.22 |
| Fig10    | tp_4h   |          4 | square          |                    5   |                   4.999 |                      5.111 |   1871.6  |   1121.38 |
| Fig10    | tp_12h  |         12 | triangle        |                    1   |                   0.996 |                     38.505 |    549.09 |     71.98 |
| Fig10    | tp_12h  |         12 | triangle        |                    1.5 |                   1.496 |                     25.95  |    714.38 |    466.52 |
| Fig10    | tp_12h  |         12 | triangle        |                    2   |                   1.997 |                     19.739 |    879.78 |    661.69 |
| Fig10    | tp_12h  |         12 | triangle        |                    2.5 |                   2.499 |                     15.929 |   1045.58 |    781.42 |
| Fig10    | tp_12h  |         12 | triangle        |                    3   |                   2.994 |                     13.443 |   1209.24 |    859.56 |
| Fig10    | tp_12h  |         12 | triangle        |                    4   |                   3.997 |                     10.328 |   1540.49 |    957.45 |
| Fig10    | tp_12h  |         12 | triangle        |                    5   |                   4.998 |                      8.5   |   1871.37 |   1014.9  |

---

## Fig11: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig11.png`
* **像素重合验证图**：[Fig11_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig11_digitization_overlay.png)
* **独立 CSV 文件**：[Fig11_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig11_literature_markers.csv)

| figure   | curve           |   eta_f_fb_pct | marker_symbol   |   DIR_nominal_pct |   DIR_detected_pct |   startup_inventory_IS0_kg |   pixel_x |   pixel_y |
|:---------|:----------------|---------------:|:----------------|------------------:|-------------------:|---------------------------:|----------:|----------:|
| Fig11    | eta_f_fb_0.5pct |            0.5 | diamond         |                10 |                9.9 |                     40.574 |    209.46 |    140    |
| Fig11    | eta_f_fb_0.5pct |            0.5 | diamond         |                30 |               30   |                     37.043 |    624.37 |    239.73 |
| Fig11    | eta_f_fb_0.5pct |            0.5 | diamond         |                50 |               50   |                     33.582 |   1039.25 |    337.5  |
| Fig11    | eta_f_fb_0.5pct |            0.5 | diamond         |                70 |               70   |                     30.154 |   1452.19 |    434.33 |
| Fig11    | eta_f_fb_0.5pct |            0.5 | diamond         |                90 |               90   |                     26.638 |   1866.29 |    533.62 |
| Fig11    | eta_f_fb_1.0pct |            1   | square          |                10 |                9.9 |                     20.759 |    209.51 |    699.68 |
| Fig11    | eta_f_fb_1.0pct |            1   | square          |                30 |               30   |                     19.029 |    624.28 |    748.52 |
| Fig11    | eta_f_fb_1.0pct |            1   | square          |                50 |               50   |                     17.297 |   1038.8  |    797.45 |
| Fig11    | eta_f_fb_1.0pct |            1   | square          |                70 |               69.9 |                     15.563 |   1451.45 |    846.44 |
| Fig11    | eta_f_fb_1.0pct |            1   | square          |                90 |               90   |                     13.84  |   1866.26 |    895.1  |
| Fig11    | eta_f_fb_2.0pct |            2   | circle          |                10 |                9.9 |                     10.803 |    209.6  |    980.88 |
| Fig11    | eta_f_fb_2.0pct |            2   | circle          |                30 |               30   |                      9.989 |    624.26 |   1003.88 |
| Fig11    | eta_f_fb_2.0pct |            2   | circle          |                50 |               50   |                      9.146 |   1038.69 |   1027.68 |
| Fig11    | eta_f_fb_2.0pct |            2   | circle          |                70 |               69.9 |                      8.294 |   1451.94 |   1051.73 |
| Fig11    | eta_f_fb_2.0pct |            2   | circle          |                90 |               90   |                      7.429 |   1866.47 |   1076.16 |
| Fig11    | eta_f_fb_3.0pct |            3   | cross           |                10 |               10   |                      7.536 |    210.35 |   1073.14 |
| Fig11    | eta_f_fb_3.0pct |            3   | cross           |                30 |               29.9 |                      7.022 |    623.45 |   1087.68 |
| Fig11    | eta_f_fb_3.0pct |            3   | cross           |                50 |               50   |                      6.425 |   1037.98 |   1104.52 |
| Fig11    | eta_f_fb_3.0pct |            3   | cross           |                70 |               69.9 |                      5.793 |   1451.83 |   1122.38 |
| Fig11    | eta_f_fb_3.0pct |            3   | cross           |                90 |               90   |                      5.242 |   1867.63 |   1137.94 |

---

## Fig12: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig12.png`
* **像素重合验证图**：[Fig12_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig12_digitization_overlay.png)
* **独立 CSV 文件**：[Fig12_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig12_literature_markers.csv)

| figure   | curve       |   eta_f_fb_pct | marker_symbol   |   reserve_time_tr_hours |   tr_detected_hours |   startup_inventory_IS0_kg |   pixel_x |   pixel_y |
|:---------|:------------|---------------:|:----------------|------------------------:|--------------------:|---------------------------:|----------:|----------:|
| Fig12    | prod_0.5pct |            0.5 | circle          |                       0 |               -0.04 |                     19.527 |    212.49 |    802.78 |
| Fig12    | prod_0.5pct |            0.5 | circle          |                       2 |                1.98 |                     21.379 |    283.39 |    755.13 |
| Fig12    | prod_0.5pct |            0.5 | circle          |                       6 |                5.96 |                     25.216 |    422.49 |    656.44 |
| Fig12    | prod_0.5pct |            0.5 | circle          |                      12 |               11.98 |                     30.863 |    632.65 |    511.2  |
| Fig12    | prod_0.5pct |            0.5 | circle          |                      24 |               24    |                     42.345 |   1053.16 |    215.89 |
| Fig12    | prod_0.5pct |            0.5 | circle          |                      32 |               31.79 |                     49.708 |   1325.28 |     26.51 |
| Fig12    | prod_1.0pct |            1   | square          |                       0 |               -0.04 |                     10.213 |    212.56 |   1042.32 |
| Fig12    | prod_1.0pct |            1   | square          |                       2 |                1.98 |                     11.174 |    283.08 |   1017.6  |
| Fig12    | prod_1.0pct |            1   | square          |                       6 |                5.96 |                     13.094 |    422.19 |    968.22 |
| Fig12    | prod_1.0pct |            1   | square          |                      12 |               11.96 |                     15.976 |    632.05 |    894.09 |
| Fig12    | prod_1.0pct |            1   | square          |                      24 |               24.01 |                     21.654 |   1053.18 |    748.05 |
| Fig12    | prod_1.0pct |            1   | square          |                      48 |               48.01 |                     33.001 |   1892.19 |    456.21 |
| Fig12    | prod_2.0pct |            2   | triangle        |                       0 |               -0.02 |                      5.561 |    213.39 |   1161.98 |
| Fig12    | prod_2.0pct |            2   | triangle        |                       2 |                1.99 |                      6.056 |    283.51 |   1149.24 |
| Fig12    | prod_2.0pct |            2   | triangle        |                       6 |                5.98 |                      7.034 |    422.91 |   1124.08 |
| Fig12    | prod_2.0pct |            2   | triangle        |                      12 |               11.99 |                      8.501 |    633    |   1086.35 |
| Fig12    | prod_2.0pct |            2   | triangle        |                      24 |               24.01 |                     11.297 |   1053.28 |   1014.44 |
| Fig12    | prod_2.0pct |            2   | triangle        |                      48 |               48.01 |                     17.023 |   1892.27 |    867.16 |
| Fig12    | prod_3.0pct |            3   | star            |                       0 |               -0.04 |                      4.1   |    212.65 |   1199.56 |
| Fig12    | prod_3.0pct |            3   | star            |                       2 |                1.98 |                      4.433 |    283.27 |   1191    |
| Fig12    | prod_3.0pct |            3   | star            |                       6 |                5.96 |                      5.013 |    422.21 |   1176.06 |
| Fig12    | prod_3.0pct |            3   | star            |                      12 |               11.96 |                      5.963 |    632.15 |   1151.63 |
| Fig12    | prod_3.0pct |            3   | star            |                      24 |               24    |                      7.888 |   1052.97 |   1102.11 |
| Fig12    | prod_3.0pct |            3   | star            |                      48 |               48    |                     11.639 |   1891.93 |   1005.65 |
| Fig12    | prod_5.0pct |            5   | diamond         |                       0 |               -0.05 |                      2.805 |    212.23 |   1232.85 |
| Fig12    | prod_5.0pct |            5   | diamond         |                       2 |                1.98 |                      2.993 |    283.22 |   1228.03 |
| Fig12    | prod_5.0pct |            5   | diamond         |                       6 |                5.96 |                      3.336 |    422.2  |   1219.2  |
| Fig12    | prod_5.0pct |            5   | diamond         |                      12 |               11.97 |                      3.935 |    632.53 |   1203.79 |
| Fig12    | prod_5.0pct |            5   | diamond         |                      24 |               24.01 |                      5.12  |   1053.3  |   1173.32 |
| Fig12    | prod_5.0pct |            5   | diamond         |                      48 |               48    |                      7.421 |   1892.06 |   1114.12 |

---

## Fig13: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig13.png`
* **像素重合验证图**：[Fig13_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig13_digitization_overlay.png)
* **独立 CSV 文件**：[Fig13_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig13_literature_markers.csv)

| figure   | curve       |   eta_f_fb_pct | marker_symbol   |   reserve_time_tr_hours |   tr_detected_hours |   reserve_inventory_Ir_kg |   pixel_x |   pixel_y |
|:---------|:------------|---------------:|:----------------|------------------------:|--------------------:|--------------------------:|----------:|----------:|
| Fig13    | prod_0.5pct |            0.5 | circle          |                       0 |                0.15 |                     0     |    219.36 |   1302.53 |
| Fig13    | prod_0.5pct |            0.5 | circle          |                       2 |                1.98 |                     2.071 |    283.3  |   1252.7  |
| Fig13    | prod_0.5pct |            0.5 | circle          |                       6 |                5.96 |                     5.76  |    422.31 |   1157.73 |
| Fig13    | prod_0.5pct |            0.5 | circle          |                      12 |               11.96 |                    11.545 |    632.52 |   1008.84 |
| Fig13    | prod_0.5pct |            0.5 | circle          |                      24 |               23.98 |                    22.992 |   1052.92 |    714.19 |
| Fig13    | prod_0.5pct |            0.5 | circle          |                      48 |               47.97 |                    45.891 |   1892.12 |    124.77 |
| Fig13    | prod_1.0pct |            1   | square          |                       0 |               -0.05 |                     0     |    212.2  |   1303.36 |
| Fig13    | prod_1.0pct |            1   | square          |                       2 |                1.96 |                     1.362 |    282.63 |   1270.95 |
| Fig13    | prod_1.0pct |            1   | square          |                       6 |                5.95 |                     2.937 |    422.18 |   1230.41 |
| Fig13    | prod_1.0pct |            1   | square          |                      12 |               11.95 |                     5.769 |    632.07 |   1157.52 |
| Fig13    | prod_1.0pct |            1   | square          |                      24 |               23.99 |                    11.56  |   1053.22 |   1008.44 |
| Fig13    | prod_1.0pct |            1   | square          |                      48 |               47.98 |                    23.001 |   1892.47 |    713.96 |
| Fig13    | prod_2.0pct |            2   | triangle        |                       0 |                0.22 |                     0     |    221.75 |   1313.31 |
| Fig13    | prod_2.0pct |            2   | triangle        |                       2 |                2.38 |                     0.757 |    297.22 |   1286.52 |
| Fig13    | prod_2.0pct |            2   | triangle        |                       6 |                5.99 |                     1.705 |    423.52 |   1262.12 |
| Fig13    | prod_2.0pct |            2   | triangle        |                      12 |               11.98 |                     2.908 |    633.03 |   1231.16 |
| Fig13    | prod_2.0pct |            2   | triangle        |                      24 |               23.99 |                     5.749 |   1053.23 |   1158.01 |
| Fig13    | prod_2.0pct |            2   | triangle        |                      48 |               47.99 |                    11.525 |   1892.75 |   1009.36 |
| Fig13    | prod_3.0pct |            3   | star            |                       0 |                0.29 |                     0     |    224    |   1315.46 |
| Fig13    | prod_3.0pct |            3   | star            |                       2 |                2.41 |                     0.683 |    298.13 |   1288.41 |
| Fig13    | prod_3.0pct |            3   | star            |                       6 |                6.04 |                     1.331 |    425.22 |   1271.75 |
| Fig13    | prod_3.0pct |            3   | star            |                      12 |               11.96 |                     2.183 |    632.39 |   1249.82 |
| Fig13    | prod_3.0pct |            3   | star            |                      24 |               23.99 |                     3.86  |   1053.25 |   1206.66 |
| Fig13    | prod_3.0pct |            3   | star            |                      48 |               47.98 |                     7.704 |   1892.25 |   1107.71 |
| Fig13    | prod_5.0pct |            5   | diamond         |                       0 |               -0.05 |                     0     |    212.42 |   1303.57 |
| Fig13    | prod_5.0pct |            5   | diamond         |                       2 |                1.97 |                     0.269 |    282.88 |   1299.07 |
| Fig13    | prod_5.0pct |            5   | diamond         |                       6 |                5.95 |                     0.655 |    421.99 |   1289.14 |
| Fig13    | prod_5.0pct |            5   | diamond         |                      12 |               11.96 |                     1.186 |    632.31 |   1275.46 |
| Fig13    | prod_5.0pct |            5   | diamond         |                      24 |               23.99 |                     2.326 |   1053.09 |   1246.13 |
| Fig13    | prod_5.0pct |            5   | diamond         |                      48 |               47.99 |                     4.616 |   1892.55 |   1187.18 |

---

## Fig14: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig14.png`
* **像素重合验证图**：[Fig14_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig14_digitization_overlay.png)
* **独立 CSV 文件**：[Fig14_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig14_literature_markers.csv)

| figure   | curve       |   eta_f_fb_pct | marker_symbol   |   reserve_time_tr_hours |   tr_detected_hours |   required_tbr |   pixel_x |   pixel_y |
|:---------|:------------|---------------:|:----------------|------------------------:|--------------------:|---------------:|----------:|----------:|
| Fig14    | prod_0.5pct |            0.5 | circle          |                       0 |               -0.01 |         1.1351 |    247.7  |    703.58 |
| Fig14    | prod_0.5pct |            0.5 | circle          |                       2 |                1.97 |         1.1412 |    315.02 |    678.19 |
| Fig14    | prod_0.5pct |            0.5 | circle          |                       6 |                5.98 |         1.1542 |    450.91 |    624.12 |
| Fig14    | prod_0.5pct |            0.5 | circle          |                      12 |               11.99 |         1.1732 |    654.85 |    544.76 |
| Fig14    | prod_0.5pct |            0.5 | circle          |                      24 |               23.99 |         1.213  |   1062.13 |    379.4  |
| Fig14    | prod_0.5pct |            0.5 | circle          |                      48 |               48    |         1.2911 |   1876.94 |     54.19 |
| Fig14    | prod_1.0pct |            1   | square          |                       0 |               -0.02 |         1.0692 |    247.41 |    977.9  |
| Fig14    | prod_1.0pct |            1   | square          |                       2 |                1.98 |         1.0722 |    315.04 |    965.2  |
| Fig14    | prod_1.0pct |            1   | square          |                       6 |                5.98 |         1.079  |    450.81 |    936.94 |
| Fig14    | prod_1.0pct |            1   | square          |                      12 |               11.99 |         1.0891 |    654.89 |    895.15 |
| Fig14    | prod_1.0pct |            1   | square          |                      24 |               23.99 |         1.1089 |   1062.12 |    812.64 |
| Fig14    | prod_1.0pct |            1   | square          |                      48 |               48    |         1.1472 |   1876.87 |    653.04 |
| Fig14    | prod_2.0pct |            2   | triangle        |                       0 |               -0.02 |         1.0369 |    247.31 |   1112.44 |
| Fig14    | prod_2.0pct |            2   | triangle        |                       2 |                1.98 |         1.0387 |    315.12 |   1104.96 |
| Fig14    | prod_2.0pct |            2   | triangle        |                       6 |                5.98 |         1.0411 |    450.81 |   1094.96 |
| Fig14    | prod_2.0pct |            2   | triangle        |                      12 |               11.99 |         1.0458 |    654.77 |   1075.16 |
| Fig14    | prod_2.0pct |            2   | triangle        |                      24 |               23.99 |         1.0559 |   1062.06 |   1033.27 |
| Fig14    | prod_2.0pct |            2   | triangle        |                      48 |               47.99 |         1.0757 |   1876.83 |    950.75 |
| Fig14    | prod_3.0pct |            3   | star            |                       0 |               -0.04 |         1.0263 |    246.53 |   1156.51 |
| Fig14    | prod_3.0pct |            3   | star            |                       2 |                1.98 |         1.0272 |    315.28 |   1152.87 |
| Fig14    | prod_3.0pct |            3   | star            |                       6 |                5.96 |         1.0288 |    450.15 |   1146.06 |
| Fig14    | prod_3.0pct |            3   | star            |                      12 |               11.96 |         1.0321 |    654.03 |   1132.39 |
| Fig14    | prod_3.0pct |            3   | star            |                      24 |               23.98 |         1.0387 |   1061.98 |   1105.03 |
| Fig14    | prod_3.0pct |            3   | star            |                      48 |               47.98 |         1.0518 |   1876.33 |   1050.46 |
| Fig14    | prod_5.0pct |            5   | diamond         |                       0 |               -0.04 |         1.0171 |    246.69 |   1194.74 |
| Fig14    | prod_5.0pct |            5   | diamond         |                       2 |                1.97 |         1.018  |    314.99 |   1191.2  |
| Fig14    | prod_5.0pct |            5   | diamond         |                       6 |                5.96 |         1.0191 |    450.39 |   1186.36 |
| Fig14    | prod_5.0pct |            5   | diamond         |                      12 |               11.98 |         1.021  |    654.54 |   1178.63 |
| Fig14    | prod_5.0pct |            5   | diamond         |                      24 |               23.99 |         1.0251 |   1062.14 |   1161.52 |
| Fig14    | prod_5.0pct |            5   | diamond         |                      48 |               48    |         1.0331 |   1876.99 |   1128.13 |

---

## Fig15: 文献离散计算真值表

* **源图文件**：`v&v/Abdou2021/Fig15.png`
* **像素重合验证图**：[Fig15_digitization_overlay.png](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Fig15_digitization_overlay.png)
* **独立 CSV 文件**：[Fig15_literature_markers.csv](file:///D:/Administrator/Documents/Github/tricys/v&v/Abdou2021/Discrete_Calculation_Markers/Fig15_literature_markers.csv)

| figure   | curve             |   eta_f_fb_pct |   reserve_time_tr_hours |   fusion_power_MW |   startup_inventory_IS0_kg |   pixel_x |   pixel_y |
|:---------|:------------------|---------------:|------------------------:|------------------:|---------------------------:|----------:|----------:|
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |               100 |                      1.413 |       270 |   1217.34 |
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |               500 |                      7.067 |       486 |   1062.69 |
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |              1000 |                     14.133 |       756 |    869.37 |
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |              1500 |                     21.2   |      1026 |    676.06 |
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |              2000 |                     28.267 |      1296 |    482.75 |
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |              2500 |                     35.333 |      1566 |    289.44 |
| Fig15    | prod_0.5pct_tr24h |            0.5 |                      24 |              3000 |                     42.4   |      1836 |     96.12 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |               100 |                      0.84  |       270 |   1233.02 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |               500 |                      4.2   |       486 |   1141.11 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |              1000 |                      8.4   |       756 |   1026.21 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |              1500 |                     12.6   |      1026 |    911.32 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |              2000 |                     16.8   |      1296 |    796.43 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |              2500 |                     21     |      1566 |    681.53 |
| Fig15    | prod_0.5pct_tr6h  |            0.5 |                       6 |              3000 |                     25.2   |      1836 |    566.64 |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |               100 |                      0.17  |       270 |   1251.35 |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |               500 |                      0.85  |       486 |   1232.75 |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |              1000 |                      1.7   |       756 |   1209.5  |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |              1500 |                      2.55  |      1026 |   1186.24 |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |              2000 |                      3.4   |      1296 |   1162.99 |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |              2500 |                      4.25  |      1566 |   1139.74 |
| Fig15    | prod_5.0pct_tr24h |            5   |                      24 |              3000 |                      5.1   |      1836 |   1116.49 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |               100 |                      0.11  |       270 |   1252.99 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |               500 |                      0.55  |       486 |   1240.95 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |              1000 |                      1.1   |       756 |   1225.91 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |              1500 |                      1.65  |      1026 |   1210.86 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |              2000 |                      2.2   |      1296 |   1195.82 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |              2500 |                      2.75  |      1566 |   1180.77 |
| Fig15    | prod_5.0pct_tr6h  |            5   |                       6 |              3000 |                      3.3   |      1836 |   1165.73 |

---

## 13. 产物文件清单与数据调用指引

### 13.1 数据存储目录结构
```text
v&v/
├── Abdou2021/
│   ├── Fig04.png ~ Fig15.png (原图)
│   ├── Fig04_digitization_overlay.png ~ Fig15_digitization_overlay.png (像素重合对标验证图)
│   └── Discrete_Calculation_Markers/ (离散计算点真值数据库)
│       ├── Fig04_literature_markers.csv
│       ├── Fig05_literature_markers.csv
│       ├── Fig06_literature_markers.csv
│       ├── Fig07_literature_markers.csv
│       ├── Fig08_literature_markers.csv
│       ├── Fig10_literature_markers.csv
│       ├── Fig11_literature_markers.csv
│       ├── Fig12_literature_markers.csv
│       ├── Fig13_literature_markers.csv
│       ├── Fig14_literature_markers.csv
│       ├── Fig15_literature_markers.csv
│       ├── Abdou2021_all_figures_literature_markers.csv (全量统一主表)
│       └── Abdou2021_all_figures_literature_markers.yaml (全量统一 YAML)
└── ABDOU2021_DISCRETE_CALCULATION_MARKERS_REFERENCE.md (本权威文献基准档案)
```

### 13.2 Python 调用示例
```python
import pandas as pd

# 读取单图真值
fig04_markers = pd.read_csv("v&v/Abdou2021/Discrete_Calculation_Markers/Fig04_literature_markers.csv")

# 读取全量真值数据库
master_markers = pd.read_csv("v&v/Abdou2021/Discrete_Calculation_Markers/Abdou2021_all_figures_literature_markers.csv")

# 筛选特定图表与工况
fig07_td3yr = master_markers[(master_markers["figure"] == "Fig07") & (master_markers["curve"] == "td_3yr")]
print(fig07_td3yr[["eta_f_fb_nominal_pct", "required_tbr"]])
```

---
> **维护与更新政策**：本档案中的提取真值已通过原图叠加反向验证，严禁任何后续提交擅自篡改数值。若原图更新，请使用 `v&v/scripts/` 下的对应提取脚本重新生成。
