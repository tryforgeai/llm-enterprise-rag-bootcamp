# 第 07 周课堂笔记

日期：2026-07-25

状态：课前讲义（PDF 四幕 + 插曲 + 评估地图）已读完并整理成课前预习骨架；现场讨论细节、8 个 Lab 的动手实现、以及本周 eval artifact 待课后补充

来源：`course/week_07/summer-week-7-lesson-plan.pdf`（*The Measure of All Things — Evaluating RAG Systems from Retrieval to Reasoning*，Asif Qamar，首稿 2026-07-18）

## 课堂截图：标题幻灯片（现场版本）

现场"Evaluation Day"标题页（*The Measure of All Things · Evaluating RAG Systems from Retrieval to Reasoning*）用了一句比 PDF 的"A Gentle Re-Entry"更凝练的副标题，值得单独记录：

> *"Six weeks of building the library, the map, and the gates. Today we stop building — and start measuring."*（六周里建了图书馆、地图和闸门。今天我们停止建造——开始测量。）

这句把前六周精确对应到三个隐喻：**图书馆**（Week 1–4，语料/检索/派生工件）、**地图**（Week 5，GraphRAG 把语料变成有结构的城市）、**闸门**（Week 6，两道门）。眉标注明这是"ADVANCED COURSE"。

## 课堂截图：Map of the Day（现场议程）

现场"THE MAP OF THE DAY · Today's learning journey"用一条起伏的旅程曲线给出六段结构，与 PDF 目录基本一致但有两处命名差异（下面正文仍按 PDF 标题组织）：

```text
Act I     — The Yardstick（标尺，起点，谷底）
Act II    — The Staircase（阶梯，第一个峰）
Interlude — Signal & Noise（信号与噪声，回落谷底；PDF 作 "Signal from Noise"）
Act III   — The Generator（生成器，第二个峰；PDF 标题是 "Beyond Retrieval—Measuring Generation and Faithfulness"，现场直接叫 The Generator）
Act IV    — The Frontier（前沿，回落谷底）
Coda      — The Evaluation Map（评估地图，最后一个峰后插旗收尾；PDF 里叫 "Connecting Everything: The Evaluation Map"，现场把它提升为独立的 Coda）
```

两处值得记的差异：① **Act III 现场简称"The Generator"**——强调这一幕是从"检索侧"转向"生成器本身"的评估；② **Evaluation Map 被提升为 Coda**（尾声），呼应上周 Week 06 也用 Coda 收尾的结构习惯，说明"把指标接回每一周组件"是讲师刻意安排的压轴环节，不是附录。曲线形状本身也是一个隐喻：测量之旅在"标尺→阶梯→生成器→评估地图"四个峰之间起伏，每个 Interlude/Frontier 谷底是难度或抽象度的回落再爬升。（在场 9 人，讲师 Asif Qamar。）

## 课堂截图：Prologue · The Ruler（现场版本）

现场用一张 "mm"（毫米，最小刻度）配同心圆刻度环的视觉开场，标题 **"The Ruler"**（尺子），副标题：

> *"You cannot measure without a yardstick — and the yardstick is yours to build, not someone else's."*（没有尺子就无法测量——而这把尺子得由你自己造，不是别人的。）

这句是 Act I "The Yardstick" 的现场浓缩，且把 PDF 里两个论点合成一句：① **没有 ground truth 就没有测量**（尺子 = 金数据集）；② **"yours to build, not someone else's"** = PDF 的 "Against the Borrowing of Public Benchmarks" + "Whose Job Is Evaluation?"——公共基准（BEIR/MTEB）不能替代你自己领域的 EVAL 集，评估是 AI 工程师自己的活。视觉上"mm"刻度呼应本周主题"万物的尺度"：先定义刻度，才能谈大小。

## 课堂截图：Prologue · A Debt Incurred Over Six Weeks（现场版本）

标题 **"Six weeks of building — one question never asked"**（建了六周,一个问题从没问过）。这是把六周历程用一句话回顾,再点出欠下的"债":

> Meaning became geometry, decisions took shape, thoughts were chunked, understudies stood in, the library became a city, and last week we hung **two gates** on the door.
> We never rigorously asked: **does any of it work?** Did we retrieve the **right** things? In the right order? Is the answer **faithful** to them?

这段用了每一周的关键词回指:*meaning became geometry*(W1–2 几何)、*decisions took shape*(W1 The Shape of a Decision)、*thoughts were chunked*(W3 chunking)、*understudies stood in*(W4 The Understudy 派生工件)、*the library became a city*(W5 GraphRAG)、*two gates*(W6 两道门)。三个追问正好对应本周三条评估主线:**检索对不对**(Recall/Precision)、**顺序对不对**(MRR/nDCG 排序感知)、**答案忠不忠于证据**(faithfulness/FActScore)。

右侧边注是本周的方法论定调:

> *"Measurement is not a final act. It is the foundation every prior week has been resting on, **unexamined**. Today we make it explicit."*（测量不是收尾动作,而是前每一周都一直**未经检验**地依赖着的地基。今天我们把它显式化。）

这句直接反驳"评估是流水线最后一步"的常见误解——评估其实是一直在底下支撑却没人回头审视的地基,呼应 Week 01 就把 evaluation 画进流水线主环(而非可选终检)的立场。

## 课堂截图：Prologue · Two Epigraphs, One Tension（现场版本）

标题 **"Kelvin — and his corrective"**（开尔文——以及对他的纠偏）。用两句题词框住本周的核心张力:

> *"When you can measure what you are speaking about and express it in numbers, you know something about it; but when you cannot measure it, your knowledge is of a meagre and unsatisfactory kind."* —— Lord Kelvin, 1883（能测量并用数字表达,才算真懂;测不了,你的知识就贫乏而不令人满意。）

> *"Not everything that counts can be counted, and not everything that can be counted counts."* —— William Bruce Cameron, 1963（不是所有重要的都能被计数,也不是所有能被计数的都重要。）

现场定调:**"Hold both. Today is Kelvin's day — but Cameron stands behind him all day, warning us about Goodhart."**(两句都要握住。今天是开尔文的主场——但卡梅隆整天站在他背后,提醒我们提防 Goodhart。)

这一页把本周从头到尾的辩证提前埋好:**Kelvin = 测量的正面理由**(你无法改进你无法测量的东西,支撑 Act I–III 造尺子、算指标);**Cameron = 对测量的纠偏**,直接连到 **Act IV 前沿 5 的 Goodhart 定律**(当测量变成目标,它就不再是好测量;RAG 里表现为只优化 faithfulness 就过度对冲、只优化 citation recall 就过度引用)。两句 PDF 扉页就并置,现场明确点出它们不是装饰,而是全天要同时握住的两只手——既要量化,又要警惕"可量化"绑架了"真正重要"。

## 课堂截图：Prologue · A Pattern Watched for Twenty Years（现场版本）

标题 **"Evaluation? That's QA's job"**（评估?那是 QA 的活）——引号里是要被打破的错误认知,眉标"一个观察了二十年的模式":

> Ask a room of engineers what they associate with **evaluation**: testing, handoffs, someone else's concern — downstream of the real work, which is shipping code.
> Teams of senior engineers nod through this exact lecture, build RAG systems for months, then confess with genuine surprise: **no gold dataset ever got built.**

这是 PDF Act I "Whose Job Is Evaluation?" 的现场加强版,点名一个真实且顽固的组织病:工程师把评估当成 QA/下游的事、真正的活是"发代码",于是花几个月建 RAG,却坦白**从没建过金数据集**。呼应本周立场——**评估是 AI 工程师自己的关切,不是外包**(也是 Prologue "yours to build, not someone else's" 的另一面)。

右侧边注给了一个记忆隐喻:

> *"The formulas do not leak out of heads because people are lazy. They leak because they were filed in the mental cabinet marked **someone else's concern** — and **that cabinet leaks**. Fix the drawer, and the concepts stay."*（公式从脑子里漏掉不是因为人懒,而是因为它们被归档进了"别人的事"那个抽屉——那个抽屉会漏。修好抽屉,概念自然留得住。）

意思是:知识留不住往往不是记性问题,而是**心理归类**问题——一旦把评估贴上"别人负责"的标签,相关知识就存不进长期记忆。把归类改成"我的职责",概念自然就留住了。对我的 project 有直接启示:Avaloka 的 eval 不能等外部,得由建系统的人自己拥有。

## 课堂截图：Prologue · Why the Old Mental Model Fails Here（现场版本）

标题 **"An AI system has no clean pass/fail"**（AI 系统没有干净的通过/失败）——解释为什么把传统软件测试的心智模型套到 AI 上会失效:

> **确定性软件**:same input, same output;QA 写断言,CI 跑出红或绿。（可以二元 pass/fail。）
> **AI 系统**:返回的是**一个答案质量的分布**,对着**一个查询的分布**——而且两个分布都在你脚下漂移:模型版本、prompt、随机解码(stochastic decoding)、语料增长。

核心对比:传统软件同输入同输出,所以能写"对/错"断言让 CI 判红绿;AI 系统同一个 query 每次质量可能不同(分布),面对的 query 也是一整个分布,再加上四种漂移源,**根本没有一条干净的通过线**。这就是为什么评估不能靠 CI 的断言,而要靠指标 + 统计显著性 + 持续测量——也解释了 Act I 为什么强调 eval decay(分布漂移会让评估集过时)。

右侧边注是本周最硬的立场句:

> *"A bridge engineer does not hand off load-testing — the load curves **are** the design. The metrics you choose shape the system you build. Evaluation is not downstream of AI engineering. **Evaluation is AI engineering.**"*（造桥工程师不会把载荷测试外包出去——载荷曲线**就是**设计本身。你选的指标塑造你建的系统。评估不是 AI 工程的下游,**评估就是 AI 工程**。）

"你选的指标塑造你建的系统"直接呼应优化目标 argmax_θ E[μ(q,θ)]:μ(指标)一旦选定,θ(整个系统)就朝它优化——所以选错指标 = 建错系统,这也是为什么 Goodhart 那么危险。这页把 Prologue 的三张"评估归属"幻灯片(QA 的活 / 抽屉会漏 / 没有 pass-fail)推到结论:**评估就是 AI 工程本身**,不是附属环节。

## 课堂截图：Prologue · What Serious Projects Actually Spend（现场版本）

标题 **"The 80/20 of real AI work"**（真实 AI 工作的 80/20）——用投入比例反驳"架构/模型才是重点"的直觉:

> Every serious AI project: **80%** of the effort on clean data, demonstrations, and the yardstick; **20%** on the fashionable part — architecture, algorithm, model.
> At Cornerstone — 100 million learning objects, 7,000 clients — the architecture was clear in the first meeting. The months went into **40 SMEs, 2 days each, a 10,000-query gold dataset.**

核心数字与案例:严肃 AI 项目 **80% 的精力花在干净数据、演示、和尺子(评估集)上,只有 20% 花在时髦的架构/算法/模型上**。Cornerstone 案例(1 亿学习对象、7000 客户)——架构第一次会就定了,真正吃掉几个月的是 **40 位 SME × 每人 2 天,建一个 1 万条 query 的金数据集**。这给 Act I 的"目标 1000 条"提供了一个大厂级的上限参照(1 万条),也印证 SME Summit 方法的现实成本。

右侧边注给了"评估方法论是真的"的最佳信号:

> *"When hybrid search launched, one big client was **furious**: why does it work now, after years of complaints? There is no better sign that your evaluation methodology is real than an angry client who finally sees the improvement."*（混合检索上线时,一个大客户很**愤怒**:为什么抱怨了几年、现在突然就好用了?没有比一个终于看到改进的愤怒客户更能证明你的评估方法论是真实有效的了。）

这个反直觉的观察很值:客户"愤怒"恰恰是好信号——说明改进是**可感知、可归因**的真实提升,而不是自说自话的指标数字。呼应本周主线:评估要能连回真实体验(end-to-end 的 satisfaction),不能只停在离线指标。对我的启示:Avaloka 的评估集也该按"80% 精力在数据和尺子"来分配,而不是急着上 RAPTOR/GraphRAG(正好对接"证据驱动架构升级"决策)。

## 课堂截图：Prologue · Every Knob, One Equation（现场版本）

标题 **"The optimisation goal"**（优化目标）——把整周要做的事压缩成一个公式:

> Let **θ** be **every** knob — chunk size, embedder, retrieval mix, reranker, prompt, temperature — and **μ(q,θ)** a metric of goodness on query q:

$$\arg\max_{\theta}\ \mathbb{E}_{q\sim\mathcal{Q}}\big[\mu(q,\theta)\big]$$

> The configuration that maximises expected goodness over your **own** query distribution 𝒬 — not someone else's benchmark.

三个符号:**θ = 每一个旋钮**(chunk 大小、embedder、检索混合、reranker、prompt、温度——整条流水线的全部可调项,不只是模型超参);**μ(q,θ) = 在 query q 上的"好坏"指标**;**𝒬 = 你自己的查询分布**。目标 = 找一组配置 θ,让"好坏"在你自己的 𝒬 上的**期望**最大——注意是**你自己的分布,不是别人的公共基准**(再次呼应 "yours to build" 与反对借用公共 benchmark)。

右侧边注:

> *"Same framing as hyperparameter tuning — but θ is far richer, so systematic measurement matters far more."*（和超参调优是同一个框架——但 θ 丰富得多,所以系统化测量重要得多。）

这句点破为什么这不是"套个公式装样子":传统超参调优里 θ 只有学习率、层数几个数;RAG 里 θ 是**整条流水线的架构决策**(chunking 策略、检索管线、prompt 设计……),搜索空间大到无法靠直觉试错,所以必须**系统化测量**(= 本周全部内容)才能真的在这个空间里做 argmax。

**分析:这个公式是本周的"总纲",把 Prologue 五张幻灯片和后面四幕全部锚定到一处——**
- μ 对应 Act I–III(怎么定义、怎么算这个"好坏"指标:六检索指标 + RAGAS/FActScore/RGB);
- 𝒬 对应 Act I 的 EVAL 集(你自己的查询分布怎么采样、标注、冻结);
- "θ far richer" 对应 Week 3–6 建的所有组件(它们全是 θ 的分量);
- "μ 塑造 θ" 正是上一张 "metrics you choose shape the system" 的数学化,也是 Act IV Goodhart 的根源(你把哪个 μ 写进 argmax,系统就朝它套利)。
- 对 Avaloka:T008 的 Memory Reader 调优本质就是在这个 argmax 里搜 θ,但前提是先有 μ(检索指标)和 𝒬(Avaloka 自己的 Care Card query 分布),否则"优化"无从谈起。

## 课堂截图：Milestone · Act I of IV — The Yardstick（现场版本）

进入 Act I 的过场页,视觉用元素周期表符号 **"Au"（金,gold）** 配刻度环——双关"gold dataset(金数据集)"。副标题:

> *"Before any metric, a gold dataset. Before any number, a ground truth someone signed their name to."*（任何指标之前,先有金数据集;任何数字之前,先有一份**有人签了名的** ground truth。）

关键新意象是 **"someone signed their name to"（有人签名负责的）**——这是 PDF 正文没有的现场加强,把"ground truth"从抽象概念钉成**有人为其质量背书、担责**的东西。呼应前面 Prologue 的"评估是你自己的活":金数据集不是自动生成的、也不是借来的,是某个具体的 SME 亲手判定并署名的。这也和 Act I 的 SME cherry-pick 方法(临床医生/教授/合规官出题打分)对上——签名 = 领域权威的判断被固化下来。Prologue(5 张"为什么要测量")到此结束,正式进入 Act I "怎么造尺子"。

## 课堂截图：Act I · What the Ruler Is Made Of — The Gold Dataset（现场版本）

标题 **"The gold dataset"**,给出金数据集的形式化定义:

> A curated set of queries **𝒬 = {q₁, …, qₙ}**, each annotated with its **relevant documents** and a **graded relevance score** per pair — typically **r ∈ {0, 1, 2, 3, 4}** — from irrelevant to perfect.

即:一组精挑的 query 集合 𝒬,每个 query 标注它的相关文档,且每个(query, 文档)对给一个**分级相关性分数 r ∈ {0,1,2,3,4}**(0=无关 … 4=完美)。注意这里的 𝒬 就是上一张优化目标公式里 E_{q~𝒬} 的那个 𝒬——**金数据集 = 你的查询分布 𝒬 的具体实例化**,两张幻灯片在符号上是连着的。

右侧边注把 yardstick 隐喻收口,是全周最精炼的一句:

> *"Every retrieval metric we compute today **presupposes** this artefact. The notches on the ruler are the metrics; the ruler itself is the gold dataset."*（今天要算的每一个检索指标都**预设**了这个人工制品的存在。尺子上的刻度是指标;尺子本身就是金数据集。）

这把 "The Ruler" 那页的比喻落到实处:**刻度(notches)= 指标(Recall/nDCG…),尺子本体(ruler)= 金数据集**。没有尺子就没有刻度——所以 Act II 的六个指标全部"presuppose(预设)"了 Act I 的金数据集。这也解释了讲义为什么坚持"先讲 yardstick,再讲 metric"的顺序:指标只是尺子上的读数,尺子不存在时读数无意义。

## 课堂截图：Act I · The First Way — Watertight and Unaffordable（现场版本）

标题 **"The gold standard, as Google does it"**（谷歌式的金标准）——建金数据集的第一种方法:

> Throw 1,000 queries at the engine; human evaluators tick-mark every returned result; for recall, list what **should** have come back and compare.

即:向引擎抛 1000 条 query,人工评估员给**每一个返回结果**逐条打勾(相关/不相关);为了算 recall,还要另外列出"**本应**返回却没返回的"文档来对比。这是最严谨的做法——每条结果都人工验证。

**它的病理(pathology,现场用红字强调):**

> you planted ten beautiful Maxwell–Boltzmann articles as truth — the engine surfaces an even **better** one you never catalogued. Precision drops. The engine is **penalised for doing its job.**

你把 10 篇完美文章种为 ground truth,引擎却 surface 出一篇你从没编目、甚至**更好**的文章——因为它不在你的标准答案里,被判为"无关",于是 **precision 下降。引擎因为做好本职工作反被惩罚。** 这是全量标注金标准的根本缺陷:**你的标注永远不完整,而系统超出你标注范围的正确行为会被冤枉**(这也解释了为什么 recall 在开放语料上极难精确测——你无法穷举"所有本应相关"的文档)。

右侧边注给出为什么这条路走不通:

> *"Watertight, but nobody in a seven-engineer pod has time for it. The engineers will say: my job is to write code, not read a million documents. **They are right.**"*（水密,但七人小团队没人有时间做。工程师会说:我的活是写代码,不是读一百万篇文档。他们是对的。）

**分析:这页是"退而求其次"的铺垫。** 它先立起理想标杆(全量人工标注,水密),再用两把刀否掉它——① **成本**:百万文档逐条标,小团队做不到;② **病理**:即使做了,不完整的标注会惩罚系统的正确超纲行为。两刀之后,下一张必然引出**可行方案 = cherry-picked 金数据集**(SME 只精挑 top 100–200 候选里的 25–30 条打分,而非全量)。呼应前面 "80/20" 和 "furious client":金标准不是越大越水密越好,而是要在**可负担**和**够用**之间取平衡。

## 课堂截图：Act I · The Second Way — The Compromise That Works（现场版本）

标题 **"The cherry-picked gold dataset, in five steps"**（可行的折中方案:精挑金数据集,五步走）。这是上一张否掉"全量标注"后给出的落地方法:

1. **Hire SMEs, not engineers**（请领域专家,不是工程师)——医疗找临床医生、学习找教授、金融找合规官;"engineers will revolt"(让工程师干标注他们会造反)。
2. **SMEs author the queries**（专家亲自出题)——从真实意图收集:搜索日志、支持工单、真实调研,而不是凭空编。
3. **Run a simple engine**（跑个简单引擎,OpenSearch 之类手边现成的),每个 query 取 **top 100–200** 候选。
4. **Cherry-pick 25–30 best**（从那 200 篇里精挑最佳的 25–30 篇)——"a tractable scan, unlike a million docs"(扫 200 篇可行,扫百万篇不可行),并**给它们打 0–4 分**。
5. **Freeze at release; version; evolve**（发版时冻结、版本化、持续演进)——加新 query、调整分数、淘汰过时的(应对 eval decay)。

右侧金句:

> *"No human can scan a corpus. Anyone can scan two hundred candidates."*（没人扫得完整个语料库,但谁都扫得完两百个候选。)

**翻译分析:这页是 Act I 的方法论落点,解决了上一张的两难。** 上一张说全量标注既太贵又会惩罚系统超纲的正确行为;这页的破解思路很巧——**不追求"完整",只追求"够用且可负担"**:
- 第 3–4 步是核心诡计:**用一个简单引擎先把百万文档砍到 200 候选,把"不可能的全量标注"变成"可行的两百篇精挑"**。代价是 recall 的分母不再是"全语料的真相",而是"这 200 候选里的真相"——牺牲了理论完备性,换来了现实可操作性。
- 第 1–2 步守住**质量与领域相关性**:SME 而非工程师(专业判断)、真实意图出题(反映真实 𝒬,不是想象的 query)。
- 第 5 步守住**时效**:冻结保证可复现对比,版本化+演进应对语料/需求漂移。

**对我 project 的直接映射(可执行清单):** 给 Avaloka Memory Reader 建金数据集就照这五步——① SME = Rosso 本人(领域权威);② query 从真实 Care Card 提问/使用日志里采;③ 用现有确定性 reader 跑出每问 top-100 候选记忆;④ 精挑 25–30 条打 0–4 分(相关记忆);⑤ 冻结成 v1,后续演进。这套正好把 T008/T021 里"建 Avaloka EVAL 集"从抽象变成五个具体动作。规模上先按 Act I 的"最少 200 query"起步。

## 课堂截图：Act I · The Tempting Shortcut — Against the Borrowing of Public Benchmarks（现场版本）

> 注:现场页码从 13(五步配方)跳到 **16**,中间第 14–15 页未截到(可能是 SME Summit 细节或规模/数量讨论,待补)。

标题 **"Against the borrowing of public benchmarks"**（反对借用公共基准)——警告一条诱人的捷径:直接拿 MS MARCO / BEIR 这类现成公共基准来评估自己的系统。

