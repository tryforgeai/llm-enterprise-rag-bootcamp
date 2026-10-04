# Week 07 总结 —— 万物的尺度：从检索到推理，怎么测一个 RAG 系统

**日期：** 2026-07-25 · **来源：** `course/week_07/summer-week-7-lesson-plan.pdf`（*The Measure of All Things — Evaluating RAG Systems from Retrieval to Reasoning*，Asif Qamar, SupportVectors）、现场幻灯片记录、Week 07 可运行 demo（`course/week_07/ndcg_demo.py`、`pr_curve_demo.py`、`rerank_eval_demo.py`）

---

## 一句话结论

整周可以压成一句话：

> **你无法改进你无法测量的东西 —— 而尺子得你自己造，不是借别人的。**

前六周一直在**建**：Week 1–2 建"意义即几何"和检索地基，Week 3 切 chunk，Week 4 造派生工件，Week 5 把图书馆变成城市，Week 6 挂上两道门。但有一个问题从来没被严肃问过：**这些东西到底管不管用？**

讲师的现场副标题把这件事说得最干净：

> *"Six weeks of building the library, the map, and the gates. Today we stop building — and start measuring."*
> （六周里建了图书馆、地图和闸门。今天我们停止建造 —— 开始测量。）

关键的立场转变是：**评估不是流水线的最后一步，而是前六周一直在下面托着、却从没被审视过的地基。**

> *"A bridge engineer does not hand off load-testing — the load curves **are** the design. Evaluation is not downstream of AI engineering. **Evaluation is AI engineering.**"*

全天挂在一个公式上：

```
argmax_θ  E_{q∼𝒬} [ μ(q, θ) ]
```

- **θ** = 每一个旋钮 —— chunk 大小、embedder、检索混合、reranker、prompt、温度。不只是模型超参，是**整条流水线的架构决策**。
- **μ(q, θ)** = 在 query q 上的"好坏"指标。
- **𝒬** = **你自己的**查询分布，不是别人的公共基准。

这个公式把全天四幕锚定到一处：Act I 造 **𝒬**（金数据集），Act II–III 定义 **μ**（六个检索指标 + 生成侧指标），Act IV 警告 **μ 一旦上墙就会被套利**（Goodhart）。

当天的结构：

```
Prologue  为什么要测量          （评估是谁的活、80/20、优化目标公式）
Act I     标尺 The Yardstick     （金数据集 —— 任何指标之前先有 ground truth）
Act II    阶梯 The Staircase     （六个检索指标，每级补下一级的盲点）
Interlude 信号与噪声             （统计显著性、公共基准的正当位置、多样性与 MMR）
Act III   生成器 The Generator   （从评食材转向评厨师）
Act IV    前沿 The Frontier      （校准、多跳、agentic、Goodhart、成本）
Coda      评估地图               （把每个指标接回前六周的每个组件）
```

两句题词框住全天的张力，**两句都要握住**：

> *"When you can measure what you are speaking about and express it in numbers, you know something about it."* —— Kelvin, 1883
> *"Not everything that counts can be counted, and not everything that can be counted counts."* —— Cameron, 1963

> 现场原话：**"Today is Kelvin's day — but Cameron stands behind him all day, warning us about Goodhart."**

---

## Prologue：评估是谁的活

三张幻灯片打破同一个错误认知。

**"Evaluation? That's QA's job."** —— 一个观察了二十年的模式：资深工程师团队听完一模一样的讲座，建了几个月 RAG，然后带着真诚的惊讶坦白：**从没建过金数据集。**

讲师给了一个很好的记忆隐喻：

> *"The formulas do not leak out of heads because people are lazy. They leak because they were filed in the mental cabinet marked **someone else's concern** — and that cabinet leaks."*

知识留不住往往不是记性问题，是**心理归类**问题。一旦把评估贴上"别人负责"的标签，相关知识就存不进长期记忆。

**为什么传统软件测试的心智模型在这里失效：**

| | 确定性软件 | AI 系统 |
|---|---|---|
| 行为 | same input, same output | 返回一个**答案质量的分布**，对着一个**查询的分布** |
| 判定 | QA 写断言，CI 跑红/绿 | **没有干净的 pass/fail 线** |
| 漂移 | 无 | 模型版本、prompt、随机解码、语料增长 —— 四个漂移源 |

**真实 AI 项目的 80/20：** 80% 的精力花在干净数据、演示、和尺子（评估集）上；20% 花在时髦的部分（架构、算法、模型）。Cornerstone 的案例（1 亿学习对象、7000 客户）——架构第一次会就定了，真正吃掉几个月的是 **40 位 SME × 每人 2 天，建一个 1 万条 query 的金数据集**。

