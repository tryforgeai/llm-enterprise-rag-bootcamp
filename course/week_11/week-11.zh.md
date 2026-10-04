# 第 11 周课堂笔记：语义缓存（Semantic Caching）

日期：2026-08-22（周六）

状态：**课前预习（第一–九节）+ 课后精读（第十–十三节）**。两份材料（讲义 + 专著）已通读；专著 Part II-B 已做逐节精读并产出英文 presentation。**现场讨论、Lab、本周 eval artifact 仍待补充；上周（Week 10, 8/15）在仓库里没有任何记录**，第一节专门处理这个缺口。

来源：

- `uploads/the-stones-in-the-river.pdf`（*The Stones in the River — Semantic Caching for Enterprise RAG*，SupportVectors，72 页，本周课堂讲义）
- `uploads/cachecraft-shareable.pdf`（*CacheCraft — When Repetition Becomes a First-Class Citizen: A Definitive Report on Semantic Caching*，SupportVectors AI School，91 页，扉页写 "First draft, August 21, 2026"，即**课前一天成稿的配套专著初稿**；讲义本身没有标日期）

> 本周定位：Week 06 讲"两道门"（请求侧护栏 + 响应侧接地），Week 07/08 当裁判（量检索、量生成器），Week 09 把语料本身当成可制造、可治理的东西（OKF）。本周走到整条流水线的**最前面**——那个决定"这次到底要不要惊动模型"的器官。一句话留存：**缓存是一场"过去会重演"的赌注；几何让这个赌注成为可能，决策论让它诚实，对手让它危险，算术决定该不该下注。**

---

## 一、先说缺口：上周（Week 10，8/15）没有记录

仓库现状：`course/` 里最新的课堂笔记是 `../week_09/week-09.zh.md`（2026-08-08，OKF + Secure Retrieval 模块开场），Git 最后一次课程相关提交是 2026-08-14。**8/15 那次课没有笔记、没有讲义 PDF、没有对应的 task 条目。** 这一周的学习轨迹目前是断的（和 `tasks/index.md` 里 T027 记的 Week 04/05 笔记缺口性质相同，但更新鲜、更容易补）。

### 从本周材料反推出的 Week 10 候选主题（**全部待你确认**）

本周专著大量回指同门的其他"craft"报告和课程模块，这些回指是推断上周内容的唯一线索：

| 线索（专著原文回指） | 推断的上周主题 | 置信度 |
| --- | --- | --- |
| "MemoryCraft taught two altitudes of eviction and commanded that the ledgers never mix"；"MemoryCraft partition interlude"；"MemoryCraft cache canon (Bélady, LRU/LFU/ARC)" | **MemoryCraft**：记忆的两个高度、驱逐策略经典、分区隔离 | 高——被引用三次以上，且专著说本周内容是它的"第三次出现" |
| "SkillCraft priced loading a skill: VoL = p·g − κ(c)"；"promotion pipeline"；"skill library" | **SkillCraft**：技能加载定价、技能晋升流水线 | 中高 |
| 讲义 p.33："The FT-course trinity returns: easy pairs first, separate the pull-together from the push-apart, and feed the encoder the near-misses it almost believed"；专著 p.17 另提到微调课的边注用 $(d-1)$ 陈述那个界 | **微调课**：curriculum learning + decoupled loss + hard negative mining | 中 |
| "the agents-course bonus-cost chapter's practitioner ladder" | Agent 成本章节 | 低 |
| Week 09 笔记里 Secure Retrieval 只讲到 Module 2，讲义地图预告了 Module 3–6 | **Secure Retrieval 后续模块**（数学、产品选型 OpenFGA/SpiceDB） | 中——这是唯一"未讲完就停下"的线头 |

> 最省事的补法：如果上周确实是 MemoryCraft/SkillCraft，本周专著那张 **Rhyme Ledger**（PDF p.76 / 印刷 p.72）（下面第五节抄了）几乎是一份上周内容的目录，可以直接拿它当骨架反向回忆。

### 要补的五个问题（照 `PROJECT_PLAN.md` 的操作节奏）

1. 上周的讲义标题是什么？有没有 PDF/截图能放进 `uploads/`？
2. 上周提取出的**一个 agent 能力**是什么？
3. 上周有没有产生/该产生一条 eval case？
4. 上周有没有 Avaloka 映射？
5. 上周有没有需要写进 `docs/decisions/decision-log.md` 的方向变化？

---

## 二、上周回顾（以仓库里最新的 Week 09 为准）

因为 Week 10 无记录，这里回顾的是**目前可核实的最近一次课**（Week 09，8/8）。好消息是：它恰好是本周的直接前置——本周专著专门为它加写了一节（见第五节"Governed Layer"）。

### 1. 上半场：OKF / 治理语料（Open Knowledge Format）

- 核心倒转：**知识可以带着自己的档案**——谁写的、谁核实过、什么时候过期。当语料是这样被"制造"出来的，检索这件事的性质就变了。
- 开场四个思想实验（*The Library in Your Head*）的收束句：**理解发生在"撰写时"，考试只是把它取回来**（"The understanding happened at authoring time. The exam merely retrieved it."）。
- 关键机制：一个知识单元 = 一个文件；卡片身份 = 文件路径；边无类型（因为读者是语言模型）；信任家族 `generated` / `verified`；`status` 取 `draft`/`stable`/`deprecated`；`stale_after` 是**作者写下的绝对日期**而不是操作者猜的相对倒计时；git 治理（CODEOWNERS、分支保护、每晚巡逻过期 concept）。
- 历史锚点：1895 年布鲁塞尔的 Mundaneum，1200 万张索引卡 + UDC 层级 + 交叉引用 = 一部用纸做的搜索引擎，比晶体管早五十年。

### 2. 下半场插曲：Module 5 — Secure Retrieval / Enterprise Entitlement-RAG

- 四种授权范式讲完：ACL（资源自己说谁能看）→ RBAC（职位暗示范围，坑：角色爆炸）→ ABAC（属性现算，坑：元数据质量 + **默认失败开放**）→ ReBAC（权限是图上的一条路径，坑：查询时图遍历是分布式系统问题）。四者不是竞品，生产系统会**叠着用**。
- 归一化安全描述符：五种源系统方言 → 一个 JSON 形状；三条设计规则——**字段缺失一律拒绝**、**deny 优先于 allow**、**描述符带版本号以便重放判定**。
- 切片时的权限传播：**内容能毫不费力地在切片中存活，权限不能——除非你专门让它做到**。检验标准：一个 chunk 被单独检索出来时，系统还能不能说清谁被允许看它？
- 两条摄取流水线必须同步：内容流水线人人都建过，权限流水线很少被同等用心地建——而权限**变化得比内容快得多**。10:01 建索引 / 10:05 权限变更 / 10:06 查询 = 一次正在等待发生的泄漏。

### 3. Week 09 自己总结出的三条贯穿主线

1. **任何被治理的状态都必须能回答"这是什么时候的快照"**，而不是被当作永远最新的既定事实（OKF 时间戳、`D_u` 逐请求现算、内容索引 vs 权限变更三处独立推出同一条）。
2. **prevention 优于 suppression**：在源头把不该发生的事变成结构上不可能，而不是事后压制。
3. **结构胜过警惕**（structure beats vigilance，因为 vigilance 会有 outage）。

### 4. 为什么这三条正好是今天的前置

| Week 09 的东西 | 今天会变成什么 |
| --- | --- |
| "结构胜过警惕" | **Scoped Cache** 模式：tenant/user 必须写进**缓存键内部**，而不是在应用代码里写 `if tenant_id != ...` 的检查 |
| 描述符带版本号、可重放 | **Version Pin**：embedder 版本 + index 版本写进条目 schema，版本不匹配 = 无条件 miss |
| `stale_after` 是作者写的绝对日期 | 专著明确说这条**修正了"我们"最老的时钟**（指本课程教的失效三件套，不是整个领域）：TTL 是消费者的猜测，`stale_after` 是作者的知识 |
| 信任层级 derived, never stored | **Principle 0.5 信任必须穿过缓存**：命中时必须从活的 bundle 重新推导 tier，否则就是 provenance laundering |
| 权限流水线比内容变得快 | Evidence Gauntlet：按证据失效，不按时钟失效 |

---

## 三、本周主题：语义缓存

### 0. 一句话

> 最便宜的检索是那次根本没有跑的检索；最昂贵的答案是那个带着自信端上来的过期答案。手艺就在于知道现在说话的是哪一句。

### 1. 讲义地图

```text
PROLOGUE  The Bet        —— 语义缓存到底是什么、不是什么
ACT I     The Geometry   —— 为什么命中从来不是巧合（球面测度集中）
ACT II    The Decision   —— 从"你选的阈值"到"你付得起的错误"
ACT III   The Machine    —— 专用编码器、对抗世界的新鲜度、给 agent 做缓存
INTERLUDE The Adversary  —— 局部性 = 碰撞风险，定理被武器化
ACT IV    The Economics  —— prefix caching 吃掉容易赚的那部分之后
ACT V     The Wild       —— 2026 市场当证据读，以及模式语言
```

### 2. Prologue：赌注与边界

**赌注**：所有缓存都在赌"精确重复"（CPU、CDN、memoize）；语义缓存把赌注加大——它赌**意思会重复，即使措辞不会**。Phil Karlton 那句"计算机科学只有两件难事：缓存失效和命名"——语义缓存两件都占了。

