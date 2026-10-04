# 第 08 周课堂笔记

日期：2026-08-01

状态：课前讲义两份已读完并整理成学习总结骨架（The Personal Equation 开场实验 + The Measure of All Things 完整版讲义，重点在生成器评估半场）；现场讨论细节、Lab 动手实现、以及本周 eval artifact 待课后补充

来源：
- `uploads/the-personal-equation.pdf`（*The Personal Equation — Seven small experiments you are going to fail*，Generator Evals 开场课，SupportVectors，29 页）
- `uploads/the-measure-of-all-things.pdf`（*The Measure of All Things — Evaluating RAG Systems from Retrieval to Reasoning* 完整版，169 页；相较 Week 07 的四幕版，本版扩为**五幕**，新增 Act V「The Observatory」并把 Act III/IV 细节全部展开）

> 本周定位：Week 07 学的是「怎么量检索」（Act I 标尺 + Act II 六指标阶梯 + Interlude），今天把镜头转到**生成器本身**——Act III The Generator、Act IV The Frontier、Act V The Observatory、Coda。开场用《The Personal Equation》先让学员**亲手失败七次**，每次失败对应下午要学的一个评估指标。一句话：*先测量测量者本身（measure the measurer first）*。

---

## 一、开场实验课：The Personal Equation（先测你，再测机器）

**核心隐喻**：1796 年格林威治天文台，皇家天文官 Maskelyne 因为助理 Kinnebrook 记录星体过中天的时刻总是「慢」而把他开除。1823 年 Bessel 发现这不是失职——每个观测者的神经系统都有一个**稳定的、可测量的个人偏差**，他把它写成一个校正项，命名为 **the personal equation（人差方程）**。教训不是「开除有偏差的仪器」，而是**测量它、写下它的方程、把它减掉**。每一个你将来雇用的 LLM judge 都有自己的人差方程（偏向啰嗦、偏向第一个答案、偏向自家模型的文风）。

规则：全部匿名、聚合（举手/纸条/半个房间），房间本身是数据；「暖心地失败」——重点不是你有缺陷，而是每一台测量仪器都有，而今天你就是那台仪器。开场白点名两个受害者：一位助理天文学家因第 1 个实验丢了职业生涯，GPT-4o 因第 4 个实验丢了 30 分事实精度。

七个实验 → 七个「你亲身体验的失败」→ 讲义给它命名 → 指向一个评估指标：

| # | 你体验到的 | 讲义的命名 | 对应的仪器/指标 |
|---|---|---|---|
| 1 | 静默一分钟：闭眼估 60 秒，两轮都朝**同一方向**错（内部时钟稳定偏快/偏慢） | Judge bias = 人差方程 | 用金数据集校准 judge、钉版本、**减掉别开除** |
| 2 | 八道题给 90% 置信区间，实际只命中约 50%（窄区间显得能干） | 过度自信 Over-confidence | ECE、可靠性图、温度缩放 |
| 3 | 「摩西带了每种动物几只上方舟？」脱口而出「两只」——其实是**诺亚** | 内在幻觉 Intrinsic hallucination | 声明级蕴含（每条原子声明对源核验） |
| 4 | 读一段只讲 Sydney/Melbourne 的澳洲短文，半屋子答「首都=Canberra」——文中根本没出现 | 参数泄漏 Parametric leakage（负拒绝失败） | 不可答测试集、负拒绝率、Calabi–Yau 探针 |
| 5 | 「Einstein 是俄亥俄州水管工，生于 1961」的假传记，仍有人答「相对论 / 1879 / 德国」 | 实体碰撞 Entity collision（名字召唤错知识） | FActScore 式原子分解、逐条核验 |
| 6 | 双问句：成立年份（有据）+ 员工数（无据），纸条自动分三堆——答/含糊/标注缺失 | 三分法 Trichotomy（答·含糊·拒） | 充分性条件下的准确率、弃权质量 |
| 7 | 两场小测同难度：+1/0/0 规则下人人乱猜，+1/−1/0 规则下「pass」满屋开花 | 评分台上的 Goodhart | 弃权感知评分（CRAG 的 +1 / 0 / −1） |

**实验 2 的战争故事（别过度校正）**：十多年前 Spark MLlib 给出一个「95% 置信、区间从 −∞ 到 +∞」的回归预测——**完美校准，永不会错，却毫无信息**。目标不是只要校准，而是**又校准又锐利（calibrated and sharp）**：谦逊到足以正确，狭窄到足以有用。

**实验 4 的最佳答案**（贯穿全天，Act III 会回来）：「短文没说——不过众所周知是 Canberra。」——**从证据回答，把先验清楚地标注为先验**。

**藏在七个实验底下的两条大道理**：
1. 对生成器来说，**检索就是证据**，理想回答是「仅以该证据为条件的后验」（一个无信息先验）。但模型和你一样「知道」，于是忍不住作答——**先验不会礼貌地待在门外**。
2. 一个好的 RAG 就是一个**好朋友**：证据支持的部分照答，其余说「我们一起查查看」，把猜测标为猜测、把先验知识标为「众所周知」。

### 现场实录与深入分析（课堂逐页，2026-08-01）

讲义分**三幕 + Coda**：Act I · The Measurer（找到你这台仪器 = 实验 1、2）、Act II · The Prior（先验挡不住 = 实验 3、4、5）、Act III · The Friend（诚实长什么样 = 实验 6、7）。以下是逐页拆解时补的几个关键洞见：