一个反直觉但很值的信号：

> 混合检索上线时，一个大客户很**愤怒**：抱怨了几年、为什么现在突然就好用了？**没有比一个终于看到改进的愤怒客户更能证明你的评估方法论是真实有效的了。**

---

## Act I：标尺 —— 任何指标之前，先有 ground truth

视觉是元素周期表的 **"Au"（金）**，双关 gold dataset。

> *"Before any metric, a gold dataset. Before any number, a ground truth **someone signed their name to**."*

"有人签了名的"是现场的加强版 —— 把 ground truth 从抽象概念钉成**有人为其质量背书、担责**的东西。

### 金数据集的定义

一组精挑的 query 集合 **𝒬 = {q₁, …, qₙ}**，每个 query 标注它的相关文档，且每个 (query, 文档) 对给一个**分级相关性分数 r ∈ {0,1,2,3,4}**（0 = 无关 … 4 = 完美）。

注意这个 𝒬 就是优化目标公式里 `E_{q∼𝒬}` 的那个 𝒬 —— **金数据集 = 你的查询分布的具体实例化**。

> *"The notches on the ruler are the metrics; the ruler itself is the gold dataset."*
> （尺子上的刻度是指标；尺子本身就是金数据集。）

### 第一条路：谷歌式全量标注 —— 水密，但付不起

向引擎抛 1000 条 query，人工评估员给**每一个返回结果**逐条打勾；为了算 recall，还要另外列出"本应返回却没返回的"来对比。

两把刀否掉它：

1. **成本** —— "七人小团队没人有时间做。工程师会说：我的活是写代码，不是读一百万篇文档。**他们是对的。**"
2. **病理（更微妙，也更重要）** —— 你把 10 篇完美文章种为 ground truth，引擎却 surface 出一篇你从没编目、甚至**更好**的文章。因为它不在标准答案里，被判为"无关"，于是 **precision 下降 —— 引擎因为做好本职工作反被惩罚。**

### 第二条路：Cherry-picked 金数据集（可行方案，五步）

1. **请 SME，不是工程师** —— 医疗找临床医生、学习找教授、金融找合规官。（"engineers will revolt"）
2. **SME 亲自出题** —— 从真实意图采集：搜索日志、支持工单、真实调研，不是凭空编。
3. **跑个简单引擎**（OpenSearch 之类手边现成的），每个 query 取 **top 100–200** 候选。
4. **从那 200 篇里精挑最佳 25–30 篇**，并给它们打 **0–4 分**。
5. **发版时冻结、版本化、持续演进** —— 加新 query、调整分数、淘汰过时的。

> *"No human can scan a corpus. Anyone can scan two hundred candidates."*

核心诡计在第 3–4 步：**用一个简单引擎先把百万文档砍到 200 候选，把"不可能的全量标注"变成"可行的两百篇精挑"。** 代价是 recall 的分母不再是"全语料的真相"，而是"这 200 候选里的真相" —— 这就是 IR 领域标准的 **pooling**（TREC 就这么做）。牺牲理论完备性，换现实可操作性。**报数字时要明确写"这是 pool 近似的 recall"，避免过度解读。**

### 规模：最少 200，目标 1000

"SME Summit"是种子 —— 聚 5–10 位专家，管早午餐，给 8 小时，产出约 100 条辩论过的分级判断，之后六个月慢慢长大。

这个数字后来在 Interlude 被统计学追认（见下文功效分析）。

### 尺子腐烂的两种方式

- **Eval decay（评估衰减）** —— 语料在演进；一月份最相关的文档，六月可能被更新的取代。**过时的相关性判断会悄悄毒化每一个指标。** 对策：定期刷新。
- **Overfitting（过拟合你自己的尺子）** —— 如果工程师知道了评估集里的 query（哪怕无意中），他们就会专门为**那些** query 优化。对策：**留一个只有评估负责人能碰的 held-out 测试集。**

> *"A yardstick everyone has memorised is no longer a yardstick — **it is a target**."*（Goodhart 会在 Act IV 回归。）

### 反对借用公共基准

> "MS MARCO 就在那儿，拿它评估不就行了？" —— 这等于**拿退烧药在不发烧的病人身上做测试**。基准上光彩夺目，到你真实用户那里灾难一片。

核心论点是**分布不匹配**：公共基准有它自己的 𝒬′。在 𝒬′ 上做 argmax 得到的 θ，搬到你的 𝒬 上可能恰好是错的。