**Front Door 三道门（一次查找）**：精确哈希层（微秒级、免费）→ 语义层（**证据，不是证明**）→ 完整流水线；每次生成都写回。

**四种被叫做"caching"的东西，必须分清**（专著说这是厂商文案和"我们自己教学里的一行"最常见的混淆）：

| 家族 | 键 | 匹配 | 复用什么 | 失败长什么样 |
| --- | --- | --- | --- | --- |
| Provider prefix caching | 相同 token 前缀 | 精确 | 服务商侧 KV 状态 | 不可能出错，miss 只是付全价 |
| KV-cache reuse 研究 | chunk 级 token 内容 | 精确/分段 | **计算** | 注意力结构变旧 → 质量退化 |
| Embedding cache | 精确字符串 | 精确 | 向量 | 零正确性风险（"把文件柜叫图书馆员"） |
| **语义缓存** | **embedding** | **近似** | **成品答案** | **5 毫秒内端出一个自信的错误答案** |

> **Principle 0.1（只有语义缓存会错）**：prefix / KV 缓存改变的是"算出答案的成本"，语义缓存改变的是"到底要不要算"。无损缓存的失败模式是延迟变高；语义缓存的失败模式是自信的错误信息。

**五个可以放缓存的层**（讲义 p.8）：embedding、retrieval、rerank、answer、agent-state。**头条里说的全是第四层（答案层），而五种危险全都集中在第四层。**

> 注意：专著 Part V 也讲"五层"，但那是**另一套划分**（答案 / 检索集 / 中间产物 / chunk-KV / 理解），不是这一套的展开。两套都记在下面第五节第 2 小节。

**两个高度，账本永不混用**：答案高度（语义键、近似命中、正确性风险）vs KV 高度（精确前缀、零风险、服务商的生意）。讲义说"今天会遇到的每一个混乱架构，都是把这两个账本混在了一起"（p.9）。

### 3. Act I：几何——为什么命中从来不是巧合

- embedding 活在 $d$ 维单位球面上。$d=3$ 的直觉在上面**不只是弱，是自信地错**。
- Lévy 集中不等式：对任意 1-Lipschitz 函数 $f:S^{d-1}\to\mathbb{R}$，$\Pr[|f(v)-\mathbb{E}f|>\varepsilon]\le 2\exp(-(d-1)\varepsilon^2/2)$。
- 缓存只关心一个 Lipschitz 函数：$f(v)=\langle u,v\rangle$（$u$ = 查询方向 = 北极）。于是 $\Pr[|\langle u,v\rangle|>\varepsilon]\le 2\exp(-(d-1)\varepsilon^2/2)\approx 2\exp(-d\varepsilon^2/2)$ ——**随机方向几乎永远不会和你的查询有非平凡的余弦相似度**。专著专门开了一个框（"一个定理，两个指数"）做调和：$(d-1)$ 是球面精确的界，$d$ 只是大 $d$ 渐近形式，不要混用。
- 两个随机单位向量夹角余弦的精确密度 $\propto (1-c^2)^{(d-3)/2}$：$d=3$ 平坦，$d=768$ 塌成一根针，$d=1536$ 更尖（宽度 $\propto 1/\sqrt d$）。
- **教义（极地熊）**：赤道装走了全部测度，所以偶然邻居被歼灭。任何出现在冰线之内的东西都是**被放进去的**——被训练放进去、被共享的意义放进去，或者（Interlude 会回来）被对手放进去。**每一次命中都是一个有原因的事件。**
- 现实的复杂化：**各向异性（anisotropy）**——现成 embedder 只用了一个很窄的锥，什么都和什么余弦相似（"整个领域都是 Fremont"）。**原始 cosine 数值依赖编码器，永不可移植。**
- 领域微调 = **大都会效应**：把锥摊到整个球面（用掉更多表面）+ 凝出近义词的紧凑"市中心"。两件事对缓存都要紧。
- 温度 = Boltzmann 因子：对比学习优化 alignment vs uniformity（Wang–Isola），温度 $\tau$ 决定邻居互斥有多狠；$\tau$ 越低，市中心越紧。
- 安慰：准正交容量——只要求方向**近**正交（两两 cosine 低于某个小 $\varepsilon$），球面装得下的不是 $d$ 个而是 $e^{c\varepsilon^{2}d}$ 个，所以近义词不必挤在一起，**高维是缓存的朋友不是敌人**。
- 病理：**Hub**（球面上的"town square"）——高维近邻图里少数点成为所有人的邻居。缓存里的一个 hub 就是一台**批量出错机**。诊断：$k$-occurrence 偏度；治疗：CSLS。
- 两个必背比喻：**罐子里的硬币**（残差流像罐子攒硬币，长文本向量更长，所以比较方向前必须归一化——归一化是"看不见的承重墙"）；**Bay Area vs Wyoming**（最近≠近；高维处处是 Wyoming，argmax 是关于排序的陈述，从不是关于接近的陈述——所以**不带阈值的 kNN 检索是被禁止的**）。

### 4. Act II：决策——从阈值到误差契约

**定理在哪里失声**：集中不等式证明"外人进不来"，但对"里面的人"一言不发。**每个条目内部，正确命中和错误命中的相似度分布是重叠的**，而且重叠形状**逐条目不同**：某个条目 0.91 就可靠安全，另一个条目 0.96 还在端错答案（因为它的 hard negative 住在 0.97）。全局 $\tau$ 不是解决这件事，只是**把不同街区平均掉**——处处错一点，而在流量最密、风险最集中的地方错得最狠。

**Cacheability**：集中给出的是两个紧的众数而不是一个尖峰；讲义把可缓存性定义为**两个众数的位移按宽度缩放**（displacement scaled by width，形式上是一个 $d'$ 式的可分性量）——**具体公式在 PDF 文本提取里丢了，上课看幻灯 p.24 补**。好的 $\tau$ 让它最大，坏的 $\tau$ 坐在山谷里。

**把这一次的"serve"定价（家族货币，一法三门）**：

```text
SkillCraft:   VoL      = p·g − κ(c)                  加载一个技能
MemoryCraft:  VoR(m)   = p_m·g_m − κ(c_m)            召回一条记忆
CacheCraft:   VoS(i|q) = p_i·g − (1 − p_i)·L − κ      端出一个存好的答案
```

新增的 $(1-p)L$ 项就是"只有语义缓存会错"这条原则进入代数。重排之后，服务条件是**一个关于概率的阈值，而不是关于相似度的阈值**：

$$\text{serve} \iff p_i > \frac{L+\kappa}{g+L} \approx \frac{L}{g+L}$$

念出来：**你必须多确信，由"伤害/帮助"之比决定。相似度在这条定律里根本没有出现**——相似度只是估计 $p_i$ 的证据。

**四级阶梯（从旋钮到契约）**：

| 级 | 是什么 | 前置条件 | 谁在这一级 |
| --- | --- | --- | --- |
| 1 | 全局 $\tau$（标定过的 sweep，报 P-CHR，每周人工评样） | 低风险高重复 FAQ | **所有产品/网关只到这一级** |
| 2 | 分类阈值 / TTL / 配额（代码类、闲聊类、监管类各自的工作点） | 流量类别可见 | 规模化生产的常态 |
| 3 | **误差契约**：per-entry 学习曲线 + 预算 $\delta$ + 探索标签 | 流量密度 + 标签供给 | **文献住在这里** |
| 4 | **验证**：异步先行，$L$ 残酷处同步 | 监管/语音/共享层 | 文献 |

> 产品交付第 1 级，文献活在第 3–4 级——**这两级的落差是整份讲义里最可利用的一个事实**（拿去做 capstone 或做产品都行）。

**vCache（Berkeley，ICLR 2026，arXiv:2502.03771）——三步走**：

1. **契约反转**：操作者不再选相似度，而是声明**误差预算**——"我端出的命中里，最多 1/50 可以是错的"（受监管场景 1/500）。这个数就是 $L/(g+L)$ 穿上运营的衣服。
2. **每个条目自己记账**：为每个缓存 embedding 维护一个小模型（单参数 sigmoid 族够了）拟合 $\Pr[\text{correct}\mid s]$。拥挤街区学出陡峭、晚起的曲线；孤单条目学出宽松的。全局 $\tau$ 溶解成 per-entry 决策边界。
3. **探索付标签的钱**：以标定后的概率，系统端出命中的同时**偷偷也去调一次模型**，比对两个答案，把一致/不一致记成这个条目曲线的标签。条目年轻时多探索少服务，证据积累后探索衰减、条目"挣得自治权"。
- 实测：命中率最高 12.5×，错误率 26× 更低，且 $\delta$ 全程被守住（跨三个 embedding 模型、两个 LLM）。开源，附四个公开 benchmark。
- 后继：**MVR-cache**（ICML 2026，多向量/late-interaction 匹配，同一保证下命中率再 +37%，需要每领域约 3k 标注 prompt，约 23ms 分段开销）；**Krites**（异步 judge 核验 near-miss 带，把祝福过的对晋升进动态层，关键路径延迟不变，被服务请求最多 3.9×）。

> **Principle 0.3**：相似度阈值是实现细节，被设计的对象是**误差契约**。**一个说不出自己已证实错误率的缓存，没有阈值，只有一个猜测。**