**实验 1 深入（偏差 vs 方差）**：这页真正的知识点是统计学的**偏差-方差之分**。第一轮单看像随机噪声（方差），第二轮的设计逼你发现两轮**同向**出错——「方差」当场塌缩成「偏差」。两者处理方式相反：方差靠取平均/多次采样消除，偏差取多少次平均都不消失，只能**测出来减掉**。名言「You do not have errors. You have *an* error.」。类比精确处在于 judge 的三个偏差（position/length/self-preference）都是**系统性、稳定、可测**的。最狠一句是 **"subtract, don't fire"**：隐含前提是「你永远得不到无偏仪器」，Maskelyne 的错不是用了有偏助理，而是以为存在无偏助理。**但要补一个限制**：时钟偏移是常数，judge 偏差**非平稳**（随 prompt、领域、尤其厂商偷偷更新而漂移），所以机器版的「校正项**带保质期**」——必须钉版本 + 冻结校准集 + 监控 Cohen's κ（漂移 >0.05 报警）。

**实验 2 八道题 + 真答案对照**（Fremont 是 SupportVectors 所在地，故意让你觉得该知道）：

| # | 题目 | 真值 | 诚实的宽区间该长什么样 |
|---|---|---|---|
| 1 | Fremont 6 月历史最高温(°F) | 记录不易精确核实；站点历史极值约 114.8°F(2022-09) | ~95–112°F（该宽） |
| 2 | Fremont 1 月历史最高温(°F) | 同上，无精确公开值 | ~70–82°F（该宽） |
| 3 | 尼罗河长度(km) | ~6,650（6,650–6,695） | 5,500–7,500 |
| 4 | 格林威治皇家天文台建于 | **1675**（查理二世） | 1600–1750 |
| 5 | 蓝鲸心脏重量(kg) | 唯一保存标本 ~180kg（含液 ~200kg/440lb） | 50–300kg（多数人锚太低） |
| 6 | 音乐会钢琴键数 | **88** | 该窄——众所周知 |
| 7 | 首届 TREC 会议 | **1992**（NIST） | 1985–2000 |
| 8 | Denali 高度(m) | **6,190m**（20,310ft，2015 复测） | 5,000–7,000 |

**现场真实校准结果**（聊天区同学答案，把 slide 论点当场演示）：一半人给**点估计**（单个数字 = 宽度为 0 的区间 = 过度自信的极端，命中率≈0；连钢琴 88 都有人写 80/83）；给区间的人也**普遍开得太窄**，8 题多半只命中 2–3 题（如把 88 写成 100–250、整段区间落在真值上方；鲸心写 2–5kg/50–100kg，差 1–2 个数量级；尼罗河统一往低猜、TREC 往近猜=**系统性偏差**呼应实验 1）。声称 90% 置信、实际约 25–40% 命中 → 可靠性图塌在对角线下 → 这个缺口叫 **ECE（期望校准误差）**。

**实验 2 战争故事（The interval that could not fail）**：早年 Spark MLlib 回归给出「−∞ 到 +∞、95% 置信」的区间——**完美校准、永不会错、毫无用处**（技术上是方差估计退化/未正则化的产物，说明「会报不确定性」不代表不确定性有用）。教训：**校准与锐利是两个正交轴**，只测校准可靠靠加宽刷满、只测锐利靠收窄作弊，所以要用**恰当评分规则（Brier）**同时罚两者。目标 = **calibrated *and* sharp**（谦逊到能对，锐利到有用）。机器版的「无限宽区间」有两个化身：**over-hedging**（只训 faithfulness → 满口「有可能……」，忠实但没用）和**在一切问题上弃权**（NRR 满分但覆盖为零）。所以本周把弃权做成**旋钮而非开关**，用**风险-覆盖曲线**找工作点（凸曲线 = 校准信号知道哪些答案危险）。

**实验 3 深入（摩西错觉 · intrinsic hallucination）**：认知学上叫 **Moses illusion**——替换词与正确词语义相近（摩西/诺亚都带方舟气味）时，理解系统不核对就放行。出题条件「立刻、齐声、数三下喊」是**故意逼出快思考（System 1）**、切断「回头核对证据」那一步——慢下来单独默读你能发现是诺亚。对应 RAG：LLM 默认就跑在「抢答」状态（自回归解码，无内建验证环节），所以缓解幻觉 = 外挂 System 2（先 CoT 自查 / 生成后声明级蕴含）。要分清：**intrinsic**（与证据矛盾，如此题）vs **extrinsic**（补了证据没有的信息）。陷阱：「每种两只」单看和方舟故事一致，naive 忠实度检查会放行——必须对**问题里真正的指称**（摩西）做蕴含核验才抓得住。总纲句：**same confidence, same grammar, wrong referent**（流畅度与正确性解耦，故不能靠肉眼看幻觉）。

**实验 4 深入（负拒绝 · correct ≠ grounded）**：最纯的参数泄漏测试——澳洲短文只提悉尼/墨尔本/珀斯/布里斯班/1788/1901，**从没出现 Canberra**。设计三个机关：① 文中反复出现 financial centre / cultural **capital**，主动激活「capital」诱你作答；② 「commit it to paper as you would defend it」断掉含糊退路；③ **最关键——泄漏进来的 Canberra 在现实里是对的**，正因为「对」你不会起疑。由此立规矩：**正确性 ≠ 有据性（correct ≠ grounded）**，一个答案可以完全正确同时仍是 grounding 失败；参数泄漏最危险的形态就是「事实正确但无据」，任何「看答案对不对」的检查都会放行。满分答案模板（Hold that sentence，Act III 会正式化为三分法）：**「资料没说——不过众所周知是 Canberra」**＝据实回答（负拒绝）+ 先验明确贴上「commonly known」标签，关键在于把先验放进对的抽屉、不冒充证据。名句：**evidence in the window, a lifetime of priors behind it**——负拒绝不是一次修好的功能，是每次生成都要重新赢的对抗，故须持续测（不可答测试集 + 负拒绝率，RGB 实测 ChatGPT 级仅 43–45%）。