但**没有全盘否定** —— 公共基准有一个正当用途：**sanity check**（基线体检，确认没莫名坏掉）。它是"体温计校准"，不是"疗效证明"。

那个"逻辑学家看羊"的隐喻很精髓：火车上的逻辑学家看到一只白羊，只肯说"存在至少一只羊，它身体的至少一侧，在观测的那一刻，看起来是白的"。**公共基准只允许你下这种极度受限、不可外推的结论。**

### Quiz 1：precision 和 recall 的不对称

> Precision 可以靠给引擎**返回的**结果逐条打勾算出来；Recall 不能。Recall 额外需要什么知识？为什么它贵得多？

**答案：** 贵在**分母**。

- **Precision** 的分母是"引擎实际返回的东西" —— 一个**封闭、有限**的集合，摆在你眼前，逐条打勾即可。
- **Recall** 的分母是"**全语料里所有本应相关的文档**"，包括引擎**没**返回的那些。这是一个**开放**问题。

$$\text{Recall@}k = \frac{|\text{relevant in top }k|}{|\textbf{all relevant in corpus}|}$$

> *"Precision judges the bucket. Recall judges the bucket **against the beach** — and only the ground truth knows what the beach holds."*

这也解释了为什么工业界常报 precision/nDCG 却回避绝对 recall —— recall 的真值几乎无法在开放语料上获得，只能在冻结的金数据集范围内近似。

---

## Act II：阶梯 —— 六个检索指标

视觉是 **"nG"**（nDCG）。

> *"Six metrics, each fixing a blindness of the one below — from a bucket on a beach to the summit called NDCG."*

### 贯穿全幕的两个比喻

**海滩捡贝壳（precision / recall）：** 一袋贝壳撒在沙滩上，有些**埋起来了**；每个孩子一只桶，任务是"捡十个贝壳"。Sarah 捡回 4 贝壳 + 6 石子；Meera 捡回 7 贝壳 + 3 石子。大家都说 Meera 更好 —— 但**好多少，用数字说？**

> 一个 query 把语料切成贝壳（相关）和石子（不相关）。搜索引擎就是那个提着桶、被要求交出 top-k 的孩子。

**阿里巴巴山洞（排序感知）：** 一条通向黑暗的过道，货架按顺序排列 = 排名；宝物混着垃圾；**强盗随时回来，时间极其宝贵**。

### Metric 1–2：Precision@k 与 Recall@k

**Precision 的两个盲点：**

1. **受 k 影响** —— 把"捡十个"改成"捡二十个"，两个孩子的排名可能**反转**。单看 precision@k 不稳。
2. **对漏检视而不见** —— 一个只捡了 3 个、但个个都是贝壳的桶，哪怕沙滩里还埋着 7 个，precision 照样满分 1.0。

**Recall** 的记忆法：**R**ecall 强调 **R**elevance —— 而且是**全部**的相关。埋 5 个蓝贝壳，找到 3 个 = 3/5 = 0.60。

讲师用了三个比喻反复砸 recall（海滩捡贝壳 / 金毛 Rookie 叼球 / 神经心理测验），因为 recall 那个"分母是全部相关、且需要预先知道"的性质最反直觉。第三个比喻特别好：讲师的女儿是临床神经心理学家，会在聊天早段随口"埋"下一些事实，两小时后突然问"你还记得多少？" —— **测年迈父母的记忆和测搜索引擎的检索器，是同一个指标。**

### k 的三条硬性质（天花板、交叉点、单行道）

记 **n = 相关文档总数，k = 你取的 top-k**：

- **天花板：** `k < n` 时完美 recall 不可能；`n < k` 时完美 **precision** 不可能，上限 = **n/k**。
- **交叉点：** 恰好 `k = n` 时，完美 precision 和完美 recall 才可能同时达到。
- **单行道：** **recall 关于 k 单调不减** —— 多挖一勺可能加进贝壳或石子，但绝不会拿走桶里已有的贝壳。

> *"This is why retrieval sets k generously."*

**这条单行道就是两阶段架构的数学依据：** 第一阶段只管别漏（靠大 k 把 recall 拉满），第二阶段只管排准（靠 reranker 提 nDCG）。分工来自 recall 和 precision 对 k 的相反反应。

**高风险领域 recall 是主人：** 法律 RAG 漏掉那条能赢官司的判例是灾难性的 —— **宁可要 50 篇含噪声但囊括所有判例的文档，也不要 5 篇干净却漏掉关键那条的。** 医疗 RAG 漏掉一个药物相互作用可能伤到病人。

### Quiz 2：天花板的数值化