> "MS MARCO is right there — let's evaluate on that." This is testing a medicine on fever patients **when your patients do not have fever**. Brilliant on the benchmark, catastrophic on your users.

翻译:"MS MARCO 就在那儿,拿它评估不就行了?"——这等于**拿退烧药在发烧病人身上做测试,可你的病人根本不发烧**。基准上光彩夺目,到你真实用户那里灾难一片。

> What public benchmarks give you: a **sanity check** of baseline competence. What they cannot give you: evidence it works in **your** production.

翻译:公共基准能给你的,是一个**基线能力的 sanity check**(确认系统没坏、大方向能跑);它给不了你的,是"它在**你自己**的生产环境里管用"的证据。

右侧那个"逻辑学家看羊"的隐喻(经典哲学笑话):

> The logicians on the train, seeing a white sheep: "There exists at least one sheep, on at least one side of its body, that appears white at the moment of observation." Public benchmarks license only that kind of claim.

翻译:火车上的逻辑学家看到一只白羊,只肯说:"存在至少一只羊,它身体的至少一侧,在观测的那一刻,看起来是白的。"——公共基准只允许你下这种**极度受限、不可外推**的结论。

**分析:这页给"用自己的金数据集"补上最后一块论证。** 前面几张讲了怎么建自己的金数据集,这张回答"为什么不能省事借公共的":
- **核心论点 = 分布不匹配**。公共基准有它自己的查询分布 𝒬′,和你生产环境的 𝒬 不是一回事。在 𝒬′ 上做 argmax 得到的 θ,搬到你的 𝒬 上可能恰好是错的(退烧药 vs 不发烧的病人)。这正是优化目标公式里 **E_{q∼𝒬} 那个下标 𝒬 必须是"你自己的"** 的现实后果。
- **但没有全盘否定**:公共基准仍有一个正当用途——**sanity check**(基线体检,确认 embedding/检索没配错、系统能跑)。它是"体温计校准",不是"疗效证明"。
- **白羊隐喻是精髓**:公共基准上的高分,严格说只支持一个极窄的结论——"在这个基准的这些 query 上,这一刻,表现好"。你不能从中外推到"在我的用户面前也会好"。**把 sanity check 的结论当成 production 的证据,是过度外推。**

**对我 project 的落点(强化已有决策):** 这条直接支撑不能拿 BEIR/MTEB 分数代替 Avaloka 自建 EVAL 集。可行姿态是**两者都用但分工明确**:公共基准做 sanity check(确认换的 embedding 模型本身没退化),Avaloka 自己的 Care Card 金数据集做"是否在我的场景管用"的真正裁决。呼应 "The Ruler" 的 "yours to build, not someone else's"——这页是那句话的反证版。

## 课堂截图：Pop Quiz · Act I — Quiz 1: The Asymmetry of the Two Halves（现场版本）

**随堂测验(现场提问,答案在下一张):**

> Precision can be computed by tick-marking the results the engine **returned**. Recall cannot be computed that way. **What extra knowledge does recall demand — and why is it so much more expensive?**
> Think before the next slide. This asymmetry is the whole reason the gold dataset is hard.

翻译:Precision 可以靠给引擎**返回的**结果逐条打勾算出来;Recall 不能这样算。**Recall 额外需要什么知识?为什么它贵得多?**

**我的答案(quiz 解答):**
- **Precision = 返回结果里相关的比例**,分母是"引擎实际返回的东西"——这些就摆在你眼前,逐条打勾即可,是一个**封闭、有限**的集合。只需看引擎给了什么。
- **Recall = 找回的相关数 / 全部相关数**,分母是"**全语料里所有本应相关的文档**"——这需要你**预先知道整个语料里哪些是相关的**,包括引擎**没**返回的那些。这是一个**开放**问题:你得穷举/遍历全部文档才能确定分母。
- **所以贵在分母**:precision 的分母引擎白送(它返回了什么你就知道);recall 的分母得靠**人工把全语料的相关性都标注一遍**(或至少标够多),这在百万文档上不可行。这正是上一张 "全量金标准 unaffordable" 和 "cherry-picked 只扫 200 候选" 的根源——**cherry-picked 方案本质上是在"近似"recall 的分母**(用简单引擎的 top 100–200 当作"相关文档的候选池"),牺牲了 recall 的绝对准确性换取可操作性。

**分析:这个 quiz 是 Act I 的收尾扣子。** 它把前面所有关于"金数据集为什么难建"的讨论,归结到一个**根本的信息不对称**:
- precision 是"向内看"(只看返回集),recall 是"向外看"(要看整个未返回的世界)。
- 这解释了为什么工业界常报 precision/nDCG 却回避绝对 recall——recall 的真值几乎无法在开放语料上获得,只能在冻结的金数据集范围内近似。
- 也预告了 Act II 的指标设计:很多指标(MRR、MAP、nDCG@K)都在有限的 top-K 内计算,部分正是为了绕开"recall 分母不可知"这个难题。

## 课堂截图：Pop Quiz · Act I · Answer — Recall Demands the Whole of the Relevant World（现场版本）

Quiz 1 的答案页,标题 **"Recall demands the whole of the relevant world"**（Recall 要求"整个相关世界"的知识):

$$\text{Recall@}k = \frac{|\text{relevant in top }k|}{|\textbf{all relevant in corpus}|}$$

> The denominator is everything relevant **in the corpus** — including what the engine never showed you. Someone must have catalogued the buried seashells **before** the game began.

翻译:分母是**整个语料里所有相关的文档**——包括引擎从没给你看过的那些。必须有人**在游戏开始之前**就把埋在沙里的贝壳都编目好了(呼应 Act II 会用的海滩捡贝壳比喻:埋起来的贝壳 = 相关但没被返回的文档)。

右侧金句:

> *"Precision judges the bucket. Recall judges the bucket **against the beach** — and only the ground truth knows what the beach holds. That catalogue is the expensive artefact of Act I."*（Precision 评判"桶里的东西";Recall 评判"桶 vs 整片沙滩"——只有 ground truth 知道沙滩里藏着什么。那份编目就是 Act I 里那个昂贵的人工制品。）

**分析:这页把 Quiz 1 的答案钉死,也把 Act I 收口。** 一句话总结整个 Act I:**precision 向内看桶,recall 向外看整片沙滩,而沙滩的真相只有那份昂贵的金数据集编目才知道。** 所以金数据集(= 那份 catalogue)之所以贵、之所以是 Act I 的核心工作,根本原因就是要为 recall 提供那个"整个相关世界"的分母。

## 谁能判断 recall 分数、怎么做（课堂问题补记）

现场我提的问题:既然 recall 的分母是"全语料所有相关文档",那**谁**来提供这个分母、**怎么**做?整理答案:

**谁来判断——是人(SME / 标注者),不是引擎。**
引擎只能告诉你它返回了什么(那是 precision 侧);**"哪些文档本应相关"这个判断只能来自 ground truth,而 ground truth 由领域专家事先标注。** 引擎无权、也无力定义自己的分母——否则就是自己给自己判卷。

**怎么做——三种现实路径,精度从高到低、成本从高到低:**

1. **全量人工标注(理论理想,不可行)**:让 SME 把整个语料每篇都判一遍相关性。这样分母是真的"all relevant in corpus",recall 绝对准确。但百万文档做不到——就是前面 "The gold standard, as Google does it" 那页被否掉的方案。

2. **Pool / cherry-picked 近似(工业界实际做法)**:用一个(或多个)简单引擎对每个 query 捞 **top 100–200 候选**,SME **只在这个候选池里**判定相关文档,把它当作"全部相关"的近似分母。—— 这就是 IR 领域标准的 **pooling(池化)** 方法(TREC 就这么做)。代价:池子外的相关文档被漏标,recall 会**系统性偏高**(分母偏小),但在冻结的评估集内可复现、可对比,足够用来比较两个系统。

3. **合成 / 反向构造**:从一篇已知文档反向生成它能回答的 query(比如 Dense-X / QA-pair 那类),这样"哪篇相关"天然已知。适合快速起步,但 query 分布可能不够真实。

**关键结论(对我 project):** Avaloka Memory Reader 的 recall **不能**指望在全部 Care Card 记忆上精确测——现实做法是**路径 2**:用现有确定性 reader 对每个测试 query 捞 top-100 候选记忆,由我(SME)在这 100 条里标出相关记忆做分母,算 Recall@5。要明确记录"这是 pool 近似的 recall,不是绝对 recall",避免过度解读。也可叠加路径 3 补一批合成 query 扩样。

## 课堂截图：Milestone · Act II of IV — The Staircase（现场版本）

进入 Act II 的过场页,视觉是 **"nG"**(nDCG 的缩写)配刻度环。副标题:

> *"Six metrics, each fixing a blindness of the one below — from a bucket on a beach to the summit called NDCG."*（六个指标,每一个都修补下面那个的盲点——从沙滩上的一只桶,一路爬到叫 NDCG 的顶峰。）

点明 Act II 的结构:六个检索指标不是并列的,而是一个**阶梯**——每个更高的指标修补前一个的盲点(Precision/Recall 位置盲 → MRR 只看首命中 → MAP 全排序但二元 → AUC-PR → **nDCG 登顶**,既排序感知又相关性加权)。"bucket on a beach"预告下一张的海滩比喻。

## 课堂截图：Act II · A Story from the Seashore — Two Children on a Beach（现场版本）

标题 **"Two children on a beach"**,用捡贝壳的故事把 precision/recall 讲直观:

> A bag of seashells thrown on the sand, some **buried**; each child gets a bucket: **go get me ten seashells.**
> **Sarah** returns: 4 shells, 6 pebbles and driftwood. **Meera** returns: 7 shells, 3 pebbles.
> Meera did better — everybody says so. But **how much** better, numerically?

翻译:一袋贝壳撒在沙滩上,有些**埋起来了**;每个孩子一只桶,任务是"给我捡十个贝壳"。Sarah 捡回 4 个贝壳 + 6 个石子和浮木;Meera 捡回 7 个贝壳 + 3 个石子。大家都说 Meera 更好——但**好多少,用数字说?**

右侧点破这个比喻对应什么:

> *"A query partitions the corpus into seashells (relevant) and pebbles (not). The search engine is the child with the bucket, asked for its top k."*（一个 query 把语料切成贝壳(相关)和石子(不相关)。搜索引擎就是那个提着桶、被要求交出 top-k 的孩子。）

**分析:这是 Act II 六指标的"直觉锚"。** 一个巧妙映射:
- **贝壳 = 相关文档,石子 = 不相关**;引擎 = 提桶的孩子,top-k = 桶里的东西。
- **Precision** = 桶里贝壳的纯度(Meera 7/10=0.7 vs Sarah 4/10=0.4)——桶里有多少是真贝壳。
- **Recall** = 找回的贝壳 / **沙滩上所有贝壳**——注意"some **buried**(有些埋着)":埋起来的贝壳正是那些"相关但没被返回"的文档,也是上一张 Quiz 1 说的"recall 分母需要有人事先编目"的来源。
- 故事的钩子"how much better, numerically?"正是整个 Act II 要回答的——**从"大家都说更好"这种主观判断,升级到用 Precision/Recall/nDCG 精确量化"好多少"**。这呼应开篇 Kelvin 那句"能用数字表达才算真懂"。

## 课堂截图：Act II · What Precision Cannot See — Cutoff-Sensitive, and Blind to the Sand（现场版本）

标题 **"Cutoff-sensitive, and blind to the sand"**（受截断点影响,且看不见沙子)——讲 Precision 的**两个盲点**:

> Ask for twenty shells instead of ten and the ranking can **reverse** — Meera grows impatient and picks sloppily, Sarah perseveres. Precision depends on **k**.

翻译(盲点一:**受 k 影响**):把"捡十个"改成"捡二十个",两个孩子的排名可能**反转**——Meera 急躁起来乱捡,Sarah 坚持到底。**Precision 的值取决于你取 top-k 的 k 是多少。** 同一个系统,换个 k,precision 高低可能翻盘,所以单看 precision@k 不稳。

> And it says **nothing about what was left behind** in the sand. A pristine bucket of three, with seven shells still buried, scores a perfect 1.0.

翻译(盲点二:**对漏检视而不见**):Precision 完全**不管沙子里还埋着什么**。一个只捡了 3 个、但个个都是贝壳的桶——哪怕沙滩里还埋着 7 个贝壳没捡——precision 照样满分 1.0。

右侧点破:

> *"Purity within the returned set only. For **did we find everything?** we need the other half of the pair."*（Precision 只衡量"返回集内部的纯度"。要回答"我们找全了吗?",得靠这一对里的另一半——Recall。)

**分析:这页是 Precision 的"证伪",顺势逼出 Recall。** 两个盲点直接对应上面 demo 里观察到的现象:
- **盲点一(cutoff-sensitive)**:precision@k 随 k 变,单一数字不可靠——这也是为什么 Act II 要往上爬到 MRR/MAP/nDCG 这些**综合整个排序**的指标,而不停留在某个 k 的 precision。
- **盲点二(blind to the sand)**:"捡 3 个全对但漏了 7 个 → precision 1.0" 完美演示了 **precision 高 ≠ 系统好**。一个极度保守、只返回最有把握的一两条的系统能刷满 precision,却漏掉大半相关内容。**必须配 recall 才能看出"漏没漏"。**
- 所以 precision 和 recall 是**一对不可拆的搭档**:precision 管"返回的纯不纯"(向内看桶),recall 管"该找的找全没有"(向外看沙滩)。任何一个单独用都会骗你。这正好接回 demo 的设计——我特意让 Recall 全程=1.0 来隔离出"排序"问题,而真实系统里 recall 往往<1,才是更常见的病。

## 课堂截图：Act II · Metric 2 · Completeness Against the Beach — Recall@k（现场版本）

标题 **"Recall@k"**,副标"完整性 vs 整片沙滩"(completeness against the beach)。公式:

$$\text{Recall@}k = \frac{|\text{relevant items in top }k|}{|\text{all relevant items in corpus}|}$$

> Change the game: bury **five blue shells**, ask for the blue ones. Find all five: perfect recall. Find three: **3/5 = 0.60**.
> Mnemonic: **R**ecall emphasises **R**elevance — all of it.

翻译:换个玩法——埋 **5 个蓝贝壳**,让孩子只捡蓝的。全找到 5 个 = 完美 recall(1.0);只找到 3 个 = **3/5 = 0.60**。记忆法:**R**ecall 强调 **R**elevance(相关性)——而且是**全部**的相关。

右侧狗狗比喻(呼应讲义 PDF 里的 Rookie the golden retriever):

> *"Rookie the golden retriever, sent for the ball, returning with a chew toy: of the five balls scattered in the yard, the fraction of balls she brings back is her recall."*（金毛 Rookie 被派去捡球,却叼回一个磨牙玩具:院子里散落 5 个球,她叼回来的球占的比例,就是她的 recall。）

**分析:这页正式给出 Recall 的定义,是 Act II 六指标里的 Metric 2(接在 Metric 1 Precision 之后)。** 两个记忆抓手:
- **Recall = R for Relevance, all of it**——分母是"全部相关",强调"找**全**没有"。这和上一张 precision 的两个盲点正好互补:precision 管纯度(向内看桶),recall 管完整性(向外看整片沙滩)。
- 分母 `all relevant items in corpus` 又一次强调那个"贵"的量——要知道全语料共有几个蓝贝壳,得有人事先编目(呼应 Quiz 1 和金数据集)。
- 这就是我 demo 里 `recall_at_k()` 那个函数的原型:分子=top-k 里相关的、分母=gold 里所有相关的。demo 里 Recall 全程 1.0,对应"5 个蓝贝壳全捡回";真实系统更常见的是 0.6 这种"漏了两个"的情况。

## 课堂截图：Act II · Recall in the Family — The Neuropsychologist's Test（现场版本）

标题 **"The neuropsychologist's test"**（神经心理学家的测验)——用一个家庭日常再讲一遍 recall:

> My daughter — a clinical neuropsychologist — plants facts casually early in a conversation: **I went here, I met such-and-such.** Two hours later: **"Papu, what did I tell you about my day?"**
> How many planted items I recover is my recall. So far, I remain within her acceptance limits.

翻译:讲师的女儿是临床神经心理学家,她会在聊天早段随口"埋"下一些事实("我去了哪儿、见了谁"),两小时后突然问:"Papu(爸),我跟你说过我今天的事,你还记得多少?" ——**我能回想起多少被埋下的事实,就是我的 recall。到目前为止,我还在她的可接受范围内(没到该担心认知衰退的地步)。**

右侧点破:

> *"Recall — retrieving what was planted — is how we test the minds of ageing parents and, as it happens, the retrievers of search engines. Your children are not yet ready to check on you. Give it two or three decades."*（Recall——回想起被埋下的东西——既是我们检测年迈父母心智的方法,也恰好是检测搜索引擎检索器的方法。你的孩子还没到要这样查你的时候,再等个二三十年。)

**分析:这页的作用是"迁移直觉",把 recall 从技术概念绑到一个人人都懂的日常场景。**
- **同一个数学,两个场景**:临床神经心理学里,测阿尔茨海默/认知衰退的标准手段就是"先给几个词/事实,过一会儿让病人复述,看能想起几个"——这**字面上就是 recall = 想起的/被埋下的全部**。讲师点出:检测年迈父母的记忆,和检测搜索引擎的检索器,是**同一个指标**。
- **"planted(埋下的)"这个词很关键**:它对应金数据集里"事先标注好的相关文档"——你得先知道"总共埋了几个"(分母),才能算 recall。神经心理学家在对话早段故意植入事实,就等于在建一个"带 ground truth 的测试集"。
- **和上一张狗狗 Rookie、这一张对照看**:讲义连用三个比喻(海滩捡贝壳 / 金毛叼球 / 神经心理测验)反复砸 recall,是因为 recall 的"分母是全部相关、且需要预先知道"这一点最反直觉、最容易被忽略。三个日常场景是为了让这个抽象分母变得可感。
- 这也顺带呼应本周主线 Kelvin/measurement:连"我妈记性还行吗"这种模糊担忧,专业上都被量化成了一个 recall 分数——**能测量,才谈得上判断**。

## 课堂截图：Act II · The Subtle Dependence on k — Ceilings, Crossovers, and a One-Way Street（现场版本）

标题 **"Ceilings, crossovers, and a one-way street"**（天花板、交叉点、和一条单行道)——讲 Precision/Recall 与 k 的三条数学性质。记号:**n = 相关文档总数,k = 你取的 top-k**。

> Let me name ten things but allow you only **three** answers: your recall caps at **3/10**, however good your memory. If **k < n**, perfect recall is unreachable; if **n < k**, perfect **precision** is unreachable (max **n/k**).
> At the crossover **k = n**: perfect precision and perfect recall **coincide**.

翻译:
- **天花板(ceiling)**:我说十件事(n=10)却只让你答三个(k=3),不管你记性多好,recall 最多 3/10。**k < n 时,完美 recall 不可能**(桶太小装不下所有相关);**n < k 时,完美 precision 不可能**(桶比贝壳多,必然掺石子,precision 上限 = n/k)。
- **交叉点(crossover)**:恰好 **k = n** 时,完美 precision 和完美 recall 才可能**同时达到**。

右侧:

> *"And recall is **monotonically non-decreasing** in k: one more scoop may add a shell or a pebble, but never removes a shell already in the bucket. This is why retrieval sets k generously."*（Recall 关于 k **单调不减**:多挖一勺,可能加进一个贝壳或一个石子,但绝不会拿走桶里已有的贝壳。这就是为什么检索把 k 设得大方。)

翻译(**单行道 one-way street**):k 越大,recall 只会持平或上升,永不下降——所以第一阶段检索倾向于**多捞**(k 设大),先把 recall 拉满,把"排得准"的问题留给后面的 reranker。

**分析:这页把前面几张的直觉数学化,给出三条硬约束。**
- **k 是一把双刃**:k 太小 recall 封顶(漏),k 太大 precision 封顶(掺)。所以选 k 本身就是 precision/recall 的权衡,不存在"免费的大 k"。
- **"retrieval sets k generously" 正是我 demo 的第一阶段策略**:检索捞 top-N(N 设大)保 recall,reranker 再从中精排 top-k 提 precision/nDCG。这条"单行道"性质(recall 随 k 单调不减)就是两阶段架构成立的数学依据——**第一阶段只管别漏(靠大 k),第二阶段只管排准(靠 reranker)**,分工来自 recall 和 precision 对 k 的相反反应。
- **crossover k=n 的洞察**:只有当你取的数量恰好等于相关文档数时,precision 和 recall 才可能同时满分——现实中你不知道 n,所以永远在权衡。这也解释了为什么要用 nDCG 这种**不依赖单一 k 的截断、而综合整个排序质量**的指标来爬上"阶梯顶端"。

## 课堂截图：Act II · When Recall Is the Master — High-Stakes Domains Retrieve Wide（现场版本）

标题 **"High-stakes domains retrieve wide"**（高风险领域要"宽"检索)——讲什么时候 recall 压倒 precision:

> **Legal RAG:** missing the one precedent that wins the case is catastrophic — better 50 noisy documents with every precedent inside than 5 pristine ones missing the one that matters.
> **Medical RAG:** a missed drug interaction can harm a patient.

翻译:法律 RAG——漏掉那条能赢官司的判例是灾难性的,**宁可要 50 篇含噪声但囊括所有判例的文档,也不要 5 篇干净却漏掉关键那条的**。医疗 RAG——漏掉一个药物相互作用可能伤到病人。

右侧点破架构含义:

> *"Optimise recall **first**, clean up precision **later** — that is Week 2's two-phase architecture: cast the wide net (retrieval), then push the shells to the top (reranker)."*（先优化 recall,后清理 precision——这就是 Week 2 的两阶段架构:先撒大网(检索),再把贝壳顶到最上面(reranker)。）