**校准（2026 的安静结论，该进 evals 周的正典）**：离线常用的 PR-AUC 奖励**排序**，但缓存不排序，缓存**卡阈值**——卡阈值需要分数本身可用（铺得开、稳定、在整个区间含义一致）。实测：BCE 训练的 reranker，PR-AUC 0.75–0.82，真去卡阈值时只保留不到四分之一的性能（P-CHR 塌到 0.17–0.20）；ColBERT 式 late-interaction 打分器纸面上排序平庸，卡阈值几乎完美。**最狠的一条：目标函数错的时候，训练数据多 38 倍反而让部署行为更差——校准由损失函数决定，不由规模决定。**

- 该报的指标：**P-CHR 曲线**（precision vs cache-hit-ratio）及其 AUC，以及 **CRR = P-CHR AUC / PR-AUC**，而不是 PR-AUC。
- 四指标仪表盘：命中率、**已证实错误率（对着 $\delta$）**、unsafe-served rate、延迟节省比。
- 治理彩蛋：这门课自制的 freshness 指标 **MRF 被正式退役**（RAG 课的章节里和 lesson plan 里定义不一致），由 unsafe-served rate + P-CHR 取代。"一个需要脚注去调和的指标，已经告诉你它的替代品该来了。"

**控制论的祖宗**：Maxwell 1868《On Governors》里的离心调速器——**这是 governor，不是 gate**：探索去测量，策略去纠偏，$\delta$ 是设定点。专著说这是本课程"同一个架构"（proposal + gate，在固定裁判下自我改进）的**第四次出现**（GEPA validator、skill governor、memory governor、cache governor）。

### 5. Act III：机器

**编码器是专才，不是通才**：缓存匹配是**改述检测（paraphrase detection）**，不是话题相似。"cancel my card" vs "cancel my flight" 是一场 0.9 余弦的灾难。所以：小编码器（ModernBERT 级）+ curriculum learning + decoupled loss + hard negative mining（微调课三件套回归）。

**第二份薪水：Near-Miss Mine**。$\tau$ 正下方那条带，恰好浓缩了编码器搞混的那些对。记录、聚类之后它们变成：下一轮微调的 hard negatives、新兴话题告警、技能候选。**缓存不只是省钱工具，它是一台对准你自己 embedder 的仪器。**

**新鲜度：证据的关卡（Evidence Gauntlet）**。TTL 在猜，世界不会来问它。命中时串行四道闸：

```text
候选命中 → 1. 查询相似度 → 2. 证据重叠（重跑廉价检索，要求与缓存里的 provenance 相交）
        → 3. chunk 版本同一性（内容寻址哈希，字节级相同才放行）
        → 4. 词法支持（缓存答案的关键声明在新证据里仍被支持）→ serve
        任何一道不过 → 重新生成（河流动了）
```

第 4 道是"承重闸"——抓的是"文档身份没变但意思变了"那种编辑。GroundedCache 实测：unsafe-served rate 从 15–35% → **0.0%**（HotpotQA）、26–52% → 1–10%（mtRAG），代价只是 1.04–1.07× 延迟。

> **Principle 0.4（按证据失效，不按时钟失效）**：TTL 编码的是关于世界的猜测，provenance 编码的是关于答案的事实。问题从来不是"这个答案多老了"，而是"**世界是否还在说这个答案当初假设的东西**"。

**失效：版本钉（Version Pin）**。在一种几何下铸造的条目必须随那种几何一起死：embedder 版本 + index 版本写进条目 schema，不匹配 = 无条件 miss，迁移靠重新 embedding 而不是靠祈祷。**悄悄升级 embedder 会以看起来像 drift 的方式腐蚀邻域。**

**给 agent 做缓存**：agent 查询重复的是**形状**，不是措辞。先规范化再做键——**W5H2 框架**（what / where / who / when / why / how / how-much），其中 (What, Where) = 可缓存的路由，**参数排除在键之外、执行时现场重新绑定**。

**缓存计划，不缓存答案**：agent 状态旧得太快，答案不能缓存，但结构会重复——从成功 episode 抽取 plan skeleton，现场适配绑定，长期赢家晋升进技能库。在 agent 高度上，**plan cache 是唯一安全的"答案邻近"缓存**。

### 6. Interlude：对手

- **熊皮衣（bear suit）可以买**：几何认证的是**放置**，从不认证**意图**。对 token 做梯度搜索，就能造出一个"穿着 0.9x 余弦"的 prompt——出现在极冠里只证明"有东西把你放在了那里"。
- **定理被反转：局部性 ⇄ 碰撞**。让命中有因果的那个集中，同时让**定向碰撞变得便宜**：攻击者只需要抵达一个很小的冠，而那个冠正是你的合法流量所在。**对抗性 hubness** 可以植入一个条目去回答很多查询。
- 实证：2026 年 1 月发表的 key-collision 攻击（arXiv:2601.23088, ICML 2026），针对的正是课上教的那种缓存——语义上与受害查询无关但在 embedding 空间碰撞的对抗 prompt，劫持缓存答案**以及缓存的工具调用**，成功率 **77–91%**，测试对象包括各大云的语义缓存参考架构。论文 Lemma 3.1 证明这个 trade-off 是**结构性的**：命中率和抗碰撞性是同一个量的正负两面。
- **让缓存工作的每一条性质，都是攻击面。不存在既开放又安全的配置。**
- 防守及其代价：**per-tenant 永远要，per-user 在内容个性化时要；scope 键住在缓存键内部，不在应用检查里**。scoping 会**腰斩**可共享人群，verification 给每个被守卫的命中上税——所以 $H$ 和 $C_{hit}$ 必须在**防守之后**报价，否则你会在事故报告里发现这笔溢价。

### 7. Act IV：经济学——prefix caching 吃掉容易赚的部分之后

**谁杀了 2023 年的那套说辞？服务商自己。** 2024–2026 三大厂全部上线 prefix caching——精确、token 级、零正确性风险，缓存输入 token 约 **90% 折扣**，OpenAI / Gemini 还是自动生效。2026 年 8 月参数：

- Anthropic：显式 `cache_control`，5 分钟 / 1 小时两档 TTL，写 1.25×/2×，读 0.1×，最小前缀 512–4096 token（按模型）
- OpenAI：≥1024 token 自动生效，折扣 50–90%（按模型家族），延长保留至 24h
- Gemini：默认隐式缓存 + 显式 `cachedContents`（按 MTok-hour 计存储费）。讲义只给了三家收敛到的共同数字（缓存输入 token 约 90% 折扣），没有给 Gemini 单独的百分比

**GPTCache 不是死于竞争对手，是死于一次调价**（最后一个 PyPI release 0.1.44，2024-08-01，之后再无发布；LlamaIndex 集成 2024 年起就是坏的）。

**还剩什么值得省（诚实的内核只有三项）**：

1. **输出 token**：prefix 命中的调用仍然全价生成，而输出费率是输入的 3–6×，在 chat 型负载上占大头——**只有语义命中能完全避开它**
2. **整条流水线**：命中跳过 embed / search / rerank / assemble，这些成本没有任何服务商折扣碰得到
3. **延迟**：秒变毫秒。这不是折扣，是**产品本身**——语音场景里两秒停顿就是一次失败的对话

**盈亏平衡（终于推导出来）**：

$$\Delta = N\cdot H\cdot (C_{full}-C_{hit}) - C_{ops},\qquad H^{*}=\frac{C_{ops}}{N\,(C_{full}-C_{hit})}$$

- $N$ = 日查询量；$H$ = 命中率；$C_{full}$ = prefix 折扣**之后**完整流水线的边际成本；$C_{hit}$ = 服务一次命中的边际成本（embedding + 索引探测 + 验证）；$C_{ops}$ = 缓存自身的日固定成本（向量库、监控、摊销的工程、误差契约要求的每周人工评样）
- 用 2026 的眼睛读分母：$C_{full}$ **每季度都在跌**（旗舰变便宜，nano 级低三个数量级），而 $C_{hit}$ 是大致恒定的物理。→ **模型降价会抬高缓存必须跨过的那道杠。**

**两个已算好的判决**：

| 场景 | 参数 | $H^{*}$ | 判决 |
| --- | --- | --- | --- |
| 旗舰模型客服助手 | $N$=50,000/天，$C_{full}\approx\$0.02$，$C_{hit}\approx\$0.0004$，$C_{ops}\approx\$40$/天 | **≈4%** | 实测 FAQ 命中率 40–60%，跨过一个数量级 → **建** |
| 同一个助手迁到 nano 级模型 | $C_{full}\approx\$0.0006$ | **≈400%** | 任何命中率都到不了 → **不要建** |

> "不要建"是分析的成功，不是勇气的失败。

**卫生：accuracy–frequency laundering（准确率-频率洗白）**。厂商测到"端出的命中里 95% 是对的"——这是一个 **precision**；营销漏斗把它重新打成"95% 命中率"，一个 **recall**。诚实的实测阶梯：

| 负载类型 | 真实命中率 |
| --- | --- |
| FAQ / 客服 | 40–60% |
| 分类 | 50–70% |
| RAG 问答 | **15–25%** |
| 开放式聊天 | 10–20% |
| Agent 工具流量 | **5–15%**（最低） |
| 混合现实 | 约 25%（对比计算器营销假设的 85%） |

X 光两问：**这个数是 precision 还是 recall？在谁的负载上测的？**

### 8. Act V：市场当证据读