> 埋了 n = 10 个贝壳。孩子交回 k = 20 个东西，其中 7 个是真贝壳。(a) Precision@20? (b) Recall@20? (c) **最好可能的** Precision@20 是多少？

**答案：** (a) 7/20 = **0.35**；(b) 7/10 = **0.70**；(c) **10/20 = 0.50** —— 世界上一共只有 10 个贝壳，桶却有 20 个位置，剩下 10 个位置必然是石子。

**教学点：Precision@k 低不一定是系统烂，可能是 k 设得比相关文档总数还大。** 这个孩子的 0.35 已经达到了理论上限 0.5 的 70%。**孤立看一个 precision 数字会误判系统。**

### F1：调和平均

$$F_1 = 2 \cdot \frac{P \cdot R}{P + R}$$

只返回一篇永远相关的文档 → P = 1.0、R = 0.1 → **F₁ ≈ 0.18**（算术平均会给 0.55，看着还行）。平衡时 P = R = 0.5 → F₁ = 0.5。**调和平均惩罚失衡：你无法靠"一半完美"买到好的 F₁。**

> *"Precision and recall are two **adversarial masters** — return the whole corpus for perfect recall, or one sure document for perfect precision; both are useless. Quote them **together**, always."*

### 为什么阶梯必须继续往上爬

Precision、Recall、F1 共有两个盲点：

- **不感知排序（not rank-aware）** —— 相关文档排在第 1/2/3 名，和排在第 48/49/50 名，**得分完全一样**。
- **不感知分级（not grade-aware）** —— 一章《费曼物理学讲义》和一条干巴巴的手册条目，都只算"相关"。

> *"Users do not read result lists uniformly. As the old search joke goes: governments hide their secrets on **page two** of the search results. Nobody ever visits."*

**两个盲点 = 两个升级方向。**

### Metric 3：MRR —— 阿里巴巴只要一件珠宝

$$MRR = \frac{1}{|Q|}\sum_{q\in Q}\frac{1}{r_q}, \qquad r_q = \text{第一个相关结果的排名}$$

第 1 名 → 1.0；第 3 名 → 0.33；第 10 名 → 0.1；第 100 名 → 0.01（系统基本等于没帮上忙）。

**关键性质：惩罚是凸的。** rank 1→2 分数腰斩；rank 10→11 几乎无感。

> *"All the metric's sensitivity lives in the early ranks — exactly where the user's patience lives."*

**何时用：导航式（navigational）查询** —— "退货政策是什么？"只想要一个确定答案，第 1 条对了第 2 条就多余。谷歌、亚马逊、企业内搜主要都是这种意图。经验法则：**MRR > 0.3 大致意味着首命中落在前 3 名**。

**MRR 的坦白：阿里巴巴不清点库存。** 语料里有 10 篇相关？MRR **分不出**"只找到 1 篇"和"前 10 名全命中"的系统 —— 两者首命中都在第 1 名，都给 1.0。对"要读全部"的研究型用户，这是致命的。

### Metric 4：MAP —— 贪心的兄弟卡西姆

卡西姆不满足于第一件珠宝，他要**每一颗**钻石，而且**越早在路上拿到越好**。他就是做研究的用户。

$$AP_q=\frac{1}{m}\sum_{i=1}^{m}\frac{i}{r_i}, \qquad MAP=\frac{1}{|Q|}\sum_q AP_q$$

> at the i-th relevant doc you've seen i treasures in r_i shelves — that ratio is precision at that moment of joy

名字是"平均的平均"（讲师吐槽：严格说该叫 mean mean precision）。完美一天：四件宝贝在前四个货架；糟糕一天：同样四件散在第 1、4、12、37 名 —— recall 一样，AP 天差地别。

**MAP 的残留盲点：仍是二元相关**，分不出 rel=4 和 rel=1。

### Metric 5：AUC-PR —— 大海捞针指标

**为什么不用 ROC：** ROC 出身信号处理（噪声线路上的电压）。对 RAG 它是**错的曲线** —— 相关文档极其稀有（百万里只有 6 篇），FPR 的分母是百万级，**假阳性率天生就低得像天使**。

> *"A trivial retriever that returns the empty set has a false-positive rate near zero — and looks superb on ROC. **Class imbalance is the assassin of ROC.**"*

**PR 曲线**的两个轴（precision、recall）**都不含"海量不相关文档"这个分母**，对稀有正类敏感。
- 细心的孩子：recall 爬到 1.0 时 precision 才缓缓下降 → **AUC-PR ≈ 0.86**
- 笨拙的孩子：precision 一开始就断崖式跌落 → **AUC-PR ≈ 0.32**
- 随机基线 = **语料的相关性基率**（不是 0.5）