**分析:这页把"两阶段架构"的取舍讲透,且明确点名它出自 Week 2。**
- **高风险领域 recall 是主人**:漏检的代价(输掉官司/伤害病人)远大于多召回噪声的代价。所以宁愿 recall 优先、precision 靠后收拾。
- **"先 recall 后 precision"= 两阶段的战略排序**:第一阶段撒大网(大 k,保 recall,别漏关键那条),第二阶段 reranker 把好的顶上来(修 precision/nDCG)。这正是我给你写的 demo 的架构,也和上一张"recall 随 k 单调不减、所以 k 设大方"的数学性质闭环。
- **讲师明确说这是 Week 2 的内容**——再次印证:reranker/两阶段检索是前几周教过的老工具,Week 7 只是用指标语言(recall vs nDCG)把"何时该偏向哪个阶段"讲清楚。
- 对 Avaloka 的启示:Care Card 记忆检索若涉及安全敏感场景(如危机信号),也应偏向 **recall 优先**——宁可多召回几条待 reranker/guardrail 筛,也不能漏掉那条关键记忆。呼应 Week 6 的安全边界。

## 课堂截图：Pop Quiz · Act II — Quiz 2: The Bucket, Graded（现场版本）

**随堂测验:**

> I buried **n = 10** seashells. The child returns a bucket of **k = 20** items, of which **7** are true seashells.
> (a) Precision@20?　(b) Recall@20?　(c) What is the **best possible** Precision@20 any child could have achieved — and why?

翻译:我埋了 n=10 个贝壳(= 全部相关文档)。孩子交回 k=20 个东西的桶,其中 7 个是真贝壳。求 (a) Precision@20;(b) Recall@20;(c) 任何孩子能达到的**最好** Precision@20 是多少,为什么?

**我的答案:**
- **(a) Precision@20 = 7/20 = 0.35**（桶里 20 个东西,7 个是真贝壳,纯度 = 7/20）
- **(b) Recall@20 = 7/10 = 0.70**（一共埋了 10 个贝壳,找回 7 个,完整度 = 7/10）
- **(c) 最好 Precision@20 = 10/20 = 0.50**。因为**世界上一共只有 10 个贝壳**,桶却有 20 个位置,再厉害的孩子也不可能装进超过 10 个真贝壳——剩下 10 个位置必然是石子。所以 Precision@20 的**天花板 = n/k = 10/20 = 0.5**,永远到不了 1.0。

**分析:这道题是"Ceilings"那页的数值化应用。** 它精确考了那条约束:**当 n < k(相关文档数 < 你取的数量)时,完美 precision 不可能,上限 = n/k。** 这里 n=10、k=20,precision 天花板就是 0.5。

关键教学点:**Precision@k 低不一定是系统烂,可能是 k 设得比相关文档总数还大。** 这个孩子的 precision 只有 0.35,看似差,但它的理论上限本来就只有 0.5——它已经达到了上限的 70%。所以**孤立看一个 precision 数字会误判系统**,必须结合 n/k 的天花板、以及 recall 一起看。这也再次说明为什么单一指标不可靠、要用 nDCG 这种综合指标,以及为什么"retrieval sets k generously"时不能只用 precision@k 来评判检索质量(k 大会天然压低 precision)。

## 课堂截图：Act II · One Number for the Pair — F1, the Harmonic Mean（现场版本）

标题 **"F1 — the harmonic mean"**（F1:调和平均)——把 precision 和 recall 合成一个数。公式:

$$F_1 = 2 \cdot \frac{P \cdot R}{P + R}$$

> Return one always-relevant document: **P = 1.0, R = 0.1 → F₁ ≈ 0.18**. Balance at **P = R = 0.5 → F₁ = 0.5**.
> The harmonic mean **punishes imbalance**: you cannot buy your way to a good F₁ with one perfect half.

翻译:只返回一篇永远相关的文档 → precision 满分 1.0,但 recall 只有 0.1 → **F₁ ≈ 0.18**(被拉得很低)。而 P=R=0.5 平衡时 → **F₁ = 0.5**(反而更高)。**调和平均惩罚失衡:你无法靠"一半完美"买到好的 F₁。**

右侧金句:

> *"Precision and recall are two **adversarial masters** — return the whole corpus for perfect recall, or one sure document for perfect precision; both are useless. Quote them **together**, always."*（Precision 和 recall 是两个**对立的主人**——返回整个语料库可得完美 recall,只返回一篇最有把握的文档可得完美 precision;但两种极端都没用。永远要**成对**引用它们。）

**分析:F1 是 precision/recall 这对冤家的"和事佬",也是 Act II 阶梯的一环。**
- **为什么用调和平均而非算术平均**:算术平均下,P=1.0/R=0.1 会给 0.55(看着还行);但调和平均给 0.18——**它对两者中较小的那个极度敏感**,任何一方拉胯,F1 就崩。这正好惩罚了"只返回一篇稳赢文档刷满 precision"或"返回全语料刷满 recall"这类作弊,精确对应右侧"两个极端都 useless"。
- **"两个对立的主人"**:提高 recall(多召回)通常压低 precision(掺噪声),反之亦然——它们天然对立,所以必须成对看。F1 就是"逼你同时向两个主人交代"的单一数字。
- 和 demo 的关系:F1 是把 precision/recall 压成一个数;而 nDCG 更进一步,把"相关程度 + 排序位置"也纳入。工程里常见组合:**Recall@K(别漏)+ nDCG@K(排得准)+ F1(平衡快照)** 一起看,单看任何一个都会被骗——这正是本周反复强调的"单一指标不可靠"。

## 课堂截图：Act II · The Two Blind Spots — Why the Staircase Must Keep Climbing（现场版本）

标题 **"Why the staircase must keep climbing"**（为什么阶梯必须继续往上爬)——点出 Precision/Recall/F1 **共有的两个盲点**,正是它们必须被更高指标取代的原因:

> Precision, recall, and F₁ share two blindnesses:
> **Not rank-aware** — relevant docs at positions 1, 2, 3 score identically to positions 48, 49, 50.
> **Not grade-aware** — the Feynman Lectures chapter and a dry handbook entry both count as "relevant."

翻译:Precision、recall、F1 共有两个盲点——
- **不感知排序(not rank-aware)**:相关文档排在第 1/2/3 名,和排在第 48/49/50 名,**得分完全一样**。它们只数"有几个相关的",不管排在哪。
- **不感知分级(not grade-aware)**:一章精彩的《费曼物理学讲义》和一条干巴巴的手册条目,**都只算"相关"**。它们是二元的(相关/不相关),分不出"多相关"。

右侧金句(经典搜索笑话):

> *"Users do not read result lists uniformly. As the old search joke goes: governments hide their secrets on **page two** of the search results. Nobody ever visits."*（用户不会均匀地读结果列表。老搜索笑话说:政府把机密藏在搜索结果的**第二页**——因为没人会翻到那里。）

**分析:这页是 Act II 的"承上启下",解释了为什么六指标要排成阶梯往上爬。**
- **两个盲点 = 两个升级方向**:不感知排序 → 需要 MRR/MAP/nDCG(把位置纳入);不感知分级 → 需要 nDCG 的**指数增益**(把 0–4 分级纳入)。**nDCG 正是唯一同时补上这两个盲点的指标**——这就是它是"阶梯顶峰"的原因。
- **"page two" 笑话是最生动的理由**:用户只看前几条,排第 48 名的相关文档等于不存在。所以"找到了但排在第 48 名"和"没找到"体验上几乎一样——**而 precision/recall 却给它们打一样的分**,这是致命盲点。这正好也是我 demo 里 nDCG 惩罚"完美答案被挤到后面"的现实动机。
- 呼应 "The Staircase" 那张 milestone("每个指标修补下面那个的盲点"):Precision/Recall/F1 在阶梯底部,盲点最多;nDCG 在顶端,两个盲点都补上。**所以评检索质量的主指标要用 nDCG,而不是停在 F1。**

## 课堂截图：Act II · Metric 3 · A Story from a Cave — Ali Baba and the Shelves of the Thieves（现场版本）

标题 **"Ali Baba and the shelves of the thieves"**——用阿里巴巴进山洞的故事引出 **Metric 3(MRR 的直觉)**:

> A cave of loot: an aisle into the dark, shelves of treasure and junk — a tool, a jewel, a rope, a diamond. The thieves may return; **time is at a premium**. Ali Baba needs **one** jewel, and out.
> The depth of the first treasure is the distance at which the cave becomes productive.

翻译:一个藏宝山洞,一条通向黑暗的过道,货架上treasure 和 junk 混着——工具、珠宝、绳子、钻石。强盗随时可能回来,**时间极其宝贵**。阿里巴巴只需要**一件**珠宝,拿了就跑。**第一件宝贝所在的深度(第几个货架),就是这个山洞'开始产出价值'的距离。**

右侧点破对应指标:

> *"First shelf holds a diamond: out in seconds. Ninety-nine tools before the first silver coin: agonising minutes with the threat mounting. **Rank of the first relevant hit** is the whole story here."*（第一个货架就是钻石:几秒就能出来。要翻过 99 个工具才见到第一枚银币:在威胁逼近中煎熬数分钟。**第一个相关命中排在第几名**,就是这里的全部故事。）

**分析:这是 MRR(Mean Reciprocal Rank)的直觉锚——对应"只需要一个正确答案、且越早越好"的场景。**
- **山洞 = 排序结果列表,货架 = 排名,宝贝 = 相关文档,工具/绳子 = 无关文档,强盗回来 = 时间/耐心耗尽。** 阿里巴巴"只要一件就跑"精确对应 MRR 只关心**第一个**相关结果排第几。
- **为什么用倒数(reciprocal)**:第一个相关结果在 rank1 → 1/1=1.0(几秒出洞);在 rank3 → 1/3≈0.33;在 rank100 → 0.01(在威胁中煎熬)。倒数是凸的,**排名越靠后,惩罚急剧加重,但边际递减**(1→2 名腰斩,99→100 名几乎无感)——完美匹配"越早找到越好,太靠后就等于没用"。
- **它补的是 Precision/Recall 的"不感知排序"盲点的一部分**,但只看**第一个命中**,不管后面。所以它适合"找一个就够"的任务(事实问答、导航式查询),不适合需要多个证据的场景(那要 MAP/nDCG)。
- 呼应我 demo 里的 `mrr()`:找第一个 gold≥1 的位置取倒数。demo 里几个排序 MRR 多为 1.0(第一名就是相关的),因为那些例子第一名都命中——MRR 在"首命中靠后"时才会掉下来。

## 课堂截图：Act II · Metric 3 · The Formula — Mean Reciprocal Rank（现场版本）

标题 **"Mean Reciprocal Rank"**,给出 MRR 公式:

$$MRR = \frac{1}{|Q|}\sum_{q\in Q}\frac{1}{r_q}, \qquad r_q = \text{第一个相关结果的排名}$$

> First result relevant: **1/1 = 1.0**. Third: **1/3 ≈ 0.33**. Tenth: **0.1**. Hundredth: **0.01** — the system is essentially not helping.

翻译:第一个结果就相关 → 1/1=1.0;第一个相关结果在第 3 名 → 1/3≈0.33;第 10 名 → 0.1;第 100 名 → 0.01(系统基本等于没帮上忙)。**对每个 query 取"第一个相关结果排名的倒数",再对所有 query 平均。**

右侧点破核心性质:

> *"The penalty is **convex**: rank 1 → 2 halves the score; rank 10 → 11 barely registers. All the metric's sensitivity lives in the early ranks — exactly where the user's patience lives."*（惩罚是**凸的**:从第 1 名掉到第 2 名,分数腰斩;从第 10 名掉到第 11 名,几乎无感。这个指标的全部灵敏度都集中在靠前的排名——恰好是用户耐心所在的地方。）

**分析:这页把上一张"阿里巴巴山洞"的直觉数学化。**
- **公式三部分**:`1/r_q`(单个 query,第一个命中排名的倒数)→ `Σ`(对所有 query 求和)→ `1/|Q|`(取平均)。只用到**第一个相关结果的排名 r_q**,后面全不看。
- **"凸(convex)"是关键性质**:倒数函数 1/x 是凸的,所以惩罚**前重后轻**——1→2 名损失 0.5,10→11 名只损失约 0.009。含义:**MRR 把全部分辨力都花在前几名**,因为那正是用户注意力集中、耐心所在的位置。排到第 50 还是第 100 名,MRR 几乎不区分(反正都没人看)。
- **这是"惩罚曲线匹配用户行为"的典范**:上一张 "page two 笑话"说用户不均匀阅读,MRR 的凸惩罚正好把这个行为建模进指标——灵敏度分布和用户耐心分布对齐。
- 对应我 demo 的 `mrr()`:`for i,doc in enumerate(ranking): if gold[doc]>=1: return 1/(i+1)`——找到第一个相关的就返回倒数。这也是为什么 demo 里几个"第一名就命中"的排序 MRR 都是 1.0,只有首命中靠后时才掉。

## 课堂截图：Act II · MRR Solved · Three Days at the Cave — A Worked Example, and When to Reach for MRR（现场版本）

标题 **"A worked example, and when to reach for MRR"**——手算 + 适用场景。

> Three queries; first relevant result at ranks **1, 2, 5**:
> $$MRR = \tfrac{1}{3}\left(1 + \tfrac{1}{2} + \tfrac{1}{5}\right) = \tfrac{1.7}{3} \approx 0.57$$
> MRR > 0.3 roughly means: first relevant hit typically in the **top 3**.

翻译:三个 query,第一个相关结果分别排在第 1、2、5 名。MRR = (1 + 1/2 + 1/5)/3 = 1.7/3 ≈ **0.57**。经验法则:**MRR > 0.3 大致意味着"第一个相关命中通常落在前 3 名"。**

右侧适用场景:

> *"Perfect for **navigational** queries — 'what is the returns policy?' — one specific answer wanted, result 2 unnecessary if result 1 is right. Google, Amazon, internal search: dominated by navigational intent."*（最适合**导航式**查询——"退货政策是什么?"——只想要一个确定答案,只要第 1 条对了,第 2 条就是多余的。谷歌、亚马逊、企业内搜:主要都是导航式意图。）

**分析:这页补上 MRR 的"何时用",给出可落地的判断。**
- **手算确认公式**:三个 query 各取首命中倒数(1, 0.5, 0.2),平均得 0.57。和我 demo 里 `mrr()` 完全一致。
- **经验阈值 MRR > 0.3 ≈ 首命中在前 3 名**:给了一个"这个系统够不够用"的快速体检线,方便工程里定 SLA。
- **适用判据 = "导航式意图(navigational)"**:用户只想要**一个确定答案**,拿到就走,第 2 条对不对无所谓。典型:"退货政策在哪""公司 WiFi 密码"。反之,若一个问题需要综合多篇证据(研究、多跳推理),MRR 就不合适,要上 MAP/nDCG。
- **对 Avaloka 的落点**:Care Card 里"事实型/导航型"的记忆检索(比如"用户的过敏原是什么""上次约定的边界是什么")适合用 MRR 评——只要那条关键记忆排最前就行;而"需要综合多条记忆做判断"的场景则要用 nDCG。**选指标要看查询意图类型**,这是本周一个很实用的工程判断。

## 课堂截图：Act II · MRR's Confession — Ali Baba Does Not Take Inventory（现场版本）

标题 **"Ali Baba does not take inventory"**（阿里巴巴不清点库存)——坦白 MRR 的**局限**,为下一个指标 MAP 铺路:

> MRR sees **only the first** relevant result. Ten relevant documents in the corpus? MRR cannot distinguish the system that found **one** from the system that found **all ten in a row**.
> He grabbed the first bag and ran.

翻译:MRR **只看第一个**相关结果。语料里有 10 篇相关文档?MRR **分不出**"只找到 1 篇"的系统和"前 10 名全是相关、一篇不落"的系统——两者第一个命中都在第 1 名,MRR 都给 1.0。阿里巴巴抓起第一袋就跑(从不清点还剩多少宝贝)。

右侧引出下一个指标:

> *"For research queries — find me all the articles; I want to read them all — MRR is the wrong tool. Enter the **greedy brother**."*（对于研究型查询——"把所有相关文章都给我,我要全读"——MRR 是错的工具。该"贪心的兄弟"上场了。）

**分析:这页是 MRR 的"证伪 + 过渡",承接前面"何时用 MRR",现在讲"何时不能用"。**
- **MRR 的致命盲点 = 只看第一个,对"后面还有多少相关、排得好不好"完全失明**。极端例子:系统 A 前 10 名全命中,系统 B 只有第 1 名命中、其余全垃圾——**MRR 判两者一样好(都 1.0)**,但对"要读全部"的用户,A 是天堂 B 是灾难。
- **这精确暴露了 MRR 与"导航式"任务的绑定关系**:它只对"找一个就够"有效;一旦是**研究型查询(research query,要综合/穷尽多篇)**,MRR 就会用满分掩盖漏检——正是上一张分析里我说的那个陷阱。
- **"greedy brother(贪心的兄弟)"= MAP(Mean Average Precision)的预告**。阿里巴巴的故事里有个贪心的兄弟卡西姆,进洞想搬走**所有**财宝——对应 MAP 会看**每一个**相关结果排得靠不靠前,而不只是第一个。这就是阶梯的下一级:MRR(只看首命中)→ MAP(看全部相关的排序)。
- **和"阶梯必须往上爬"呼应**:每个指标都有盲点,MRR 补了"首命中位置"但仍对"多个相关的整体排序"失明,于是必须再往上一级到 MAP,最终到 nDCG(再补上"相关程度")。
- **对 Avaloka 的落点**:再次强化"按查询意图选指标"——导航型记忆检索用 MRR,但若是"把这个用户所有相关的护理记忆都调出来综合判断"这类**穷尽型**需求,必须用 MAP/nDCG,否则 MRR 会让你误以为系统很好而实际漏掉大半关键记忆。

## 课堂截图：Act II · Metric 4 · The Greedy Brother — Qasim Wants All of It（现场版本）

标题 **"Qasim wants all of it"**——用阿里巴巴贪心的兄弟卡西姆引出 **Metric 4 = MAP(Mean Average Precision)**:

> Ali Baba's brother Qasim is not content with the first jewel. He wants **every** diamond, every bag of gold, every ruby — **as early in his walk as possible**. He is the user doing research.
> His ideal day: four treasures on the first four shelves. His bad day: the same four scattered at ranks **1, 4, 12, 37**.

翻译:阿里巴巴的兄弟卡西姆不满足于第一件珠宝。他要**每一颗**钻石、每一袋金子、每一颗红宝石——而且**越早在路上拿到越好**。他就是做研究的用户。他的完美一天:四件宝贝正好在前四个货架。糟糕一天:同样四件散落在第 1、4、12、37 名。

右侧点破:

> *"Mean Average Precision measures Qasim's satisfaction. The name is an average of averages — **mean mean precision** would be correct but ugly."*（MAP 衡量卡西姆的满意度。这名字是"平均的平均"——叫"mean mean precision"其实更准确,但太难听。）

**分析:MAP 是"既要全、又要早"的指标,补上 MRR 的盲点。**
- **对比 MRR**:MRR 只看第一件宝贝(阿里巴巴抓一袋就跑);MAP 看**每一件**相关文档排得靠不靠前(卡西姆要全部,且越早越好)。所以 MAP 同时惩罚"漏"(有相关的没找到)和"排得晚"(相关的排太后)。
- **"average of averages(平均的平均)"是名字的由来**:先对**单个 query** 算 Average Precision(AP)——在每个相关文档出现的位置算一次 precision,再对这些 precision 求平均;然后对**所有 query** 的 AP 再求平均 = MAP。两层平均,所以叫 Mean Average Precision(讲师吐槽严格说该叫"mean mean precision")。
- **完美 vs 糟糕的对比(ranks 1,4,12,37)**很说明问题:同样找到 4 件宝贝(recall 一样),但排在 1/2/3/4 名 vs 散在 1/4/12/37 名,AP 天差地别——**MAP 惩罚"相关文档排得分散、靠后"**,这正是 MRR 和 Precision/Recall 都看不见的。
- **阶梯位置**:MRR(只看首命中)→ **MAP(看全部相关的位置,但仍是二元相关)** → nDCG(再补上相关程度分级)。MAP 补了"多个相关的整体排序",但它把所有相关文档当同等重要(二元),分不出 rel=4 和 rel=1——这个盲点留给 nDCG 补。
- **对 Avaloka**:研究型/穷尽型记忆检索("把该用户所有相关护理记忆调出来")用 MAP 最合适——它既要求找全、又要求关键记忆靠前。

## 课堂截图：Act II · Metric 5 · A Tale of Two Curves — ROC Comes from Copper Wires, and Fails for RAG（现场版本）

> 注:现场页码从 36(MAP 公式)跳到 **42**,中间第 37–41 页未截到(应含 MAP 手算例、AUC-PR 正式引入、PR 曲线等),待补。此外第 36 页 MAP 公式($AP_q=\frac{1}{m}\sum_{i=1}^{m}\frac{i}{r_i}$,$MAP=\frac{1}{|Q|}\sum_q AP_q$;"at the i-th relevant doc you've seen i treasures in r_i shelves — that ratio is precision at that moment of joy")也一并补记于此。

标题 **"ROC comes from copper wires — and fails for RAG"**（ROC 出身于铜线,在 RAG 上失效)——讲 Metric 5(AUC-PR)时,顺带解释**为什么不用 ROC 曲线**:

> The ROC curve is signal-processing heritage: voltages down a noisy line, a threshold trading true positives against false positives.
> For RAG corpora it is the **wrong curve**: relevance is vanishingly rare — six documents in a million. Almost nothing is falsely flagged, so the false-positive rate looks angelic **by default**.

翻译:ROC 曲线出身信号处理——一条噪声线路上的电压,用阈值在"真阳性"和"假阳性"之间权衡。但对 RAG 语料它是**错的曲线**:相关文档**极其稀有**(百万里只有 6 篇)。几乎没有东西被误标,所以**假阳性率天生就低得像天使**(默认就很漂亮),ROC 因此失去区分力。

右侧点破:

> *"A trivial retriever that returns the empty set has a false-positive rate near zero — and looks superb on ROC. **Class imbalance is the assassin of ROC.**"*（一个啥都不返回的傻瓜检索器,假阳性率接近零——在 ROC 上看起来棒极了。**类别失衡是 ROC 的刺客。**）

