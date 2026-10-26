#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Consolidation of All Abdou 2021 Literature Markers into Unified Master Dataset and Markdown Archive."""

from pathlib import Path
import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TRACK2_DIR = REPO_ROOT / "v&v" / "data" / "track2"
MARKERS_DIR = REPO_ROOT / "v&v" / "Abdou2021" / "Discrete_Calculation_Markers"
MARKERS_DIR.mkdir(parents=True, exist_ok=True)
MD_FILE = REPO_ROOT / "v&v" / "ABDOU2021_DISCRETE_CALCULATION_MARKERS_REFERENCE.md"

# 1. Standardize Fig04 into Discrete_Calculation_Markers/Fig04_literature_markers.csv
fig04_src = TRACK2_DIR / "Fig04_literature_digitized.csv"
fig04_target = MARKERS_DIR / "Fig04_literature_markers.csv"
if fig04_src.exists() and not fig04_target.exists():
    df04 = pd.read_csv(fig04_src)
    df04_std = pd.DataFrame({
        "figure": "Fig04",
        "curve": df04["curve"],
        "tp_hours": df04["tp_hours"],
        "marker_symbol": df04["curve"].apply(lambda c: "circle" if "1h" in c else ("square" if "4h" in c else "triangle")),
        "eta_f_fb_nominal_pct": df04["eta_f_fb_pct"],
        "eta_f_fb_detected_pct": df04["detected_x_pct"],
        "required_tbr": df04["required_tbr"],
        "pixel_x": df04["pixel_x"],
        "pixel_y": df04["pixel_y"],
    })
    df04_std.to_csv(fig04_target, index=False)
    print("Standardized Fig04 -> Discrete_Calculation_Markers/Fig04_literature_markers.csv")

# 2. Gather all 11 figures
fig_keys = ["Fig04", "Fig05", "Fig06", "Fig07", "Fig08", "Fig10", "Fig11", "Fig12", "Fig13", "Fig14", "Fig15"]
all_dfs = []
yaml_db = {
    "provenance": {
        "paper_title": "Physics and technology considerations for the deuterium-tritium fuel cycle and conditions for tritium fuel self sufficiency",
        "authors": "M. Abdou, M. Riva, A. Ying, C. Day, A. Loarte, L. R. Baylor, P. Humrickhouse, T. F. Fuerst, S. Cho",
        "journal": "Nuclear Fusion",
        "volume": 61,
        "number": 1,
        "article_id": "013001",
        "year": 2021,
        "doi": "10.1088/1741-4326/abbf35",
        "purpose": "Permanent ground truth archive of all discrete calculation markers extracted from Figures 4 through 15 for TRICYS V&V benchmarks.",
    },
    "figures": {},
}

for fk in fig_keys:
    csv_path = MARKERS_DIR / f"{fk}_literature_markers.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        all_dfs.append(df)
        yaml_db["figures"][fk] = {
            "total_points": len(df),
            "curves": sorted(list(df["curve"].unique())),
            "records": df.to_dict(orient="records"),
        }
        print(f"Loaded {fk}: {len(df)} points")

# Master CSV
master_df = pd.concat(all_dfs, ignore_index=True)
master_csv = MARKERS_DIR / "Abdou2021_all_figures_literature_markers.csv"
master_df.to_csv(master_csv, index=False)
print(f"\nMaster CSV saved: {master_csv} (Total records: {len(master_df)})")

# Master YAML
master_yaml = MARKERS_DIR / "Abdou2021_all_figures_literature_markers.yaml"
with open(master_yaml, "w", encoding="utf-8") as f:
    yaml.dump(yaml_db, f, sort_keys=False, indent=2)
print(f"Master YAML saved: {master_yaml}")

# 3. Generate Comprehensive Markdown Document
print("\nGenerating Markdown reference document...")

total_points_master = len(master_df)
repo_path_posix = REPO_ROOT.as_posix()
markers_path_posix = MARKERS_DIR.as_posix()