- **信徒**：Redis LangCache（2025-09-04 公开预览，一年后仍标 preview；2026 年 5 月被打包进 "Redis Iris" agent 上下文引擎；按处理的输入 token 计费——**命中和 miss 都收**，这悄悄挪动了盈亏平衡点；预览价约 \$1.50/M input token，计算器头条节省假设 85% 命中率）；Azure APIM（`llm-semantic-cache-lookup` 策略族，外接 Redis 兼容存储，`vary-by` 分区表达式；**自己的文档写着这个缓存"可能端出不正确、过期或不安全的回应……请谨慎评估并实施防护"——一家超大厂在同一份文档里既卖它又警告它，这不是混乱，这是五种危险被公证了**）；Kong（最成熟的网关插件，pgvector + Redis 后端，支持流式，现已收进企业版）；Portkey（**坦率奖**：语义模式仅企业版，cosine 默认 0.95，并公布自家早期生产测试约 **20% 命中率（按负载 18–60%）**——厂商自愿交出的最诚实的数字）
- **怀疑者（负空间教得更多）**：Cloudflare——全世界缓存 DNA 最多的公司，AI gateway 里**只做精确匹配**，语义功能年复一年停在"planned"；Helicone——按设计只做精确匹配，写得明明白白。**两家最有资格知道近似匹配代价的公司选择不发货，这是最响的弃权。**
- **腐烂**：LiteLLM 名义上有语义后端，但 issue tracker 才是事实文档——2026 年 3 月报告 Qdrant 语义路径"完全不可用"（启动崩、请求崩、静默写失败），被 close as not planned。**2026 年的"网关勾选框语义缓存"，更多时候是货架件而不是系统。**
- **转身**：Momento——早期语义缓存厂商，整个搬到另一个高度去做 KV-cache offload，用自己的资产负债表得出结论：**持久的钱在缓存计算，不在缓存答案。**
- **坟墓**：GPTCache。这个领域的参考架构现在是一份参考文献。（专著脚注诚实标注：仓库并未正式归档，"abandoned" 是从两年沉默推断出来的——只是每个从业者都做了同一个推断。）

**一个活的坑：阈值之塔**。市面上对"那个旋钮是什么意思"毫无共识：

| 产品 | 单位 | 默认值 | 哪个方向更严 |
| --- | --- | --- | --- |
| Portkey | 相似度 | 0.95 | 越高越严 → |
| Azure | 距离 | 0.05（超过 0.2 有警告） | ← 越高越松 |
| Kong | 距离 | 0.2 | ← 越高越松 |
| AWS 参考架构 | 相似度 | 0.75 | 越高越严 → |

把 Kong 的 0.2 抄进 Portkey，**不是把缓存放松了一点，是把它的含义反转了**——索引返回的几乎一切都会被端出去。动任何产品阈值之前三问：**相似度还是距离？什么度量、归一化过没有？哪个方向更严？**

### 9. 模式语言：十个模式 + 四个反模式

| 模式 | 意图 | 什么时候用 |
| --- | --- | --- |
| **Front Door** | 在昂贵机器醒来之前回答回头客 | 可行性闸门通过——**抽样 10 个查询里有 1 个在 0.85 匹配上，否则不要建** |
| **Canonical Key** | 缓存意思，不缓存措辞 | 永远（这是耦合教义）；agent 用 (What, Where) 路由、参数排除 |
| **Two-Tier Threshold** | 从 near-miss 带取价值但不端它 | 任何完整流水线缓存：$\tau_{full}$ 以上服务，以下当**提示**（扩写查询、种子检索） |
| **Error Contract** | 把"你选的阈值"换成"你付得起的错误" | 流量密度够喂曲线、风险值得付探索税 |
| **Verified Hit** | 把证据转成保证 | 受监管答案、语音产品、任何共享层 |
| **Scoped Cache** | 让泄漏和碰撞**结构上不可能** | 永远——无 scope 的变体是第一号反模式 |
| **Version Pin** | 在一种几何下铸的条目随它一起死 | 永远；失效绑定 index 版本，句号 |
| **Evidence Gauntlet** | 对着世界查新鲜度，不对着时钟 | 活语料上的第一层答案缓存 |
| **Plan Cache** | 世界不会重复时，复用工作的形状 | agent 负载——那里它是唯一安全的答案邻近缓存 |
| **Near-Miss Mine** | 缓存不只是省钱工具，是仪器 | 永远——这是缓存的第二份薪水 |

**四个反模式（每一个都是"有操作、没策略"）**：

- **Global Threshold** = 有 serve 操作，没有决策策略
- **Unscoped Shared Cache** = 有共享操作，没有访问策略（已是公开的攻击目标）
- **Hit-Rate Worship** = 有测量操作，没有真相策略。**命中率是危险指标：答案越差它越高。盯着错误，否则命中率会来盯着你。**
- **Checkbox Cache** = 有部署操作，没有归属策略

**周一早上的执行顺序**：① 打开 prefix caching（免费、无风险、约占总收益 60%）② 跑可行性闸门（抽样十里有一在 0.85 匹配——否则不要建）③ 只在密集、已 scope 的切片上动手术刀 ④ 签误差契约 ⑤ 每周人工评样。

**收束（Say it back）——五种仪器 ↔ 五种失败**：

```text
cap bound       → the chance hit      （不存在偶然命中；命中都是有原因的）
error contract  → the confident wrong answer
evidence gauntlet → the stale serve
scoped key      → the tenant leak
break-even H*   → the money pit
```

**几何让赌注可能；策略让它诚实；scope 让它安全；算术决定该不该下注。**

---

## 四、课前把六道 Pop Quiz 先答一遍

讲义里六道题的**答案里有两道是"以上都不是"**（第 2、第 5 题）——这是故意设计的陷阱，先自己踩一遍再上课，收益最大。（注：PDF 文本提取把公式里的数字丢掉了，具体数值上课看幻灯。）

| # | 题 | 该怎么想 | 陷阱/答案 |
| --- | --- | --- | --- |
| 1 | 熊口普查：$d$ 维球面，冠 $\varepsilon$，用一千万条随机查询探测，落进一个冠的期望条数？"在冠里找到一个点"证明了什么？ | 代 $\Pr\le 2\exp(-d\varepsilon^2/2)$，乘 $10^7$ | 约 **2 条**。Say-back：偶然被歼灭，所以冠里的点是**被放进去的**——每次命中都有原因，缓存的工作是判断**是哪个原因** |
| 2 | 两个条目共用缓存：A（"什么是 RAG"）改述正确匹配低到某个 cosine；B（"最大日剂量"）错误匹配高到某个 cosine。选一个全局阈值同时服务好两者 | 试着把三个选项都代进去 | **以上都不是**。松了 B 端毒，紧了 A 饿死而 B 仍重叠，中间两个失败一起来。修法是 per-entry 策略 = 误差契约。附赠一句：**被迫从给定选项里选的学生，就是被迫从给定上下文里作答的模型——"以上都不是"是负拒绝，请一直上着膛** |
| 3 | 语音客服机器人：正确即时答案值 $g$，错答清理成本 $L$，查找本身 $\kappa$。求正当化"端出"的最小胜率 $p^*$ | $p^{*}=(L+\kappa)/(g+L)$ | 降低风险（如问营业时间）$p^*$ 就降。Say-back：**服务门槛由后果的不对称性决定，不由 cosine 决定**——所以一个全局旋钮永远无法同时给"退款政策"和"营业时间"定价 |
| 4 | 两个客户共用语义缓存。租户 A 的分析师问"我们 Q3 收入多少"被缓存；第二天租户 B 的分析师问一模一样的话 | 想"结构 vs 检查" | tenant ID 必须**住在键里面**：同样的字、不同租户 = 结构上不同的键空间，查找根本找不到外来条目，所以没有东西可泄漏。**检查只是禁止泄漏，scoped 键让它不可能——vigilance 会有 outage** |
| 5 | nano 级判决 $H^{*}\approx400\%$，团队不肯放弃。(a) 缓存扩容一倍 (b) 微调更好的匹配器抬命中率 (c) 降低 $\tau$ 把更多查找变成命中 | 看 $H^{*}$ 公式里有没有这个变量 | **以上都不是**。(a) 尺寸不在公式里；(b) 抬 $H$ 但命中率上限 100%，杠在 400%；(c) 同时抬 $H$ 和错误率。**当杠本身不可及时，每个旋钮都是错旋钮**——诚实的选择只有"不要建"或换一种筹码（延迟，那里 $\Delta$ 以转化率计量） |
| 6 | 工程师把 Kong 配置里久经沙场的 0.2 抄进 Portkey，"让缓存行为保持一致" | 查单位和方向 | Kong 的 0.2 是**距离**（严），Portkey 的 0.2 是**相似度**（几乎贴地板）。没有放松，是**反转了含义**。两问：相似度还是距离？哪个方向更严？ |

---

## 五、专著（CacheCraft）里讲义没展开的增量

讲义是 72 页的五幕剧；专著是 91 页的报告，扉页写"first draft, August 21, 2026"。以下是专著独有、明天课上大概不会细讲但对项目有用的部分。

### 1. 三十年血统：1996 年语义缓存是一个**定理**

数据库文献里的 semantic caching（Dar et al., VLDB 1996）存的是**查询谓词 + 结果**：缓存知道自己装着"salary > 80,000 的员工"，来了"salary > 100,000"就能**证明包含关系**，从缓存回答，只把余量查询发去服务器。**等价性是可判定的，命中是一小段逻辑。**