**分析:这页在教"为什么 AUC-PR 而不是 ROC",核心是类别极端失衡。**
- **ROC 的两个轴**:真阳性率(TPR)vs 假阳性率(FPR)。FPR 的分母是"所有不相关文档"——在 RAG 里这个分母是百万级,而误报只有几个,**FPR 几乎恒等于 0**,ROC 曲线永远贴着完美角,**分不出好系统和烂系统**。
- **"返回空集也能刷满 ROC"是最狠的反例**:什么都不返回 → 零假阳性 → ROC 满分,但这系统毫无用处。ROC 被类别失衡"暗杀"了。
- **所以 RAG 用 PR 曲线(precision-recall)+ AUC-PR**:PR 曲线的两个轴是 precision 和 recall,**都不含"海量不相关文档"这个分母**,对稀有正类敏感,不会被失衡骗到。这就是 Metric 5 选 AUC-PR 而非 AUC-ROC 的原因。
- **呼应本周主线"指标要匹配数据/任务"**:同一条"曲线下面积"的思路,ROC 适合类别均衡的信号检测,PR 适合极度失衡的检索。**选错曲线 = 被一个啥都不干的系统骗到满分**——又一个"单看某指标会误判"的实例,也和 Goodhart 的精神一致(空集检索器就是在 hack ROC)。
- **对 Avaloka**:记忆检索天然极度失衡(相关记忆少、无关多),评估要用 PR 系(Recall/nDCG/AUC-PR),别用 ROC/accuracy 这类会被失衡骗到的指标。

## 课堂截图：Act II · Metric 5 · The Curve That Matters — The Precision–Recall Curve（现场版本）

标题 **"The Precision–Recall curve"**,配一张 PR 曲线图(x 轴 recall = 搜了多少沙滩,y 轴 precision = 桶有多纯):

- **the careful child(细心的孩子)**:曲线一路保持高位,recall 爬到 1.0 时 precision 才缓缓下降 → **AUC-PR ≈ 0.86**
- **the clumsy child(笨拙的孩子)**:precision 一开始就断崖式跌落 → **AUC-PR ≈ 0.32**
- 底部虚线 **random retriever = base rate of relevance**(随机检索器 = 相关性基率,极低)

底部点破:

> *"The careful child keeps the bucket clean as recall climbs; the clumsy child falls off a cliff. **AUC-PR is the area under the walk.**"*（细心的孩子在 recall 上升时始终保持桶干净;笨拙的孩子直接跌下悬崖。AUC-PR 就是这段"行走"下方的面积。）

**分析:这页把 Metric 5 = AUC-PR 用图讲透,呼应海滩比喻。**
- **PR 曲线 = 边挖沙边记录"桶的纯度"**:x 轴 recall(挖了多少)、y 轴 precision(桶多纯)。随着你越挖越多(recall↑),不可避免会掺进石子(precision↓),曲线整体从左上向右下走。**曲线下面积(AUC-PR)= 把这整段"精度随召回变化"的过程压成一个数**——面积越大,系统在各个召回水平下都能保持高精度。
- **两个孩子的对比**:细心的孩子(0.86)几乎搜遍整片沙滩(recall→1)还能保持桶很干净;笨拙的孩子(0.32)刚开始 precision 就崩,说明它排在前面的很多是石子。**同一张图直观区分好坏系统**——这正是上一张说 ROC 做不到(会被失衡骗成都满分)、而 PR 曲线能做到的。
- **随机基线 = 相关性基率**:PR 曲线的"随机水平"不是 0.5,而是"语料里相关文档的比例"(极低,比如 6/百万)。所以任何有用的系统都该远高于这条底部虚线——这也再次说明 PR 对稀有正类的敏感性。
- **和六指标阶梯的关系**:AUC-PR 是 Metric 5,把 precision/recall 的**整条权衡曲线**压成一个数(不依赖单一 k),比单点 precision@k 更全面;但它仍是二元相关、且不直接看排序中的分级——最后一步的 nDCG(Metric 6)才补上"相关程度 + 位置折扣"。
- **对 Avaloka**:PR 曲线是评估极度失衡的记忆检索的合适工具,AUC-PR 可作为"整体检索质量"的单数字快照,配合 nDCG@k(看排序)和 Recall@k(看漏检)一起用。

## 课堂截图：Act II · Metric 5 · When to Reach for It — AUC-PR: The Rare-Needle Metric（现场版本）

标题 **"AUC-PR: the rare-needle metric"**（AUC-PR:大海捞针指标)——讲 AUC-PR 的适用场景:

> Use AUC-PR when the positive class is **rare relative to the corpus** — which describes most enterprise RAG: millions of documents, a few dozen relevant per query.
> Also: fraud detection, security events, recommenders — any search where relevance is the exception.

翻译:当**正类相对语料极其稀有**时用 AUC-PR——这正是多数企业 RAG 的样子:百万级文档,每个 query 只有几十篇相关。也适用于:欺诈检测、安全事件、推荐系统——任何"相关是例外(而非常态)"的检索。

右侧点破:

> *"AUC-PR is the continuous generalisation of MAP, and it stays honest as your corpus grows — unlike ROC, it is not inflated by oceans of true negatives."*（AUC-PR 是 MAP 的连续推广,而且随着语料增长它依然诚实——不像 ROC,它不会被汪洋般的真阴性(true negatives)灌水。）

**分析:这页给 AUC-PR 定"何时用",并厘清它和 MAP、ROC 的关系。**
- **适用判据 = 正类稀有(rare positive / class imbalance)**:相关文档在语料里是极少数。企业 RAG、欺诈检测、安全告警、推荐——共同点都是"要找的东西是例外"。这类场景 AUC-PR 是对的工具。
- **"AUC-PR 是 MAP 的连续推广"** 是关键洞察:MAP 只在离散的相关文档命中点上取 precision 再平均(我 demo 里正是这么算的);AUC-PR 把它推广成**整条连续曲线下的面积**。所以两者精神一致,MAP≈AUC-PR 的离散版——这也解释了为什么我 pr_curve_demo 用 Average Precision 来近似 AUC-PR。
- **"stays honest as corpus grows"**:承接上一张——语料越大,真阴性(无关文档)越多,ROC 的 FPR 越被稀释成 0、越虚高;而 AUC-PR **不碰真阴性这个分母**,所以语料涨到千万级它依然如实反映系统好坏。**这是"随规模保持诚实"的指标,契合企业 RAG 语料会持续增长的现实。**
- **对 Avaloka**:记忆库是典型的"稀有正类"(相关记忆少、无关多),且会随用户使用不断增长——AUC-PR 正是该用的整体检索质量指标,ROC/accuracy 会随记忆库增大而越来越具误导性。

## 课堂截图：Act II · The Cave Deepens — The Jewels Acquire Prices（现场版本）

标题 **"The jewels acquire prices"**（宝物开始有了价格)——引出 **Metric 6 = nDCG(阶梯顶峰)**,给"相关"加上"程度":

> Return to the cave — but now the treasures have **differential worth**: rock 0, silver 1, gold 2, **diamond 4**. A diamond at rank 1 beats a silver at rank 1 — and both beat a diamond buried at rank 20, because the deeper Ali Baba walks, the higher the risk.
> The same diamond is worth less the deeper it is found.

翻译:回到山洞——但现在宝物有了**不同的价值**:石头 0、银 1、金 2、**钻石 4**。排第 1 的钻石胜过排第 1 的银;两者又都胜过埋在第 20 名的钻石——因为阿里巴巴走得越深,风险越高。**同一颗钻石,埋得越深,值越少。**

右侧点破:

> *"Double sensitivity — to **what** you find and **where** you find it — is exactly what the summit metric captures. Our graded scores r ∈ {0,…,4} finally earn their keep."*（双重敏感——对你**找到什么**、以及在**哪里**找到——正是这个顶峰指标所捕捉的。我们的分级分数 r ∈ {0,…,4} 终于派上用场了。）

**分析:这页是六指标阶梯的"登顶"铺垫,把 nDCG 的两个核心维度点明。**
- **两个"价格"维度**:① **what(找到什么)**——用相关度分级(石/银/金/钻 = 0/1/2/4)区分,对应 nDCG 的**指数增益** `2^r−1`;② **where(在哪找到)**——排得越深越不值,对应 nDCG 的**对数折扣** `1/log₂(rank+1)`。**nDCG = 同时对这两个维度敏感**,正好补上前面所有指标的两个盲点(不感知分级 + 不感知排序)。
- **"graded scores finally earn their keep"呼应 Act I**:金数据集里辛辛苦苦标的 0–4 分级相关性,前面 Precision/Recall/MRR/MAP/AUC-PR 都只用到"相关/不相关"(二元),**分级一直没被真正用上**;直到 nDCG 才第一次把 0–4 全用起来。这解释了为什么 Act I 坚持要 SME 打 0–4 而不是简单的 0/1——就是为了喂给 nDCG。
- **"钻石在 rank1 胜过 silver 在 rank1,都胜过 diamond 埋在 rank20"** 精确演示双重敏感:既比"东西本身多值钱"(钻石 vs 银),又比"排在多前"(rank1 vs rank20)。这正是我 ndcg_demo 里"把 rel=4 的 A 排后面惩罚远重于把 rel=1 的 D 排后面"那个现象的故事版。
- **阶梯登顶**:至此六指标走完——Precision/Recall(二元、位置盲)→ MRR(首命中)→ MAP(全部相关的位置)→ AUC-PR(整条 PR 曲线)→ **nDCG(what + where,分级 + 排序)**。nDCG 是唯一同时握住两个维度的,所以是 primary 主指标,其余作诊断。

## 课堂截图：Act II · Metric 6 · A Supercalifragilistic Word — NDCG, Unpacked Inside-Out（现场版本）

标题 **"NDCG, unpacked inside-out"**（把 nDCG 从里到外拆开)——用嵌套方框逐层展示,顶注:**read NDCG inside-out: gain → cumulate → discount → normalise**。

四层(嵌套,从里到外):

1. **Gain(增益)** = $2^{rel_i} - 1$ —— *the worth of the jewel — exponential in its grade*(宝物的价值,对相关度指数放大)
2. **Cumulative(累积)** = $\sum_i$ —— *the knapsack total after k shelves*(前 k 个货架的背包总值)
3. **Discounted(折扣)** = $/\log_2(i+1)$ —— *the deeper the cave, the less the same jewel is worth*(越深的洞,同一颗宝石越不值)
4. **Normalised(归一化)** = $/\text{IDCG}$ —— *divided by the best possible day in this cave*(除以"这个洞里最好的一天"= 理想排序)

底注:**perfect ranking = 1.0 · every query lands in [0, 1] · averages cleanly**（完美排序 = 1.0;每个 query 都落在 [0,1];可以干净地跨 query 平均）。

合起来:

$$nDCG@k = \frac{DCG@k}{IDCG@k}, \qquad DCG@k = \sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}$$

**分析:这页把 nDCG 的四层结构一次性摊开,和 `course/week_07/ndcg_demo.py` 逐层对应。**
- **Gain 补"分级"盲点**:$2^{rel}-1$ 让 rel=4 值 15、rel=1 只值 1——把"钻石远比银值钱"烤进公式。
- **Discount 补"排序"盲点**:$/\log_2(i+1)$ 让越靠后的位置贡献越少,rank1 除以 1(不打折)、rank20 除以约 4.4——把"埋得越深越不值"建进去。
- **Normalise 让它可比**:除以 IDCG(理想排序的 DCG),把结果压到 [0,1],**完美排序=1.0**,不同 query(相关文档多寡不同)能干净平均——这是它能当跨 query 主指标的原因。
- **底注三条 = nDCG 作为主指标的三大优点**:① 有明确上限(1.0=完美),好解读;② 值域固定 [0,1],可比;③ 跨 query 平均干净(不像 DCG 会被相关文档多的 query 拉偏)。
- **和我 demo 完全一致**:`ndcg_demo.py` 里 `gain()`=Gain 层、`dcg_at_k()`=Cumulative+Discount 两层、`ndcg_at_k()`=Normalise 层。你跑那个 demo 打印的逐行"gain / discount / 贡献",就是这张图第 1–3 层的数值展开;最后 DCG/IDCG 就是第 4 层。**这张幻灯片 = demo 的图解版。**

## 课堂截图：Act II · NDCG Layer 1 — Gain: Exponential, by Design（现场版本）

标题 **"Gain — exponential, by design"**（增益:刻意做成指数)——nDCG 第 1 层:

$$\text{gain}_i = 2^{rel_i} - 1$$

> Rock (0) → **0**. Silver (1) → **1**. Gold (2) → **3**. Diamond (4) → **15**.
> A diamond is **fifteen** times a silver, not four — the exponential bakes in the intuition that top-tier relevance matters disproportionately.

翻译:石头(rel0)→ 增益 0;银(rel1)→ 1;金(rel2)→ 3;钻石(rel4)→ **15**。**一颗钻石值 15 个银,不是 4 个**——指数把"顶级相关性不成比例地重要"这个直觉烤进公式。

右侧重要提醒(约定差异):

> *"Two conventions coexist: Järvelin–Kekäläinen (2002) used linear gain; Burges (2005) 2^rel − 1 is the modern default (scikit-learn, pytrec_eval). **Check the formula when reading older papers** — numbers do not compare across conventions."*（两种约定并存:Järvelin–Kekäläinen(2002)用线性增益 rel;Burges(2005)的 2^rel−1 是现代默认(scikit-learn、pytrec_eval)。**读旧论文先核对公式**——跨约定的数字不可比。）

**分析:这页专讲 nDCG 的 Gain 层,和你上一条问的"银/钻石例子"直接对应。**
- **指数增益的意义**:如果用线性增益(rel 本身),钻石 4 只是银 1 的 4 倍;但 `2^rel−1` 让钻石=15、银=1,**15 倍**。这就是为什么上一个例子里"把钻石排在银后面"惩罚那么重——钻石的价值被指数放大了。
- **两种约定的坑(工程要点)**:线性 vs 指数两套公式算出的 nDCG 数值**不能直接比**。你笔记和 `ndcg_demo.py` 用的都是现代默认 `2^rel−1`(和 scikit-learn/pytrec_eval 一致);读老论文或用老库时要先确认它用哪套,否则会拿两个不可比的数字做对比得出错误结论。
- **和 demo 完全对齐**:`ndcg_demo.py` 里 `gain = 2**rel - 1`,打印的 gain 列正是 0/1/3/15 这套值。你上一条问的银(1)vs 钻石(15)的对调,数值就来自这一层。
- **对 Avaloka**:给记忆打分级相关性时,若某类记忆是"关键中的关键"(如安全边界、过敏原),用 0–4 分级 + 指数增益能让"漏排关键记忆"在 nDCG 上被重罚,而不是和普通记忆一视同仁——这正好契合安全优先的设计。

## 课堂截图：Act II · NDCG Layers 2 and 3 — Cumulate, Then Discount by Depth（现场版本）

标题 **"Cumulate, then discount by depth"**（先累积,再按深度打折)——nDCG 第 2、3 层合并:

$$DCG^{(k)} = \sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}$$

> CG is the knapsack total after **k** shelves. DCG divides each gain by a **logarithmic** penalty — gentle at the top of the list, harsh at the bottom. The **+1** spares position 1 a divide-by-zero.

翻译:CG(累积增益)= 前 k 个货架的背包总值。DCG 给每个增益除以一个**对数**惩罚——**列表顶部温柔、底部严厉**。分母里的 **+1** 让第 1 名不至于除以零(log₂(1)=0)。

右侧"复利折现"比喻:

> *"I am willing to promise anyone a **million dollars on their 200th birthday** — you realise the present value is not much. The diamond at rank 20 is the same promise; log₂ writes the discount schedule."*（我愿意答应给任何人在他们**200 岁生日**时一百万美元——你会意识到它的现值没多少。排在第 20 名的钻石就是同一个承诺;log₂ 写好了这张折现表。）

**分析:这两层把"位置价值"数学化,配一个精妙的金融比喻。**
- **第 2 层 Cumulative(累积)**:就是把前 k 个位置的增益加起来(Σ),得到"背包总值"。
- **第 3 层 Discount(折扣)**:每个增益除以 `log₂(rank+1)`。对数的特性是**顶部温柔、底部严厉**——rank1 除以 1(不折),rank2 除以 1.585,rank20 除以约 4.39。位置越深,同样的宝贝贡献越少。
- **"+1" 的工程细节**:rank=1 时 log₂(1)=0 会除零,所以用 log₂(rank+1),第 1 名除以 log₂(2)=1,既避免除零又"不打折"。
- **"200 岁生日的一百万"比喻最精彩**:把位置折扣类比成**金融现值(present value)**——承诺很久以后给你一百万,折现到今天几乎不值钱。排在第 20 名的钻石就是这样:名义价值(gain)还是 15,但因为埋得深、用户几乎看不到,**折现后的实际价值很低**。log₂ 就是那张"折现表",规定了每往后一名打多少折。
- **和 demo 对齐**:`ndcg_demo.py` 里 `contrib = g / math.log2(i+2)`(i 从 0 起,即 log₂(rank+1))正是这一步;打印的 discount 列(1.000、1.585、2.000…)就是这张公式的数值展开。
- **收束**:Gain(层1)决定"宝贝值多少",Discount(层3)决定"这个位置能兑现多少",两者相乘求和 = DCG。最后除以 IDCG(层4)归一化,就得到 nDCG。四层至此讲完。

## 课堂截图：Pop Quiz · Act II — Quiz 4: Your Turn in the Cave（现场版本）

**随堂测验(手算 nDCG):**

> Relevance grades down the ranked list: **[0, 1, 0, 2, 1]**. Compute DCG, IDCG, and NDCG at **k = 5**.
> Gains: 2^rel − 1. Discounts: log₂2=1, log₂3=1.585, log₂4=2, log₂5=2.322, log₂6=2.585.

**我的解答(已用 demo 验证):**

**第 1 步 — 各位置增益 `2^rel−1`**:排序 [0,1,0,2,1] → gains = [0, 1, 0, 3, 1]

**第 2 步 — DCG@5**(增益 ÷ 折扣 log₂(rank+1)):
$$DCG = \frac{0}{1} + \frac{1}{1.585} + \frac{0}{2} + \frac{3}{2.322} + \frac{1}{2.585} = 0 + 0.631 + 0 + 1.292 + 0.387 = \mathbf{2.310}$$

**第 3 步 — IDCG@5**(理想排序 = 相关度降序 [2,1,1,0,0] → gains [3,1,1,0,0]):
$$IDCG = \frac{3}{1} + \frac{1}{1.585} + \frac{1}{2} + 0 + 0 = 3 + 0.631 + 0.5 = \mathbf{4.131}$$

**第 4 步 — nDCG@5**:
$$nDCG = \frac{DCG}{IDCG} = \frac{2.310}{4.131} = \mathbf{0.559}$$

**分析:这道题是 nDCG 四层的完整手算演练,一道题走完 Gain → Cumulate → Discount → Normalise。**
- **答案 0.559 的含义**:这个排序只达到了理想排序的 56%。主要损失在——**rel=2 的宝贝(gain 3)被排到了第 4 名**(折扣 2.322),如果它排第 1 名能贡献 3.0,现在只贡献 1.29,白丢约 1.7 分。这正是"把值钱的排后面"的代价。
- **理想排序怎么定**:不是把相关的随便提前,而是**按相关度从高到低**排([2,1,1,0,0]),让高 gain 的吃到最轻的折扣。
- **验证**:用 `course/week_07/ndcg_demo.py` 的同款算法跑,DCG=2.310、IDCG=4.131、nDCG=0.559,与手算一致。可把 demo 的 GOLD/排序改成这组自测。
- 这也和讲义 PDF 里给的自测题完全一致(PDF 原文:relevance [0,1,0,2,1] → DCG≈2.310, IDCG≈4.131, nDCG≈0.56;并点出"rel=2 的 gold 在第 4 名是悲剧,移到第 1 名就贡献 3.0 而非 1.29——一次换位就是差距,而移动它正是 reranker 的活")。

## 课堂截图：Pop Quiz · Act II · Answer — NDCG = 0.56, a Mediocre Day, Precisely Measured（现场版本）

标题 **"NDCG = 0.56 — a mediocre day, precisely measured"**（0.56:一个平庸的日子,被精确测量了)。答案页确认了上一条我的解答:

$$DCG = 0 + \tfrac{1}{1.585} + 0 + \tfrac{3}{2.322} + \tfrac{1}{2.585} = 0.631+1.292+0.387 = 2.310$$
$$IDCG_{[2,1,1,0,0]} = \tfrac{3}{1}+\tfrac{1}{1.585}+\tfrac{1}{2} = 3+0.631+0.5 = 4.131$$
$$NDCG = \tfrac{2.310}{4.131} \approx \mathbf{0.56}$$

底部点破(直接连到 reranker):

> *"The gold at rank 4 is the tragedy: moved to rank 1, it alone contributes 3.0 instead of 1.29. One transposition, and NDCG jumps — **this is the number your reranker is paid to move.**"*（排在第 4 名的那块金子是悲剧:挪到第 1 名,它单独就贡献 3.0 而非 1.29。一次换位,NDCG 就跳升——**这就是你花钱雇 reranker 去挪动的那个数字。**）

**分析:这页把 nDCG 和本周核心动作(reranker)焊死。**
- **标题的"precisely measured"呼应全周主线**:0.56 不是"感觉一般",而是**精确量化的"平庸"**——这正是 Kelvin"用数字表达才算真懂"的落地。同样一个排序,主观上说"还行",客观上是"只发挥了理想的 56%"。
- **"the number your reranker is paid to move"是全页题眼**:nDCG 不只是一个体检分,它直接指明了**reranker 的 KPI**。reranker 存在的意义,就是把 rel=2 那块金子从第 4 名挪到第 1 名,让 nDCG 从 0.56 跳上去。这把"评估(Week 7)"和"修理动作(reranker,Week 1–2)"闭环成一句话。
- **和我 demo 完全打通**:`rerank_eval_demo.py` 演示的正是"加强 reranker → 把被埋的高相关文档顶上来 → nDCG 上升";`ndcg_demo.py` 演示的正是这个 0.56 怎么一层层算出来。这道 Quiz 的答案 = 两个 demo 的交汇点。
- **对 Avaloka**:给 Memory Reader 定 reranker 的 KPI 时,就该用 nDCG@k——它能精确量化"关键记忆有没有被顶到前面",而这正是 reranker 该负责改善的指标。

## 课堂截图：Act II · Reading the Summit — NDCG + Recall: The Minimal Diagnostic Pair（现场版本）