md_header = f"""# Abdou 2021 原始文献离散计算点真值数据库与永久基准档案
# (Abdou 2021 Discrete Calculation Markers Reference Database)

> **权威文献来源**：  
> **M. Abdou, M. Riva, A. Ying, C. Day, A. Loarte, L. R. Baylor, P. Humrickhouse, T. F. Fuerst, S. Cho**  
> *"Physics and technology considerations for the deuterium–tritium fuel cycle and conditions for tritium fuel self sufficiency"*  
> **Nuclear Fusion**, Vol. 61, No. 1, 013001 (2021). [DOI: 10.1088/1741-4326/abbf35](https://doi.org/10.1088/1741-4326/abbf35)  
>
> **本档案定位与用途**：  
> 本文档是 TRICYS 验证与对标套件（V&V）的**永久离散真值基准数据归档**。  
> 针对原文献中未公布完整数值表格的 Figures 4 ~ 15，采用**亚像素计算机视觉（Sub-pixel Computer Vision）与加权双向质心定位技术**，从原版高分辨率矢量光栅图像中严格提取了文献作者的所有**离散数值模拟计算点（Discrete Calculation Markers）**，并通过像素级图形重合叠加（Pixel Overlay）严格自检。  
> **总共提取 11 幅图表、共计 {total_points_master} 组离散计算真值点**。

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
| **Fig 04** | 所需 TBR vs 核心乘积 | eta_f*fb in [0.3%, 5.0%] | TBR_R in [1.00, 1.30] | tp = 1, 4, 12 h | 27 | [Fig04_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig04_digitization_overlay.png) |
| **Fig 05** | 所需 TBR vs 可用率 | AF in [6.5%, 100%] | TBR_R in [1.00, 1.30] | eta_f*fb = 0.5, 1, 2, 3% | 22 | [Fig05_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig05_digitization_overlay.png) |
| **Fig 06** | 所需 TBR vs DIR 旁路比 | f_DIR in [10%, 90%] | TBR_R in [1.00, 1.25] | eta_f*fb = 0.5, 1, 2, 3% | 20 | [Fig06_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig06_digitization_overlay.png) |
| **Fig 07** | 近期装置 TBR vs 倍增时间 | eta_f*fb in [0.5%, 5.0%] | TBR_R in [1.00, 1.30] | td = 1, 3, 5, 7 yr (AF=30%) | 29 | [Fig07_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig07_digitization_overlay.png) |
| **Fig 08** | 商业电站 TBR vs 倍增时间 | eta_f*fb in [0.5%, 5.0%] | TBR_R in [1.00, 1.25] | td = 1, 3, 5, 7 yr (AF=80%) | 32 | [Fig08_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig08_digitization_overlay.png) |
| **Fig 10** | 启动库存 vs 核心乘积 | eta_f*fb in [0.5%, 5.0%] | I_S^0 in [0, 40] kg | tp = 1, 4, 12 h | 24 | [Fig10_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig10_digitization_overlay.png) |
| **Fig 11** | 启动库存 vs DIR 旁路比 | f_DIR in [10%, 90%] | I_S^0 in [0, 45] kg | eta_f*fb = 0.5, 1, 2, 3% | 20 | [Fig11_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig11_digitization_overlay.png) |
| **Fig 12** | 启动库存 vs 储备时间 | tr in [0, 48] h | I_S^0 in [0, 50] kg | eta_f*fb = 0.5, 1, 2, 3, 5% | 30 | [Fig12_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig12_digitization_overlay.png) |
| **Fig 13** | 储备库存 vs 储备时间 | tr in [0, 48] h | Ir in [0, 50] kg | eta_f*fb = 0.5, 1, 2, 3, 5% | 30 | [Fig13_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig13_digitization_overlay.png) |
| **Fig 14** | 所需 TBR vs 储备时间 | tr in [0, 48] h | TBR_R in [1.00, 1.30] | eta_f*fb = 0.5, 1, 2, 3, 5% | 30 | [Fig14_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig14_digitization_overlay.png) |
| **Fig 15** | 启动库存 vs 聚变功率 | Pfus in [0, 3000] MW | I_S^0 in [0, 45] kg | eta_f*fb=0.5, 5.0% (tr=6, 24h) | 28 | [Fig15_overlay](file:///{repo_path_posix}/v&v/Abdou2021/Fig15_digitization_overlay.png) |
| **合计** | - | - | - | **41 条物理曲线** | **{total_points_master} 组真值点** | - |

---
"""

md_content = md_header

# Append per-figure sections
for fk in fig_keys:
    csv_file = MARKERS_DIR / f"{fk}_literature_markers.csv"
    if not csv_file.exists(): continue
    df_fig = pd.read_csv(csv_file)
    
    md_content += f"\n## {fk}: 文献离散计算真值表\n\n"
    md_content += f"* **源图文件**：`v&v/Abdou2021/{fk}.png`\n"
    md_content += f"* **像素重合验证图**：[{fk}_digitization_overlay.png](file:///{repo_path_posix}/v&v/Abdou2021/{fk}_digitization_overlay.png)\n"
    md_content += f"* **独立 CSV 文件**：[{fk}_literature_markers.csv](file:///{markers_path_posix}/{fk}_literature_markers.csv)\n\n"
    
    # Table of columns
    md_table = df_fig.to_markdown(index=False)
    md_content += md_table + "\n\n---\n"

md_content += """
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
"""

with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"\nSuccessfully written master Markdown reference: {MD_FILE}")