**何时用：正类相对语料极其稀有时** —— 企业 RAG、欺诈检测、安全事件、推荐。

> *"AUC-PR is the continuous generalisation of MAP, and it stays honest as your corpus grows."*
> （语料越大，ROC 的 FPR 越被稀释成 0 越虚高；AUC-PR 不碰真阴性这个分母，所以随规模保持诚实。）

### Metric 6：nDCG —— 顶峰

**宝物开始有了价格：** 石头 0、银 1、金 2、**钻石 4**。排第 1 的钻石胜过排第 1 的银；两者又都胜过埋在第 20 名的钻石 —— 走得越深风险越高。**同一颗钻石，埋得越深，值越少。**

> *"Double sensitivity — to **what** you find and **where** you find it. Our graded scores r ∈ {0,…,4} finally earn their keep."*

这句呼应 Act I：金数据集里辛苦标的 0–4 分级，前面五个指标都只用到二元，**直到 nDCG 才第一次把分级真正用起来**。这就是为什么 Act I 坚持要 SME 打 0–4 而不是 0/1。

**从里到外读四层：gain → cumulate → discount → normalise**

$$nDCG@k = \frac{DCG@k}{IDCG@k}, \qquad DCG@k = \sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}$$

| 层 | 公式 | 作用 |
|---|---|---|
| **Gain** | `2^rel − 1` | 宝物的价值，对相关度**指数**放大 |
| **Cumulative** | `Σ` | 前 k 个货架的背包总值 |
| **Discounted** | `/ log₂(i+1)` | 越深的洞，同一颗宝石越不值 |
| **Normalised** | `/ IDCG` | 除以"这个洞里最好的一天"（理想排序） |

**Gain 层 —— 刻意做成指数：** 石头 0 → 0；银 1 → 1；金 2 → 3；钻石 4 → **15**。**一颗钻石值 15 个银，不是 4 个** —— 指数把"顶级相关性不成比例地重要"烤进公式。

> ⚠️ **工程坑：两种约定并存。** Järvelin–Kekäläinen (2002) 用线性增益 `rel`；Burges (2005) 的 `2^rel − 1` 是现代默认（scikit-learn、pytrec_eval）。**读旧论文先核对公式 —— 跨约定的数字不可比。**

**Discount 层 —— 复利折现的比喻最精彩：**

> *"I am willing to promise anyone a **million dollars on their 200th birthday** — you realise the present value is not much. The diamond at rank 20 is the same promise; log₂ writes the discount schedule."*

对数的特性是**顶部温柔、底部严厉**：rank 1 除以 1（不打折）、rank 2 除以 1.585、rank 20 除以约 4.39。分母里的 **+1** 让第 1 名不至于除以零。

**Normalise 层的三个好处：** 完美排序 = 1.0（有明确上限，好解读）；值域固定 [0,1]（可比）；跨 query 平均干净（不像 DCG 会被相关文档多的 query 拉偏）。这是它能当跨 query 主指标的原因。

### Quiz 4：手算 nDCG

> 排序的相关度分级：**[0, 1, 0, 2, 1]**。求 DCG、IDCG、NDCG @ k=5。

$$DCG = \tfrac{0}{1} + \tfrac{1}{1.585} + \tfrac{0}{2} + \tfrac{3}{2.322} + \tfrac{1}{2.585} = 0.631+1.292+0.387 = \mathbf{2.310}$$
$$IDCG_{[2,1,1,0,0]} = \tfrac{3}{1}+\tfrac{1}{1.585}+\tfrac{1}{2} = 3+0.631+0.5 = \mathbf{4.131}$$
$$NDCG = \tfrac{2.310}{4.131} \approx \mathbf{0.56}$$

> *"The gold at rank 4 is the tragedy: moved to rank 1, it alone contributes 3.0 instead of 1.29. One transposition, and NDCG jumps — **this is the number your reranker is paid to move.**"*

**0.56 = "一个平庸的日子，被精确测量了"。** 主观上说"还行"，客观上是"只发挥了理想排序的 56%"。这把"评估"和"修理动作（reranker）"闭环成一句话。

（`course/week_07/ndcg_demo.py` 跑出完全一致的数：DCG=2.310、IDCG=4.131、nDCG=0.559。）

### 本周最实用的一页：最小诊断对

| 现象 | 诊断 | 动作 |
|---|---|---|
| **nDCG 低 + Recall 高** | 文档找到了但排序烂 | **修 reranker** |
| **nDCG 低 + Recall 低** | 根本没找到 | **修检索** —— chunking、embedder、hybrid 混合 |
| **nDCG 高 + Recall 高** | 检索侧没问题 | 庆祝，进 Act III 评生成侧 |