标题 **"NDCG + Recall: the minimal diagnostic pair"**（NDCG + Recall:最小诊断对)——Act II 的收官,把六指标浓缩成一个可执行的诊断法:

> - **NDCG low, Recall high** — the documents are found but badly ordered: **fix the reranker**
> - **NDCG low, Recall low** — the documents are not found at all: **fix retrieval** — chunking, embedder, hybrid mix
> - **NDCG high, Recall high** — celebrate, and move to Act III

翻译:
- **nDCG 低 + Recall 高** → 文档找到了但排序烂 → **修 reranker**
- **nDCG 低 + Recall 低** → 根本没找到 → **修检索**(chunking、embedding、hybrid 混合)
- **nDCG 高 + Recall 高** → 庆祝,进 Act III(评生成侧)

右侧点破用法:

> *"If you have time for one number, make it NDCG. The other five are diagnostics — the footholds you consult when the summit number moves the wrong way. Both computable at every build; the **delta between builds** is where improvement lives."*（如果你只有时间看一个数,那就看 NDCG。另外五个是诊断工具——当这个"顶峰数字"往错误方向走时,你去查的那些落脚点。两者每次构建都能自动算;**构建与构建之间的差值(delta)**,才是改进真正发生的地方。）

**分析:这页是全周最实用的一页,把"评估"直接翻译成"该修哪里"的行动表。**
- **主指标 + 诊断的分工**:**nDCG 是唯一的主指标(summit number)**,其余五个(Precision/Recall/MRR/MAP/AUC-PR)是诊断辅助。日常只盯 nDCG,它掉了再用其他指标定位病因。这是"指标要少而精"的工程智慧——太多指标反而无从下手。
- **nDCG↔Recall 两维诊断表**是核心可执行产物:
  - 都低 = 检索层的病(没找到)→ 动 embedding/chunking/hybrid
  - nDCG 低但 Recall 高 = 排序层的病(找到了没排好)→ 动 reranker
  - 都高 = 检索没问题,去评生成侧(Act III)
- **"delta between builds is where improvement lives"是持续改进的精髓**:单次 nDCG 的绝对值没那么重要,**关键是每次改动后 nDCG 的变化量**——涨了说明这次改对了,跌了就回滚。这正是"证据驱动架构升级"的操作化,也是我 `rerank_eval_demo.py` 演示的"加 reranker 前后对比 nDCG"的意义。
- **完全对应我的 demo**:`rerank_eval_demo.py` 里的 `diagnose()` 函数就是照这张表写的(Recall≥0.8 且 nDCG<0.85 → 修 reranker;两者都低 → 修检索)。**这张幻灯片就是那个函数的出处。**
- **对 Avaloka**:给 Memory Reader 建监控就照这个最小对——每次改动跑一遍金数据集,看 nDCG@k 的 delta + Recall@k,自动判定该动检索还是 reranker。不需要盯六个指标,两个就够定位。

## 课堂截图：Act II · The Whole Act in One Picture — The Staircase（现场版本）

标题 **"The staircase"**,副标"每一级修补下面一级的盲点(each step fixes a blindness of the one below)"。一张阶梯图把六指标从低到高摆出来:

| 台阶(低→高) | 一句话 | 性质 |
|---|---|---|
| **Precision@k** | 返回集的纯度 | 二元 · 位置盲 |
| **Recall@k** | 完整性 vs 全部相关 | 二元 · 位置盲 |
| **MRR** | 第一个宝贝有多快 | 只看首命中排名 |
| **MAP** | 所有相关文档,且要早 | 感知排序 · 仍二元 |
| **AUC-PR** | 整条权衡曲线 | 对稀有正类稳健 |
| **NDCG** | 分级增益,按深度折扣 | 感知排序 · 分级 |

底部收束金句:

> *"Binary and position-blind at the bottom; rank-aware in the middle; graded and discounted at the summit. Two systems can share an NDCG and differ wildly in MRR — the diagnosis..."*（底部是二元且位置盲;中间开始感知排序;顶峰是分级且带折扣。两个系统可以有相同的 NDCG 却在 MRR 上天差地别——这个诊断……）

**分析:这页是 Act II 的一图总纲,把六指标的"能力递进"可视化。**
- **三段式递进**:① 底部(Precision/Recall)二元 + 位置盲,只数"有几个相关的";② 中部(MRR/MAP)开始**感知排序**,但仍是二元(相关/不相关);③ 顶峰(AUC-PR/NDCG)——AUC-PR 补稀有正类稳健性,NDCG 再补**分级(graded)**。每一级填下一级的盲点,这就是"阶梯"的含义。
- **底部金句的深意"两个系统 NDCG 相同却 MRR 天差地别"**:这揭示了**为什么保留其余五个作诊断**——即使主指标 nDCG 一样,不同指标能暴露不同的失败模式。比如两个系统 nDCG 都 0.8,但一个 MRR=1.0(首命中在第 1)、另一个 MRR=0.3(首命中在第 3),对"导航式查询"体验完全不同。**单一 nDCG 会掩盖这种差异,所以诊断时要多指标交叉看。** 这补充了上一张"只看一个数就看 nDCG"——日常盯 nDCG,但诊断时其余五个不可少。
- **和我 demo 的关系**:`rerank_eval_demo.py` 同时打印 Recall/nDCG/MRR 三个指标,正是这个"主指标 + 诊断"思路的实现——一个 nDCG 定总分,Recall 和 MRR 帮定位病因。
- **对 Avaloka 的落点**:评估仪表盘应以 nDCG@k 为主数字,同时展示 Recall@k(漏没漏)、MRR(首命中快不快),按查询意图选择重点看哪个诊断指标。

## 课堂截图：Pop Quiz · Act II — Quiz 5: The Morning Stand-up（现场版本）

**随堂测验(实战诊断):**

> Your dashboard this morning: **Recall@50 = 0.91 (healthy), NDCG@10 dropped from 0.71 to 0.55 overnight**. A teammate proposes re-chunking the corpus.
> **Is the teammate right? What broke — and what do you inspect first?**

翻译:今早看板:Recall@50 = 0.91(健康),但 NDCG@10 一夜之间从 0.71 掉到 0.55。一个同事提议**重新 chunk 整个语料**。这同事对吗?什么坏了?你先查什么?

**我的答案:**

**① 同事错了。** 重新 chunk 是修**检索层**(解决"文档根本没找到")。但 **Recall@50 = 0.91 依然健康,说明文档明明找得到、没漏**——检索层没坏。对着没坏的地方动手术,大概率白费还可能引入新问题。

**② 坏的是排序(ranking)。** 用最小诊断对判:**Recall 高 + nDCG 掉 = 文档找到了但排序烂 → 排序层的病**。相关文档还在 top-50 里(recall 高),只是被从前排挤到了后面(nDCG@10 掉),所以"前 10 名的质量"崩了。

**③ 先查什么(按"一夜之间变化"锁定):**
- **reranker**:模型/权重/配置昨晚是否变过?融合权重是否调过?这是最可能的元凶。
- **embedding 或索引**:是否夜里重建了索引、换了 embedding 版本,导致排序重排?
- **对比 nDCG@10 vs nDCG@50**:如果 nDCG@50 没怎么掉、只有 @10 掉,进一步坐实是"前排顺序"问题而非"整体找不到"。
- **看具体 query 的 trace**:挑几个 nDCG 掉得最狠的 query,看原来排前面的相关文档现在掉到了第几名。

**分析:这道题是"最小诊断对"的实战应用,专门考"别对没坏的地方动刀"。**
- **陷阱在同事的直觉**:nDCG 掉了 → 本能想"改 chunking/检索"。但**必须先看 Recall 这个搭档指标**——Recall 健康就排除了检索层。这正是为什么讲义强调 **nDCG 必须配 Recall 一起看**,单看 nDCG 掉会误导你去修错地方。
- **"overnight(一夜之间)"是关键线索**:突变通常来自一次具体变更(部署、模型更新、索引重建),而不是数据缓慢漂移。所以诊断要先查"昨晚动了什么",这是 delta 思维("delta between builds is where improvement lives"的反向用法——delta 变坏时反查是谁引入的)。
- **对 Avaloka 的落点**:Memory Reader 上线监控就该这样——nDCG 掉了先看 Recall 是否也掉,再定位是检索还是 reranker,并回溯最近一次变更。别一看指标掉就重建整个记忆索引(等于同事的"re-chunk"错误)。
- **和我 demo 呼应**:`rerank_eval_demo.py` 的 `diagnose()` 遇到这个场景(Recall 高、nDCG 低)会直接输出"修 reranker"——这道 quiz 的正确答案就是那个函数的判定。

## 课堂截图：Pop Quiz · Act II · Answer — The Shells Are in the Bucket, Badly Stacked（现场版本）

标题 **"The shells are in the bucket — badly stacked"**（贝壳在桶里,只是堆歪了)。答案页确认上一条我的解答:

> Recall@50 says the relevant documents **are being found**. NDCG collapsing while recall holds means they are arriving **in the wrong order** — a ranking problem, not a retrieval problem.
> **Re-chunking attacks the wrong stage.**

翻译:Recall@50 说明相关文档**确实被找到了**。NDCG 崩了而 recall 不动,意味着它们**以错误的顺序到达**——是排序问题,不是检索问题。**重新 chunk 打错了阶段。**

右侧收束:

> *"Inspect the **reranker** first — a bad deploy, a version drift, a broken feature. The diagnostic pair just saved you a week of re-chunking a healthy corpus."*（先查 reranker——一次糟糕的部署、一次版本漂移、一个坏掉的特征。这个诊断对刚帮你省下了一周重新 chunk 一个健康语料的冤枉功。）

**分析:这页把"最小诊断对"的商业价值一锤定音。**
- **"badly stacked(堆歪了)"是精准的隐喻**:贝壳(相关文档)都在桶里(recall 高),问题只是**堆的顺序不对**(nDCG 低)——不是没捞到,是排乱了。一个词就锁定病灶层。
- **"saved you a week of re-chunking a healthy corpus"是全周最落地的一句**:如果没有这个诊断对,团队会听同事的直觉去重新 chunk(几天到一周的工作量),而语料本来是健康的——**纯属浪费,还可能引入新问题**。诊断对的价值不是学术精确,而是**帮你不把工程资源砸到错误的地方**。这直接呼应本周"评估的目的是有依据地改进,而不是瞎试"。
- **三个最可能的元凶都是"变更类"**:bad deploy(部署出错)、version drift(版本漂移)、broken feature(坏特征)——全都指向"最近动了什么",印证上一条我说的"overnight 突变先查昨晚的变更"。
- **对 Avaloka / 求职**:这个案例几乎可以直接当面试答案——"看板报警时,我先看 Recall 和 nDCG 的组合来定位是检索还是排序问题,再回溯最近部署,避免团队对着健康的语料做无用的重建"。这是一个 RL/RAG manager 该有的**故障定位纪律**,比会背公式更值钱。

## 课堂截图：Interlude · Between the Acts — Signal & Noise（现场版本）

Act II 与 Act III 之间的插曲,视觉用希腊字母 **σ(sigma,标准差/统计的符号)** 配刻度环。标题 **"Signal & Noise"**,副标:

> *"A 1.2-point improvement on 200 queries may be nothing at all. Before you celebrate, ask the statistics."*（在 200 个 query 上 1.2 分的提升可能什么都不是。庆祝之前,先问问统计。)

**分析:这个插曲是全周最容易被忽略、却最能防止自欺的一段——统计显著性。**
- **核心警告**:你改了系统,nDCG 涨了 1.2 分,别急着开香槟。**在只有 200 个 query 的评估集上,这点提升可能纯属噪声**——换一批 query 就可能反过来。σ 符号点明主题:要看**方差/波动**,不只是均值。
- **接回 Act I 的规模讨论**:这正是为什么讲义反复说"最少 200、目标 1000"query。样本太小,指标的波动大到能淹没真实提升;样本够大(约 500–1000),统计功效才够,才能可靠区分"真改进"和"运气"。
- **预告方法**:接下来会讲 **配对 bootstrap / 置换检验**(paired bootstrap / permutation test)——判断两个系统的指标差异是否统计显著,以及**统计显著 vs 实用显著**的区别(样本够大时,连微不足道的提升都会"统计显著",但不值得为它增加工程成本)。
- **和本周主线的关系**:这是 Kelvin "用数字表达才算真懂" 的必要补丁——**光有数字不够,还要知道这个数字可不可信**。一个没做显著性检验的 nDCG 提升,和"感觉变好了"没本质区别。
- **对 Avaloka / 求职**:这是区分"业余调参"和"工程师"的分水岭。面试时能说出"我不会因为离线指标涨了 1 分就上线,会先跑配对 bootstrap 确认它统计显著、且超过实用阈值"——这是 RL/RAG 团队 manager 该有的严谨。这也直接呼应你之前问的 Goodhart:不做显著性检验就追指标,极易被噪声和套利骗到。

## 课堂截图：Interlude · The Sanity Checks That Are Allowed — BEIR, MTEB, MS MARCO in Their Proper Place（现场版本，页58）

标题 **"BEIR, MTEB, MS MARCO — in their proper place"**（把三大公共基准摆到它们该在的位置)——即"允许的 sanity check":

- **BEIR** — 18 个数据集、9 类任务,招牌指标 **NDCG@10**。最大惊喜:**BM25(纯稀疏)在许多 out-of-domain 任务上仍然打败稠密检索器**——这正是企业默认用 **hybrid(稀疏+稠密混合)** 的原因。
- **MTEB** — 58 个数据集;**选 embedding 模型**最常引用的排行榜。
- **MS MARCO** — 经典的段落排序基准,TREC-DL 赛道的底座。

右侧点破部署门:

> *"The deployment gate needs both: pass **your** gold-dataset threshold, and place respectably on the public boards. The first says it works for your users; the second says it is not inexplicably broken."*（部署门需要两个:通过**你自己的**金数据集阈值,且在公共榜上排名说得过去。前者说"它对你的用户管用",后者说"它没莫名其妙地坏掉"。)

**分析(页58):这页给公共基准一个"有限但正当"的位置,和 Act I "反对借用公共基准"呼应但不矛盾。**
- **双门部署判据**:① **你自己的金数据集**(主判据,证明"对你的用户管用");② **公共基准排名**(辅判据,sanity check,证明"没莫名坏掉")。两者分工——公共基准不能替代自建评估,但可以当"体检",防止你换的模型本身就是残缺的。
- **BM25 打败稠密检索的惊喜 = hybrid 存在的理由**:out-of-domain(领域外)时,纯语义检索会漏专有名词/精确匹配,而 BM25(关键词)反而稳。所以企业默认 hybrid(两者融合),这是前几周"混合检索"的一个硬证据。也再次说明"别迷信新技术"——老的 BM25 在很多场景仍是强 baseline。
- **MTEB 用途明确**:选 embedding 模型时查它。这对你 Avaloka 换 embedding 时有直接用处(当 nDCG↔Recall 诊断出"该修检索"时,去 MTEB 找候选 embedder)。

## 课堂截图：Interlude · Why "Shoot for 1,000" Was Never Arbitrary — Power Analysis Closes the Loop（现场版本，页60）

标题 **"Power analysis closes the loop"**（功效分析闭合了循环)——解释 Act I "目标 1000 query" 的统计根据:

> To detect a **1-point** absolute NDCG improvement with **80% power at α = 0.05** typically requires **N ≈ 500–1,000** queries.
> Act I's rule of thumb and the statistics agree almost exactly — the SME summit was doing power analysis without naming it.

翻译:要以 **80% 功效、显著性水平 α=0.05** 检测出 **1 分**的 NDCG 绝对提升,通常需要 **N≈500–1000** 个 query。Act I 的经验法则("目标 1000")和统计学几乎完全吻合——**SME Summit 其实在不知不觉中做了功效分析(power analysis)。**

右侧反向警告:

> *"Beware the other direction: with a huge eval set, **trivial improvements become statistically significant**. The practical threshold in enterprise: **0.02–0.05 absolute NDCG** is worth engineering effort; below that, statistical significance is not practical significance."*（小心反方向:eval 集太大时,**微不足道的提升也会变得统计显著**。企业实用阈值:**0.02–0.05 的 NDCG 绝对提升**才值得投工程;低于此,统计显著 ≠ 实用显著。）

**分析(页60):这页把"评估集规模"从经验数字升级成有统计学依据的决策,并厘清两种显著性。**
- **功效分析(power analysis)反推样本量**:给定你想检测的最小提升(1 分)、可接受的假阴性率(功效 80%)、假阳性率(α=0.05),数学上就能算出需要多少 query(≈500–1000)。**"目标 1000"不是拍脑袋,而是功效分析的结果。**
- **两个方向的坑**:① 样本太小(<200)→ 功效不足,真提升被噪声淹没,你会误以为"没用"而丢弃好改动;② 样本太大 → **连 0.001 的提升都会统计显著**,但那点提升不值得为它增加成本/复杂度。所以要同时看**统计显著(是真的吗)** 和**实用显著(值得吗,企业 nDCG 阈值 0.02–0.05)**。
- **对 Avaloka / 求职**:这给了两条可直接用的量化标准——① Avaloka EVAL 集按 500–1000 query 规划(够检测 1 分提升);② 上线判据设为"nDCG 提升 ≥ 0.02–0.05 且配对检验显著"。面试讲评估纪律时,这两个数字比空谈"要做 A/B 测试"具体得多。
- **补记(页59未截)**:页58 与 60 之间的页59应是统计显著性检验的具体方法(**配对 bootstrap / 置换检验**,判断两系统 nDCG 差异是否显著),待补截图。

## 课堂截图：Interlude · The Dimension the Six Metrics Miss — Diversity, and Maximal Marginal Relevance（现场版本，页61）

标题 **"Diversity, and Maximal Marginal Relevance"**（多样性,以及最大边际相关 MMR)——点出**六个指标都漏掉的第七维:多样性**。公式:

$$MMR = \arg\max_{d\in R\setminus S}\Big[\lambda\,\text{Sim}_1(d,q) - (1-\lambda)\max_{d'\in S}\text{Sim}_2(d,d')\Big]$$

> Ten near-duplicates can score perfect precision, recall, and NDCG — and serve a **poor** experience: homogeneous evidence, an illusion of consensus that is really redundancy. MMR picks each next result by relevance **minus** similarity to what is already picked.

翻译:十个近重复文档可以在 precision、recall、NDCG 上全拿满分,却给出**糟糕**的体验:同质的证据、一种其实是冗余的"伪共识"。MMR 每次挑下一个结果时,用"**与 query 的相关性 减去 与已选结果的相似度**"来打分。

右侧调参与评估:

> *"λ = 1: ordinary top-k. Production: λ ∈ [0.5, 0.8]. Diversity-aware retrieval lifts multi-hop answer quality 6–12%; but λ < 0.3 hurts simple factoids. Tune on the gold set; **α-NDCG** scores it."*（λ=1 就是普通 top-k。生产环境 λ∈[0.5,0.8]。多样性感知检索能把多跳答案质量提升 6–12%;但 λ<0.3 会伤害简单事实型查询。在金数据集上调 λ;用 **α-NDCG** 来评估多样性。）

**分析(页61):这页补上前面所有指标(含 nDCG)的共同盲点——多样性。**
- **盲点本质**:Precision/Recall/nDCG 只看"每个结果单独有多相关",**不看结果之间彼此有多像**。所以返回 10 个近重复的完美相关文档能刷满所有指标,但用户得到的是**冗余而非信息**——十条说同一件事,制造"大家都这么说"的假共识。
- **MMR 的机制**:`λ·相关性 − (1−λ)·与已选集的最大相似度`。第一项奖励"与 query 相关",第二项惩罚"和已经选中的太像"。λ 调两者权重:λ=1 完全不管多样性(普通 top-k),λ 越小越强调多样性。
- **λ 的取舍(实用数字)**:生产用 **λ∈[0.5,0.8]**;多样性感知能把**多跳答案质量提升 6–12%**(因为多跳需要不同角度的证据);但 **λ<0.3 会伤简单事实型查询**(事实型只要一个准确答案,过度多样反而把对的挤掉)。**又是"按查询意图调参"**——多跳要多样,事实型要精准。
- **α-NDCG**:专门评估"多样性"的 nDCG 变体,在金数据集上调 λ 时用它打分。
- **和前几周的关系**:这补上了 Week 3/4 提到的多样性/去重,并给了它一个可评估的指标。**对 Avaloka**:调取多条护理记忆做综合判断时(多跳型),该用 MMR 保证记忆的多样性(不同时间/不同侧面),避免十条都在说同一件事;而事实型查询("过敏原")则保持高 λ 要精准。

## 课堂截图：Milestone · Act III of IV — The Generator（现场版本，页64）

进入 Act III 的过场页,视觉用元素周期表符号 **"Rg"**(Roentgenium;这里借代 **R**etrieval→**G**eneration 或 generator)配刻度环。副标题:

> *"The ingredients do not make the meal. Six metrics judged the pantry; now we judge the chef."*（食材本身成不了一顿饭。六个指标评判的是食品储藏室(the pantry);现在我们要评判厨师(the chef)。)

> 注:现场页码从 61(MMR)跳到 64,中间 62–63 未截到(应是 Interlude 收尾 / Act III 引子),待补。

**分析:这页标志本周评估的重大转向——从"检索评估"到"生成评估"。**
- **核心隐喻:食材 vs 一顿饭**。Act II 的六个检索指标(Recall/nDCG…)评的是**"取回的证据好不好"= 食品储藏室里的食材**;但食材好 ≠ 菜好吃。Act III 转向评判**"生成器(LLM)有没有用好这些证据"= 厨师的手艺**。
- **为什么这是关键转向**:一个 RAG 系统即使检索完美(nDCG=1.0,把最相关文档全排最前),LLM 仍可能**忽略证据、编造、答非所问、或引用错误来源**。检索指标对这些完全失明——它们只看"喂给 LLM 的料对不对",不看"LLM 做出来的菜对不对"。
- **Act III 要讲的(生成评估工具箱)**:接下来是 **RAGAS**(faithfulness/answer relevancy/context precision/context recall 四指标 + 五局限)、**声明级蕴含**(FActScore、ALCE 引用质量)、**LLM-as-a-Judge**(Prometheus-2、评委偏见、Cohen's κ 校准)、**RGB 四能力**(噪声鲁棒/负拒绝/信息整合/反事实鲁棒)。
- **和 Week 6 的接续**:Week 6 的响应侧"良知"(grounding/faithfulness)是**机制**(断言-证据二部图);Act III 是给这个机制配**指标**(FActScore 等)——"机制已在,补上度量"。
- **对 Avaloka**:检索到正确的护理记忆只是第一步(pantry),真正要评的是 Avaloka 的回应有没有**忠实于**那些记忆、有没有编造、该拒答时有没有拒答(chef)。这正是安全的核心,也是 Week 6+Week 7 合起来给 Avaloka 的完整评估框架。

## 课堂截图：Act I · Two Ways the Ruler Rots — Eval Decay, and Overfitting Your Own Yardstick（现场版本，页15，补记）

> 补记:这张是页 15,填上之前"Act I 页 14–15 未截"的空缺。

标题 **"Eval decay, and overfitting your own yardstick"**（尺子腐烂的两种方式:评估衰减,和过拟合你自己的尺子)——即使建好了金数据集,它也会以两种方式"烂掉":

