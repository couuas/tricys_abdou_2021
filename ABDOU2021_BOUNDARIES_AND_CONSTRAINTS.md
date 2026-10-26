# Abdou 2021 聚变燃料循环边界条件与约束规范手册

> **参考文献**：
> M. Abdou, M. Riva, A. Ying, C. Day, A. Loarte, L. R. Baylor, P. Humrickhouse, T. F. Fuerst, S. Cho,
> *"Physics and technology considerations for the deuterium–tritium fuel cycle and conditions for tritium fuel self sufficiency"*,
> **Nuclear Fusion**, Vol. 61, No. 1, 013001 (2021). [DOI: 10.1088/1741-4326/abbf35](https://www.google.com/search?q=https://doi.org/10.1088/1741-4326/abbf35).

---

## 1. 引言与理论模型体系

在 Abdou 2021 文献中，聚变氚燃料循环自持（Tritium Self-Sufficiency）由**动态质量平衡**、**过程损耗补偿**、**放射性衰变补偿**以及**下一代装置倍增装料**四大物理支柱构成。

### 1.1 核心状态变量与流率定义

* **额定小时氚燃烧率** $\dot{N}^-_{\text{burn}}$：

$$\dot{N}^-_{\text{burn}} = \frac{P_{\text{fus}}}{3000\text{ MW}} \times 19.125\text{ g/h} \quad (\approx 0.459\text{ kg/day at } 3\text{ GW})$$


* **等离子体加料流率** $\dot{N}_{\text{fuel}}$：

$$\dot{N}_{\text{fuel}} = \frac{\dot{N}^-_{\text{burn}}}{\eta_f f_b}$$



其中 $f_b$ 为燃烧分额（Burn Fraction），$\eta_f$ 为加料效率（Fueling Efficiency），乘积 $\eta_f f_b$ 统称为**堆芯燃烧产物（Core Product）**。
* **增殖包层回流流率** $\dot{N}^+_{\text{breed}}$：

$$\dot{N}^+_{\text{breed}} = \text{TBR} \times \dot{N}^-_{\text{burn}} \times (1 - \epsilon_{\text{loss}})$$



### 1.2 最小启动库存与储备定义（Abdou Eq. 3.8 ~ 3.10）

系统最小启动装料 $I_S^0$ 必须满足两重物理约束：


$$I_S^0 = \Delta I_V + I_r$$

1. **动态回路充盈滞留亏空 $\Delta I_V$**：

$$\Delta I_V = I_S(0) - \min_{t} I_S(t) \approx \dot{N}_{\text{fuel}} \cdot t_p \cdot \phi_p$$



在下游回路（TEP、ISS、包层）滞留建立前，存储罐单向失血下潜的最大深度。
2. **应急储备库存 $I_r$**：

$$I_r = \dot{N}_{\text{fuel}} \cdot t_r \cdot q = \frac{\dot{N}^-_{\text{burn}}}{\eta_f f_b} \cdot t_r \cdot q$$



在主处理系统故障时，维持等离子体供料时间 $t_r$、以故障比例 $q$ 供料所需的安全储备。

### 1.3 自持临界产氚比解析模型（Abdou Eq. 3.1 ~ 3.7）

$$\mathrm{TBR}_R = 1 + \epsilon_{\text{loss}} + \frac{\lambda \bar{I}_{\text{total}}}{\dot{N}^-_{\text{burn}} \cdot AF} + \frac{I_S^0 + I_r}{\dot{N}^-_{\text{burn}} \cdot AF \cdot t_d}$$


* 燃烧项：$1.0$
* 工艺不可回收损耗项：$\epsilon_{\text{loss}} \approx 0.1\%$
* 放射性衰变惩罚项：$\frac{\lambda \bar{I}_{\text{total}}}{\dot{N}^-_{\text{burn}} \cdot AF}$，其中 $\lambda = 6.425 \times 10^{-6}\text{ h}^{-1}$（半衰期 12.32 年）
* 倍增装料项：$\frac{I_S^0 + I_r}{\dot{N}^-_{\text{burn}} \cdot AF \cdot t_d}$，在倍增时间 $t_d$ 内为后续新堆积攒初始装料与安全备料[cite: 8, 11]。

---

## 2. 产氚自持边界与约束分析（Fig 04 ~ Fig 08, Fig 14）

### 2.1 Fig 04: 堆芯燃烧产物与回路滞留对 Required TBR 的约束

```
Required TBR as a function of the product of TBF and fueling efficiency for various tritium processing time in the plasma exhaust of the IFC (1, 4, and 12 h) and availability factor of 50%. Fixed parameters used in the analysis: BZ residence time = 1 day; TES processing time = 1 day; availability factor = 50%; fusion power = 3 GW; reserve time = 24 h; fraction failing = 25%; doubling time = 5 years.
```

* **物理场景与工程目标**：评估不同燃料循环处理时间（$t_p = 1, 4, 12\text{ h}$）下，堆芯燃烧产物（$\eta_f f_b$）对系统全寿期实现氚自持所需临界产氚比 $\mathrm{TBR}_R$ 的约束。
* **边界参数设置**：
* **聚变功率 $P_{\text{fus}}$**：$3000\text{ MW}$（燃烧率 $\dot{N}^-_{\text{burn}} = 19.125\text{ g/h}$）
* **堆芯燃烧产物 $\eta_f f_b$**：$[0.1\%, 5.0\%]$
* **处理时间 $t_p$**：$1\text{ h}$（先进短滞留）、$4\text{ h}$（基准工况）、$12\text{ h}$（保守工况）
* **固定约束常数**：可用率 $AF = 50\%$，储备时间 $t_r = 24\text{ h}$，故障分额 $q = 25\%$，倍增时间 $t_d = 5\text{ yr}$


* **工程可行性边界划分**：
1. **包层物理上限（Hard Ceiling）**：$\mathrm{TBR} \le 1.15$（目前固态/液态增殖包层中子学可实现的上限）；
2. **高置信度自持区（High-Confidence Window）**：$\mathrm{TBR}_R \le 1.05$；
3. **燃烧产物可行红线（Core Product Threshold）**：
* 若 $\eta_f f_b < 1.0\%$，$\mathrm{TBR}_R > 1.30$，全系统自持在物理上不可能实现；
* 若 $t_p = 4\text{ h}$，为确保 $\mathrm{TBR}_R \le 1.15$，必须满足 $\eta_f f_b \ge 2.0\%$；若 $t_p = 12\text{ h}$，则需 $\eta_f f_b \ge 3.0\%$。



---

### 2.2 Fig 05: 反应堆可用率对 Required TBR 的双曲约束

```
Required TBR as a function of reactor availability factor for various TBF and fueling effciency product. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, reserve time = 24 h, fraction failing = 25%, doubling time = 5 years.
```

* **物理场景与工程目标**：量化反应堆年可用率（$AF$）对自持产氚比的非线性放大惩罚效应。
* **边界参数设置**：
* **可用率范围 $AF$**：$10\% \sim 100\%$
* **对比核心产物 $\eta_f f_b$**：
* $0.09\%$（ITER 基准：$f_b = 0.36\%, \eta_f = 25\%$，专用验证基准）
* $0.5\%, 1.0\%, 2.0\%, 3.0\%$（DEMO 及商业堆）


* **固定常数**：$P_{\text{fus}} = 3000\text{ MW}, t_p = 4\text{ h}, t_d = 5\text{ yr}, t_r = 24\text{ h}, q = 25\%$


* **关键物理约束**：
* 反应堆可用率越低，停堆停机时间越长，不仅停止产生新氚，而且全堆已有滞留氚（以 12.32 年半衰期）持续单向衰变灭失；
* 为了在有限的运行时间内填平停机衰变赤字并积攒启动装料，$\mathrm{TBR}_R$ 呈 $1/AF$ 暴涨[cite: 15]；
* 结论：商业聚变电站要迈入可行区（$\mathrm{TBR}_R \le 1.15$），不仅要求 $\eta_f f_b \ge 2\%$，还必须要求 **$AF \ge 50\% \sim 80\%$**[cite: 3, 14]。

---

### 2.3 Fig 06: 直接内循环（DIR）旁路分流解耦对 Required TBR 的约束

```
Required TBR as a function of DIR fraction for TBF and fueling efficiency products of 0.5%, 1.0%, 2.0%, and 3%. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, availability factor = 50%, reserve time = 24 h, fraction failing = 25%, doubling time = 5
years.
```

* **物理场景与工程目标**：评估通过直接内循环（DIR，绕过高滞留的同位素分离系统 ISS）分流不同比例的等离子体排气对降低 $\mathrm{TBR}_R$ 的敏捷效益。
* **边界参数设置**：
* **DIR 旁路分流比 $f_{\text{DIR}}$**：$10\% \sim 90\%$
* **堆芯燃烧产物 $\eta_f f_b$**：$0.5\%, 1.0\%, 2.0\%, 3.0\%$
* **固定常数**：$P_{\text{fus}} = 3000\text{ MW}, AF = 50\%, t_p = 4\text{ h}$（针对未旁路部分）, $t_d = 5\text{ yr}, t_r = 24\text{ h}$


* **物理约束结论**：
* 线性减阻特征：当 $\eta_f f_b = 1.0\%$ 时，若不采用 DIR（$f_{\text{DIR}} = 0$），$\mathrm{TBR}_R = 1.120$；当 $f_{\text{DIR}} = 80\%$ 时，$\mathrm{TBR}_R$ 显著降至 $1.075$。
* 饱和阈值：当 $\eta_f f_b \ge 3.0\%$ 时，因总流量变小，DIR 的边际减排效益减弱（$\mathrm{TBR}_R$ 仅从 $1.037$ 微降至 $1.026$）。


---

### 2.4 Fig 07: 近期试验装置（AF = 30%）倍增时间 $t_d$ 约束

```
Required TBR as a function of DIR fraction for TBF and fueling effciency products of 0.5%, 1.0%, 2.0%, and 3%. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, availability factor = 50%, reserve time = 24 h, fraction failing = 25%, doubling time = 5
years.
```

* **物理场景与工程目标**：分析在可用率较低（$AF = 30\%$，如 FNSF、CFETR 或早期 DEMO 阶段）时，为了支持快速发展的聚变市场（不同倍增时间 $t_d = 1, 3, 5, 7\text{ yr}$），系统对 $\mathrm{TBR}_R$ 的苛刻要求。
* **边界参数设置**：
* **可用率 $AF$**：$30\%$
* **倍增时间 $t_d$**：$1\text{ yr}$（极速扩张）、$3\text{ yr}$、$5\text{ yr}$、$7\text{ yr}$（平稳发展）
* **堆芯燃烧产物 $\eta_f f_b$**：$0.5\% \sim 5.0\%$


* **关键物理约束**：
* 若要求 $t_d = 1\text{ yr}$（即 1 年内积攒够一座新堆的启动料），在 $AF = 30\%$ 下，即使 $\eta_f f_b$ 达到 5.0%，$\mathrm{TBR}_R$ 仍然高达 $1.15$ 以上，**在物理上几乎不可实现**。
* 只有当 $t_d \ge 5 \sim 7\text{ yr}$ 且 $\eta_f f_b \ge 1.5\%$ 时，$\mathrm{TBR}_R$ 才能落入可能自持窗口（$1.05 \le \mathrm{TBR}_R \le 1.15$）。


---

### 2.5 Fig 08: 商业聚变电站（AF = 80%）倍增时间 $t_d$ 约束

```
Required TBR as a function of the product of TBF and fueling effciency for various doubling time (1, 3, 5, and 7 years) for availability factor of 80%. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1day, TES processing time = 1 day, fusion power = 3 GW, reserve time = 24 h, fraction failing = 25%, availability factor = 80%
```

* **物理场景与工程目标**：针对高可用率（$AF = 80\%$）的成熟商业聚变电站，评估不同倍增时间 $t_d$ 下的产氚自持边界。
* **边界参数设置**：
* **可用率 $AF$**：$80\%$
* **倍增时间 $t_d$**：$1, 3, 5, 7\text{ yr}$


* **关键物理约束**：
* 得益于 $AF$ 从 30% 跃升至 80%，单位时间内有效发电与产氚积分大幅增加。
* 在 $t_d = 5 \sim 7\text{ yr}$ 的成熟商用倍增节奏下，只要 $\eta_f f_b \ge 1.0\%$，$\mathrm{TBR}_R$ 便可轻松进入高置信度自持区（$\mathrm{TBR}_R \le 1.05$）。
* 即使严苛要求 $t_d = 3\text{ yr}$，只要 $\eta_f f_b \ge 2.0\%$，也可以在包层能力上限（$1.15$）内实现。

---

### 2.6 Fig 14: 储备缓冲时间 $t_r$ 对 Required TBR 的衰变叠加约束

```
Required TBR as a function of the reserve time for various TBF and fueling effciency products. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power
= 3 GW, fraction failing = 25%, doubling time = 5 years.
```
* **物理场景与工程目标**：评估为防范前端燃料循环系统故障而必须维持的储备时间 $t_r$（$0 \sim 48\text{ h}$），对系统全寿期 $\mathrm{TBR}_R$ 带来的惩罚影响。
* **边界参数设置**：
* **储备时间 $t_r$**：$0 \sim 48\text{ h}$
* **故障分额 $q$**：$25\%$
* **堆芯燃烧产物 $\eta_f f_b$**：$0.5\%, 1.0\%, 2.0\%, 3.0\%, 5.0\%$


* **关键物理约束**：
* $t_r$ 每增加 24 小时，不仅静态上要求储罐多备一天的供料，而且动态上由于这部分氚长期静置在储罐中，增加了系统的平均滞留库存 $\bar{I}_{\text{total}}$，进而推高了衰变消耗。
* 当 $\eta_f f_b = 1.0\%$ 时，若 $t_r = 0$，$\mathrm{TBR}_R \approx 1.07$；当 $t_r$ 增至 48 小时，$\mathrm{TBR}_R$ 飙升至 $1.15$（触及包层可行性红线）。
* 结论：高可靠性（RAMI）是降低 $t_r$ 需求、从而守住 TBR 自持底线的关键工程保障。


---

## 3. 初始装料与安全储备边界与约束分析（Fig 10 ~ Fig 13, Fig 15）

### 3.1 Fig 10: 启动库存 $I_S^0$ 随燃烧产物的非线性塌缩边界

```
Start-up inventory as a function of TBF and fueling effciency product for processing time in the plasma exhaust (IFC) of 1, 4, and 12 h. Parameters used in the analysis: BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, reserve
time = 24 h, fraction failing = 25%, doubling time = 5 years
```

* **物理场景与工程目标**：计算在 3000 MW 聚变功率下，不同管道处理时间 ($t_p = 1, 4, 12\text{ h}$) 与堆芯燃烧产物（$\eta_f f_b$）对反应堆启动所需初始氚装料 $I_S^0$ 的决定性约束[cite: 16, 17]。
* **边界参数设置**：
* **聚变功率 $P_{\text{fus}}$**：$3000\text{ MW}$[cite: 17]
* **加料燃烧产物 $\eta_f f_b$**：$0.5\% \sim 5.0\%$[cite: 17]
* **处理时间 $t_p$**：$1\text{ h}$（蓝线）、$4\text{ h}$（红虚线）、$12\text{ h}$（黑三角线）[cite: 17]
* **固定常数**：$t_r = 24\text{ h}, q = 25\%, t_d = 5\text{ yr}$[cite: 17]

* **关键边界与结论**：
* 存在强烈的**双曲线非线性塌缩特征**。
* 当 $\eta_f f_b = 0.5\%$ 时，若 $t_p = 12\text{ h}$，启动库存将高达惊人的 **$>50\text{ kg}$**；即使 $t_p = 1\text{ h}$，也需要近 **$30\text{ kg}$**[cite: 17]。
* 外部非聚变源（如 CANDU 裂变副产品）峰值总共才约 $27\text{ kg}$（且在 2027 年左右达峰后由于放射性衰变迅速枯竭）[cite: 16, 17]。因此，低燃烧产物（$\eta_f f_b < 1\%$）直接宣告启动商业 DEMO 成为不可能。
* 只有当 $\eta_f f_b \ge 3.0\% \sim 5.0\%$ 且 $t_p \le 1 \sim 4\text{ h}$ 时，$I_S^0$ 才能被压低至 **$5 \sim 8\text{ kg}$** 的可获取区间[cite: 17]。

---

### 3.2 Fig 11: DIR 旁路对启动装料 $I_S^0$ 的削减效益约束

```
Start-up inventory as a function of DIR fraction for TBF and fueling effciency products of 0.5%, 1.0%, 2.0%, and 3%.Parameters used in the analysis: processing time in the plasma
exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, reserve time = 24 h, fraction failing = 25%, doubling time = 5 years.
```

* **物理场景与工程目标**：评估引入 DIR 旁路分流技术（$10\% \sim 90\%$）对压低不同燃烧产物水平下启动库存 $I_S^0$ 的工程实效[cite: 18]。
* **边界参数设置**：
* **DIR 比例 $f_{\text{DIR}}$**：$10\% \sim 90\%$[cite: 18]
* **堆芯燃烧产物 $\eta_f f_b$**：$0.5\%, 1.0\%, 2.0\%, 3.0\%$[cite: 18]
* **固定常数**：$P_{\text{fus}} = 3000\text{ MW}, t_p = 4\text{ h}, t_r = 24\text{ h}, q = 25\%$[cite: 18]


* **关键物理约束**：
* 线性减排效应：当 $\eta_f f_b = 0.5\%$ 时，随着 DIR 比例从 10% 提升至 90%，启动装料从 **$41\text{ kg}$ 显著削减至 $26\text{ kg}$**[cite: 18]。
* 对于 $\eta_f f_b = 1.0\%$ 的工况，装料可从 $21\text{ kg}$ 降至 $14\text{ kg}$[cite: 18]。
* 结论：DIR 技术是缓解早期 DEMO 启动氚短缺的强力工程对策。

---

### 3.3 Fig 12: 故障缓冲储备时间 $t_r$ 对启动总装料 $I_S^0$ 的线性边界

```
Start-up inventory as a function of the reserve time for various TBF and fueling efciency products. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, fraction failing = 25%, doubling time = 5 years.
```

* **物理场景与工程目标**：量化备用维持时间 $t_r$（$0 \sim 48\text{ h}$）对系统总启动装料 $I_S^0$ 的线性拉动效应[cite: 19]。
* **边界参数设置**：
* **储备时间 $t_r$**：$0 \sim 48\text{ h}$[cite: 19]
* **故障分额 $q$**：$25\%$[cite: 19]
* **堆芯燃烧产物 $\eta_f f_b$**：$0.5\%, 1.0\%, 2.0\%, 3.0\%, 5.0\%$[cite: 19]


* **关键物理约束**：
* 呈现完美的**线性叠加规律**。
* 在 $\eta_f f_b = 1.0\%$ 时，若不考虑备用（$t_r = 0$），初始装料约 $10\text{ kg}$；若要求 24 小时备用（$t_r = 24\text{ h}$），初始装料直接翻倍至 **$22\text{ kg}$**[cite: 19]。
* 结论：过分追求长达数天的盲目高备用时间在物理装料上代价极其高昂，必须依靠提高主回路可靠性来缩短 $t_r$[cite: 18, 19]。

---

### 3.4 Fig 13: 纯应急储备库存 $I_r$ 随 reserve time 的解耦约束

```
Reserve inventory as a function of the reserve time for various TBF and fueling efciency products. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fusion power = 3 GW, fraction failing = 25%, doubling time = 5 years.
```

* **物理场景与工程目标**：专门针对储罐内由于防范故障而**纯粹划拨的应急备用库存 $I_r$** 随 $t_r$ 的演化规律进行边界解耦[cite: 19]。

* **关键物理约束**：
* 在低燃烧产物（$\eta_f f_b = 0.5\%$）且 $t_r = 48\text{ h}$ 时，单单应急备用库存一项就高达 **$45\text{ kg}$**[cite: 19]，完全超越了任何现实供货能力。
* 只有当 $\eta_f f_b \ge 2.0\%$ 且 $t_r \le 24\text{ h}$ 时，$I_r$ 才能被严格控制在 $5 \sim 6\text{ kg}$ 以下[cite: 19]。

---

### 3.5 Fig 15: 聚变功率 $P_{\text{fus}}$ 宽域标度约束（100 ~ 3000 MW）

```
Start-up inventory as a function of fusion power for TBF and fueling effciency product of 0.5% and 5%, and reserve time of 6 and 24 h. Parameters used in the analysis: processing time in the plasma exhaust (IFC) = 4 h, BZ residence time = 1 day, TES processing time = 1 day, fraction failing = 25%, doubling time = 5 years.
```

* **物理场景与工程目标**：评估聚变装置功率从小型实验堆（如 100 MW 的 FNSF）到大型商业电站（3000 MW）跨越时，初始启动库存 $I_S^0$ 的缩放边界[cite: 19, 20]。
* **边界参数设置**：
* **聚变功率 $P_{\text{fus}}$**：$0 \sim 3000\text{ MW}$[cite: 20]
* **对比参数方案**：
* 方案 A（基准低效）：$\eta_f f_b = 0.5\%$，备用时间 $t_r = 6\text{ h}$ 或 $24\text{ h}$[cite: 20]
* 方案 B（先进高效）：$\eta_f f_b = 5.0\%$，备用时间 $t_r = 6\text{ h}$ 或 $24\text{ h}$[cite: 20]


* **关键物理约束与标度结论**：
* 呈现严格的**正比例线性标度关系**[cite: 18, 20]。
* **小型化突破口**：对于 $P_{\text{fus}} = 100\text{ MW}$ 的近期装置（FNSF / CFETR），即使在较差的燃烧产物（$\eta_f f_b = 0.5\%$）下，其启动库存也仅需 **$0.7\text{ kg}$（$t_r = 24\text{ h}$）**或 **$0.26\text{ kg}$（$\eta_f f_b = 3\%$）**，这在当前人类剩余的 CANDU 产能尾料（约几公斤）支持下是**完全可获取的**[cite: 19, 20]。
* **大型堆警示**：若不加改造直接建造 3000 MW 的 DEMO 且燃烧产物停留在低水平，其启动装料将高达 **$40\text{ kg}$**，面临无米之炊的绝境[cite: 20]。
* 战略指导：近期聚变路线必须坚持“**小功率科学/工程试验堆（$P_{\text{fus}} \le 150\text{ MW}$）积累氚并孵化技术 $\to$ 大规模商业电站**”的渐进演化路线[cite: 19, 20]。

---

## 4. 全图表边界、参数与判据综合速查矩阵

| 图表编号 | 研究核心自变量 | 关键控制参数 | 核心物理边界与阈值约束 | 工程指导与设计启示 |
| --- | --- | --- | --- | --- |
| **Fig 04** | $\eta_f f_b$ ($0.1\% \sim 5\%$) | $t_p$ (1, 4, 12 h) | 若 $\eta_f f_b < 1\%$，$\mathrm{TBR}_R > 1.30$（无法自持）；需 $\eta_f f_b \ge 2\%$ 才能守住 1.15 上限 | 必须攻克先进加料与短滞留分离工艺 |
| **Fig 05** | 可用率 $AF$ ($10\% \sim 100\%$) | $\eta_f f_b$ ($0.09\% \sim 3\%$) | 呈 $1/AF$ 双曲发散；$AF < 30\%$ 时自持极其艰难 | 增强 RAMI 可靠性，确保电站可用率超 50%~80% |
| **Fig 06** | DIR 旁路比 ($10\% \sim 90\%$) | $\eta_f f_b$ ($0.5\% \sim 3\%$) | 线性减排；$\eta_f f_b = 1\%$ 时，80% DIR 可使 $\mathrm{TBR}_R$ 降至 1.075 | 强烈推荐在内循环中部署金属箔泵（MFP）旁路 |
| **Fig 07** | $\eta_f f_b$ ($0.5\% \sim 5\%$) | 倍增时间 $t_d$ ($1 \sim 7\text{ yr}$), $AF=30\%$ | 在低可用率下，极短倍增时间（$1\text{ yr}$）在物理上不可行 | 近期试验堆不宜设定过激进的产业扩张倍增目标 |
| **Fig 08** | $\eta_f f_b$ ($0.5\% \sim 5\%$) | 倍增时间 $t_d$ ($1 \sim 7\text{ yr}$), $AF=80\%$ | 商用高可用率下，$\eta_f f_b \ge 1\% \sim 2\%$ 即可轻松满足长期倍增 | 商业电站成熟期自持窗口宽广 |
| **Fig 10** | $\eta_f f_b$ ($0.5\% \sim 5\%$) | $t_p$ (1, 4, 12 h), $P_{\text{fus}}=3\text{ GW}$ | 低燃烧产物（$<1\%$）将导致启动库存飙升超 $30 \sim 50\text{ kg}$ | 外部无外部氚源支撑宏大初期的粗放设计 |
| **Fig 11** | DIR 旁路比 ($10\% \sim 90\%$) | $\eta_f f_b$ ($0.5\% \sim 3\%$) | 启动库存随 DIR 比例增加呈线性显著下降（最多可省 $10\text{ kg}$） | 优化燃料循环体系架构 |
| **Fig 12** | 备用时间 $t_r$ ($0 \sim 48\text{ h}$) | $\eta_f f_b$ ($0.5\% \sim 5\%$) | 启动总装料随 $t_r$ 延长呈严格正比例线性上升 | 减少盲目过长的应急备料仓容 |
| **Fig 13** | 备用时间 $t_r$ ($0 \sim 48\text{ h}$) | 故障份额 $q=25\%$ | 纯应急仓储 $I_r$ 在 $t_r = 48\text{ h}$ 时可高达数万克 | 必须提升系统平均无故障时间（MTBF） |
| **Fig 14** | 备用时间 $t_r$ ($0 \sim 48\text{ h}$) | $\eta_f f_b$ ($0.5\% \sim 5\%$) | $t_r$ 延长带来的静态与动态滞留惩罚会推高 $\mathrm{TBR}_R$ | 兼顾安全性与自持性的平衡点通常在 $t_r \le 24\text{ h}$ |
| **Fig 15** | 聚变功率 $P_{\text{fus}}$ | $\eta_f f_b$ (0.5% vs 5%), $t_r$ | **正比例线性标度**；100 MW 装置仅需 $<1\text{ kg}$ 启动料，3 GW 需上百公斤 | **确立了近距实验堆（FNSF $\le 150\text{ MW}$）作为孵化基地的路线方针** |

---