> *"If you have time for one number, make it NDCG. The other five are diagnostics — the footholds you consult when the summit number moves the wrong way. Both computable at every build; **the delta between builds is where improvement lives.**"*

**"delta between builds"是持续改进的精髓：** 单次 nDCG 的绝对值没那么重要，关键是每次改动后的**变化量**。

### Quiz 5：早会上的实战诊断

> 今早看板：**Recall@50 = 0.91（健康），NDCG@10 一夜之间从 0.71 掉到 0.55**。一个同事提议重新 chunk 整个语料。这同事对吗？

**答案：同事错了。** Recall@50 = 0.91 说明文档**明明找得到、没漏** —— 检索层没坏。重新 chunk 是对着没坏的地方动手术。

> *"The shells are in the bucket — **badly stacked**. Re-chunking attacks the wrong stage. Inspect the **reranker** first — a bad deploy, a version drift, a broken feature. The diagnostic pair just saved you a week of re-chunking a healthy corpus."*

**"overnight"是关键线索** —— 突变通常来自一次具体变更（部署、模型更新、索引重建），不是数据缓慢漂移。所以先查"昨晚动了什么"。

**这页的价值不是学术精确，是帮你不把一周的工程资源砸到错误的地方。**

### 一图总纲：阶梯

| 台阶（低 → 高） | 一句话 | 性质 |
|---|---|---|
| **Precision@k** | 返回集的纯度 | 二元 · 位置盲 |
| **Recall@k** | 完整性 vs 全部相关 | 二元 · 位置盲 |
| **MRR** | 第一个宝贝有多快 | 只看首命中排名 |
| **MAP** | 所有相关文档，且要早 | 感知排序 · 仍二元 |
| **AUC-PR** | 整条权衡曲线 | 对稀有正类稳健 |
| **NDCG** | 分级增益，按深度折扣 | 感知排序 · 分级 |

> *"Two systems can share an NDCG and differ wildly in MRR."*
> —— 这就是为什么其余五个要保留作诊断：主指标相同，失败模式可能完全不同。

---

## Interlude：信号与噪声

视觉是 **σ**（标准差）。

> *"A 1.2-point improvement on 200 queries may be nothing at all. Before you celebrate, ask the statistics."*

### 公共基准的正当位置

- **BEIR** —— 18 个数据集、9 类任务，招牌指标 NDCG@10。最大惊喜：**BM25（纯稀疏）在许多 out-of-domain 任务上仍然打败稠密检索器** —— 这正是企业默认用 **hybrid** 的硬证据。
- **MTEB** —— 58 个数据集；**选 embedding 模型**最常引用的排行榜。
- **MS MARCO** —— 经典段落排序基准，TREC-DL 赛道底座。

> *"The deployment gate needs both: pass **your** gold-dataset threshold, and place respectably on the public boards. The first says it works for your users; the second says it is not inexplicably broken."*

### 功效分析闭合了循环

> 要以 **80% 功效、α = 0.05** 检测出 **1 分**的 NDCG 绝对提升，通常需要 **N ≈ 500–1000** 个 query。

**Act I 的"目标 1000"不是拍脑袋 —— SME Summit 其实在不知不觉中做了功效分析。**

两个方向的坑：

- **样本太小（< 200）** → 功效不足，真提升被噪声淹没，你会误以为"没用"而丢弃好改动。
- **样本太大** → **连微不足道的提升也会统计显著**。

> 企业实用阈值：**0.02–0.05 的 NDCG 绝对提升**才值得投工程；低于此，**统计显著 ≠ 实用显著**。

方法：**配对 bootstrap / 置换检验**。

### 六个指标都漏掉的第七维：多样性

$$MMR = \arg\max_{d\in R\setminus S}\Big[\lambda\,\text{Sim}_1(d,q) - (1-\lambda)\max_{d'\in S}\text{Sim}_2(d,d')\Big]$$

**十个近重复文档可以在 precision、recall、NDCG 上全拿满分**，却给出糟糕的体验：同质的证据、一种其实是冗余的**伪共识**。MMR 每次挑下一个结果时，用"与 query 的相关性 **减去** 与已选结果的相似度"打分。

实用数字：λ = 1 就是普通 top-k；**生产环境 λ ∈ [0.5, 0.8]**；多样性感知检索能把**多跳答案质量提升 6–12%**；但 **λ < 0.3 会伤害简单事实型查询**。在金数据集上调 λ，用 **α-NDCG** 评估多样性。

**又是"按查询意图调参"** —— 多跳要多样，事实型要精准。