LLM 时代保留了名字，把逻辑换成了几何——包含关系变成了余弦邻近。**这次替换是现代缓存之所以通用的原因（无 schema、无谓词语言、任何自然语言问题），也是原罪：邻近不是包含。** "Basel III capital requirements" 和 "Basel IV capital requirements" 在任何通用 embedding 空间里只隔一口气，却要求不同答案；1996 的缓存永远不可能搞混（因为不存在包含证明），2023 的缓存**默认就会搞混**，除非 $E$ 或 $\tau$ 被专门教过。

> 整份报告一句话：**我们用一个定理换了一个赌注，赌注让缓存变得通用，然后这个领域花了三年学着诚实地给赌注定价。**

时间线：`1996 定理 → 2023 GPTCache 换成赌注 → 2024 服务商 prefix 浪潮吃掉容易的钱 → 2025 vCache 给赌注定价 → 2026 CacheAttack 对手到场`

### 2. 五层缓存（RAG 课 Session 9 的定位图只画了一个阀门，专著数出五个）

```text
Query → Transform → Retrieve → Assemble → Generate → Answer
                                                       ①答案（前门）
                              ②检索到的文档集
                                        ③中间产物（摘要）
        ⑤理解（intent / plan）
                              ④chunk KV 状态（服务层——不同账本，虚线以下）
```

| 层 | 省什么 | 会不会错 | 失效难度 | 备注 |
| --- | --- | --- | --- | --- |
| ① 答案 | 最多 | **会** | 最难 | RAG 命中率最低（15–25%），因为 RAG 查询天生长尾。病理：**把生成冻结在一个移动的索引上**——重切片/改政策/换生成器之后，每个旧答案都是一具自信的化石 |
| ② 检索集 | 中（检索延迟、向量库负载） | **不会** | **精确**（文档版本变 → 含该 ID 的缓存集全死，按索引查而非语义猜） | **几乎没人发货、更多团队该用的那个**。存 ID 和分数不存散文，条目很小；偏斜负载上砍掉 77.2% 的向量库查询而答案全部保持最新。**给风险厌恶的团队先教这一层：这是把危险切掉的那版教学架构** |
| ③ 中间产物 | 标准 QA benchmark 上省 50–60% 冗余计算 | 退化不致命 | 温和 | **artifact 越粗，复用越广、staleness 越安全**。被编辑弄旧的摘要会让答案退化；被弄旧的最终答案**本身就是**退化 |
| ④ chunk KV | 服务层计算 | 只会"擦伤" | — | **不同高度、不同账本，永不混用**（专著把讲义读物里把 CacheBlend 当语义缓存作品的引用列为勘误） |
| ⑤ 理解 | 最深的赌注 | schema 存在时可判定 | — | Instacart 的引擎缓存**查询理解**（98% 头部的解析后 intent 离线预计算），答案保持实时。**它缓存的是重复真正保证的那一个 artifact：意思** |

### 3. 第六层：Governed Layer（缓存之上的缓存）——本周材料和 Week 09 的正式接榫

专著说：这一节是 2026 年 8 月中的修订版才加进来的，因为 OKF 那份规范当时只有八周大。

> 规范里从没出现 cache 这个词。但用缓存的眼睛读，**整个设计就是一个缓存论证**：OKF 把智力从**查询时**搬到**撰写时**——昂贵的理解行为在评审下执行一次，然后被服务很多次。**一个被治理的 concept 文件就是被缓存的理解。**
>
> Part I 的立身经济学"最便宜的检索是那次没跑的检索"于是有了一个兄长：**最便宜的理解，是在问题到达之前就已经完成的那次理解。**

- 五层全都在**查询时**缓存、按查询做键；治理层按 **concept** 做键、由**作者**而非流水线写、在服务前被**评审**而不是服务后被验证。它不是第六个阀门，它坐在整条流水线的**上游**，在语料里。
- `stale_after` 修正了"我们最老的时钟"：TTL 是相对时钟、写入时启动、由操作者猜挥发性；`stale_after` 是**绝对日期，由知道这个事实保质期的作者盖上**——定价政策随财年过期，而不是"某人恰好缓存了一个相关问题之后 n 秒"。**知识在这个设计里像牛奶一样变质，不像酒：纸盒上印的是日期，不是倒计时。**
- **Principle 0.5（信任必须穿过缓存）**：从治理知识派生的缓存答案必须带上 provenance 反向指针；每个被引用 concept 的 tier / status / expiry 都必须在服务时**从活的 bundle 重新推导**，绝不信条目里存的那份。**一个把档案剥掉的缓存，会在五毫秒内把一份草稿洗成一个权威**（provenance laundering，比 accuracy-frequency laundering 更糟）。
- 于是关卡长出第五道闸：**provenance-tier identity**——任何被引用的 concept 若已 deprecated、已过 `stale_after`、或现在推导出比铸造时更低的 tier，拒绝服务。好处是**第一层拿到了第二层的美德**：一个 concept 过期，所有引用它的缓存答案按 ID 查找精确死亡。
- 诚实的尾注：五层用算力计价，治理层用**merge 处的持续人类注意力**计价——这是杀死过此前每一个知识工程倡议的那种货币。赌注（OKFcraft 提出但不肯结算）是 agent 改变了策展的经济学：机器巡逻过期队列、重核来源、起草刷新 diff，人类只在需要判断的地方裁决。**截至撰写时没有任何生产部署发表过复盘，这个赌注还开着。**
- 漂亮的对称：**缓存的前提是重复；策展是提前注意到的重复**——分布的头部从查询时缓存搬进了语料，在任何人提问之前就被理解过一次。而**侦察问题早就被本报告自己的机器解决了**：near-miss mine 那条带（组织里"几乎重复"的问题浓缩处）本来是缓存的第二份薪水（$E$ 的 hard negatives、agent 的技能候选），现在付第三份：**治理层的 concept 候选**。

### 4. Agent 部分的三次"改变可缓存单位"

- 经典语义缓存指向 agent 流量，在文献的合成 agent 任务负载上命中率 **3%**——而且其中一些命中是危险的那种。
- **Principle 0.6（对动作，等价性必须被判定，不能被打分）**：$p=0.98$ 的答案是一个好赌注；$p=0.98$ 的动作是 **2% 的事故率**。"check my email" 和 "send an email" 是余弦邻居、操作上的反义词；反转意义的动词几乎不动 embedding（check/send、enable/disable、buy/sell），改变一切的参数在语义上不可见（$100 vs $100,000），而真正等价的命令可能一个字都不共享（"clear my afternoon" vs "cancel today's meetings after 1pm"）。
- 三级递进：**canonical intent 键**（W5H2；few-shot 微调小模型 **91.1% / 2–5ms** vs 20B 通用模型 **68.8% / 3.4s**——"要的是一致性，不是智力"；五级 cascade 本地解决 85% 交互）→ **plan cache** → **state key**（当状态本身就是要点时）。

### 5. 一个公开的空白 = 现成的 capstone

> **负缓存（negative caching）**。以上所有处理都在缓存成功；**没有人对"缓存缺席"有一套有原则的处理**——检索不到东西的查询、系统正当拒答的问题、miss 本身（好让缓存停止反复探测自己已知的空洞）。经典系统把负查找缓存当家常便饭；语义版本——一个被缓存的"我们不知道"必须在语料学会答案时以某种方式过期——**截至撰写时没有值得引用的文献。一个 capstone 大小、形状还挺趁手的洞。**

### 6. Rhyme Ledger（专著 PDF p.76 / 印刷 p.72）——如果上周是 MemoryCraft/SkillCraft，这张表就是上周的目录

| 本卷 | 同门 | 韵在哪里 |
| --- | --- | --- |
| $VoS = pg-(1-p)L-\kappa$ | SkillCraft 的 VoL；MemoryCraft 的 VoR | 一法三门；$(1-p)L$ 是缓存的签名项 |
| Error Contract（proposal + gate） | GEPA validator；skill governor；memory governor | 本课程"同一个架构"的**第四次**出现 |
| Scoped Cache | RetrievalCraft 的 cabinet；**MemoryCraft 的 partition interlude** | scope 作为对操作的访问控制；**结构胜过检查** |
| 两个高度（答案 vs KV） | **MemoryCraft 的 message-level vs KV-level 驱逐** | 账本永不混用；这条戒律的**第三次**出现 |
| 替换正典，修订 | **MemoryCraft 的 cache canon（Bélady、LRU/LFU/ARC）** | 近似命中打破了地面规则；正典只撑得住一个高度 |
| Aperture doctrine，晋升 | RetrievalCraft Part II；**微调课的 Lévy 边注**；LLM 课的几何周 | 一个定理，三门课，现在有了一个正典陈述 + 三种沉默被命名 |
| Near-Miss Mine | 教学章节的诊断镜；**SkillCraft 的 promotion pipeline** | 缓存作为苗圃：给 $E$ 的 hard negatives，给 agent 的 skills |
| Governed layer；信任穿过缓存 | **OKFcraft** 的 tiers（derived, never stored）、`stale_after` | 层五之上的"被缓存的理解"；命中要带着自己的档案 |

---

## 六、课堂上要提的问题（按优先级）