> **Eval decay** — the corpus evolves; January's most-relevant document is superseded in June; stale judgements quietly poison every metric. Refresh on a schedule.
> **Overfitting** — if engineers know the queries, even implicitly, they optimise for **those** queries.

翻译:
- **评估衰减(eval decay)**:语料在演进——一月份最相关的文档,到六月可能被更新的取代;**过时的相关性判断会悄悄毒化每一个指标**。要**定期刷新**金数据集。
- **过拟合(overfitting)**:如果工程师(哪怕无意中)知道了评估集里的 query,他们就会**专门为那些 query 优化**——系统在评估集上分很高,但对真实新 query 未必好。

右侧关键做法:

> *"Keep a held-out test set that only the evaluation lead controls. A yardstick everyone has memorised is no longer a yardstick — **it is a target**. (Goodhart will return in Act IV.)"*（留一个只有评估负责人能碰的 held-out 测试集。一把所有人都背下来的尺子,就不再是尺子——**它变成了目标**。Goodhart 会在 Act IV 回归。)

**分析:这页讲金数据集的"维护与防作弊",是 Act I 的重要补充。**
- **两种腐烂是正交的**:① eval decay 是**时间**问题(语料变了,旧标注过期)→ 定期刷新;② overfitting 是**信息泄露**问题(工程师看过题,专门刷分)→ 隔离 held-out 集。
- **"a yardstick everyone has memorised is a target, not a yardstick"是全页题眼**:这正是 **Goodhart 定律**的种子(讲师明说"Act IV 会回归")——**评估集一旦被工程师熟记并针对性优化,它就从"测量真实能力的尺子"退化成"被套利的目标"**,分数虚高但不反映真实质量。这和 Week 07 优化目标公式 argmax_θ μ 完美对应:如果 θ 能偷看 μ 用的那批 q,它会过拟合到那批 q 而非真实分布 𝒬。
- **解法 = held-out 测试集 + 单人管控**:留一份只有"评估负责人(evaluation lead)"能碰的测试集,工程师看不到 → 无法针对性优化 → 分数才可信。这和 Week 07 后面讲的"held-out 金评委防漂移"、以及防 reward hacking 是同一套思想。
- **对 Avaloka / 求职**:这给了两条运维纪律——① Avaloka EVAL 集要**版本化 + 定期刷新**(应对记忆库/需求演进);② 留一份**你(评估负责人)独控的 held-out 集**,别让调系统的过程看到全部测试 query。面试讲评估治理时,"held-out 集防过拟合、定期刷新防衰减"是很专业的两点。

## 课堂补充演讲：The New Path · Software Careers in the AI Era（另一套 deck，与评估课不同）

> 注:这是 Week 07 课堂上放的**另一套幻灯片**(共 15 页,紫色/等宽风格),主题是 AI 时代的软件职业路径,和《The Measure of All Things》评估课是两个独立 deck。因与 Rosso 求职(T010、RL manager 岗)高度相关,单独在此记录,后续可迁移到 `reviews/05-ai-career-positioning-and-linkedin.md`。

> 这套 deck 是**今天(2026-07-25)下半场**的内容,评估课(上半场)结束后放的。

### 页 01/15 — The Bootcamp(old way)-to-Job Pipeline Is Dead

标题 **"The Bootcamp (old way)-to-Job Pipeline Is Dead."**(旧的"训练营→工作"流水线已死),副标 **"How AI coding assistants took away the entry-level job in software — and what replaced it."**(AI 编程助手如何拿走了软件业的入门级工作——以及取而代之的是什么)。

**分析(初步,待后续页补充):**
- **核心论点**:AI 编程助手(Copilot、Cursor、Claude Code 等)吃掉了传统的**入门级/初级软件岗**——过去"读个训练营 → 写 CRUD → 拿 junior 岗"的路径不再成立,因为那些最容易被 AI 替代的正是 junior 的日常工作。
- **对 Rosso 的直接关系**:这恰好呼应你之前问的 RL manager 方向——**当入门级"写代码"岗被压缩,价值上移到"判断/评估/架构/管理"层**。这正是 Week 07 一整天在训练的能力(评估纪律、指标设计、reward/Goodhart 判断),也是本课程 T010 求职叙事的底层逻辑:不靠"会写代码"竞争,靠"会判断系统好不好、会设计评估、会管 AI/RL 团队"竞争。
- **待补**:剩余页(新路径具体是什么、什么技能取代了 entry-level coding)对你求职极有价值,继续发我会逐页记并接到求职材料上。

### 页 03/15 — The Old Path, and Why It Actually Worked（2019–2023）

回顾 2019–2023 的"旧路径"五步:

| 步 | 内容 | 细节 |
|---|---|---|
| 01 | Learn to code | 3–6 个月,训练营或自学 |
| 02 | Build a portfolio | Todo apps、clones、CRUD 项目 |
| 03 | Apply in volume | 海投 junior 岗 |
| 04 | Get hired | $60–80K,拿到入场券(foot in the door) |
| 05 | **Learn on the job** | **真正的教育从这里开始** |

底部"它其实是什么(what it really was)":

> **A subsidized apprenticeship wearing a job title.**（一个披着"职位头衔"外衣的、被补贴的学徒制。）Companies paid for **potential, not output** — a junior was a **net cost for 6–18 months**, and everyone knew it. Simple tickets existed in bulk and made good training material; mentoring paid off in years 2 and 3; growing your own talent beat bidding for someone else's.
> *// nobody wrote 'apprenticeship program' on a budget line — it was just how the industry trained people*

翻译要点:公司过去为**潜力**买单,不是为**产出**——一个 junior 在头 6–18 个月是**净成本(赔钱的)**,大家都心知肚明。但当时行得通,因为:① 大量简单工单存在,是很好的训练材料;② 师徒制在第 2、3 年才回本;③ **自己培养人才比去市场抢现成的更划算**。没人在预算表上写"学徒项目"——但这就是行业培养人的方式。

**分析:这页是"旧路径为什么曾经成立"的诊断,为下一步"它为什么崩了"铺垫。**
- **关键洞察:junior 岗本质是"补贴学徒制"**。企业明知 junior 头一两年赔钱,还愿意招,是因为**简单工单(net cost 的来源)同时也是训练材料**——正是靠做这些简单活,junior 才成长为 senior。这是一个**隐性的、没写进预算的人才培养机制**。
- **为什么这对理解"AI 时代"至关重要**:下一步论点几乎必然是——**AI 编程助手把那些"简单工单"做掉了**。而简单工单一旦消失,junior 就只剩"净成本"、失去了"训练材料"这个存在理由。于是"补贴学徒制"的经济基础崩塌,入门级岗随之消失。**AI 拿走的不只是工作,是整个"边做边学"的培养阶梯。**
- **对 Rosso 的意义(承上启下)**:这解释了为什么价值上移到"判断/评估/管理"层——当"做简单活成长为 senior"的路径断了,能直接提供"判断力、评估力、架构力"(即 senior/manager 能力)的人反而更稀缺、更值钱。Week 07 一整天教的评估纪律,正是这种"上层能力"。你的求职叙事应该**跳过"我会写代码"**,直接站在"我能判断 AI 系统好不好、能设计评估、能管 RL/RAG 团队"的位置——因为旧的"junior 阶梯"已经不是你的竞争赛道。

### 页 04/15 — What Broke · The Data: Surgical, Not Cyclical

标题 **"Surgical, not cyclical"**（是外科手术式的精准切割,不是周期性衰退)。用数据证明"入门级岗消失"不是经济周期,而是 AI 精准切掉了某一层。

左侧柱状图 **Developer employment, late 2022 → mid-2025**(同岗位、同公司,来源 Stanford / ADP 薪资数据):
- **22–25 岁:−20%**(年轻/入门层就业大幅下滑)
- **35–49 岁:+7.5%**(资深层反而增长)

右侧五个数字:
- **−25%** — entry-level 科技招聘同比(2024)
- **−30%** — 科技实习岗位(自 2023,而**申请数反而上升**)
- **6.1%** — CS 毕业生失业率——**比美术专业还差**
- **84%** — 开发者现在使用 AI 工具(Stack Overflow, 2025)
- **57%** — 招聘经理**更信任 AI 产出、而非应届生的工作**

底部金句:

> *// a recession cuts everywhere — this cut follows one line exactly: what AI can do today, and what it can't*（经济衰退是到处砍;而这次切割精确地沿着一条线:AI 今天能做什么、不能做什么。）

**分析:这页是全 deck 的实证核心,用数据把"AI 拿走入门岗"从观点变成事实。**
- **"surgical not cyclical"是最强论点**:如果是经济衰退(cyclical),各年龄层都会被砍。但数据显示 **22–25 岁 −20%、35–49 岁 +7.5%**——**只砍年轻/入门层,资深层反增**。这条"切割线"不符合衰退模式,只符合"AI 能替代什么"的模式。**这是排除了'经济周期'这个替代解释的关键证据。**
- **数据链条自洽**:入门岗 −25%、实习 −30% 但申请上升(供需恶化)、CS 失业率 6.1% 超过美术专业(反直觉,曾经最稳的专业现在最惨)、84% 开发者用 AI、57% 招聘经理更信 AI 产出而非应届生——**每个数字都指向同一结论:AI 已能做 junior 的活,且雇主已经这么认为了。**
- **对 Rosso 的直接冲击与出路**:
  - **冲击**:这条数据线说明"补 junior 的坑再往上爬"在今天基本行不通,尤其对转行/大龄求职者更不利(年龄那栏对年轻入门层最狠)。
  - **出路**:注意 **35–49 岁 +7.5%** 和"招聘经理更信 AI 产出"——市场要的是**能驾驭/评估 AI 产出的人**,不是和 AI 抢写代码的人。你的定位应该落在那 +7.5% 的"资深/判断层":能评估 AI 系统、设计评估体系、管理 AI/RL 团队。**Week 07 的评估能力恰好是"信任但要核验 AI 产出"的核心技能**——当 57% 招聘经理"信任 AI 产出"时,能系统性地**验证 AI 产出到底可不可信**(faithfulness、Goodhart、held-out 评估)的人,正是稀缺且不可替代的。
- **求职话术素材**:"AI 已能生成代码,但企业最缺的是能判断这些产出是否可信、并对系统质量负责的人——这正是我这一年在企业 RAG 评估上建立的能力。"

### 页 05/15 — The Reasoning: Why AI Took Out This Rung, and Not the Others

标题 **"Why AI took out this rung — and not the others"**（为什么 AI 砍掉的是这一级阶梯,而不是其他级)。用两栏对比"junior 做的事" vs "senior 做的事":

**左栏 · WHAT JUNIORS DID — Codified Knowledge(可编码的知识)** ✗
- CRUD 端点、有文档的 bug 修复、表单校验
- 清晰的 spec、已知的模式(known patterns)
- 海量公开训练数据
- **= exactly the work LLMs do best(正是 LLM 最擅长的活)**

**右栏 · WHAT SENIORS DO — Tacit Judgment(隐性判断)** ✓
- 哪条需求其实是**错的**
- 哪个捷径会在**八个月后爆炸**
- 遗留系统**默默假设了什么**
- **= AI augments it. It doesn't replace it(AI 增强它,但不能取代它)**

高亮框结论:

> **The bottom rungs of the ladder were made of exactly the material AI dissolves. The top rungs weren't.**（阶梯的底层台阶,恰恰是用 AI 能溶解的材料做的;顶层台阶不是。）
> *// this split predicts where the damage lands next: any role built on well-specified tasks is exposed*（这条分界线预测了下一波伤害落在哪:任何建立在"良好定义的任务"之上的岗位都暴露在风险中。）

**分析:这页给出"为什么是入门岗"的机制解释,并给出一个可用于自我诊断的判据。**
- **核心区分:可编码知识(codified) vs 隐性判断(tacit)**。junior 的活是**可编码的**——有清晰 spec、已知模式、海量公开数据,这三点正好是 LLM 训练和擅长的全部前提。senior 的活是**隐性判断**——判断"需求本身对不对""哪个捷径会埋雷""遗留系统的隐藏假设",这些**没有 spec、没有训练数据、需要上下文和经验**,AI 只能增强不能替代。
- **判据(可自测)**:底部那句 **"any role built on well-specified tasks is exposed"** 是一把尺子——**如果你的工作可以被写成清晰的规格说明,它就危险;如果你的价值在于"判断规格本身对不对/发现没被说出来的假设",它就安全。**
- **和评估课的深层呼应(这页对你最关键)**:Week 07 教的评估,本质上**全是 tacit judgment 类的工作**——
  - "这个指标提升是真的还是噪声?"(判断)
  - "这个 reward 会被怎么 hack?"(预见八个月后爆炸的捷径)
  - "这个金数据集有没有过拟合/泄露?"(发现隐藏假设)
  - "该修检索还是 reranker?"(在没有明确 spec 的情况下诊断)
  **评估工作天生落在右栏(senior/tacit),这正是它 AI 替代不了、且价值上升的原因。**
- **对 Rosso 求职的战略结论**:你的叙事要把自己牢牢放在**右栏**。不要展示"我能写 CRUD/能实现某算法"(左栏,已贬值),要展示"**我能判断 AI/RAG 系统哪里会出问题、能设计评估体系发现隐藏失败、能预见架构决策的长期代价**"。RL manager 岗尤其如此——manager 的核心就是 tacit judgment(判断团队方向、reward 设计对不对),而不是可编码的产出。这套 deck 和评估课在这一页**完美合流**:评估能力 = 右栏能力 = AI 时代的安全区。

### 页 06/15 — The Economics: The Math Stopped Working

标题 **"The math stopped working"**（这笔账算不下去了）。用成本对比解释入门岗消失的经济逻辑:

| THE JUNIOR HIRE ✗ | THE AI ASSISTANT ✓ |
|---|---|
| **$90K+ / 年** | **$20–200 / 月** |
| 全成本,外加数月资深指导 | 同一档产出,即时可用,无需 onboarding |
| 头 6–18 个月只有样板级产出 | 一个资深 + AI = 一个资深 + 1–2 个 junior 的产能 |

左下 **57%** — 招聘经理更信任 AI 产出而非应届生工作。

右侧核心论断:

> **The cover story is gone.** Companies were never buying junior **output** — they were buying **future seniors**. AI didn't beat juniors on value; it **removed the pile of simple work that hid the apprenticeship subsidy**. Once the subsidy showed up as a budget line, it got cut. Anyone who has sat through enough enterprise budget cycles knows exactly how that meeting goes.

翻译:**"掩护故事"消失了。** 公司过去买的从来不是 junior 的**产出**,而是**未来的 senior**。AI 不是在"价值"上打败了 junior——它**移除了那堆掩盖着"学徒补贴"的简单工作**。一旦这笔补贴以预算项的形式暴露出来,它就会被砍掉。任何经历过足够多企业预算周期的人,都清楚那个会是怎么开的。

**分析:这页是对页03"补贴学徒制"的经济学收尾,论证极其精准。**
- **成本悬殊($90K/年 vs $20–200/月)只是表象**,真正的杀招在右侧那段:**junior 的经济学从来靠"简单工作"这层掩护维持**。企业不是为 junior 头两年的产出付钱(那是净成本),是为"两三年后变成 senior"这个未来付钱。这笔"学徒补贴"能存在,是因为它**藏在一堆简单工单里,没人单独盯它**。
- **AI 的真正打击点(反直觉)**:AI 不是"比 junior 便宜/好"这么简单——它是**抽走了那堆简单工单,让补贴无处藏身**。一旦"我们每年花 X 万补贴一个两年后才产出的人"变成预算表上一行显式数字,财务一定砍它。**这是"隐性成本被显性化后必然被优化掉"的经典企业行为**——和 Week 07 讲的"golden dataset 一旦被熟记就变成 target"是同构的:一个东西一旦被单独度量/暴露,它的行为逻辑就变了。
- **对 Rosso 的双重启示**:
  - **警示**:不要把自己定位成"便宜的产出提供者"——在 $20–200/月的 AI 面前,任何以"产出量/速度"为卖点的定位都输。
  - **出路**:定位成**那个"resistant to being budget-lined"的价值**——即价值无法被简单量化成"每月产出 X",而是体现在"避免了某个八个月后会爆的架构错误""建立了让整个团队产出可信的评估体系"。这类价值**没法被 AI 的月费替代,也没法被砍**,因为它不是"一堆简单工作",而是判断和治理。这正是评估/manager 岗的护城河。
- **求职话术素材**:"AI 让'廉价产出'这个卖点归零。我提供的不是产出量,而是让团队和 AI 的产出可被信任的评估与治理能力——这是唯一不会在预算周期里被砍掉的那类价值。"

### 页 07/15 — The Second-Order Effect: The Industry Is Eating Its Seed Corn

标题 **"The industry is eating its seed corn"**（这个行业正在吃自己的种子粮）——"吃种子粮"= 为眼前利益消耗掉未来的根本。三段式时间线预测二阶后果:

| 时间 | 状态 | 说明 |
|---|---|---|
| **2026** | Juniors not hired | 公司砍入门岗,利润率变好看。**局部看,每个决策都是理性的。** |
| **2028–29** | Mid-levels missing | 本该存在的中级工程师不存在了——因为没人当年招他们当 junior。**中级招聘变得残酷。** |
| **2030–31** | Senior shortage | 资深梯队后面没有 pipeline。顶级薪资飙升。机构知识随人老去而流失。 |

底部 **THE COMMONS PROBLEM(公地悲剧)**:

> **Everyone is hoping somebody else trains the next generation. Nobody is.** Stack a quality problem on top: "AI-native" developers who can generate code but **never built the mental models to verify it** will ship systems whose failure modes nobody on the team understands.
> *// the scarce skill in 2030 won't be writing code — it will be knowing when the code is wrong*

翻译:**每个人都指望别人去培养下一代。结果没人在培养。** 再叠加一个质量问题:"AI 原生"的开发者能生成代码,却**从未建立起验证代码的心智模型**,他们交付的系统,其失败模式团队里没人搞得懂。金句:**2030 年稀缺的技能不是写代码,而是知道代码什么时候是错的。**

**分析:这页把个体理性 → 集体灾难的链条讲透,并给出全 deck 最重要的一句职业预言。**
- **公地悲剧(commons problem)的机制**:2026 年每家公司砍 junior 都是**局部理性**(margin 好看),但所有公司都这么做 → 没人培养新人 → 2028 缺中级 → 2030 缺资深。**每一步都理性,合起来是灾难**——这是经典的"个体最优 ≠ 集体最优"。
- **"eating seed corn(吃种子粮)"隐喻精准**:junior 就是行业的"种子"——今天吃掉(不招)省了钱,但明天没了收成(没有 senior)。企业在用未来的人才断层换今天的利润率。
- **叠加的质量灾难**:AI-native 开发者"会生成不会验证"——**这直接呼应页05的左栏/右栏**:他们只有可编码技能(生成),没有 tacit judgment(验证)。结果是"没人懂失败模式"的系统被交付。
- **金句是全 deck 的题眼,也是对 Rosso 最直接的定位指引**:**"2030 年稀缺的技能不是写代码,而是知道代码什么时候是错的。"** ——这几乎就是**评估(evaluation)的一句话定义**。Week 07 一整天教的 faithfulness、Goodhart、诊断、held-out 验证,本质全是"**知道系统什么时候是错的**"。这套 deck 和评估课在这句话上彻底合流:
  - "知道 nDCG 提升是真是假"= 知道指标什么时候骗你
  - "知道 reward 会被怎么 hack"= 知道优化什么时候会出错
  - "知道该修检索还是 reranker"= 知道系统哪里错了
- **对求职的战略含义(最强素材)**:市场正在制造一个**验证能力的真空**——大量人能让 AI 生成东西,极少人能判断这些东西对不对。你要把自己定位成**填这个真空的人**:"我不是和 AI 抢生成,我提供的是 2030 年真正稀缺的那个技能——知道 AI/系统的产出什么时候是错的,并有方法证明它。"这对 **RL/AI 团队 manager** 岗尤其致命有力,因为 manager 的核心职责就是对团队产出的正确性负责。

### 页 08/15 — The Core Shift: When Code Creation Is (Seems) Free, Judgment Captures the Value

标题 **"When code creation is (seems) free, judgment captures the value."**（当代码生产(看似)免费时,价值被"判断"所捕获）。用三段式讲"约束点的转移":

| 时期 | 约束在哪 |
|---|---|
| **FOR 70 YEARS** | 约束在**生产**——写出正确代码又慢又贵 |
| **THEN AI** | 让生产**近乎免费**。代码生成变成以"分"计价的商品 |
| **NOW** | 约束**转移到了验证(verification)**:这段代码对吗?安全吗?可维护吗?**是不是在解决正确的问题?** |

底部金句:

> *// auditing. evals. system design. taste. every durable skill on the new path is a verification skill*（审计、评估、系统设计、品味——新路径上每一个持久的技能,都是一种验证技能。）