---

## Act III：生成器 —— 从评食材转向评厨师

> *"The ingredients do not make the meal. Six metrics judged the pantry; now we judge the chef."*

**为什么这是关键转向：** 一个 RAG 系统即使检索完美（nDCG = 1.0），LLM 仍可能忽略证据、编造、答非所问、或引用错误来源。**检索指标对这些完全失明** —— 它们只看"喂给 LLM 的料对不对"，不看"LLM 做出来的菜对不对"。

### RAGAS 四指标 + 五个局限

四指标：**faithfulness**（忠实度，Week 6 响应侧 grounding 的生成侧对应）、**answer relevancy**（从答案反推 n 个合成问题，测与原问题的 cosine 相似度）、**context precision**、**context recall**。

**局限（记住，别把它当唯一裁判）：**

1. **无声明级粒度** —— "Einstein 生于 Ulm，1879 年，1921 得诺奖"是一条含 3+ 条可独立证伪声明的语句；大部分子句被支持时整条通过，**一个错声明搭便车混过**。
2. **评估模型间分数不稳定** —— GPT-4 / Claude / Llama 给不同分，厂商还会中途悄悄更新模型。
3. **无归因验证** —— 只查与上下文一致，不查每条声明是否引用了**正确**段落。
4. **评估器 pinning** —— 永远把 judge 钉到带日期的 checkpoint；维护 50–200 条人工核验的冻结校准集，定期重跑，**若 Cohen's κ 漂移 > 0.05 说明评估器变了**。

**裁决：把 RAGAS 当诊断基线（任何 RAG 都不该低于的地板），不当质量的唯一仲裁。**

### 声明级蕴含：FActScore 与 ALCE

生成评估最重要的进步 = **从答案级到声明级**。

- **FActScore**（EMNLP 2023）：把答案分解成原子事实，逐条核验。ChatGPT 生成的传记 **FActScore 只有 58%** —— 近一半原子声明无据。
- **ALCE** 扩展到引用质量：**引用准确率 40–75%**，约**每三条引用就有一条错或缺**，即便答案是对的。企业里引用准确率是**部署门槛**。

> **"撑不住的脚注比没脚注更糟。"**

### LLM-as-a-Judge 2.0

评估是特定任务，理应用**专用 judge** 而非租来的前沿模型。**Prometheus-2**（EMNLP 2024，开源、可本地跑）：直接评分 + 成对排名；与人工一致率 **72–85%**。

**四种评委偏见：** 位置、长度、自我偏好、重形式轻实质。

**必须用 Cohen's κ 对齐人工**（Landis–Koch：0.41–0.60 中等，0.61–0.80 substantial）。**企业 RAG 拒用 κ < 0.6 的 judge。** 另有 Kendall's τ 管排名一致、Krippendorff's α 管多评委。

**评委三铁律：**

1. judge 用与 generator **不同的模型家族**；
2. 成对比较**两个顺序都跑**再平均；
3. **永不信单一评委** —— 用第二个交叉验证并人工抽查。

（CoT 评委提升 8–12 分一致性但 3–5× token 成本 —— 便宜评委做持续监控，CoT 评委做周期深检。）

### RGB 四能力（RAGAS 测不了的）

RGB 基准（AAAI 2024）识别 RAG 生成器必须具备的四种能力：

- **噪声鲁棒性** —— 能否忽略话题相关但不含答案的文档
- **负拒绝率** —— 无答案时能否弃权
- **信息整合** —— 能否跨多篇综合
- **反事实鲁棒性** —— 能否发现检索文档中的事实错误（例：文档说 480 端口而其余都说 48 —— 它会标出矛盾还是盲从上下文）

---

## Act IV：前沿

1. **知道何时说"我不知道"** —— **ECE（期望校准误差）**：各置信度 bin 内 accuracy 与 confidence 的加权差。完美 = 0；现代 LLM 跑 **0.05–0.15**；**指令微调常更差**（把置信度推高却没推高准确率）。配可靠性图使用。
   > 讲师暴言："至今没见过一个企业 RAG 系统诚实说过 'I don't know'。" 试试 **Calabi–Yau 测试** —— 问一个开关厂的 RAG 关于 Calabi–Yau 流形。