**实验 5 深入（实体碰撞的机制）**：为什么「Einstein 水管工」传记还有人答相对论？① 名字是极强的**检索键**，挂着一大团高频高置信先验（相对论/1879/德国/诺贝尔），而「水管工/代顿/1961」是低频弱关联，竞争不过；② 贝叶斯视角——`后验 ∝ 似然(证据) × 先验`，「Einstein=物理学家」是一个**极尖的先验尖峰**，即使证据反先验也几乎推不动后验；③ 泄漏发生在「先验强 × 证据反先验」交叉最狠处，所以第 1、2 题（最著名于/生于何时何地）泄漏、第 3 题（学徒六年，无竞争先验）不泄漏；④ Transformer 里实体 token 激活高权重关联通路，可压过对上下文的注意力（= 实验 3 fluent substitution 的顺名字触发版）。防法 = 上周响应侧 grounding（每条声明须在证据里找到支撑）+ 本周 FActScore 声明级核验；**凡 query 带知名实体名就是实体碰撞高危区**（对 Avaloka 直接适用）。

**实验 6 深入（三分法 · The Friend）**：给「Meridian Cartworks 成立于 2011」的短文，问「哪年成立 + 今天多少员工」——**成立有据、员工数无据**。纸条自动分三堆：硬答两问的（编了个员工数）、含糊的（「大概几百？」）、只答有据并标出缺口的。这就是**诚实生成的完整三分法：answer / hedge / refuse**，每个用对地方。好 RAG = 第三堆但更有礼貌：「Founded in 2011. The headcount isn't in what you gave me — let's find out.」核心：**诚实不是拒绝，而是给问题的每一半用对动词**（呼应实验 4 满分答案的「据实+标注先验」）。仪器：sufficiency-conditioned accuracy（把答案的正确率按「证据是否充分」分开读）、abstention quality。

