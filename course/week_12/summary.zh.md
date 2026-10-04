# Week 12 课后总结：语义缓存

2026-08-29 · *The Stones in the River*（SupportVectors，讲师 Asif Qamar，72 页）

---

## 一句话

> **缓存是一场「过去会重演」的赌注。而这门课教的不是怎么建它，是怎么判断该不该建、以及建到什么程度。**

讲义标题「**从奇迹到专科仪器**」就是全课的立场：**语义缓存不是默认开关，是一把有明确适应症的手术刀。**

---

## 一、五幕的骨架

| 幕 | 主题 | 回答什么 | 结论 |
| --- | --- | --- | --- |
| **序幕** | The Bet | 这是什么 | 传统缓存赌**字节**重复（可验证）；语义缓存赌**意义**重复（**只能判断，永远可能错**） |
| **ACT I** | The Geometry | 凭什么可能 | 高维集中让随机撞入概率 $\approx 2\times10^{-7}$ → **命中都是有因的**。但现成编码器各向异性，**几何的礼物打了折** |
| **ACT II** | The Decision | 怎么诚实 | 不存在正确的 τ。用 $d'$ 判断该不该建，用 **δ 合同**代替阈值，用 $p^*$ 定价每一次服务 |
| **ACT III** | The Machine | 怎么造 | 专用小编码器；**证据夹道**代替 TTL；版本钉死；agent 缓存**计划**不缓存答案 |
| **Interlude** | The Adversary | 什么时候危险 | **能让缓存工作的每个性质，都是攻击面。不存在既开放又安全的配置** |
| **ACT IV** | The Economics | 值不值得 | $H^*$ 每季度上涨；**「别建」是分析的成功** |
| **ACT V** | The Wild | 现实如何 | **最懂缓存的公司选择不做**；十个模式，四个反模式 |

---

## 二、⭐ 三个我课前理解错的地方

这是今天最值钱的部分——**不是学到了新东西，是改掉了错的东西**。

### 1. τ 不是"风险偏好"，是"校准结果"

| | 我原来以为 | 实际 |
| --- | --- | --- |
| **τ** | 我怕不怕犯错，由业务定 | **两个分布的中点**（"τ sits in the valley"），由**数据校准**出来 |
| **γ** | 一个调节旋钮 | **模型能力的度量**，$= \Delta\mu/\sigma^2$，等价于信号检测论的 $d'$ |
| **风险偏好** | 藏在 τ 里 | **另一个门槛 $p^*$**，从成本算出来 |

**把校准和风险偏好混在一个参数里，是绝大多数团队"调不好阈值"的根因。**

### 2. $p^*$ 少了一项

$$\text{我推的：} p^* = \frac{C}{G+C} \qquad\qquad \text{讲义：} p^* = \frac{L+\kappa}{g+L}$$

$\kappa$ = **查缓存本身的成本**（embedding + 向量检索）。$\kappa \to g$ 时 $p^* \to 1$ ——
**查缓存跟重算差不多贵，就不该有这个缓存。**这也解释了 Front Door 为什么要在语义层前面放一个免费的哈希层。

### 3. 失效不该以 TTL 为主

> ***"TTLs guess; the world doesn't consult them."***

**时间和正确性之间没有可靠关系。**正确做法是 **evidence gauntlet**：命中时刻串行核对**相似度 → 证据重叠 → chunk 版本 → 词面支持**，TTL 只做兜底。

---

## 三、五件仪器 ↔ 五种失败（讲义 p.66）

| 仪器 | 抓住的失败 |
| --- | --- |
| **cap bound** 极冠界 | **偶然命中**（根本不存在——命中都是有因的） |
| **error contract δ** | **自信的错答案** |
| **evidence gauntlet** | **陈旧服务** |
| **scoped key** | **租户泄露** |
| **break-even $H^*$** | **烧钱坑** |

> ***几何让这个赌注成为可能；策略让它诚实；范围让它安全；算术决定到底要不要下注。***

**一件仪器缺席 = 一整类失败没人管。**

---

## 四、四道闸门（决策流程）

```text
① d' 够高吗？（编码器分得开对错吗）
   d' < 1  →  别建，换模型/领域微调
   │
② H* 够得着吗？（账算得过来吗）
   H* > 可达命中率  →  别建
   │
③ L/(g+L) 多高？（错了多惨）
   → 决定爬到四级阶梯的第几级
   │
④ 赌注是不是太大？
   actions / schemas / states  →  停止赌博，回到证明
```

**第 ④ 条是全课最漂亮的闭环**：1996 年谓词包含是**可证明的定理**，2023 年被换成了**赌注**。而结构化的东西（SQL、agent 调用、状态）**本来就不必陪着一起赌**——只有自然语言被迫如此。

> **与其在一个不可证的表示上提高赌博水平，不如换一个可证的表示。**

---

## 五、周一早上，按顺序（讲义 p.70）

1. **打开 prefix caching** —— 免费、无风险、**约 60% 的收益**
2. **跑可行性闸门** —— 抽样查询里 **1/10 能在 0.85 匹配上**，**否则不要建**
3. **手术刀只切密集、已划范围的切片**
4. **签下误差合同 δ**
5. **每周给样本打分**

> ***prefix caching 是默认项。语义缓存是一把手术刀 —— 决定它往哪儿切的是那张表格，不是热情。***