1. **上周（8/15）到底讲了什么？**——先把这个补上，其他都好办。
2. **"可行性闸门"（抽样十里有一在 0.85 匹配）该怎么在一个还没有真实流量的系统上跑？** Avaloka 现在没有生产流量分布，是应该拿合成对话先估，还是这个闸门本身就意味着"现在还不该谈缓存"？
3. **per-entry 误差曲线的探索税，在低流量系统上是不是必然不划算？** vCache 的 online learning 要流量密度喂曲线；如果我的条目一辈子只被命中三次，第 3 级阶梯是否退化成第 1 级？有没有"冷启动条目"的推荐做法？
4. **Evidence Gauntlet 的第四道闸（lexical support）具体怎么实现？** "关键声明在新证据里仍被支持"听起来就是 Week 08 的 claim-level entailment，只是跑在命中路径上。是同一套机器吗？延迟预算怎么分？
5. **治理层 + 前门的组合里，那第五道 provenance-tier 闸门，谁来维护"活 bundle"的读取？** 每次命中都去读 git bundle 的 frontmatter，会不会把 5ms 变成 50ms？有没有一个"tier 索引"式的中间层，同时不违反 derived-never-stored？
6. **负缓存真的没有文献吗？** 如果是，一个"被缓存的弃权（cached abstention）"在什么条件下可以安全过期——是否必须绑定语料的 index 版本，从而退化成 Version Pin？
7. **对 agent，plan cache 的晋升门槛怎么设？** "长期赢家晋升进技能库"——赢家的判据是成功率、还是 $VoS$ 式的定价？
8. **各向异性让 cosine 数值不可移植**，那阈值之塔的问题在自建系统里怎么根治——是不是所有阈值都必须以"该 embedder + 该语料上的分位数"而不是绝对 cosine 来表达？

---

## 七、对 Avaloka 的直接影响

Week 01 的笔记里已经埋过一条边界（`../week_01/week-01.zh.md` 第 642 行）：

> **Avaloka 边界**：不能跨用户语义复用个性化回答。涉及私有记忆、情绪状态、危机风险、健康背景或变化中用户情况的回答，应绕过共享回应缓存。需要缓存时，应先从公共、稳定知识的检索缓存开始。

本周材料证明这条边界写对了，但**理由比当时写的更强，且措辞需要升级**：

| Week 01 的写法 | 本周之后该改成什么 |
| --- | --- |
| "不能跨用户语义复用个性化回答"（策略性表述） | **per-user scope 键必须写在缓存键内部**——不是一条规则，是结构。Interlude Quiz 4：检查只是禁止泄漏，scoped 键让泄漏不可能 |
| "需要缓存时，应先从公共、稳定知识的**检索缓存**开始" | ✅ 这句极其正确——正是专著的**第二层（检索集缓存）**，"把危险切掉的那版教学架构"。可以直接升级成"Avaloka 默认只做第二层" |
| 讲师说成熟负载约 90% 查询由缓存服务，"应视为需要测量的假设" | ✅ 谨慎是对的。诚实阶梯：RAG 问答 **15–25%**，agent 工具流量 **5–15%**；90% 那个数是 accuracy-frequency laundering |
| 未提及经济学 | Avaloka 要先跑 $H^{*}=C_{ops}/N(C_{full}-C_{hit})$。以 Avaloka 目前的流量规模，$N$ 小、$C_{ops}$ 相对大，**"不要建"很可能就是正确答案**——先打开服务商 prefix caching |
| 未提及 agent 高度 | Avaloka 是 agent loop。**在 agent 高度，plan cache 是唯一安全的答案邻近缓存**；答案缓存在这里几乎必然错（状态旧得太快 + check/send 式的余弦反义词） |
| 未提及记忆 | 关键区分：**缓存不是记忆**（"memory is about you, not about the question"）。Avaloka Memory Reader 属于记忆，不属于缓存，两者的失效、scope、定价规则不能互相借用 |

**一条现成的、和当前 v0.1 目标直接对齐的收获**：`evals/` 已经在跑 recall@5 / nDCG@5 / MRR，而本周给出了**缺失的那半张仪表盘**——unsafe-served rate 和 P-CHR 曲线。T026（用可答性检查替换词覆盖弃权）本质上就是"$p$ 的估计比相似度更该做决策依据"这条原则的一个实例；$p>L/(g+L)$ 这条不等式可以直接当 T026 的决策规则来写。

---

## 八、要更新的项目文件（课后执行）

| 文件 | 动作 |
| --- | --- |
| `course/00-course-overview.md` | 加 Week 11 链接；补 Week 10 的占位与缺口说明 |
| `tasks/index.md` | 新增 T029「补 Week 10 课堂记录」；新增 T030「Avaloka 缓存决策：先跑 $H^{*}$ 再谈架构」；T026 的决策规则改写成 $p>L/(g+L)$ |
| `evals/` | 仪表盘补两项：unsafe-served rate、P-CHR 曲线（替代 PR-AUC） |
| `docs/decisions/decision-log.md` | 记一条：**Avaloka 不建答案缓存，先做检索集缓存 + 服务商 prefix caching**（若课堂讨论支持） |
| `toolkit/` | 新增方法卡：Scoped Cache、Version Pin、Evidence Gauntlet、Error Contract、Near-Miss Mine |

---

## 九、必读顺序（讲义 p.71，按依赖排序）

1. **Wang & Isola** — alignment and uniformity on the hypersphere
2. **vCache** — verified caching and the error contract（arXiv:2502.03771，ICLR 2026，Berkeley）
3. **GroundedCache** — evidence-grounded freshness
4. **对抗 hubness / cache-attack 文献**（key collision attacks，arXiv:2601.23088，ICML 2026）
5. **CacheCraft** — 全本专著，含极地熊

补充（专著附录 "Further Reading, in Order" 与脚注里值得一读的）：Blum–Hopcroft–Kannan《Foundations of Data Science》Ch.2（annulus theorem 最干净的初等处理）；Dar et al., *Semantic Data Caching and Replacement*, VLDB 1996（那个定理本身）；*Closing the Calibration Gap in Semantic Caching*（P-CHR / CRR）；Krites（异步 judge）；MVR-cache（ICML 2026）。

---

## 十、课后补充 A：把专著按"章"重读一遍（11 章骨架）

前面第三节是按**讲义的五幕剧**组织的。专著自己的分章不同，做 presentation 时用专著的章号更好对齐。两套骨架对照：

| 专著 Part | 中文 | 核心问题 | 对应讲义 | 适合做 presentation？ |
| --- | --- | --- | --- | --- |
| I. Foundations: The Front Door and Its Borders | 基础：前门与它的四条边界 | 语义缓存到底是什么、不是什么 | Prologue | 适合当开场，不适合单独讲 |
| II-A. The Geometry: The Cap and the Equator | 几何：极冠与赤道 | 为什么 cosine 阈值有理论依据 | Act I 前半 | 数学重，但故事漂亮 |
| **II-B. Crowds, Hubs, and the Capacity of the Sphere** | **几何续：拥挤、枢纽与球面容量** | **冠**里面**长什么样** | Act I 后半（讲义只给了三张 slide） | **非常适合**——见下一节 |
| III. The Decision: When the Cap Is Not Enough | 决策：光有冠不够时 | 为什么单一阈值站不住 | Act II | 最强故事线 |
| IV. Implementation: The Modern Lookup Stack | 实现：现代查找栈 | 2026 该怎么真建 | Act III 前半 | 工程向 |
| V. What to Cache in a RAG System | RAG 到底该缓存什么 | 答案不是唯一能缓存的东西 | 讲义几乎没讲 | **非常实用**，见第五节第 2 小节 |
| VI. Caching for Agents | 给 agent 做缓存 | 为什么 agent 不能用答案缓存 | Act III 后半 | 和 Avaloka 最相关 |
| Interlude. The Adversary at the Door | 门口的对手 | 缓存怎么被攻击 | Interlude | 最抓人 |
| VII. Economics | 经济学 | 现在还值不值得做 | Act IV | 结论最硬 |
| VIII. In the Wild | 业界现状 | Redis/Azure/Kong 到底怎么做 | Act V 前半 | 轻松、有梗 |
| IX. Pattern Language & Synthesis | 模式语言与综合 | 最终该怎么设计 | Act V 后半 | 适合当结尾 |

> 讲义（*The Stones in the River*）是把 I–IX 压缩成五幕的**课堂版**；专著是展开版。讲义里被压成一页的东西，专著里往往是一整章——**Part II-B 就是最典型的例子**：讲义 Act I 只用 hub / 各向异性 / 准正交容量三张 slide 带过，专著给了它五节。

---

## 十一、课后补充 B：Part II-B 精读（Crowds, Hubs, and the Capacity of the Sphere）

专著 PDF p.25–31。这一章作者开宗明义："上一章讲的是我教了很多年、这次修好并终于接上阈值的那个故事；**这一章讲的是我没教过的四个故事**"——集中不等式这面镜子只对着冠和赤道，看不见旁边这四件事。四个故事各自终结在一个缓存设计决策上。

### 1. "最近邻还有意义吗"——质疑与救援

**质疑**（Beyer, Goldstein, Ramakrishnan, Shaft，*When Is "Nearest Neighbor" Meaningful?*，ICDT 1999）：在很宽松的条件下，随着维度增长，查询到**最近邻**和到**最远邻**的距离会收敛，相对对比度

$$\frac{D_{\max}-D_{\min}}{D_{\min}}\longrightarrow 0$$