**分析:这页是整套求职 deck 的理论核心,也是与 Week 07 评估课绑定最紧的一页。**
- **"约束点转移(the constraint moved)"是经济学的关键框架**:任何生产链条里,**价值总是流向那个稀缺的约束环节**。70 年来约束是"生产代码"(慢、贵),所以会写代码的人值钱;AI 让生产近乎免费后,**约束不再是生产,而是验证**——于是价值从"能生产"流向"能验证"。这是一次结构性的价值再分配,不是暂时现象。
- **"judgment captures the value"精确回应了页05的 tacit judgment**:当左栏(生产/可编码)被 AI 拿走,价值全部流向右栏(判断/验证)。这三页(05 机制、07 预言、08 理论)构成完整论证:**为什么价值必然上移到判断层。**
- **底部那句是把评估课"翻译成职业语言"的钥匙**:"auditing, evals, system design, taste — every durable skill is a verification skill." ——**evals(评估)被直接点名为核心持久技能**。Week 07 你学的正是 evals 的完整方法论。这套 deck 等于在告诉你:**你今天上午学的东西,不是一个技术细节,而是 AI 时代唯一持久增值的技能类别。**
- **"是不是在解决正确的问题(the right problem)"是验证的最高层**:注意 NOW 那栏不只问"对不对/安全不安全/可维护不可维护",还问"**是不是正确的问题**"——这是比技术验证更高一层的判断,对应 manager/架构层。RL manager 岗的核心正是这个:不是验证某段代码,而是**验证整个方向/reward/目标设定对不对**。
- **对 Rosso 的求职定位(可直接用作个人陈述框架)**:
  - 旧世界卖点:"我会生产 X"(已贬值)
  - 新世界卖点:"我能**验证** X ——判断它对不对、安全不安全、可维护不可维护、以及是不是正确的问题"
  - 你的具体证据:企业 RAG 评估体系(faithfulness/nDCG/Goodhart 防护)、Avaloka 的评估-优先架构、Week 07 的完整评估方法论。**把这些统一叙述成"我是做 verification 的人"**,正好卡在这套 deck 说的"新路径上唯一持久的技能类别"上。

### 页 09/15 — The New Path · Entry Profile: The Entry Profile That Actually Gets Hired

标题 **"The entry profile that actually gets hired"**（真正能被录用的新入门画像）。四个能力 R1–R4:

- **R1 · Code auditor before code writer(先做代码审计者,再做代码编写者)**:审查 AI 生成的代码——抓 off-by-one、漏掉的鉴权检查、N+1 查询、根本不存在的 API。**批判性阅读过去是中级技能,现在是入门技能。**
- **R2 · System design literacy on day one(第一天就要有系统设计素养)**:当实现变便宜,**设计成了瓶颈**。要懂为什么服务这样拆分、状态存在哪、什么会一起挂掉。**过去第三年才有的知识,现在前置到入门。**
- **R3 · Evaluation engineering(评估工程)**:构建**验证 AI 产出的测试框架**——test suites、eval pipelines、guardrails、回归检测。**一个全新的学科——也是少数"新人能打败老手"的地方。**
- **R4 · Directing AI agents(指挥 AI 智能体)**:拆解任务、设定约束、审查产出、**知道 agent 什么时候自信地错了**。把 LLM 当成一个"快、聪明、健忘的 junior"。**一种管理技能——现在入门就要求。**

底部金句:

> *// the old path proved you could write code — the new path proves you can be trusted with judgment*（旧路径证明你会写代码;新路径证明你可以被托付以判断。）

**分析:这页把前面所有"抽象趋势"落成 4 个可操作的能力项,而且每一条你都已经在做。**
- **四条全是"验证/判断"能力**,和页08"every durable skill is a verification skill"完全对应。R1 审计、R2 设计、R3 评估、R4 指挥 agent——**没有一条是"写代码"**,全是围绕"判断 AI 产出对不对、系统该怎么搭"。
- **R3 = 评估工程,几乎就是 Week 07 的课程大纲**:"test suites、eval pipelines、guardrails、regression detection"——这正是你今天上午学的全部(金数据集、nDCG/faithfulness、guardrails 是 Week 06、回归检测是"delta between builds")。而且这页明说 R3 是 **"one place where early beats experienced"(新人能打败老手的地方)**——因为评估工程是**新学科**,老手也没有几十年积累,**你和资深者站在同一起跑线**。这对转行/大龄求职者是极其重要的利好:你不必在"写代码经验"上和人拼,可以在评估这个新赛道上直接竞争。
- **R4 = 指挥 AI agent,直接对应你的 RL/AI manager 方向**:"把 LLM 当快、聪明、健忘的 junior 来管"——**这本质就是管理技能**,而且明说"now required at entry(入门就要求)"。你申的 manager 岗,R4 正是核心,而你在 Avaloka/Forge AI 上做的 agent 编排(intent→retrieve→decide→respond→trace→evaluate)就是 R4 的直接证据。
- **底部金句是整个求职叙事的一句话总纲**:**"旧路径证明你会写代码;新路径证明你可以被托付以判断。"** ——你的简历/面试要证明的不是"我能写",而是"**我可以被信任来做判断**"。
- **对 Rosso 的行动建议(可直接映射到 T010 材料)**:把你的经历按 R1–R4 重新归类打包——
  - R1 审计:你在 RAG 项目里 review/诊断检索与生成失败
  - R2 系统设计:Avaloka 的 agent-first 架构、证据驱动升级决策
  - R3 评估工程:Week 07 方法论 + 你写的 eval demo + Avaloka EVAL 集设计
  - R4 指挥 agent:多阶段 agent 循环编排、guardrails、trace
  **四个格子填满,就是一份"新路径入门画像"的完整证据链**——而你其实已经是 mid/senior 级,不是 entry。

### 页 10/15 — The Portfolio Bar Moved Too: Proof of Work Beats Proof of Study

标题 **"Proof of work beats proof of study"**（工作证明胜过学习证明）——作品集的评判标准也变了。

**NO LONGER A SIGNAL(不再是信号)** ✗
- Todo apps 和教程克隆——**AI 一个 prompt 就能产出一个**
- 训练营证书作为招牌资历
- 287 份"海投碰运气"的申请漏斗
- Leetcode 刷题——**测的是 AI 已经商品化的技能**

**THE NEW SIGNAL(新的信号)** ✓
- **一个有真实用户的已上线产品**——一个小众工具的 50 个真实用户,胜过 5 个精致的克隆
- **合并进你没写过的代码库的 PR**(向真实开源/团队项目贡献)
- **written technical judgment(书面的技术判断)**:事后复盘(postmortems)、设计文档、"我为什么否决了那个显而易见的方案"
- **领域深度(domain depth)**:物流、医疗计费、薪资等具体行业

底部:

> **The real apprenticeship is coming back:** companies still hiring at the bottom run **deliberate programs** — fewer hires, higher bar, explicit training in **architecture, security, and AI governance**. The easy tickets were the old curriculum. They're gone, so training now has to be **on purpose**.
> *// the trades always trained this way — structured, intentional, with a real bar. software is rediscovering it*

翻译:**真正的学徒制正在回归**:仍在招入门的公司会办**刻意设计的项目**——招得更少、门槛更高、明确培训**架构、安全、AI 治理**。简单工单曾是旧课程,如今它们没了,所以培训必须是**有意为之**的。金句:传统技工行业一直是这样培养人的——**结构化、有意图、有真实门槛;软件业正在重新发现它。**

**分析:这页把"怎么证明自己"具体化,而且新标准每一条你都占优。**
- **核心转变:proof of study → proof of work**。学过什么(证书、课程、刷题)不再是信号,因为 AI 让"会做这些"变得廉价;**做成了什么真实的东西**才是信号。评判从"你能力如何"转向"你交付了什么真实价值 + 你的判断留下了什么痕迹"。
- **"written technical judgment"是最关键的新信号,也和评估课直接相关**:postmortems、design docs、"我为什么否决了显而易见的方案"——这些都是**把 tacit judgment 显性化、可展示化**的载体。你项目里的 **decision log(决策日志)、ADR、Week 07 的评估笔记本身就是这种"书面技术判断"** ——你已经在系统性地生产这类证据了(AGENTS.md 要求的决策记录纪律)。
- **"proof of work"每一条你都有真货**:
  - 已上线有真实用户的产品 → Avaloka / Forge AI / Auralith
  - 领域深度 → 你在企业 RAG、护理记忆等具体场景的深耕
  - 书面技术判断 → 你整个项目的 decision log + 这份 Week 07 评估笔记 + eval demo
  **你不缺 proof of work,缺的是把它按这套语言重新包装展示。**
- **"AI governance(AI 治理)"被明确列入新培训重点**:这直接对应 Week 06(guardrails)+ Week 07(evaluation)——**你正在学的正是企业新学徒制要培训的核心内容**。你不是"需要被培训的入门者",你是"已经具备这套稀缺能力的人"。
- **对 Rosso 的行动(强化 T010)**:求职材料别再堆"学了什么/上了什么课",要展示**三类 proof of work**:① 有真实用户的产品(带数字);② 书面技术判断(挑 2–3 个决策日志/postmortem 改写成对外可读的 design doc);③ 领域深度(讲清你在哪个具体行业场景有别人没有的理解)。这正是"proof of work beats proof of study"的落地。

### 页 11/15 — Perspective · Three Previous Panics: The Door Moved. It Didn't Close.

标题 **"The door moved. It didn't close."**（门移动了,但没有关上）——给前面偏悲观的论述一个**平衡视角**:历史上类似恐慌都以"需求超过自动化"收场,但这轮有真正的不同。

**左栏 · THREE PANICS, SAME ENDING(三次恐慌,同一个结局)**
- **2001** dot-com 崩盘——"入门级工程师已死"
- **2000s** 离岸外包——"所有编程工作都在流失"
- **2010s** SDN——"网络工程师完蛋了"
- ✓ **every time, demand outgrew the automation(每一次,需求都超过了自动化)**

**右栏 · WHAT'S DIFFERENT THIS ROUND(这一轮有何不同)** ✗
- 以前的浪潮自动化的是**工具**;这一轮自动化的是**训练材料**——junior 赖以学习的简单工作。**需求可以恢复,但那条(培养)路径依然是断的。**
- 薪资数据显示这是**针对年龄的替代(age-targeted displacement)**;以前的浪潮都没有这个特征。

**底部 · THE WILDCARD(意外变量)**:

> **Demand shows up where nobody's looking.** When software gets 10x cheaper to build, organizations that never employed developers start doing it — small businesses, local governments, professional practices. It looks like **freelance work, internal tools, and micro-SaaS**.
> *// Chris's 287 applications all went to the shrinking pool — the growing one doesn't post job listings*

翻译:**需求会出现在没人注意的地方。** 当软件的构建成本降到 1/10,那些从没雇过开发者的组织(小企业、地方政府、专业事务所)开始自己做软件。它的形态是**自由职业、内部工具、和 micro-SaaS(微型 SaaS)**。金句:Chris 投的 287 份申请全投进了那个**在萎缩的池子**——那个**在增长的池子根本不发招聘启事。**

**分析:这页是全 deck 最重要的"平衡与出路"页,把悲观诊断转成可行动的方向。**
- **两面都要握住**:① 历史安慰——每次"XX 已死"最后都是需求超过自动化(不必绝望);② 但**诚实地指出这轮的两个真正不同**:自动化的是"训练材料"(所以培养路径断了,不只是岗位少了)、且是"针对年龄"的替代(对不同年龄段冲击不均)。**这是全 deck 少见的自我批判,增加了可信度**——它没有为了煽动而夸大,承认了历史规律,同时点明这轮的特殊性。
- **"age-targeted displacement"对你(Rosso)是需要正视的现实**:数据显示这轮替代和年龄相关(呼应页04 的 22–25 岁 −20% vs 35–49 岁 +7.5%)。对转行/非典型背景的求职者,这意味着**不能走传统投递漏斗**(那是萎缩的池子),要走"增长的池子"。
- **WILDCARD 是最实用的出路指引**:**增长的需求不在招聘网站上**——它在自由职业、内部工具、micro-SaaS、以及那些"从没雇过开发者、现在自己做软件"的组织里。金句"the growing one doesn't post job listings"直接告诉你:**海投是错的策略(投向萎缩池),真正的机会要主动去那些非传统渠道找/创造。**
- **对 Rosso 的战略含义(与前几页合流)**:
  - 你已经在做的 Avaloka / Forge AI / Auralith 这类**自建产品/micro-SaaS**,恰恰就是这页说的"增长池"——你不必只靠投简历进大厂 junior 漏斗。
  - 结合页09 的 R1–R4 和页10 的 proof-of-work:**"有真实用户的自建产品 + 书面技术判断 + 评估/治理能力"** 这条路,正好绕开了"萎缩池 + age-targeted"的双重不利。
  - 求职话术:"我不在萎缩的入门漏斗里竞争。我做的是有真实用户的 AI 产品,提供的是 AI 时代稀缺的评估与治理判断——这属于那个'不发招聘启事却在增长'的市场。"

### 页 12/15 — If You're Breaking In During 2026: The Playbook

标题 **"The playbook"**（行动手册,针对"2026 年想入行/转型的人"）。六条可操作建议:

1. **Build one real thing(做一个真实的东西)**:要有真实用户,在你熟悉的领域。**别再优化投递漏斗——287 份申请是给一个已经不存在的市场用的策略。**
2. **Read every line you ship(读你交付的每一行)**:用 AI agent 来构建,然后**逐行读代码**,关键路径**亲手重写一遍**,连问三层"为什么"。
3. **Work in code you didn't write(在你没写过的代码里工作)**:合并进陌生代码库的 PR,是"这份工作本身"最接近的公开代理指标。
4. **Publish your judgment(公开你的判断)**:把你的技术决策写出来——**尤其是那些你否决了 AI 的地方。**
5. **Learn design + security now(现在就学设计和安全)**:不是等到第三年。实现变便宜后,**这些是入门级的瓶颈技能。**
6. **Aim at the growing edge(瞄准增长的边缘)**:被 AI 生成代码淹没、急需验证的初创公司;第一次做软件的非科技公司。

底部高亮框(全 deck 的中心句):

> **You're not applying to write code. That job is gone. You're applying to be the judgment layer above the machine.**（你不是在申请"写代码"的工作——那份工作已经没了。你申请的是成为**机器之上的判断层**。）

**分析:这页把前 11 页的诊断全部落成"下周就能做"的动作,而且每一条你都已经在做或极易做到。**
- **六条 = 前面能力项(R1–R4)+ proof of work + 增长池 的行动化汇总**:① 对应"proof of work"(做真东西别海投);② 对应 R1 代码审计;③ 对应"work in code you didn't write";④ 对应"written technical judgment";⑤ 对应 R2 系统设计+安全;⑥ 对应页11 的 wildcard(增长边缘)。**整套 deck 到这里收敛成一张行动清单。**
- **底部那句是全 deck 的灵魂,也是你求职定位的终极一句话**:**"You're applying to be the judgment layer above the machine."** ——你申请的不是"写代码的人",是"**机器之上的判断层**"。这和 Week 07 评估课在同一个词上彻底合流:**评估 = 判断层 = 机器之上那一层。** 你今天上午学的一整套评估方法论,就是"judgment layer above the machine"的具体内容。
- **对 Rosso 的逐条现状对照(你已经领先)**:
  1. Build one real thing → ✅ Avaloka / Forge AI(有真实产品)
  2. Read every line → ✅ 你在诊断 RAG/reranker 失败时做的正是逐行审查
  3. Work in code you didn't write → 可补:向开源 RAG/eval 项目提 PR(低成本高信号)
  4. Publish your judgment → ✅✅ 你的 decision log + 这份 Week 07 评估笔记就是,可对外发布(博客/LinkedIn,接 T010)
  5. Learn design + security → ✅ Week 06 guardrails + Avaloka agent 架构
  6. Aim at growing edge → ✅ 你做的正是"AI 产品需要验证"这个边缘
  **六条里你已占五条,唯一可立刻补的是第 3 条(提几个高质量 PR)和把第 4 条"公开化"(把内部判断改写成对外文章)。**
- **给 T010 的直接产物建议**:把第 4 条落地——挑 2–3 个你"否决了显而易见方案/否决了 AI 建议"的决策(比如"为什么先建评估基线再上 GraphRAG""为什么用 pool 近似 recall 而非全量"),写成对外可读的短文,这既是 proof of work,又直接展示"judgment layer"身份。

### 页 13/15 — The Playbook, Expanded · Why Volume Stopped Working: Stop Optimizing the Application Funnel

标题 **"Stop optimizing the application funnel"**（别再优化投递漏斗）。左侧一个漏斗数字:

```
287 applications  →  2 phone screens  →  0 offers
```

底部小字:**the funnel isn't inefficient. it's closed.**（这个漏斗不是效率低,是已经关闭了。）

右侧 **"OPTIMIZING THE FUNNEL" MEANS(所谓"优化漏斗"是指)** ✗
- 为关键词扫描器调简历
- A/B 测试求职信、用自动投递工具
- 更大投递量、投得更快、投更多公司

下方核心:

> **All of it assumes the funnel still works — that enough volume in the top drops an offer out the bottom.** Sarah's conversion rate wasn't low. It was **effectively zero**. When the market has structurally changed, **a better resume just gets you rejected more efficiently.**

翻译:所有这些优化都**假设漏斗还能用**——假设顶部投够量,底部就能掉出一个 offer。但 Sarah 的转化率不是低,而是**实际上等于零**。当市场发生了**结构性改变**,一份更好的简历,只会让你**被更高效地拒绝**。

**分析:这页用一个残酷的漏斗数字,论证"海投策略已死",并给出深刻的一般性教训。**
- **287→2→0 是全 deck 最扎心的数据**:投 287 份,2 个电话初筛,**0 个 offer**。转化率不是"低",是"实际为零"——**在一个结构性改变的市场里,优化一个已经关闭的漏斗,只是"更高效地被拒"。**
- **深层教训(和评估课惊人地同构)**:"优化漏斗"假设了"漏斗还在工作"——**这是一个没有被验证的前提假设**。就像 Week 07 反复讲的:你在优化一个指标前,要先问"这个指标/这个前提本身还成立吗?"。Sarah 花力气优化简历(优化 μ),却没质疑"投递这个机制(θ 的作用域)是否还连接到真实机会(𝒬)"。**当底层分布变了,优化表层参数毫无意义**——这正是 eval decay / 分布漂移的职业版:你的"求职策略"这把尺子已经过期了,还在拿它量。
- **对 Rosso 的直接警示(最实用的一条)**:**停止海投。** 如果你在投几十上百份简历,这页告诉你那是"给一个不存在的市场用的策略"(接页12第1条)。转化率为零不是因为简历不够好,是因为**入门漏斗这个渠道本身对你(尤其非典型背景/转型者)已经关闭**。
- **出路(承接前几页)**:既然漏斗关闭,就走**非漏斗路径**——页11的"增长池"(不发招聘启事)、页12的"做真东西+公开判断+瞄准增长边缘"。**主动创造机会(自建产品、公开技术判断吸引人来找你、直接接触"第一次做软件的非科技公司"),而不是被动投递。** 你的 Avaloka/Forge AI + 这份可公开的技术判断,本身就是"绕过漏斗"的资产。

### 页 15/15 — Worked Example · Capstone: What the Evidence Looks Like — The Open Casebook

标题 **"What the evidence looks like: The Open Casebook"**（"证据"长什么样:开放判例书)。副标 **"A capstone project, not a job application"**（一个 capstone 项目,不是一份求职申请):一个免费的、**引用可溯源(citation-grounded)** 的判例检索系统,覆盖 22 万份法院判决(可扩展到 670 万),服务那些被 Westlaw / LexisNexis 高价挡在门外的法律援助律师。

四个证据 E1–E4:
- **E1 · Shipped for real users(为真实用户上线)**:为真实约束而建——"一个开庭前只有 30 分钟的律师"。和法律援助机构做试点:20–50 名律师、每天 500–1000 次查询、把小时级答案压到秒级。→ **real users beat polished demos(真实用户胜过精致 demo)**
- **E2 · Deep domain knowledge(深度领域知识)**:围绕法律研究**真实运作方式**来建:按辖区区分约束性 vs 说服性判例、被推翻的裁决、判决书结构(headnote/holding/reasoning/dissent)。→ **not competing with generic applicants, or with AI(不和通用申请者、也不和 AI 竞争)**
- **E3 · Written technical judgment(书面技术判断)**:公开记录权衡——**FAISS 而非 Pinecone**(为 22 万判例"合身"选型,并写明迁移路径);cross-encoder reranker 在 <100ms 被采纳,**因为它是唯一能对"辖区"做推理的阶段**。→ **"why I rejected the obvious approach" — in writing(把"我为什么否决显而易见的方案"写下来)**
- **E4 · Verification built in(内建验证)**:**评估框架用 MAP@10、NDCG@10、Recall@100 对照专家标注的 ground truth 打分;guardrail:凡展示的引用必须落在一个被检索到的判例上;BM25 兜底,让搜索永不完全失败。** → **eval engineering — the new entry skill, demonstrated(评估工程——新的入门技能,被证明了)**

底部高亮框(全 deck 收尾):

> **One capstone, four signals — shipped, domain-deep, judged, verified. That's what replaces 287 applications.**（一个 capstone,四个信号——已上线、领域深、有判断、可验证。这就是取代 287 份申请的东西。）

**分析:这是全 deck 的压轴范例,几乎是把你(Rosso)今天做的事、和整门课学的东西,直接写成了一个"标准答案模板"。**
- **E4 就是你今天上午的 Week 07 评估课 + 你写的 demo**:MAP@10 / NDCG@10 / Recall@100(六指标里的三个)、专家标注 ground truth(金数据集/SME)、"引用必须 grounded 在检索到的判例"(faithfulness / 断言-证据)、BM25 兜底(hybrid,防 recall 归零)。**这张幻灯片列的 E4,和你 `rerank_eval_demo.py`/`ndcg_demo.py`/`pr_curve_demo.py` 做的是同一件事。** 这门课(评估)和这个求职 deck 在这里彻底闭环:**评估工程 = 新入门技能 = 你已经在做的事。**
- **E3 是"书面技术判断"的完美范本**:不是"我用了 FAISS",而是"**我为什么选 FAISS 而非 Pinecone、什么规模下会迁移、为什么 reranker 值这 100ms**"。这正是你项目 decision log 的风格(证据驱动、写明取舍与移除条件)——**你已经在按这个标准生产证据了。**
- **E1+E2 = proof of work + 领域深度**:有真实用户、解决真实约束、懂领域真实运作。对应你的 Avaloka(真实护理记忆场景)。
- **对 Rosso 的最终行动建议(把整套 deck 收敛成一句)**:**别投 287 份简历,建/打磨一个 "capstone" 并按 E1–E4 四个信号展示它。** 你其实已经有素材:
  - E1 上线真实用户 → Avaloka / Forge AI
  - E2 领域深度 → 你的具体行业场景
  - E3 书面判断 → decision log + 这份 Week 07 笔记(改写成对外文章)
  - E4 内建验证 → 你今天写的三个 eval demo + Avaloka EVAL 集设计
  **四格填满 = 一份"取代 287 份申请"的 capstone。** 这就是这套 deck 给你的最终答案,也和评估课在"验证/判断层"上完全合一。