**第 ② 步是全篇最实用的一句**：不需要建任何东西，一个下午能跑完，同时检验了「够不够头部集中」和「重复是不是近似的」两个必要条件。

```python
sims = [max_cosine_against_others(q) for q in sample(query_log, 1000)]
print(f"{mean(s >= 0.85 for s in sims):.1%} —— 低于 10% 就别建")
```

---

## 六、四个反模式（讲义 p.64）

> ***每一个反模式，都是一次「有操作、无策略」。***

| 反模式 | 操作 | 缺的策略 |
| --- | --- | --- |
| Global Threshold | serve | **决策策略** |
| Unscoped Shared Cache | share | **访问策略** |
| Hit-Rate Worship | measurement | **真相策略** |
| Checkbox Cache | deployment | **归属策略** |

> ***命中率是那个危险的指标：当答案变得更糟时，它会上升。盯住误差，否则命中率会盯上你。***

---

## 七、对 Avaloka 的映射

| 讲义的东西 | Avaloka 该怎么用 |
| --- | --- |
| **cache ≠ memory** | 缓存按**问题**分区、跨用户共享；记忆按**用户**分区、绝不共享。**搞混 = 泄露 或 永不失效** |
| **Plan Cache** | agent 层**缓存计划骨架**，不缓存答案——状态过期太快，但结构会重复 |
| **Scoped key** | 租户/权限维度必须在 key 里，不能靠 `if` 检查 |
| **Version pin** | 条目 schema 加 `embedder_version` + `index_version` |
| **Near-miss mine** | 阈值下方那条带 = **最便宜的 hard negatives** |
| **可行性闸门** | 先跑，再决定要不要做这个方向 |

---

## 八、留存的十句话

1. **bet 不是修辞，是技术史事实：这个领域在 2023 年主动放弃了证明。**
2. **每一次命中都是一个有因之事。熊，永远是某人的手笔。**
3. **集中性证明外人进不来，对里面的人只字未提。定理交棒给政策。**
4. **微调不是让相似度变高，是让相似度变得有区分力。**
5. **σ 是编码器发给你的牌，γ 是你能打出的上限。**
6. **A threshold is a hope. A contract is a measurable promise.** / **δ is portable and τ never was.**
7. **Every property that makes the cache work is the attack surface.** / **结构胜过警惕，因为警惕会宕机。**
8. **「Do not build」是分析的成功，不是胆怯的失败。**
9. **一个精确率，被重新打字成了一个召回率** —— 听到漂亮百分比，先问分母。
10. **最便宜的检索是那次从未运行的检索；最昂贵的答案是那个被自信送出的陈旧答案。手艺，就是知道此刻说话的是哪一句。**

---

## 九、课后待办（按优先级）

- [ ] ⭐ **跑可行性闸门**（1000 条真实 query，看 0.85 处的匹配比例）—— 一个下午
- [ ] 检查现有 prompt 是否已开 prefix caching（免费的先拿）
- [ ] 用真实 query log 跑一次 Platt scaling，量出自己场景的 $d'$、$\gamma$、$\tau$
- [ ] 算 $r = C_{\text{full}}/C_{\text{hit}}$ 和 $H^*$，做成**每季度重算**的看板
- [ ] 报表改成四个数并排（$P(\text{命中})$ / $P(\text{对}\mid\text{命中})$ / $P(\text{错且命中})$ / $H^*$）
- [ ] 加**入度分布**监控（同时防几何 hub 和人造 hub）
- [ ] 缓存 schema 加版本钉死
- [ ] 用「操作 / 策略」框架审一遍现有系统
- [ ] 按依赖顺序读 p.71 那五篇
- [ ] 补 Week 10 记录缺口（线索又 +1：讲义两次回指 **MemoryCraft 的分区插曲**）

---

## 十、本周笔记索引

| 文件 | 覆盖 |
| --- | --- |
| [`prologue.zh.md`](prologue.zh.md) | 讲义 p.4–7 |
| [`act1-geometry.zh.md`](act1-geometry.zh.md) | p.12–22 |
| ⭐ [`sigmoid-decision.zh.md`](sigmoid-decision.zh.md) | 白板：σ/γ/τ/p/p\* 完整推演 |
| [`act2-decision.zh.md`](act2-decision.zh.md) | p.21–31 |
| [`act3-machine.zh.md`](act3-machine.zh.md) | p.32–40 |
| [`interlude-adversary.zh.md`](interlude-adversary.zh.md) | p.41–46 |
| [`act4-economics.zh.md`](act4-economics.zh.md) | p.47–56 |
| [`act5-wild-and-close.zh.md`](act5-wild-and-close.zh.md) | p.57–72 |
| [`kv-cache-and-prefix-caching.zh.md`](kv-cache-and-prefix-caching.zh.md) | 最底三层缓存 |
| [`rag-request-flow.zh.md`](rag-request-flow.zh.md) | RAG 请求全流程（地基参考） |
| [`week-12.zh.md`](week-12.zh.md) | 现场笔记 + 总索引 |

原始材料：[`uploads/`](uploads/)（讲义 PDF 72 页 + 专著 91 页在 [`../week_11/uploads/`](../week_11/uploads/) + 55 张原页与白板截图）