于是"最近邻"渐近地**谁也不是**。作者自己承认：**如果这条定理适用于我们的 embedding，那语义缓存就是一套用很复杂的方法返回任意答案的系统。**（配套结论：Aggarwal–Hinneburg–Keim, ICDT 2001——$L_p$ 范数越高集中得越糟，分数阶范数抵抗最久。）

**救援**：那条定理的前提要求**数据真的填满环境维度**，而真实 embedding 从来不会。存在一条逆定理（Durrant & Kabán, *J. Complexity* 2009）把这件事说精确：**内在维度低的数据逃过这次坍缩**——当数据活在一个远小于容器的结构上时，相对对比度就存活下来。

**实测**：语言模型 embedding 的**内在维度只有几十**，比 768 / 1536 的环境维度低一到两个数量级——**一张意义的流形被折进一个巨大的空容器里**。（Valeriani et al. / Tulchinskii et al., NeurIPS 2023；Bruno et al., *Less is More: Local Intrinsic Dimensions of Contextual Language Models*, NeurIPS 2025, arXiv:2506.01034。估计方法：Levina–Bickel, NeurIPS 2004；Facco et al. TwoNN, Sci. Reports 2017。）

> **两条定理其实说的是同一件事的两半**：集中保证（偶然被歼灭）和意义性质疑（对比被歼灭）**都是关于高维随机性的陈述**；而 embedding 流形既低维又有结构，于是**继承了前者**（对抗随机的赤道世界）**同时逃掉了后者**（在学到的流形内部，对比是真实的）。
>
> 作者的定论：**缓存住在最好的那个象限——被环境维度保护，在内在维度里做区分。**（"The cache lives in the best quadrant: protected by the ambient dimension, discriminating within the intrinsic one."）

**一个带牙齿的诊断工具**：内在维度是**局部**的，随流形位置变化。某点周围的**局部内在维度（LID）**恰好预测缓存运营者关心的三件事——这个点的邻域有多稳定、它的最近邻关系有多可信、以及**它对对抗性接近有多暴露**（对抗区域恰恰就是 LID 异常高的区域，Ma et al., ICLR 2018）。

> **capstone 机会**：Interlude 里那件"熊皮衣"因此获得了一个**几何签名**——碰撞构造出来的 prompt，坐落在一个 LID 可测量地异常的邻域里。**一个逐条目记录 LID 的缓存，就有了一根没人在卖的、廉价的对抗性绊线。**

### 2. Metropolis Effect：微调到底对球面做了什么

作者在这里**公开纠正自己**（"I have caught myself implying it at the board"）。常见叙事是：

```text
预训练编码器各向异性 = 一个窄锥        ✅ 真
微调恢复各向同性                       ✅ 真
所以微调把点摊开                       ❌ 假，而且错在最要紧的地方
```

**降低各向异性不等于一切变得更弥散。** 领域微调真正产生的、理论也说它必须产生的，是一个**全局铺开、局部凝聚**的球面：表面被广泛占据，但被一个个高强度浓缩的口袋刺穿。**球面不会变成均匀气体，它会城市化。**

> **Metropolis Effect（大都会效应）**：近等价意义的紧密、密集**市中心**——"LCR 的定义是什么"的每一种改述都挤在一根汗毛之内——之间隔着这个领域的语义**真的不居住**的**开阔郊野**。

**背后的理论**（专著说这是对比学习里最优雅的结果，值得和 InfoNCE 并列进教学流水线）：对比目标**可证明地分解成两种渐近力**（Wang & Isola, ICML 2020）：

| 力 | 做什么 | 在城市比喻里 |
| --- | --- | --- |
| **Alignment（对齐）** | 正样本对被拉到同一点 | **建起市中心** |
| **Uniformity（均匀性）** | 特征分布被推向球面均匀，形式化为最小化成对高斯核能量 | **把市中心彼此推开** |
| **Temperature（温度）** | 直接支配 uniformity–tolerance 的取舍 | **分区法（zoning law）**：$\sigma$ 低 → 惩罚近邻更狠 → 市中心更紧更分离；$\sigma$ 高 → 容忍语义摊大饼 |

- uniformity 项正是在对抗预训练那个锥（Gao et al. 的 representation degeneration, ICLR 2019）。
- **深挖（专著的 Deep Dive 边注）**：uniformity 项**逐字就是物理**——在球面上最小化成对高斯核能量就是 **Thomson 问题**（点电荷互斥到最大铺开）。于是大都会效应是**微缩版的宇宙结构形成**：alignment 演引力，uniformity 演膨胀压力，微调后的球面最后长得和宇宙一样——**团簇、纤维、空洞**。训练温度不是温度的比喻，**它就是同一个 Boltzmann 因子里的同一个 $\beta^{-1}$**。
- **命名的双关**：球面在城市化，而 **Nicholas Metropolis**——1953 年在 Los Alamos 教会统计力学如何采样这类能量地形的那个人——正从页边微笑。

**对缓存的直接后果**（这一段闭合了决策章开的那个环）：

```text
市中心 = 缓存之乡：密集重复、冠里有人、命中率高
        ↑ 同时也是 hard negative 挤得最近的街区
          （Basel III 紧贴着 Basel IV，同一个市中心的同一个街区）
开阔郊野 = 长尾：没有邻居、没有命中、也没有危险
```

> **阈值的困难度不是均匀分布在球面上的——它恰恰浓缩在流量所在的地方。** 这就是"逐条目重叠测量"这件事的**几何版重述**：
>
> **一个全局 $\tau$，是给 Manhattan 和 Wyoming 用同一套分区法。**

而且这给微调流水线一个比"恢复各向同性"**锐利得多**的目标：缓存想从 $E$ 那里得到的，是**答案不同的市中心之间间距最大化的、彼此分离良好的都会群**——而这正是 curriculum 挖出来的 hard negative 一个街区一个街区在做的事。

### 3. Hubs：不平等的市民

第三个故事是高维邻域一个真正的怪异之处，相似性搜索文献知道了十五年，而**我们这门课几乎从没提过**：

> **邻域不是民主。**（"nearest-neighborhood is not a democracy"）

随着维度增长，"这个点多经常成为别人的最近邻"这个分布变得**剧烈右偏**：一小撮 **hub 贵族**出现在极大比例查询的邻居列表里，而对应的一整类 **antihub 谁的邻居都不是**。而且这**不是坏数据的产物，是集中现象本身的内在后果**——**稍微更靠近数据均值的点，就会稍微更靠近所有人**。（Radovanović, Nanopoulos, Ivanović, *Hubs in Space*, JMLR 11:2487–2531, 2010。现代句向量空间上的测量与缓解：Nielsen, Sandholt, Hansen, NLDL 2024, arXiv:2311.18364——**hubness 降低约 75%，错误降低约 9%**，SBERT 级空间。）

**对语义缓存，这不是趣闻，是一个此前没有名字的失败模式**：

> 一个 hub 缓存条目是一台 **false-hit magnet（误命中磁铁）**：它坐在来自球面各处查询的检索路径上，赢下它根本没资格参加的最近邻竞赛，而且——**因为它一直被端出去**——在命中率仪表盘上看起来像整个缓存**最成功的那位市民**。

**诊断**：教过的 near-miss mining 最终会浮出它的**受害者**；而 hubness 文献说你可以直接找到**元凶**——**审计逐条目的 serve-count 分布，把极端右尾的条目当成几何嫌疑人，而不是成功案例。**

```text
Entry A   1,200
Entry B   1,500
Entry C     980
Entry D   1,100
Entry X 185,000   ← 不是英雄，是嫌疑人
```

**治疗**：**CSLS** 是一个可以直接插进去的修正——**用候选自身邻域的平均相似度去惩罚它的相似度，让"到处留情"的点为自己的人缘付费**。它本来是为跨语言检索里的同一个病理造的（Conneau et al., ICLR 2018），**逐字迁移到缓存匹配**。（年长的兄弟：Schnitzer et al., *Mutual Proximity*, JMLR 2012。两者都是相似度重标定，都能和决策章的一切组合。）

> **一个意外的韵脚（专著边注）**：CSLS 是**对全局相似度做的逐条目修正**，从每个点自己的邻域学出来。**它是 per-entry 阈值的廉价静态表亲**——这个领域**隔了十年，两次独立地发现：一个数字治不了所有街区。**

**而这个故事刚刚有了对手**：**对抗性 hubness**——攻击者精心构造**单独一个点**，让它成为一个 hub、一个被数百万条不相关查询检索到的**通用最近邻**。对基于 embedding 的检索来说，这是一个和"一次一个受害者"的碰撞攻击**完全不同量级**的投毒放大器：**植入一个条目，端给所有人。**（Zhang, Suya, Jha, Zhang, Shmatikov, *Adversarial Hubness in Multi-Modal Retrieval*, IEEE S&P 2026, arXiv:2412.14113。）

> 熊皮衣是**一个冠里的一个冒名者**；对抗性 hub 是**一个竞选成为所有人邻居的冒名者**。同样的几何，更大的杀伤半径，同样的结论：**局部性就是权力，而权力招引攻击者。**
>
> 防守也押韵：scoping 缩小 hub 能触及的观众，verification 抓住它端出的胡话，而 **CSLS + serve-count 审计**作为 hub 专属绊线加入工具箱。

### 4. 球面的容量

最后一个故事回答一个基本到很少被问的问题：**球面上到底装得下多少个可区分的意义？**