**实验 7 深入（Goodhart at the grading desk）+ 学术backbone**：两场同难度小测，规则从 +1/0/**0**（答错不罚）换成 +1/0/**−1**（答错扣分），弃权当场开花——**知识没变，激励变了**。要点：① 诚实是对**评分规则**的理性反应，不是性格——猜在「答错不罚」下严格占优；② 「right=1, wrong-or-blank=0」正是模型一辈子考的卷子，所以我们**亲手把它训成爱蒙的应试者**（They guess because we paid them to）；③ 修法是**改规则不是改模型**——abstention-aware scoring，CRAG 的 **+1/0/−1**；惩罚/奖励之比 = 隐含置信阈值（医院把错答定价 −10 → 阈值更高 → 更爱弃权，接回 Act IV 风险-覆盖曲线）；④ 这坐实全周总纲 `argmax_θ E[μ(q,θ)]`：**选的指标 μ 塑造系统 θ，选错指标=建错系统**——是 Goodhart 的人体实验证明。

> **学术backbone — Kalai, Nachum, Vempala & Zhang, "Why Language Models Hallucinate"（OpenAI, 2025-09, arXiv:2509.04664）**：把实验 7 证成数学结论。两段因果：预训练即使数据完美也因**统计压力**涌现幻觉（错误陈述与事实统计上不可分）；后训练因主流基准**惩罚不确定**而持续。最该记的结论 = **Generation–Classification Inequality：生成错误率 ≥ 2 × 分类错误率（减校准项）——生成正确文本天生比判断其对错更难**。这条不等式是本周多处的统一底座：解释了 Act III **小验证器模式**（验证比生成便宜一半以上，所以用小模型逐条核验大模型划算，非 trick）、也呼应 RAGChecker 双向蕴含与「recall 是难的一半」。解决方案与本周同构——**socio-technical，改主流基准的计分而非另加幻觉基准**：奖励恰当不确定、对自信的错罚得更重、盯校准而非准确率、高风险用 RAG + 置信阈值（逐字 = CRAG +1/0/−1 + ECE + 风险-覆盖曲线）。

---

## 二、The Measure of All Things（生成器半场：Act III–V + Coda）

> Act I 标尺、Act II 六指标阶梯、Interlude 信号与噪声 → 见 [[week-07.zh]]（本版细节更全，如 TREC 2024–25 的 UMBRELA/AutoNuggetizer、rank-biased precision、judged@k 等 fine print，但主线不变）。本周从 Act III 开始。

### Act III · The Generator——从「评食材」到「评厨师」

主厨用普通食材也能做出好菜，笨厨师有完美食材也糟蹋。前面六个指标只评「对的证据有没有送到」，这一幕评「LLM 有没有用好证据」。是上周「响应侧良知（断言-证据二部图）」的**指标侧对应**。

**RAGAS 四指标（起点/地板）**：
- **Faithfulness 忠实度**：把答案拆成声明，逐条对检索上下文核验，报支持比例。后端可用 LLM（灵活但循环）或经典 NLI（更便宜保守，即上周用的 DeBERTa 蕴含）。我们的两道门比 RAGAS 默认分解更激进，通常在这项得分高——但仍要用**外部尺子**测。
- **Answer relevancy 答案相关性**（Psych「Shawn 竞选市长」梗）：从答案反推合成问题，再与原问题算 cosine。答非所问（问无家可归、答棕色软糖豆）→ 相关性 ≈ 0。
- **Context precision**：交给 LLM 的 chunk 里，相关的排在前面吗？（检索排序，换到生成视角。）
- **Context recall**：把 ground-truth 答案拆成声明，每条能否归因到某个检索到的 chunk？漏了关键段落这个数就掉。

> **Quiz 7 流畅的敷衍**：问退款、答运费，每句都被文档完美支持。→ **Faithfulness 仍高，Answer relevancy 崩**。一个对证据、一个对问题，缺一不可——有据的敷衍能完全骗过前者。

**RAGAS 五个局限（所以只当地板不当天花板）**：① 循环 LLM 依赖 + 自我增强偏见（模型给自己打高分，要请「Kepler 不是 Ptolemy」——不同模型家族当 judge）；② 上下文窗口盲（只看送进来的，看不见检索漏掉的十个更好 chunk——那是 Act II 的活）；③ 无声明粒度（一句含 3+ 可独立证伪的声明能整体蒙混过关）；④ 分数不稳定（GPT-4/Claude/Llama 给不同分，厂商还偷偷更新）；⑤ 无归因核验（只查与上下文一致，不查每条声明是否引对段落）。配套纪律 **evaluator pinning**：judge 钉到带日期 checkpoint、维护 50–200 条冻结校准集、定期重跑，**Cohen's κ 漂移 >0.05 = 评估器动了**。

**RAGAS 长大了（2025）**：answer relevancy → response relevancy（说「无可奉告」直接判 0）；context relevance → rank-aware context precision@k + context recall；新增 noise sensitivity 与 factual correctness（对参考做声明级 F1，悄悄放弃纯 reference-free）；加多轮 schema。五条抱怨里两条部分解决、三条仍在。

**FActScore（RAGAS 以来最锋利的进步）**：答案 → 原子事实，逐条核验，报支持比例。2023 年 ChatGPT 生成传记只有 **58%** 事实精度。三年后（页 97）这个数字被**检索+弃权**推动而非单靠规模：2026 带浏览的推理模型 ~99% 声明精度（GPT-5 system card，~1% 错）；GPT-4o 级非推理模型 62–71%（HalluLens LongWiki 71%）；但**无检索的尾部知识依旧残酷**——SimpleQA Verified 最好 72.1%，多数前沿 29–55%，DeepMind FACTS 聚合约 69%。

**RAGChecker**：把「回答」和「ground-truth」都拆成原子声明，双向蕴含核验 → **检索诊断**（claim recall：证据到没到；context precision）+ **生成诊断**（faithfulness、hallucination、noise sensitivity、context utilization，外加别人不测的 **self-knowledge**：答对却不在检索证据里 = 从参数记忆答，暗示污染或参数域知识）。发现 **faithfulness–gullibility 权衡**：越信上下文的模型越忠实、也越容易被噪声带偏——所以 faithfulness 与 noise sensitivity 必须同屏看。RAGAS 是遥测，RAGChecker 是遥测报警后才拿出来的诊断仪。

**核查的经济学（小验证器模式）**：MiniCheck（约 1/400 成本达 GPT-4 精度）、HHEM（便宜到能逐条上生产、驱动公开幻觉榜）、Lynx（HaluBench 87.4%，微超 GPT-4o）。路由策略：**小验证器测每条答案 → RAGChecker 抽样 → 前沿 judge 只测没有专用验证器覆盖的维度**（「家里穿拖鞋，出门穿好鞋」）。

**ALCE（引用本身对不对）**：把声明级核验延伸到引用质量——每条声明引对段落了吗？ChatGPT 级在 ASQA 约 **50% 引用召回**，ELI5 更差；**约每两条引用就有一条可疑**，哪怕答案是对的。企业里**引用准确率是部署门槛**（撑不住的脚注比没脚注更糟）。自动指标与人类一致 85%/78%——够用，别崇拜。

### Act IV · The Frontier——五到六条前沿（书还没合上）

**前沿 1 · LLM-as-a-Judge 2.0**：评估是一项**特定任务**，理应用专用模型而非租前沿大模型。**Prometheus 2**（开源、本地跑、无 API 泄漏）：直接打分（按用户 rubric）+ 成对排名，与人类一致 72–85%。**AutoJ**（打乱顺序防位置偏见）、**JudgeLM**（创新在训练数据=人类偏好）、**G-Eval**（CoT + 分数 token 概率加权，校准更好；要 CoT 一致性 +8–12 分但 3–5× token 成本）。**四种评委偏见**：长度（长答胜）、位置（A/B 摆动 40–60 分）、自我偏好（能翻转排名）、重形式轻实质。**三铁律**：不同模型家族、两个顺序都平均、绝不信单一评委。**Cohen's κ<0.6 拒用**（Landis–Koch：0.41–0.60 中等、0.61–0.80 substantial）；排名用 Kendall's τ，多评委用 Krippendorff's α。**JudgeBench**（350 对客观对错难题）：最好的常规 judge ~64%，推理模型 judge ~75%，微调开源 judge 勉强过随机——**在难对上今天的 judge 都在猜**。**PoLL（评委陪审团）**：3 个异构小 judge 投票，κ 0.763 完胜单个 GPT-4 的 0.627，成本约 1/7——多样性胜过规模（正好呼应「对多个观测者取平均抵消人差方程」）。当心 **preference leakage**（generator 与 judge 同家族/蒸馏血缘会抬分，是污染而非边角）。

**Frontier 1 现场深入（2026-08-01 逐页）：**

*为什么不租通用前沿大模型当评委*（注意：专用评委本身也是 LLM，只是小、微调、本地）——五个理由：① **太贵**（1 万条 $500–2000/次，只敢季度评，本地专用评委边际≈0，能小时级盯）；② **数据泄漏**（每条回答+证据发外部 API；本地无泄漏，Avaloka 个人记忆场景是硬要求）；③ **专用更准**：在 5000 条领域标注上微调的 7B judge，在该领域的人类一致性上**打败 prompt 版 GPT-4**；④ **不可控/会漂移**（厂商悄悄更新模型 → 尺子自变，API 钉不住版本，本地 checkpoint 能钉）；⑤ **偏见+合谋**（同家族 = evaluator collusion，分数虚高）。理论依据 = Generation–Classification 不等式（[[2509.04664-why-language-models-hallucinate]]）：核查比生成便宜，小验证器够用。

*Prometheus 2*：两模式——**direct assessment**（你现场给 rubric，它按标准打绝对分）+ **pairwise ranking**（判 A/B 谁好）。HHH（honest/helpful/harmless）优先级取医生式：**先无害、再诚实、再有用**。例：答「相对论是什么」甩场方程 `G_μν=8πT_μν`——诚实且无害，但对十岁小孩没用（不 helpful）；rubric 能把 helpfulness 编进评分。*三个专用评委各修一个毛病*：AutoJ 修**位置偏见**（自动打乱顺序）、JudgeLM 修**「评委该学什么」**（训练数据=人类评估判断，不是好答案）、G-Eval 修**校准**（CoT + 分数 token 概率加权，得平滑连续分）。

*四偏见→解药*：自我偏好→不同家族；位置(40–60分摆动)→两顺序取平均、只留一致对；长度(长答胜)→把简洁写进 rubric；重形式轻实质→用例子锚 rubric + 先推理再打分。

*Cohen's κ 手算例*（100 条，评委判有据/瞎编 vs 人工真值），公式 κ=(p_o−p_e)/(1−p_e)：
- **迷惑评委**：两者一致 75 条 → p_o=0.75；p_e=0.75×0.70+0.25×0.30=0.60；**κ=(0.75−0.60)/0.40=0.375** → 原始一致率 75% 唬人，κ 只 0.375，**拒用**（那 60% 是碰运气）。
- **偷懒评委**（永远说「有据」）：p_o=0.70 却 p_e=1.0×0.70=0.70 → **κ=0**，当场揭穿「零本事」。
- **靠谱评委**：p_o=0.90，p_e=0.70²+0.30²=0.58 → **κ=0.762**（substantial），**上线**。
要点：**原始一致率会被类别不平衡骗，κ 扣掉运气只留真本事**；企业 κ<0.6 拒用；报给外部的绝对数字必须来自 κ 达标评委。

**前沿 2 · RGB 四能力（RAGAS 从不测的）**：噪声鲁棒（能忽略近似干扰吗？好系统 >80%，naive <50%）、负拒绝、信息整合、反事实鲁棒（文档说 480 端口而其余说 48，会标出矛盾还是盲从？规则：**矛盾是一等公民**，摆出冲突、双方都引、让用户裁决）。→ **Quiz 9 Calabi–Yau 测试**：卖网络交换机的公司，RAG 却热情正确地讲超弦几何 → **负拒绝失败**，答案来自参数记忆，上周的**响应门**本应拦下。RGB 实测 ChatGPT 级负拒绝仅 **43–45%**——「从噪声里编造」仍是多数行为，也是企业最危险的失败模式。

**前沿 3 · 认知谦逊（本周最硬的一段）**：
- 成熟标志：一个**从不说「我不知道」的系统很危险**。讲师暴言仍成立：数百个学生、数百个系统，没见过一个企业 RAG 诚实说过 I don't know。
- **负拒绝率 NRR**：造「语料答不了」的 query 集测诚实弃权；监管行业部署门槛 **>70%**。「机制没有测量只是希望，没有它 guardrail 只是装饰。」
- **2025 警告（AbstentionBench）**：o1/R1 式**推理微调会降低弃权**，规模解决不了。永远**成对报告**：不可答上的拒绝率 + 可答上的过度拒绝率（单看一个都能被 game）。
- **充分性条件下的准确率**：「不可答」在 RAG 里是**检索集的属性**，不是问题的属性。给 pair 标 sufficient/insufficient（autorater 93%）后分开读：前沿模型在充分上下文下极好，在不充分时不弃权反而硬答，靠参数记忆蒙对 35–62%。混合平均会掩盖这个恶习。
- **ECE 期望校准误差**：分 bin 比对「陈述置信度 vs 实际准确率」加权差。完美 0，现代 LLM 0.05–0.15，**越大的 instruction-tuned 模型往往越差**（把置信度推高却没推高准确率）。手算两 bin 例：高置信 bin 过度自信 15 分且主导误差——正是典型 LLM 签名，也是危险区（用户最听高置信答案）。修法：**温度缩放（最便宜最有效）**、Platt、isotonic。
- **风险–覆盖曲线**：只在置信超阈值时作答，扫阈值画曲线。**凸 = 校准好**（弃权一小撮就换来大幅降错）。一次扫描：全答 12% 风险，答 60% 降到 3% 风险。CRAG 把一次幻觉定价为「放弃一个正确答案」，医院定价为十个——**同一条曲线，两种价格，相反工作点**。
- **Conformal abstention（从 vibe 到合同）**：留出集算 nonconformity 分、排序取第 ⌈(n+1)(1−α)⌉ 小当阈值 → 分布无关地保证覆盖率（80–90% factuality 同时保留大部分内容）。是 **SLA 级证书**，但假设与生产流量可交换，**漂移会让证书过期**。

**前沿 4 · 多跳**：信息整合、矛盾检测、桥接推理（Doc A: 药 X 抑制酶 Y；Doc B: 酶 Y 在病 Z 过表达 → 桥：X 可能治 Z）。基准 HotpotQA / MuSiQue / 2WikiMultihopQA / **MultiHop-RAG（每跳标注 ground-truth，可评路径非只评终点）** / BRIEF（压成原子命题，看答案是否幸存）。

**前沿 5 · 会反击的评估集**：**ARES**（150 条人工标注 + 合成扩展 + **PPI 预测驱动推断** 给每指标置信区间；合成买覆盖、少量人工买校准）。**变异算子**进化题库：翻转期望答案（测负拒绝）、加约束、增歧义（测消歧）、要求多跳、注入干扰项。**Giskard RAGET**（直接从知识库生成）、**DeepEval**（RAGAS 超集）。让尺子永不僵化。

**前沿 6 · Agentic / 轨迹评估**：两个 agent 同样答对，一个靠推理一个靠蒙——只看终点分不出，蒙的那个下一道难题就崩（**Illusion of Competence**）。**TRACE** 评轨迹：过程效率（步数/token/工具调用）、认知质量（规划/假设）、每步证据 grounding，加脚手架评估。三层：端到端 / 轨迹质量 / 节点级。**pass@k（乐观数）vs pass^k（工程师数）**：单run 0.70 时，pass@3 升到 ~0.973，pass^3 落到 ~0.34；GPT-4o 在 τ-retail 从 ~61%@k=1 掉到 ~25%——「70% 成功」不是完成 70%，是对十个客户里三个彻底坏掉。**Quiz 10**：10 次跑 7 成，pass@3≈0.99（乐观）、pass^3≈0.29（进 SLA）。归因难：**MAST**（14 种失败模式，验证失败和能力失败一样常见）、**Who&When**（找出肇事 agent 仅 53.5%、肇事步 14.2%，事后取证未解决）——所以**在运行时给每个阶段埋点**，让「谁失败」变成自家遥测里的查表。**工作栈**：离线闸门（gold+NDCG+RAGAS+FActScore+ECE 卡合并）+ 在线驱动（thumbs、shadow judge、人工抽检、interleaving）。工具 LangSmith/Phoenix/Langfuse/W&B。行业冷数字：过半组织已上生产 agent，质量是首要障碍，**约 70% 的 RAG 仍无系统化评估——你不会在那 70% 里**。

**Frontier 6 现场深入（p.136–139，Claude 受限期间用 ChatGPT 补的，例子已核对与讲义一致）：**

*三层 agentic 评估（p.136）*——① **Level 1 系统效率**（latency / tokens / tool calls / cost per query）：operational，只说跑得快不快贵不贵，**不证明质量**。例：问「酒店报销上限」，Agent A(2s/1检索/1k token/$0.01) vs Agent B(25s/8检索/7k/$0.12)，都答对 $250 → Level 1 说 A 好，但快而便宜也可能答错。② **Level 2 会话结果**（task success / answer correctness / satisfaction）：传统端到端视角，只看**最后成没成**，不告诉你**为什么**（可能碰巧蒙对）。③ **Level 3 节点级精度**（right tool? well-formed query? sound step?）：逐节点查——**诊断力就在这层**。例：问「收购我们最大供应商的公司的 CEO 是谁」（正解 Maria Chen），Level 2 只说「对/错」；若错成 David Lee，Level 3 能定位到「多跳没崩，是**实体消歧**崩了——Beta Holdings vs Beta Technologies 选错」，于是针对性修（查询加全名/实体 ID/同名干扰测试）。医疗例：问「病人适不适合药 X」答「不建议」——Level 2 都算对，但 Level 3 分得出「查了过敏史+禁忌」的好过程 vs「没查记录、凭常识碰巧蒙对」的坏过程，**高风险场景这两者绝不能同分**。

*pass@k vs pass^k（p.137，两问一日志）*——`pass@k = 1−(1−p)^k`（乐观数：k 次里至少成一次）；`pass^k = p^k`（工程师数:k 个同境客户全部成功）。单次 p=0.7 时：pass@3=0.973、pass@8≈0.9999(趋近 1)；pass^3=0.343、pass^8≈5.8%(趋近 0)。**同一批日志、两个相反结论**——「给我 8 次机会几乎必成一次」vs「连续服务 8 个客户全成只有 5.8%」。**有 verifier+可重试的 harness 活在乐观曲线(pass@k)；面向客户的 agent 活在工程曲线(pass^k)**。陷阱：报「pass@8=99%」若无可靠 verifier 从 8 个候选里挑出对的，对生产几乎没价值。退款 5 步链例：每步 0.9 → 0.9⁵≈59%、0.9¹⁰≈35%，「每步 90%」不等于流程 90%。

*Quiz 10（p.138–139，用不放回精确算）*——10 次跑 7 成(成7败3)，从中抽 3 次：**pass@3** = 1 − C(3,3)/C(10,3) = 1 − 1/120 = **119/120 ≈ 99.2%**（只有恰好抽中那 3 次失败才算不通过）；**pass^3** = C(7,3)/C(10,3) = 35/120 ≈ **29.2%**。**客户 SLA 写 pass^3≈29.2%**（连续三个同境客户全成才三成）；pass@3≈99.2% 只license「允许多试+有可靠 verifier 时，很可能产出至少一个对的」。（注:不放回精确值 99.2%/29.2% ≠ 理论独立近似 97.3%/34.3%。）

**贯穿一切的告诫 · Goodhart 定律**：「当测量变成目标，它就不再是好测量。」RAG 特有的 reward hacking + 防护：hedge inflation（只训 faithfulness → 过度对冲「有可能……」；配 relevancy+informativeness）、citation padding（配 precision + rubric 里放简洁）、length gaming（长度归一化 judge）、**evaluator collusion（generator 与 judge 同家族 → 三铁律）**。防护套装：**指标集成 + 对抗 eval + 红队攻击指标 + 从不用于训练的 held-out 金评委**。一句总纲：**Kelvin 测量、Cameron 警告、Goodhart 解释警告如何成真**。

**答案的经济学（Pareto 前沿）**：$5/30 秒的答案可能不如 $0.05/2 秒且质量 85% 的。配 cost@quality、quality@cost、tokens-per-correct-answer、以及 CFO 的 **dollars-per-correct-answer**；前沿之下的系统不该上线。

**多轮**：contextual faithfulness、context-switch 处理、turn efficiency。**MTRAG**（首个人造端到端多轮 RAG 基准：110 段对话、均 7.7 轮、~25% 不可答）——系统在后段退化、最难的是不可答、直接用最后一轮 query 检索远差于改写后；**把同样事实分片跨轮给，性能掉 ~39%**（模型早早猜、锁死、不回头）。

### Act V · The Observatory（本周相较 Week 07 的全新一幕）

评估不再在「生产开始处」结束——**天文台从不关门**。一个器官，两种节奏：
- **离线（gate the merge）**：eval 套件在它能**卡住一次合并**的那天成为基础设施——每个 PR 跑金数据集回归（确定性断言 + 钉住的 judge 指标）、每晚更大套件、每周刷新。
- **在线（drive improvement）**：canary 用隐式信号给实时流量打分——**改写=反对票、复制进邮件=赞成票、关标签页=用脚投票**。
- **棘轮（ratchet）**：每一次生产失败都变成**永久、带版本的用例**，闸门此后永远拒绝它。
- 离线通过而在线下滑，这个**分歧本身就是一个指标**：世界正在离开你的测试集。

**Drift（缓慢的紧急事件）**：生成仍流畅而检索在挨饿；数月里结构化任务稳定、**RAG 任务漂移 25–75%**，漂移集中在检索耦合路径。默认做法 **domain-classifier bet**：训小分类器区分「冻结参考样本的 query embedding」与「本周实时的」，**AUC≈0.5 睡得香**，每高一分都是可利用的真实差异——这是 Act I 的 eval decay 装上了针，每天读而不是事后验尸才发现。

> **domain-classifier 漂移探针搭建步骤**（本质=分类器两样本检验：分类器能分开两拨=分布不同，AUC 是效应量）：① 上线时冻结 1000–5000 条 query 的 embedding，标 class0=参考（**冻结不动**）；② 本周实时抽等量 embedding，标 class1；③ 训个**简单**分类器（逻辑回归/小 MLP/GBDT）区分二者，交叉验证；④ 读 AUC——**≈0.5 无漂移（你希望输的赌注），>0.6–0.7 报警**；⑤ 每天/每周跑、画 AUC 时序、设阈值；⑥ 报警后：看哪些 query 最像 class1（新主题/新用户群）→ 在漂移切片上重测 Recall/nDCG → 刷新评估集/重 embedding/重建索引。要点：两类样本量对齐、参考与实时用**同一 embedding 模型**、参考要冻结较久否则测不出慢漂移、它只报「变了」不报「变好变坏」（需回检索指标确认）。

**Shadow / Canary / Interleave**：shadow（复制流量不服务，比 judge 胜率/成本/延迟 + 检索重叠 Jaccard，重建索引迁移最划算的诊断）；canary（1–10% 流量走预注册闸门 + 自动回滚 + 旧索引保温）；**interleaving**（把两个 ranker 结果混进同一 session、按点击记功，同样偏好用 **10–100× 更少流量**测出——一下午 vs 十天）。

**CFO 指标**：cost per correct answer（5¢/query × 78% 正确 = 6.4¢/正确答案；40¢ × 88% = 45¢——多花 7 倍买 10 分质量，值不值不是 x 轴能回答的。**你买的是正确答案不是查询，先做除法再比较**）。

**三角闭合**：红队变成 CI 里的回归套件，成对计分（攻击成功率 + 良性误报率）——只压 ASR 最省的路是过度封锁，合法 query 买单。成熟度指标 = **对全新攻击模式的检测时间（time-to-detection）**，这是攻击者无法替你 Goodhart 的一个数。

### Coda · The Evaluation Map（把一切接回前几周）

**每个组件有失败模式，每个失败模式有指标，一个低分就是一个诊断/工单**。压力下读图（从红仪表盘到最便宜的下一步）：
- NDCG 低但答案 FActScore 高 → 生成器能扛，**reranker 在饿它** → 修 reranker。
- Faithfulness 低、context recall 高 → **生成器的错** → 重训/微调/换（prompt 工程救不了）。
- Context recall 低 → **修 chunking/检索**，下游无法补救没到的证据。
- ECE 高 → 温度缩放置信头 / 在校准集上回归口头置信度。
- 负拒绝低 → 收紧**请求门 + grounding 严格度**（上周的两个旋钮）。

**最深的指标**：不是 faithfulness、不是 NDCG，而是开场那个——**它知道自己不知道吗？** 95% faithfulness + 20% NRR 听着辉煌，直到遇上唯一答不了的问题然后撒谎；在法庭/医院/交易台，那个谎是唯一重要的指标。**最后一句归用户**：系统的度量不是精选基准上的最佳表现，而是**没人预料到的 query 上的最差表现**（NPS、满意度、赞/踩）——把评估集建成能在用户之前找到那些 query。

**三个参考栈**：① **研讨栈**（一个周末、$0）：pytrec_eval + RAGAS + 对 20 个抽样失败跑 RAGChecker + 手搓风险-覆盖曲线，一台笔记本涵盖全课概念；② **创业栈**（自托管精简）：Langfuse 追踪 + promptfoo 卡合并 + MiniCheck 逐条 + RAGET 种子题库（改写 + 掺不可答）+ Phoenix/Evidently 测漂移；③ **受监管企业栈**：全部自托管+钉版本、对常设人工审计样本做 PPI 认证区间、conformal 弃权按季校准。工具是「冻结在软件里的意见」，**judge（不是库）决定有效性**。

**五篇「承重墙」如何连成一套体系**（缺一块就漏）：RAGAS（整体模块该测什么）→ FActScore（每条原子事实是否可靠，58% 唤醒钟）→ RGB（生成器四能力）→ On Calibration of Modern Neural Networks（Guo et al. ICML，ECE/温度缩放/可靠性图的经典理论根）→ Prometheus 2（开源本地评委）。链条：**RAGAS 测模块 → FActScore 核原子事实 → RGB 诊断生成能力 → ECE 校准置信度 → Prometheus 2 规模化评审**。延伸阅读（Oliver Twist 8）：BEIR（别迷信向量检索，BM25 曾羞辱 dense）· MTEB（选 embedding 看 retrieval 子分）· ALCE（引用≠证据正确）· ARES（150 人工标注 + PPI 放大）· Smucker 2007（配对 bootstrap 判涨幅真假）· MultiHop-RAG（逐跳证据链）· BRIEF（原子命题压缩，压后须测 context recall）· LangChain State of AI Agents（趋势比百分比耐久）。

**全天收尾（Kelvin/Cameron 的平衡）**：*Kelvin* 说「测量才会知道」（没测量就只能凭感觉改）；*Cameron* 说「不是所有重要的都能被计数」（仪表盘全绿也可能漏掉长尾致命错、语气误导、关键时刻过度自信）。工程师站在两者之间：**造尺子 → 逐层评估 → 评估 judge 本身 → 而比墙上所有指标都重要的,是造一个「知道自己何时不知道」的系统**。最危险的从来不是系统不知道,而是**它不知道却仍表现得非常确定**。

---

## 三、与前几周的关系 / 解锁的 Agent 能力

Week 01–02 建「意义即几何」和检索地基 → Week 07 用六指标量它 → **本周量生成器 + 上线后的观测**。上周（Week 06）挂了两道门给系统「弃权」和「核查」的机制，**本周给认知谦逊造指标**：NRR 测弃权、noise robustness 测抗干扰、ECE 测置信诚实。机制 + 测量才是可信生产系统。是「证据驱动架构升级」（2026-06-06 决策）的方法论闭环：**先有指标基线，才谈加组件**。

解锁：可测量的自我怀疑（NRR + ECE 给数字）、组件级诊断（Evaluation Map 把红仪表盘变工单）、忠实度/引用硬门（FActScore/ALCE 设成部署 gate）、防 Goodhart 的评估纪律（指标集成 + held-out 金评委）、以及**上线后的持续观测**（离线闸门 + 在线驱动 + 漂移分类器 + 棘轮）。

## 四、Avaloka 应用（初步，待课后细化）

- 把「好朋友」范式写进 Avaloka 的回答契约：**答有据的、对无据的说「一起查查看」、把先验标为「众所周知」**——正是实验 4/6 的最佳答案形态。
- eval artifact 升级：在 Week 07 的检索指标基线（Recall@5/MRR/nDCG@5）之上，补 **RAGAS 四指标（地板）+ FActScore（声明级）+ ALCE（引用）+ ECE + 负拒绝率**。
- 用 **Calabi–Yau 探针**测 Avaloka 的负拒绝，回应讲师「没见过企业 RAG 说过 I don't know」的挑战；目标向监管门槛 >70% 靠拢。
- 上小验证器路由（MiniCheck/HHEM 逐条 + 抽样 RAGChecker），别一上来就租前沿 judge；judge 用**不同家族 + 钉 checkpoint + κ 校准**。
- 建 Observatory 雏形：离线金数据集回归卡合并 + 在线隐式信号（改写/复制/关闭）+ **domain-classifier 漂移探针**每日读 + 失败棘轮。
- 求职（T010）呼应上周合流：**评估工程 = machine 之上的判断层**，按 R3/E4「内建验证」重新包装 Avaloka + 本周指标能力。

## 五、一句话总结

上周量检索，这周量**生成器本身 + 上线后的世界**。开场七个亲手失败（人差方程 → judge 偏见、过度自信、幻觉、参数泄漏、实体碰撞、答/含糊/拒三分法、评分台 Goodhart）逐一对应下午的指标；正课把 RAGAS（地板）→ FActScore/ALCE（声明与引用）→ LLM-as-Judge 2.0 + RGB 四能力 + NRR/ECE/风险-覆盖（认知谦逊）→ 多跳/进化题库/轨迹评估（前沿）→ Observatory（离线闸门 + 在线驱动 + 漂移 + 棘轮）串成一条链，最后用 Evaluation Map 把每个低分接回「该修哪个组件、花下一个工程小时在哪」。总纲不变：**你无法改进你无法测量的东西**；而最深的一个指标，是**它知道自己不知道吗**。

## 参考文献（本版新增/强调，部分）

Es et al. 2023 RAGAS · Min et al. 2023 FActScore(EMNLP) · Chen et al. 2024 RGB(AAAI) · Kim et al. 2024 Prometheus 2(EMNLP) · Guo et al. 2017 On Calibration(ICML, ECE) · Gao et al. 2023 ALCE(EMNLP) · Saad-Falcon et al. 2024 ARES(NAACL) · Ru et al. 2024 RAGChecker(NeurIPS D&B) · Verga et al. 2024 PoLL(Replacing Judges with Juries) · Upadhyay/Pradeep et al. 2024 UMBRELA & TREC RAG · Mohri & Hashimoto 2024 Conformal Factuality(ICML) · Katsis et al. 2025 MTRAG(TACL) · OpenAI 2025 GPT-5 System Card · Tang & Yang 2024 MultiHop-RAG · Jiang et al. 2025 BRIEF(NAACL)