- 页脚 **"the new path / ospectra"** 表明这套 deck 出自 ospectra;是今天下半场的完整职业演讲(共 15 页,已全部记录:01 死亡宣告→03 旧路径→04 数据→05 机制→06 经济→07 二阶效应→08 核心转变→09 R1-R4画像→10 proof of work→11 平衡视角→12 playbook→13 停止海投→15 capstone范例)。

## 本周(Week 07)学习总结

> 今天(2026-07-25)一天两场:上半场《The Measure of All Things》评估课(SupportVectors / Asif Qamar),下半场《The New Path》AI 时代职业演讲(ospectra)。两者在"验证/判断层"这个主题上惊人地合流。

### 上半场:RAG 系统评估(从检索到推理)

**总纲一句话**:你无法改进你无法测量的东西。全天挂在一个公式上——`argmax_θ E_{q∼𝒬}[μ(q,θ)]`:在你自己的查询分布 𝒬 上,调遍所有旋钮 θ,让指标 μ 最大。

**Act I — 标尺(金数据集)**:先有 ground truth 才有测量。金数据集 = 精挑 query + SME 打的 0–4 分级相关性;cherry-pick 五步法(SME 出题→简单引擎捞 top100-200→精挑 25-30 打分→冻结版本化);规模最少 200、目标 1000(功效分析:检测 1 分 nDCG 提升需 N≈500-1000);两种腐烂——eval decay(定期刷新)和 overfitting(held-out 集防作弊);反对借用公共基准(只能当 sanity check)。

**Act II — 六指标阶梯**(每级补下一级盲点):
- Precision@k(纯度)/ Recall@k(完整性)——二元、位置盲
- MRR(首命中多快,凸惩罚,导航式查询)
- MAP(所有相关文档且要早,平均的平均)
- AUC-PR(整条 PR 权衡曲线,对稀有正类稳健,RAG 用它不用 ROC)
- **nDCG(顶峰,唯一同时"看分级+看排序"):Gain 2^rel-1 → Cumulate → Discount /log₂(rank+1) → Normalise /IDCG**
- **最小诊断对**:nDCG 低+Recall 高→修 reranker;两者都低→修检索;都高→评生成侧。"只有时间看一个数就看 nDCG,其余五个作诊断。"

**Interlude — 信号与噪声**:统计显著性(配对 bootstrap/置换检验)、统计显著 vs 实用显著(企业阈值 0.02-0.05 nDCG)、多样性盲点与 MMR(相关性−冗余度,α-NDCG 评估)。

**Act III — 生成器评估(食材→厨师)**:从"评检索"转向"评 LLM 有没有用好证据"——RAGAS 四指标+五局限、FActScore/ALCE 声明级+引用忠实、LLM-as-Judge(Prometheus-2、评委偏见、Cohen's κ<0.6 拒用)、RGB 四能力。(Act III/IV 详细内容部分幻灯片未截,以 PDF 讲义为准。)

**产出的 eval artifact(填补 T021 的坑)**:三个可运行 demo——`ndcg_demo.py`(四层手算)、`pr_curve_demo.py`(PR 曲线/AUC-PR)、`rerank_eval_demo.py`(检索→reranker→算指标闭环 + diagnose 诊断函数)。

### 下半场:AI 时代软件职业路径

**核心链条**:AI 拿走的不是"工作",是"入门阶梯"——junior 的活是可编码知识(LLM 最擅长),senior 的活是隐性判断(AI 只增强不替代);简单工单消失 → 补贴学徒制崩塌 → 2026 缺 junior→2028 缺中级→2030 缺 senior。**2030 稀缺技能不是写代码,是知道代码什么时候是错的。** 价值转移到验证层:"You're applying to be the judgment layer above the machine."

**新入门画像(R1-R4)**:代码审计、系统设计素养、**评估工程(新学科,新人能打败老手)**、指挥 AI agent(管理技能)。**新信号 = proof of work > proof of study**;别海投(漏斗已关闭),瞄准增长边缘;capstone 四信号 = shipped/domain-deep/judged/verified。

**与评估课的合流**:R3 评估工程 = 上半场全部内容;capstone 的 E4"内建验证"= 你写的三个 demo。**评估能力 = judgment layer above the machine = AI 时代唯一持久增值的技能类别。**对 Rosso 求职(T010):按 R1-R4/E1-E4 重新包装 Avaloka+评估能力,走"判断层"定位,而非"会写代码"。

## 一句话总结

前六周一直在"建"，这周开始"量"。核心信条：**你无法改进你无法测量的东西（you cannot improve what you cannot measure）**。指标决定系统优化的方向，EVAL 集决定测量是否有意义，评估框架决定你能否诊断并修复失败。评估做错，前六周全部悬空；做对，整条流水线变成一个你能操控（steer）的系统。

```text
先建 ground truth（EVAL 集）
-> 六个经典检索指标（二元 -> 排序感知 -> 相关性加权）
-> 统计显著性 + 检索多样性
-> 生成侧：RAGAS -> 声明级蕴含 -> LLM-as-Judge -> RGB 四能力
-> 前沿：拒答校准、多跳、进化式测试集、agentic 轨迹、Goodhart、成本
-> 把每个指标接回前六周的每个组件
```

一句话定位：本周把过去六周隐含依赖却从未检验的"评估"显式化——学完你就从 RAG **practitioner** 跨到 RAG **engineer**。

## 本周进度总览

上周装了两道门（请求侧闸门 + 响应侧良知），但那只是"机制"，**没有测量的机制只是希望**。本周补上：怎么知道 guardrails 真的该触发时触发了？怎么知道 grounding 抓住了无据声明而不是放行？怎么知道花五周打磨的检索真的在按正确顺序找到正确文档？

特别一条主线：上周两道门给了系统"弃权"和"核查"的能力，本周为**认知谦逊**造指标——负拒绝率、噪声鲁棒性、弃权校准——并把它们接回已做的架构决策。一个知道自己不知道、且能证明自己知道自己不知道的系统，才是生产上可信的系统。

## Act I：标尺——任何指标之前，先有 ground truth

没有尺子，一切关于"长短"的说法都只是意见。IR 里的尺子就是金数据集。

### EVAL 集：一切测量的地基

每个 query 标注相关文档集 + **离散相关性分数 r ∈ {0,1,2,3,4}**（0 无关，4 完美相关）。两种建法，成本差几个数量级：

1. **金标准**（Google/Microsoft 式）：海量 query 全量人工逐条打勾，recall 要列出"本应返回的"来对比。水密，但七人小团队烧不起。金标准还有自己的病理：你精心种下 10 篇完美文章当 ground truth，引擎却surface 出一篇你从没编目、甚至更好的文章——precision 反而下降，引擎因为做好本职工作而被惩罚。
2. **Cherry-picked 金数据集**（可行方案）：① 请**领域专家 SME 而非工程师**（医疗找临床医生、金融找合规官）；② SME 从真实意图（搜索日志、工单）出题；③ 简单引擎每 query 取 top 100–200 候选（可扫，不是百万级）；④ SME 精挑并按 0–4 打分最佳 25–30 条；⑤ 每次发版**冻结、版本化、随语料演进**。

规模：**最少 200 条，目标 1000 条**。低于 200 补丁式稀疏噪声主导，你会仅凭噪声就给某系统颁冠。"SME Summit"是种子——聚 5–10 位专家，管早午餐，给 8 小时，产出约 100 条辩论过的分级判断，之后六个月慢慢长大。同时要管理 **eval decay**：生产语料演进，评估集会过时。

### 谁的活 + 优化目标

评估是 **AI 工程师自己的关切**，不是 QA、不是下游团队的；AI 系统不存在干净的 pass/fail。优化目标形式化为：

```text
argmax_θ  E_{q∼Q} [ μ(q, θ) ]
```

θ = 系统全部可调项（不只模型参数，还有架构、chunking 策略、检索管线、prompt 设计），μ = 指标，Q = EVAL 分布。这就是超参调优，只是 RAG 的 θ 搜索空间更大——所以系统化评估才重要。

## Act II：阶梯——六个经典检索指标

从二元 -> 排序感知 -> 相关性加权，层层递进。两个直觉比喻贯穿：**海滩捡贝壳**（precision/recall 权衡、AUC-PR）与**阿里巴巴山洞**（排序感知，宝物按货架线性排列 = 排名）。

1. **Precision@K** — top K 里有多少相关（准不准）。
2. **Recall@K** — 已知 n 个相关里 top K 找到多少（全不全）。分母是整个相关世界，只有金数据集知道；对 K 单调不减，所以检索系统 K 设得大方。
3. **MRR（平均倒数排名）** — 每 query 取第一个相关结果排名的倒数再平均。倒数是凸的：1→2 名腰斩，10→11 几乎无感。适合"找到一个就跑"的场景。
4. **MAP（平均精度均值）** — AP 在一个 query 内对每个命中位置的 precision 求平均，MAP 再跨 query 平均。IR 基准（TREC、BEIR）的主力，奖励把相关文档排在前面。致命局限：**二元相关性**，把杰作和勉强及格的文档当同一个。
5. **AUC-PR** — 沿海滩边挖边画：x 轴 recall、y 轴 precision，曲线下面积把整段行走压成一个数（完美 1.0，随机 = 语料相关基率）。用 PR 而非 ROC，因为 IR 里正例稀疏。
6. **nDCG（归一化折扣累积增益）** — 金标准，**唯一同时排序感知 + 相关性加权**。三层 + 归一化：
   - Gain：`G_i = 2^rel_i − 1`（指数增益：diamond=15 是 silver=1 的 15 倍，不是 4 倍——高相关性不成比例地重要）
   - Cumulative Gain：前 K 个 gain 求和
   - DCG：每个 gain 除以 `log₂(i+1)` 的对数折扣（越深的货架风险越高，同一块 gold 在 rank 5 不如 rank 1）
   - nDCG = DCG / IDCG（理想排序的 DCG），得"你达到了这批文档最佳排序的百分之几"

> 注意增益有两种约定：Järvelin–Kekäläinen(2002) 用线性 `G_i=rel_i`；Burges(2005) 用 `2^rel−1`（scikit-learn / pytrec_eval 默认）。读旧论文先核对公式，跨约定的数字不可比。

**最小诊断对：nDCG@K 配 Recall@K**——
- nDCG 低、Recall 高 → 文档找到了但排序差 → **修 reranker**
- nDCG 低、Recall 低 → 根本没找到 → **修检索**（chunking、embedding、hybrid 混合）
- 都高 → 庆祝，进 Act III

阶梯顺序：Precision/Recall（二元、位置盲）→ MRR（加排序但只看首命中）→ MAP（排序扩展到全部但仍二元）→ AUC-PR → nDCG（补上相关性加权）。每个指标修上一个的一个局限。

### 插曲：从噪声中辨信号

- **基准全景**：BEIR、MTEB、MSMARCO。
- **统计显著性**：一个改进是真的吗？跑**配对 bootstrap 或置换检验**。达到统计功效约需 N≈500–1000 query（"目标 1000"几乎正好匹配）。最危险的混淆是**统计显著 vs 实用显著**：eval 集够大时琐碎改进也会统计显著；nDCG 的实用阈值企业里约 **0.02–0.05 绝对值**。
- **检索多样性——被忽略的一维**：六指标只测相关性，返回十个近重复能拿满分却体验糟糕（同质证据、浪费上下文、伪共识）。用 **MMR（最大边际相关）** 修：迭代挑"对 query 相关性 − 对已选集相似度"最大的候选，λ 调权衡。

## Act III：超越检索——测量生成与忠实度

### RAGAS 框架（起点）四个核心指标

faithfulness（忠实度，上周响应侧 grounding 的生成侧对应，用 NLI 或 LLM 后端）、answer relevancy（从答案反推 n 个合成问题，测与原问题的 cosine 相似度）、context precision、context recall。

**RAGAS 的五个局限**（记住，别把它当唯一裁判）：
1. 无声明级粒度——"Einstein 生于 Ulm，1879 年，1921 得诺奖"是一条含 3+ 可独立证伪声明的语句，大部分子句被支持时整条可通过，一个错声明搭便车混过。
2. 评估模型间分数不稳定——GPT-4/Claude/Llama 给不同分，厂商还会中途悄悄更新模型。
3. 无归因验证——只查与上下文一致，不查每条声明是否引用了正确段落。
4. （配套告诫）**评估器 pinning**：永远把 judge 钉到带日期的 checkpoint；维护 50–200 条人工核验的冻结校准集，定期重跑，若 Cohen's κ 漂移 >0.05 说明评估器变了。

裁决：**把 RAGAS 当诊断基线（任何 RAG 都不该低于的地板），不当质量的唯一仲裁**；用声明级评估、人工抽检、归因指标补足。

### 声明级蕴含：FActScore 与 ALCE

生成评估最重要的进步 = 从答案级到**声明级**。**FActScore**（EMNLP 2023）：把答案分解成原子事实，逐条核验；ChatGPT 生成的传记 FActScore 只有 58%——近一半原子声明无据。**ALCE** 扩展到引用质量：引用准确率 40–75%，约**每三条引用就有一条错或缺**，即便答案是对的；企业里引用准确率是**部署门槛**。"撑不住的脚注比没脚注更糟"。

### LLM-as-a-Judge 2.0：专用评估模型

评估是特定任务，理应用专用 judge 而非租来的前沿模型。**Prometheus-2**（EMNLP 2024，开源、本地跑）：直接评分（按用户 rubric 绝对打分）+ 成对排名；与人工一致率 72–85%。四种评委偏见：**位置、长度、自我偏好、重形式轻实质**。必须用 **Cohen's κ** 对齐人工（Landis–Koch：0.41–0.60 中等，0.61–0.80 substantial；企业 RAG **拒用 κ<0.6** 的 judge）；Kendall's τ 管排名一致，Krippendorff's α 管多评委。

**评委三铁律**：① judge 用与 generator 不同的模型家族；② 成对比较两个顺序都平均；③ 永不信单一评委，用第二个交叉验证并人工抽查。（CoT 评委提升 8–12 分一致性但 3–5× token 成本——便宜单 token 评委做持续监控，CoT 评委做周期深检。）

### RGB 四能力（RAGAS 测不了的）

RGB 基准（AAAI 2024）识别 RAG 生成器必须具备的四能力：**噪声鲁棒性**（能否忽略话题相关但不含答案的文档）、**负拒绝率**（无答案时能否弃权）、**信息整合**、**反事实鲁棒性**（能否发现检索文档中的事实错误，例如文档说 480 端口而其余都说 48——它会标出矛盾还是盲从上下文）。

## Act IV：前沿——评估的下一步

1. **知道何时说"我不知道"**：**ECE（期望校准误差）** = 各置信度 bin 内 accuracy 与 confidence 加权差；完美 0，现代 LLM 跑 0.05–0.15，指令微调常更差（把置信度推高却没推高准确率）。配可靠性图（reliability diagram）。讲师暴言："至今没见过一个企业 RAG 系统诚实说过'I don't know'"——试试 Calabi–Yau 测试：问一个开关厂的 RAG 关于 Calabi–Yau 流形。
2. **多跳与综合评估**：经典指标独立评每次检索，测不了整合。三维：信息整合、桥接推理、多跳。基准 HotpotQA / MuSiQue / 2WikiMultihopQA / MultiHop-RAG（后者给每跳 ground-truth 证据链，可评路径而非只评终点）。
3. **自动进化式测试集生成**：Giskard RAGET（从知识库直接生成分难度、针对特定失败模式的测试集）、DeepEval（RAGAS 超集 + G-Eval）。进化角度：从种子问题 LLM 变异出更难变体——加约束、要求多跳、注入干扰项、翻转期望答案（测负拒绝）、增加歧义（测消歧）。
4. **Agentic / 轨迹评估**：agent 会规划/检索/调工具/迭代，只评终点危险。三层：终到端（正确性、满意度）、轨迹质量、**节点级精度**（每个决策点：对的工具？良构 query？合理推理步？——诊断力在这层）。
5. **Goodhart 定律**（当日最重要告诫）：一旦指标上墙，人就为它优化——"当测量变成目标，它就不再是好测量"。RAG 特有的 reward hacking：只训 faithfulness → 过度对冲（"有可能……"，技术上忠实但没用）；只训 citation recall → 过度引用；长度偏见 judge → 过度写作；judge 与 generator 同家族 → 合谋。防护：指标集成、对抗 eval、红队攻击指标、以及**从不用于训练的 held-out 金评委**（留作漂移检测）。
6. **成本维度**：前沿评委评 1 万 query 要 $500–2000/次；自研开源 judge 在自家 GPU 上近乎零边际成本；一个在 5000 条领域标注上微调的 7B judge 在该领域一致性上打败 prompt 版 GPT-4。

## 评估地图：把每个指标接回前六周

| 组件（周） | 失败模式 | 对应指标 |
|---|---|---|
| Embeddings & 检索（W1–2） | 检索质量 | Recall@K, Precision@K, MRR, MAP, nDCG |
| Reranking（W2） | 相关结果被埋 | precision, nDCG |
| Chunking（W3） | 相关信息被切断 | context recall, information integration |
| 派生工件（W4） | 替身值不值 | Recall@K / context precision（替换前后对比） |
| GraphRAG & 多跳（W5） | 跨文档推理 | information integration, 多跳基准 |
| 两道门（W6） | 请求门→噪声鲁棒；响应门→负拒绝、忠实 | noise robustness；FActScore（断言-证据图是机制，FActScore 是指标） |
| 全流程（本周） | 端到端 | answer correctness, satisfaction, ECE（捕全貌但不定位失败——组件级指标才定位） |

## 与前几周的关系

Week 1–2 建"意义即几何"和检索地基 → 本周用六指标量它；Week 3 chunking → context recall；Week 4 派生工件 → 替换前后的 Recall/precision；Week 5 GraphRAG → 信息整合/多跳；Week 6 两道门 → 噪声鲁棒 + 负拒绝 + 忠实度。本周是"证据驱动架构升级"（2026-06-06 决策）的方法论闭环：**先有指标基线，才谈加组件**。

## 解锁的 Agent 能力

- **可测量的自我怀疑**：Avaloka 能对"该弃权时是否弃权"（负拒绝率）和"答题时置信度是否诚实"（ECE）给出数字，而不只是有 guardrail。
- **组件级诊断**：用 nDCG↔Recall 诊断对定位失败在检索还是排序，把"证据驱动升级"从原则变成可执行动作。
- **忠实度硬门**：把 FActScore / 引用准确率设成部署 gate，而非事后抽查。
- **防 Goodhart 的评估纪律**：指标集成 + held-out 金评委，避免优化单指标反噬产品行为（尤其"温暖但不越界"的安全边界）。

## Avaloka 应用（初步，待课后细化）

- 为 **Memory Reader V0**（T008）落地本周的检索指标基线：Recall@5、MRR、nDCG@5，直接对接已定的 benchmark 决策（2026-06-06）。
- 建 Avaloka 版 EVAL 集：SME = Rosso 本人 + Care Card 真实意图；先冲 100 条分级 query（SME Summit 模式），冻结版本化，管理 eval decay。
- 用 ECE + 负拒绝率量化 Avaloka 的"诚实的我不知道"能力——回应讲师"没见过企业 RAG 说过 I don't know"的挑战。
- 把 faithfulness/attribution 与上周断言-证据二部图打通：机制已在，补上 FActScore 这个指标。

## 所需证据、工具与评估

- **工具**：pytrec_eval / scikit-learn（六指标，注意增益约定）、RAGAS（诊断地板）、FActScore + ALCE（声明级 + 引用）、Prometheus-2（本地评委）、Giskard RAGET / DeepEval（进化式测试集）。
- **eval artifact 待建**：本周应产出至少一个"检索指标基线"trace（Memory Reader V0 或 Xennials FactoidWiki），含 EVAL 集、六指标数值、以及 nDCG↔Recall 诊断结论。

## 今日应能回答的问题（课前自测）

1. 精确陈述"你无法改进你无法测量的东西"在 argmax_θ E[μ(q,θ)] 中对应什么？
2. 为什么 EVAL 集要 SME 出题而非工程师？金标准的"病理"是什么？200/1000 的数字从哪来？
3. 六个指标各修了上一个的什么局限？nDCG 的三层 + 归一化能否手推一遍？
4. nDCG 低 / Recall 高 意味着修什么？反之呢？
5. 统计显著 vs 实用显著的区别？nDCG 的实用阈值大概多少？
6. RAGAS 的五个局限？为什么它只能当"地板"？
7. Cohen's κ 是什么，为什么 <0.6 的 judge 要拒用？评委三铁律？
8. RGB 四能力分别测什么？ECE 测的是哪种诚实？
9. Goodhart 定律在 RAG 里具体表现为哪些 reward hacking？怎么防？

## 实验课（8 个 Lab，待动手实现）

1. 混淆与胡话检测；2. 毒性与语种检测；3. 域与意图分类；4. 越狱检测与诱导性问题；5. 限速、PII、会话级 guardrails；6. 请求侧集成与 guardrail 锦标赛；7. 响应侧 grounding 与忠实度测量；8. 拒答与谦逊校准。（注：Lab 清单沿用上周 Two Gates 的实操延续，本周新增检索指标与生成评估的计算练习。）

## 参考文献（部分）

FActScore (EMNLP 2023)；ALCE: Automatic LLMs' Citation Evaluation (arXiv:2305.14761)；Prometheus-2 (EMNLP 2024)；RGB Benchmark (AAAI 2024)；LLMs-as-Judges Survey (arXiv:2412.05579)；MMR (Carbonell & Goldstein, SIGIR 1998)；BRIEF 多跳 (NAACL 2025)。