如果答案是"大约 $d$ 个"——一维一个——那 768 维就是一个拥挤的文件柜，近乎相同的意义**被迫共用地址**。真相更奇怪：

| 要求 | 容量 |
| --- | --- |
| **严格正交**（真正 90°） | 约 $d$ 个地址 |
| **$\varepsilon$-近正交**（两两 cosine 低于某个小 $\varepsilon$） | $e^{c\varepsilon^{2}d}$ 个地址——**维度的指数** |

**把正交性放松一根汗毛，地址簿就爆炸。**（Kabatjanskii–Levenstein 界；Tao 2013 的"廉价版 K–L 界"讲法最干净；Vershynin, *HDP* 2018 §3.3；Cai, Fan, Jiang, JMLR 2013。）

> 这是一句值得刻下来的直觉的**精确版本**：**指数级的是球面的地址簿，不是它的维度。**（"it is the sphere's address book, not its dimension, that is exponential"）
>
> $d=768$ 时这个数是天文数字——**每一个用户将来会问的每一个问题，都有自己的地址，哪怕它们的语义几乎相同。点会叠在一起，只因为编码器把它们放在了那里。**

这就是可解释性领域重新发现的那同一套数学：**superposition**——网络通过给特征分配近正交方向，存下远多于维度数的特征（Elhage et al., *Toy Models of Superposition*, 2022, arXiv:2209.10652）。

**对缓存，容量定理以审计般的终局性解决了一个归责问题**：

> **碰撞从来不是容量问题。** 当 Basel III 和 Basel IV 坐在 cosine 0.96 时，**球面没有用完空间——它们之间站着指数级多的空地址**。它们的接近是**编码器训练数据做出的一个选择，而且是可撤销的**：实现章那条微调流水线（Basel 相似度经领域微调从 **0.96 掉到 0.72**）在这个视角下，就是**把两个被错误分配到同一个地址的租客，搬进球面一直为他们准备着的独立住所**。

容量定理同时也是大都会图景的**幕后担保人**：市中心可以任意密集且内部可区分，**因为哪怕在一个很紧的冠里，也还有指数级多的子地址。密度限制的是编码器的分辨率，从来不是球面的。**

### 5. Aperture Doctrine 完成

四个故事其实是一个故事：

```text
上一章的定理  → 建起对抗偶然的墙：没有东西是意外进入冠的
这一章        → 勘察墙内的城市
  内在维度    → 流形在容器里很小，所以对比存活、最近邻有意义
  大都会效应  → 微调不是把城市摊平，是把城市建起来
                （alignment 打包、uniformity 分隔、temperature 分区）
  Hubness     → 城市有贵族，需要逐街区修正；而且现在有对手在竞选加入
  容量        → 城市永远不会用完地址，只会用完编码器的分辨率
```

决策章的每一条结论都能从这张地理图**重新推出来**：

- **per-entry 阈值**，因为**分区是局部的**
- **校准**，因为**市中心各不相同**
- **verification**，因为**贵族会撒谎**
- **scoping**，因为**冒名者会竞选**

> **上一章用统计学的语言把阈值从一个数字晋升成一条策略；这一章用球面的语言说同一件事：**
>
> **一座城市不可能靠一条规则治理；缓存是这座城市的守门人，不是它的测地员。**（"a city is not governed by a single rule, and the cache is the city's gatekeeper, not its geometer."）

---

## 十二、课后补充 C：四种 cache 的机制补课

第三节第 2 小节那张"四种被叫做 caching 的东西"表，只给了结论。这里补上机制，因为讲 Part I 时一定会被问。

### 1. KV cache：复用 attention 计算

Transformer 每层 attention 里，每个 token 生成三组向量：

$$Q = XW_Q,\quad K = XW_K,\quad V = XW_V,\qquad \text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^{\top}}{\sqrt d}\right)V$$

直观理解：**Q = 我现在在找什么；K = 过去每个 token 挂出的标签；V = 真正关注它时拿到的信息。**

自回归（autoregressive）生成是一个 token 接一个 token 地做 $P(\text{next}\mid\text{previous})$。生成第 $n{+}1$ 个 token 时，**只需要算这个新 token 的 Q/K/V**，让它的 Q 去和之前保存好的 $n$ 个 K 做 attention、读取对应的 V；**过去那 $n$ 个 K/V 不必重算**，算完把新的 K/V 追加进 cache。

```text
Token 1 → 存 K1,V1
Token 2 → 复用 K1,V1，只算 K2,V2
Token 3 → 复用 K1,K2 / V1,V2，只算 K3,V3
...
```

比喻：开会记笔记。没有 KV cache = 每听到一句新话就从会议第一分钟重听一遍；有 KV cache = 前面已整理成内部笔记，新话只需结合笔记理解。**缓存的不是文字、不是答案，是 attention 的中间张量。**

### 2. Provider prefix caching：把 KV 复用跨到不同 request

普通 KV cache 是**同一次生成过程内部**复用。服务商的 prefix caching 更进一步：**不同 request 之间，只要前缀 token 完全相同，也复用之前 prefill 算好的 KV**。

```text
Request 1: [ 5000-token system prompt ][ Question A ]
             ↑ prefill：算这 5000 个 token 每层的 K/V

Request 2: [ 5000-token system prompt ][ Question B ]
             └──────── 完全相同的前缀 ────────┘
             ↑ 直接复用缓存的 KV，只算新增后缀
```

三个必须讲清的点：

1. **要求精确 token 匹配。** "You are a helpful AI assistant." vs "You are a **very** helpful AI assistant." 人看几乎一样，但 token 序列变了 → 不复用。**它不会说"意思差不多，算了我复用"**——这正是它和语义缓存的分界。
2. **它不缓存答案。** 同一个 system prompt 下问 "2+2" 和 "10+10"，prefix cache 绝不会返回 4；它只是省掉重复前缀的 prefill，答案照样重新生成。专著原话：**"Prefix caching makes computing the answer cheaper; it never avoids computing it."**
3. **所以它零正确性风险**，miss 的代价只是付全价。适合长 system prompt、tool/MCP schema、few-shot 例子、共享 RAG 文档。

### 3. Embedding cache：精确字符串 → 向量

```text
Key:   "How do I reset my password?"          （原始文本，精确匹配）
Value: [0.12, -0.43, 0.77, ..., 0.08]         （算好的向量）
```

同一段文字再来 → 直接返回向量，embedding 模型不必运行。但把 "How **do** I…" 换成 "How **can** I…"，对它就是 **MISS**——它不问两个向量近不近，**只问原始文本一不一样**。因此它是**纯成本优化、零正确性风险**：最坏情况只是多算一次 embedding。专著的挖苦：把这个叫"语义缓存"，**就像把文件柜叫图书馆员**。

### 4. 三者在流水线上的位置

```text
User Query
   ↓
┌────────────────────────────┐
│ Embedding Cache            │  精确文本 → 向量（省 embedding 调用）
└────────────────────────────┘
   ↓ embedding
┌────────────────────────────┐
│ Semantic Cache             │  相似向量 → 过去的成品答案（唯一会错的那个）
└────────────────────────────┘
   ↓ miss 才继续
Retrieve → Assemble → Generate
                        ↑
              ┌──────────────────────┐
              │ Prefix / KV Cache    │  相同 token 前缀 → 复用 attention 计算
              └──────────────────────┘
```

一句话收束：**KV / prefix / embedding 缓存的是"计算"，语义缓存缓存的是"答案"；前三者失败退化成延迟，只有第四者会在 5 毫秒内自信地给你一个错的答案。**

---

## 十三、本周产出与下一步

**已产出**：Part II-B（*Crowds, Hubs, and the Capacity of the Sphere*）的英文 presentation，8 张 slide，主线为

```text
高维悖论（nearest ≈ farthest？）
  → 内在维度救援（真实 embedding 不填满容器）
  → 大都会效应（微调建城，不是摊平）
  → 为什么一个全局阈值不行（Manhattan ≠ Wyoming）
  → Hubness（最受欢迎的条目可能最危险）
  → 球面容量（碰撞是编码器的锅，不是维度的锅）
  → 结论：一座城市不能靠一条规则治理
```

讲 10–15 分钟时，时间应压在**内在维度 → 大都会效应 → Hubness → 为什么全局阈值失败**这四点上；球面容量一分钟讲完即可——它的作用是**归责**（把锅从维度转到编码器），不需要展开。

**仍然缺的**：

1. **Week 10（8/15）的课堂记录**——见第一节，这是本周之后最优先要补的一件事。
2. **本周的现场实录**——这份笔记完全建立在两份 PDF 和课后精读上，课堂讨论、答疑、Lab 部分尚未记录。
3. **本周的 eval artifact**——照 `PROJECT_PLAN.md` 的操作节奏，每周应该产出/更新至少一条 eval case；本周对应的是第八节表格里 `evals/` 那两项（unsafe-served rate、P-CHR）。

---

## 十四、一句话总结

> 前十周都在优化"模型看见什么"；本周优化的是**根本没有窗口被打开的那些情况**——语义缓存是整个架构里唯一一个"成功以从未发生的前向传播来衡量"的器官。而它也是唯一一个会**错**的缓存，所以它必须同时是四样东西：一个几何论证（命中都是有原因的）、一个可证实的误差契约（不是一个阈值）、一个结构化的 scope（不是一次检查）、和一张必须先算清的账（"不要建"是一个骄傲的判决）。
