# Abdou 2021 原始文献参数基准库与对照档案

> **原始权威文献来源**：
> **M. Abdou, M. Riva, A. Ying, C. Day, A. Loarte, L. R. Baylor, P. Humrickhouse, T. F. Fuerst, S. Cho**
> *"Physics and technology considerations for the deuterium–tritium fuel cycle and conditions for tritium fuel self sufficiency"*
> **Nuclear Fusion**, Vol. 61, No. 1, 013001 (2021). [DOI: 10.1088/1741-4326/abbf35](https://doi.org/10.1088/1741-4326/abbf35)
>
> **本档案用途**：作为 TRICYS 验证套件（V&V）对齐原文献的**永久源头数据备份与基准对照规范**。任何人或后续版本不得擅自改动下述文献真实参数。

---

## 1. 原文献参数表汇总（Tables 1 ~ 5 & Table A.3）

### 1.1 Table 1: 基准工况主参数（Main parameters for the reference case）

| 参数名称 (Parameter) | 符号 | 原文献数值 (Value) | 单位 | 来源与物理说明 (Source/explanation) |
| :--- | :---: | :---: | :---: | :--- |
| 聚变热功率 | $P_{\text{fus}}$ | **3000** | MW | 3 GW 聚变电站基准 |
| 等离子体氚燃烧率 | $\dot{N}^-_{\text{burn}}$ | **0.459** | kg/day | 对应 $19.125\text{ g/h}$ ($3\text{ GW}$ 堆) |
| 等离子体氚燃烧份额 | $f_b$ | **0.36%**<br>**1.5%** | 1 | 0.36% 为 ITER 50-50 DT 最大加料工况；<br>1.5% 为首座 DEMO 预期值 |
| **加料效率** | $\eta_f$ | **25% (0.25)** | 1 | 详见原文献 Section 7.2 |
| 倍增时间 | $t_d$ | **5** | years | $5 \times 365.25 \times 24 = 43830\text{ h}$ |
| 储备时间 | $t_r$ | **24** | hours | 应急安全储备时间 |
| 燃料循环部分失效份额 | $q$ | **25% (0.25)** | 1 | 部分子系统失效率 |

### 1.2 Table 2: 内燃料循环（IFC）处理时间（IFC processing times）

| 组件/系统 | 原文献代表值 | 选定分析基准值 | 说明 |
| :--- | :---: | :---: | :--- |
| **燃料净化与同位素分离系统 (FCU + ISS)** | 1.3 h ~ 24 h | **4 h** | 原文献选定 $4\text{ h}$ 作为 IFC 等离子体排气总处理时间 $t_p$ |
| **水除氚系统 (WDS)** | 1 h ~ 20 h | **1 h** | 对应组件 10 ($\tau_{10} = 1.0\text{ h}$) |
| **加料系统 (Fueling system)** | 20 ~ 30 min | 并入 4 h | 模型未单独设立滞留，已打包计入 $t_p = 4\text{ h}$ |

### 1.3 Table 3: 外燃料循环（OFC）滞留与处理时间（OFC processing times）

| 组件/系统 | 符号 | 原文献基准值 | 单位 | 说明 |
| :--- | :---: | :---: | :---: | :--- |
| **增殖包层区 (Breeding Zone, BZ)** | $\tau_1$ | **1 (24.0)** | day (h) | 氚在包层增殖区的平均滞留停留时间 |
| **氚提取系统 (TES)** | $\tau_2$ | **1 (24.0)** | day (h) | 增殖包层载气/提取回路处理时间 |
| **第一壁 (First Wall, FW)** | $\tau_3$ | **1000** | s | 注入滞留释放特征时间 ($\approx 0.278\text{ h}$) |
| **偏滤器 (Divertor, DIV)** | $\tau_4$ | **1000** | s | 偏滤器靶板滞留特征时间 ($\approx 0.278\text{ h}$) |
| **主蒸汽发生器/热交换器 (HX/SG)** | $\tau_5$ | **1000** | s | 冷却剂回路热交换滞留时间 ($\approx 0.278\text{ h}$) |
| **冷却剂净化系统 (CPS)** | $\tau_6$ | **10 (240.0)** | days (h) | 冷却水/冷却氦净化回路处理时间 |

### 1.4 Table A.3: 回路分流比与组件效率（Flow rates fractions and efficiencies）

| 分流/效率参数 | 符号 | 原文献基准值 | 说明 |
| :--- | :---: | :---: | :--- |
| BZ 渗透至 HX 分额 | $f_{1-5}$ | $10^{-2}$ (0.01) | 包层向主冷却剂的渗透损失 |
| 等离子体注入 FW 分额 | $f_{p-3}$ | $10^{-4}$ (0.0001) | 边缘等离子体粒子向第一壁的注入 |
| 等离子体注入 DIV 分额 | $f_{p-4}$ | $10^{-4}$ (0.0001) | 边缘等离子体向偏滤器的直接打击注入 |
| HX 冷却剂流向 FW 分额 | $f_{5-3}$ | $0.6$ | 第一壁冷却回流分配 |
| HX 冷却剂流向 CPS 分额 | $f_{5-6}$ | $10^{-2}$ (0.01) | 主冷却流向冷却剂净化的支路分流比 |
| HX 冷却剂流向 WDS 分额 | $f_{5-10}$ | $10^{-4}$ (0.0001) | 主回路微量泄漏至水除氚 |
| CPS 未回收流向 FW 分额 | $f_{6-3}$ | $0.6$ | 净化后主冷却剂分配比 |
| **DIR 直接内循环分流比** | $f_{8-11} / f_{\text{DIR}}$ | **`0`** | **基准工况无 DIR！仅在 Fig06/Fig11 中扫查 0.1~0.9** |
| ISS 排气流向 WDS 分额 | $f_{9-10}$ | $10^{-1}$ (0.1) | 同位素分离尾气进入水除氚 |
| **TES 提取效率** | $\eta_2$ | **0.95 (95%)** | 增殖包层氚提取系统单程回收率 |
| **CPS 提取效率** | $\eta_6$ | **0.95 (95%)** | 冷却剂净化回路单程脱氚效率 |
| **非放射性损失系数** | $\epsilon_i$ | 真空与低温区 $=0$<br>其余回路 $=10^{-4}$ | $\epsilon_1=\epsilon_3=\epsilon_4=\epsilon_{11}=\epsilon_{12}=0$<br>$\epsilon_2=\epsilon_5=\epsilon_6=\epsilon_7=\epsilon_8=\epsilon_9=\epsilon_{10}=10^{-4}$ |
| **放射性衰变常数** | $\lambda$ | **$6.422 \times 10^{-6}\text{ h}^{-1}$** | 半衰期 $T_{1/2} = 12.32\text{ yr}$ |

### 1.5 Table 5: 产氚自持基准测试对照表（Table 5 Calculated Values of Required TBR）

* **工况固定参数**：
  $P_{\text{fus}} = 3\text{ GW}, f_b = 0.36\%, \eta_f = 25\% (\eta_f f_b = 0.09\%), t_p = 4\text{ h}, \tau_1 = 1\text{ d}, \tau_2 = 1\text{ d}, t_r = 24\text{ h}, q = 25\%, t_d = 5\text{ yr}, f_{\text{DIR}} = 0$。

| 可用率 $AF$ | 原文献公布 $\text{TBR}_R$ (Table 5) | 物理特征说明 |
| :---: | :---: | :--- |
| **10%** | **5.05** | 严重停堆导致衰变灭失激增，$\text{TBR}_R$ 呈 $1/AF$ 双曲发散 |
| **30%** | **2.67** | 近期试验装置（FNSF/CFETR 早期）基准工况 |
| **50%** | **2.16** | 早期 DEMO 堆设计基准 |
| **70%** | **1.94** | 进阶电站过渡阶段 |
| **90%** | **1.85** | 商业运行电站高可用率工况 |
| **100%** | **1.82** | 连续稳态运行极限 |

---

## 2. 原文献图表对应工况参数清单（Figures 4 ~ 15）

| 图号 | 主题 | 扫查自变量 | 固定参数集合 (文献题注与正文严格定义) | 是否启用 DIR |
| :--- | :--- | :--- | :--- | :---: |
| **Fig 04** | 所需 TBR vs 核心乘积 | $\eta_f f_b \in [0.1\%, 5.0\%]$ | $P_{\text{fus}}=3\text{GW}, AF=50\%, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%, t_d=5\text{yr}$<br>3条曲线: $t_p = 1\text{ h}, 4\text{ h}, 12\text{ h}$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 05** | 所需 TBR vs 可用率 | $AF \in [10\%, 100\%]$ | $P_{\text{fus}}=3\text{GW}, t_p=4\text{h}, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%, t_d=5\text{yr}$<br>曲线: $\eta_f f_b = 0.09\%$ (Table 5), $0.5\%, 1.0\%, 2.0\%, 3.0\%, 5.0\%$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 06** | 所需 TBR vs DIR 旁路 | $f_{\text{DIR}} \in [10\%, 90\%]$ | $P_{\text{fus}}=3\text{GW}, AF=50\%, t_p=4\text{h}, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%, t_d=5\text{yr}$<br>4条曲线: $\eta_f f_b = 0.5\%, 1.0\%, 2.0\%, 3.0\%$ | **是 ($f_{\text{DIR}}=0.1 \sim 0.9$)** |
| **Fig 07** | 近期装置 TBR vs 倍增时间 | $\eta_f f_b \in [0.5\%, 5.0\%]$ | $P_{\text{fus}}=3\text{GW}, \mathbf{AF=30\%}, \mathbf{t_p=4\text{h}}, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%$<br>4条曲线: $t_d = 1, 3, 5, 7\text{ yr}$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 08** | 商业电站 TBR vs 倍增时间 | $\eta_f f_b \in [0.5\%, 5.0\%]$ | $P_{\text{fus}}=3\text{GW}, \mathbf{AF=80\%}, \mathbf{t_p=4\text{h}}, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%$<br>4条曲线: $t_d = 1, 3, 5, 7\text{ yr}$ (**注意: 文献原题注确为 $t_p=4\text{h}$，非 1h**) | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 10** | 启动库存 vs 核心乘积 | $\eta_f f_b \in [0.5\%, 5.0\%]$ | $P_{\text{fus}}=3\text{GW}, AF=100\%, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%, t_d=5\text{yr}$<br>3条曲线: $t_p = 1\text{ h}, 4\text{ h}, 12\text{ h}$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 11** | 启动库存削减 vs DIR 旁路 | $f_{\text{DIR}} \in [10\%, 90\%]$ | $P_{\text{fus}}=3\text{GW}, AF=100\%, t_p=4\text{h}, \tau_1=1\text{d}, \tau_2=1\text{d}, t_r=24\text{h}, q=25\%, t_d=5\text{yr}$<br>4条曲线: $\eta_f f_b = 0.5\%, 1.0\%, 2.0\%, 3.0\%$ | **是 ($f_{\text{DIR}}=0.1 \sim 0.9$)** |
| **Fig 12** | 启动库存 vs 储备时间 | $t_r \in [0, 48\text{ h}]$ | $P_{\text{fus}}=3\text{GW}, AF=100\%, t_p=4\text{h}, \tau_1=1\text{d}, \tau_2=1\text{d}, q=25\%, t_d=5\text{yr}$<br>4条曲线: $\eta_f f_b = 0.5\%, 1.0\%, 2.0\%, 5.0\%$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 13** | 储备库存 vs 储备时间 | $t_r \in [0, 48\text{ h}]$ | 公式: $I_r = \frac{19.125}{\eta_f f_b} \cdot t_r \cdot 0.25$<br>4条曲线: $\eta_f f_b = 0.5\%, 1.0\%, 2.0\%, 5.0\%$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 14** | 所需 TBR vs 储备时间 | $t_r \in [0, 48\text{ h}]$ | $P_{\text{fus}}=3\text{GW}, AF=50\%, t_p=4\text{h}, \tau_1=1\text{d}, \tau_2=1\text{d}, q=25\%, t_d=5\text{yr}$<br>4条曲线: $\eta_f f_b = 0.5\%, 1.0\%, 2.0\%, 5.0\%$ | **否 ($f_{\text{DIR}}=0$)** |
| **Fig 15** | 启动库存标度 vs 聚变功率 | $P_{\text{fus}} \in [100, 3000\text{ MW}]$ | $AF=100\%, t_p=4\text{h}, \tau_1=1\text{d}, \tau_2=1\text{d}, q=25\%, t_d=5\text{yr}$<br>4条曲线: $\eta_f f_b=0.5\% (t_r=6, 24\text{h})$, $\eta_f f_b=5.0\% (t_r=6, 24\text{h})$ | **否 ($f_{\text{DIR}}=0$, 文献明文声明)** |

---

## 3. 历史修改与审计纠偏追溯记录 (2026/10/21 ~ 2026/10/22)

1. **底层物理模型 `v&v/models/Abdou2021.mo` 修正**：
   * `Baseline.eta_f`: 从历史笔误 `0.75` 严格修正为 Table 1 规定的 `0.25`。
   * `Baseline.f_8_11`: 从历史遗留 `0.8` 严格修正为 Table A.3 规定的 `0.0`（恢复基准工况无 DIR 状态）。
2. **Fig08 配置文件物理工况对齐**：
   * 将 `Fig08` 中排气处理时间从历史误配的 $t_p = 1\text{ h}$（`tau_9 = 0.50`）恢复为原文献题注规定的 $t_p = 4\text{ h}$（`tau_9 = 3.50`）。
3. **配置文件全局显式封闭声明**：
   * 在非 DIR 算例（Fig04, Fig05, Fig07, Fig08, Fig10, Fig12, Fig13, Fig14, Fig15）中显式逐一注入 `f_DIR: 0.0`，杜绝任何运行期依赖模型隐式默认值的不良耦合。
4. **复现基准集精简优化 (2026/10/22)**：
   * 移除原 Fig03（非优化单次 500h 动态瞬态演化），不再将其作为自持求解复现基准。
   * 全面聚焦 Figures 4 ~ 15 的双轨自持优化与参数敏感性（Required TBR 与 Startup Inventory）基准闭环。