2. **多跳与综合评估** —— 经典指标独立评每次检索，测不了整合。基准：HotpotQA / MuSiQue / 2WikiMultihopQA / **MultiHop-RAG**（后者给每跳 ground-truth 证据链，可评**路径**而非只评终点）。
3. **自动进化式测试集生成** —— Giskard RAGET、DeepEval（RAGAS 超集 + G-Eval）。从种子问题 LLM 变异出更难变体：加约束、要求多跳、注入干扰项、翻转期望答案（测负拒绝）、增加歧义（测消歧）。
4. **Agentic / 轨迹评估** —— agent 会规划/检索/调工具/迭代，只评终点危险。三层：端到端（正确性、满意度）、轨迹质量、**节点级精度**（每个决策点：对的工具？良构 query？合理推理步？）—— **诊断力在第三层**。
5. **Goodhart 定律（当日最重要的告诫）** —— "当测量变成目标，它就不再是好测量"。RAG 特有的 reward hacking：

   | 只优化 | 系统学会的套利 |
   |---|---|
   | faithfulness | **过度对冲** —— "有可能……"，技术上忠实但没用 |
   | citation recall | **过度引用** |
   | 长度偏见的 judge | **过度写作** |
   | judge 与 generator 同家族 | **合谋** |

   **防护：** 指标集成、对抗 eval、红队攻击指标本身、以及**一个从不用于训练的 held-out 金评委**（留作漂移检测）。
6. **成本维度** —— 前沿评委评 1 万 query 要 **$500–2000/次**；自研开源 judge 在自家 GPU 上近乎零边际成本；**一个在 5000 条领域标注上微调的 7B judge，在该领域一致性上打败 prompt 版 GPT-4。**

---

## Coda：评估地图 —— 把每个指标接回前六周

讲师把这一节从 PDF 的附录提升为独立 **Coda**，说明"把指标接回每一周组件"是刻意安排的压轴环节，不是附录。

| 组件（周） | 失败模式 | 对应指标 |
|---|---|---|
| Embeddings & 检索（W1–2） | 检索质量差 | Recall@K, Precision@K, MRR, MAP, nDCG |
| Reranking（W2） | 相关结果被埋 | precision, **nDCG** |
| Chunking（W3） | 相关信息被切断 | context recall, information integration |
| 派生工件（W4） | 替身值不值 | Recall@K / context precision（替换前后对比） |
| GraphRAG & 多跳（W5） | 跨文档推理 | information integration, 多跳基准 |
| 两道门（W6） | 请求门 → 噪声；响应门 → 弃权、忠实 | noise robustness；**FActScore**（断言-证据图是机制，FActScore 是指标） |
| 全流程（本周） | 端到端 | answer correctness, satisfaction, ECE |

**最后一行的告诫：** 端到端指标捕获全貌但**不定位失败** —— 定位靠组件级指标。

---

## 本周产出的 eval artifact

三个可运行 demo，放在 `course/week_07/`：

| 文件 | 内容 |
|---|---|
| `ndcg_demo.py` | nDCG 四层逐行展开（gain / discount / 贡献），复现 Quiz 4 的 0.559 |
| `pr_curve_demo.py` | PR 曲线 + AUC-PR（用 Average Precision 近似） |
| `rerank_eval_demo.py` | 检索 → reranker → 算指标的闭环，含 `diagnose()` 诊断函数（照"最小诊断对"那页写的） |

---

## 可以直接拿走的几条

1. **先建尺子，再谈指标。** 没有金数据集，Act II 的六个指标全部无意义 —— 它们"presuppose"那个人工制品。
2. **金数据集走 cherry-pick 五步法**，并在报告里明确写"这是 pool 近似的 recall"。规模最少 200、目标 1000（功效分析支持）。
3. **日常只盯 nDCG@K，配 Recall@K 做诊断对。** nDCG 低 + Recall 高 → 修 reranker；两者都低 → 修检索。这一条能省下一周对着健康语料重新 chunk 的冤枉功。
4. **nDCG 要先确认增益约定**（线性 vs `2^rel−1`），跨约定的数字不可比。
5. **指标涨了先跑配对 bootstrap。** 上线判据建议：**nDCG 提升 ≥ 0.02–0.05 且配对检验显著**。
6. **公共基准只当 sanity check**，自己的金数据集才是裁决。部署门需要两个都过。
7. **留一个 held-out 集，只有评估负责人能碰。** 防过拟合，也防 Goodhart。
8. **生成侧要到声明级。** 答案级的 faithfulness 会让一条错声明搭便车混过。引用准确率设成部署门槛。
9. **judge 要 pin 版本、跨模型家族、κ ≥ 0.6**，并保留一个从不用于训练的金评委做漂移检测。

---

## 一句话定位

前六周一直在"建"，这周开始"量"。**评估做错，前六周全部悬空；做对，整条流水线变成一个你能 steer 的系统。** 学完这一周，就从 RAG **practitioner** 跨到 RAG **engineer**。
