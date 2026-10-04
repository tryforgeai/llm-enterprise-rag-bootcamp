# Week 04 总结 —— 替身演员：search-native text 与派生 artifact

**日期：** 2026-06-27 · **来源：** `resources/week-4-summer-lesson-plan.pdf`（Asif Qamar, SupportVectors）、Dense X Retrieval 与 RAPTOR 论文、Week 04 实验（T016、T017）

---

## 一句话结论

整周可以压成一句话：

> **我们检索派生 artifact；我们展示原文。**

Week 01–03 一直悄悄假设着同一件事：我们索引的东西**就是**作者写的文本。Semantic chunking 只是换了个切法。Contextual retrieval 只是给原文加了装饰。Late chunking 只是在隐空间里对原文做 pooling。**底料从来没变过。**

Week 04 放弃这个假设，整门课的姿态随之转向。我们不再问「怎么把文档切好」，而开始问：

> **如果最适合被检索的文本，是这篇文档从来没有字面写过的文本呢？**

整周遵循的设计原则：

> **不要等用户的 query 去匹配你的文档。制造能匹配用户 query 的文档。**

---

## 第一幕：目的问题（The Purpose Problem）

只有一个论点，但要让它扎进去：**文本抗拒检索不是偶然，而是设计使然** —— 因为每一篇文本都是为某个人写的，而那个人从来不是搜索引擎。

### Meera 和 Ravi

两个准备 IIT 入学考试的学生。**Meera** 读物理是为了**理解**它 —— 她在牛顿第三定律上停留，直到能在骨头里感受到力的对称；她推导、她怀疑、她重建。**Ravi** 有一个教练和一万道往年真题。他刷到看见「两个滑块、一个滑轮、摩擦系数 μ」的瞬间，手就已经动起来了。他不是在理解问题。**他是在匹配问题。**

谁对？这是个坑 —— **目的决定表示（purpose dictates representation）。** 考深度概念迁移，Meera 赢。考「三小时两百题」，Ravi 赢，而且不是小赢。这不是在贬低 Ravi；**对他的目的而言，他的表示是正确的。** 错误在于把他的目的和 Meera 的目的搞混。

对我们这门课的落点：

```
教科书是为 Meera 写的。
Query 时刻的 RAG 就是 Ravi。
```

教科书是累积式地搭建理解，每个想法压在上一个之上。RAG 需要看一个短问题，然后立刻抓到能回答它的那段。**当你把一份 Meera-文本索引给一个 Ravi-任务，你得到的就是错配 —— 而这个错配，是我们见过的一半烂 RAG demo 的沉默病根。** 解法不是把教科书读得更好，而是**从它里面制造出 Ravi 的抽认卡，然后索引那些卡。**

### 每一段文本都穿着戏服

同一个底层发现 —— *某药物把 30 天死亡率降低了 4%* —— 写在六个不同的房间里：

| 戏服 | 为谁写 | 对这个 claim 做了什么 |
| --- | --- | --- |
| **论文在对冲** | 一个怀疑的 peer reviewer | IMRaD 把它拆开：数字在 Results，含义在 Discussion，Abstract 把两者都软化成 "may suggest a modest benefit" |
| **法律文书在封堵** | 对手 | 预判反驳，把操作性条款埋在 "notwithstanding the foregoing" 后面 |
| **财报电话会在稀释共识** | 股东和律师同时 | 责任被分散，每个 claim 都戴着头盔 |
| **新闻稿** | 买家 | 在卖 |
| **教科书** | 学习者 | 在教 |
| **推文** | 观众 | 在挑逗 |

六件戏服，一个真相 —— 而真正该让人不安的是：用户的 query，*"does the drug reduce deaths?"*，**跟其中任何一件都匹配得不好。**

> **Query 是赤裸的。文本穿着戏服。** 检索就是那场尴尬的聚会：赤裸的 query 必须在六层伪装里认出一个朋友。

### Search-native text

**Search-native text** —— 被塑造成「让一个直白 query 能落在上面」的文本 —— 几乎从来不是原始文本。搜索者是一个**在写作完成之后才到场**的受众，说着另一种方言：短、陈述式、没耐心、以问句形式出现。

原文和理想的检索 artifact 可以几乎不共享任何词：

```
Query:  "Can the licensor end the contract early?"
原文:    "notwithstanding the provisions of Section 12(b), the Licensor
         retains the irrevocable right to terminate"
```

**同义，词汇完全不相交。** Embedding 模型能桥接一部分 —— 它就是干这个的 —— 但不是全部。

### 几何上的原因：embedding dilution（嵌入稀释）

这是整周赖以成立的机制。一个断言了 *n* 个不同 claim 的段落，**不会**嵌在其中任何一个附近。一阶近似下：

```
e_para ≈ (1/n) · Σ e_i
```

其中每个 `e_i` 是一个 self-contained claim 的 embedding。一个尖锐的 query `q` 坐在某个顶点 `e_k` 附近。那么它和段落的相似度就是一个**被稀释**的量：

```
cos(q, e_para) ≈ (1/n) · Σ cos(q, e_i)  ≤  cos(q, e_k)
```

因为唯一有用的那一项 `cos(q, e_k)`，被 *n − 1* 个不相关的邻居**平均掉了**。

几何上讲：若干语义上彼此不同的向量取均值，会落在它们**凸包的内部** —— 离每一个顶点都远。段落的 embedding **就是**那个内点。**这不是 embedding 模型的缺陷；这是算术。**（当成启发式而非定理 —— 真实的 pooling 是非线性的 —— 但方向完全正确。）

**Factoid 抽取就是解药**：单独索引 `e_k`，稀释就消失了。

---

## 第二幕：派生 artifact —— 以及证明

四种 artifact，加上那条让它们变安全的 pattern。而且刻意在中间被一次测量打断，好让没人凭信仰接受「派生的更好」。

### 1. Factoid（proposition）—— 意义的原子

**factoid 是仍然具有意义的最小文本单元。** 化学类比不只是修辞：分子是仍保有某物质性质的最小单元。把水劈开，你得到氢和氧 —— 有用，但**不再是湿的**。factoid 就是语义分子：劈开它，你得到的碎片不再**关于**任何东西。

经典例子：

> Berlin, situated on the banks of the River Spree, serves as the capital of Germany and is its most populous city, with a metropolitan population exceeding six million residents. The city has been a center of European politics since reunification in 1990.

这一段里藏了**至少五个 factoid** —— 柏林位于施普雷河畔；柏林是德国首都；柏林是德国人口最多的城市；柏林都会区人口超过六百万；柏林自 1990 年起是政治中心。每一个都完整、可独立站立，而**没有任何一个以独立句子的形式出现在原段落里**。"the capital of Germany" 被焊在一个更长的从句里。抽取就是把它撬下来、把代词解析掉，让它能**不带任何关于原段落的记忆**站在索引里。

**功夫全在 self-containment 上。** 一个懒惰的抽取器返回 *"It is the capital"* —— 没用，因为 "it" 已经和 "Berlin" 断了。一个好的抽取器返回 *"Berlin is the capital of Germany."* 这就是为什么 factoid 抽取是整条 pipeline 里**最值得做 prompt 优化**的一环；生产用的 prompt 是在自己语料上做大量 **DSPy 调优**的产物，正因为「self-contained factoid」和「悬空碎片」之间的差别，就是「可被检索的思想」和「噪声」之间的差别。

Dense X Retrieval 给的规模参照：**FactoidWiki 平均每句约 2.25 个 proposition** —— 这既是普通文字压缩了多少意义的度量，也是 passage 级索引**藏起了多少检索目标**的度量。

### 2. Passage rewrite（段落重写）—— 源文本的替身

> 学术文字是为了被论辩而写，法律文字是为了被辩护而写，企业文字是为了被遗忘而写。

**passage rewrite** 把一段文本改写成朴素、直接、便于检索的语言，**同时不改变其含义**。原文保留；重写是一份**影子文档**，和原文并列索引 —— 对用户不可见，对 retriever 高度可见。

```
原文:  Notwithstanding the provisions of Section 12(b), the Licensor retains
       the irrevocable right to terminate this Agreement upon thirty (30)
       calendar days' written notice.

重写:  The licensor can terminate the agreement with 30 days' written
       notice, regardless of Section 12(b).
```

必须诚实点出的真实风险：**简化会掉精度。** "irrevocable" 是一个法律术语，朴素重写把它丢了。这个风险靠下面那条核心 pattern 化解 —— 重写只负责**找到**条款；生成模型读的和引用的，是原文。

> **重写是诱饵；原文是证据。** 替身演员为 retriever 试镜，好让主角能上台表演。

### 3. QA pair —— 种下 query 形状的对象

所有 artifact 里最狡猾的一种，也是对「戏服问题」最直接的攻击。给定一个 chunk，让 LLM 生成这个 chunk 能回答的那些可能问题，配上答案，然后把两者都 embed。

为什么有效：检索是一个**匹配**问题，而**当两边说同一种方言时匹配最容易**。通常 dense retriever 做的是**跨体裁**比较 —— 一个问句去量一段陈述性散文。但如果被索引的对象本身就是从**问句**派生出来的，这个比较就变成了**同体裁：问句对问句**。你种下了一个 query 形状的诱饵，retriever 应该能找到它。

一条好的 pipeline 给每个 chunk 生成 **3 到 8 个问题**，在三个轴上变化：

- **具体度** —— 从 "what does this section discuss?" 到 "what learning rate did experiment 3 use?"
- **表述方式** —— 偏关键词 到 偏自然语言
- **抽象层级** —— 事实型 到 解释型

每一对都存一个**指回源 chunk 的指针**，因为生成答案时模型必须看到 chunk，而不是那个合成出来的问题。

**要用眼睛去查的失败模式：** 一个粗心的合成问题会误导 retriever，承诺一个源文本其实并不包含的答案。**生成卫生（generation hygiene）很重要。**

> **HyDE 是镜像。** QA pair 在**入库时**把索引变成问句形状。HyDE 在**查询时**把 query 变成文档形状 —— 让 LLM 幻觉出一个假想答案，embed 它，再用它去检索。两者从相反的两端关闭同一个体裁鸿沟。**两个都可以做。**

### 4. 核心 pattern —— 让这一切变安全的那条

> **检索打派生物。生成用源文本。**
> **每个派生 artifact 都带着一个回家的指针。**

factoid、rewrite、QA pair —— 每一个对某类 query 来说都是**比 raw chunk 更好的诱饵**，同时也都是**更糟的引用对象**。所以我们永远不引用它们。**它们赢得检索；原文提供证词。**

这才是把爆炸半径限住的东西。因为模型读的和引用的永远是源文本，**一个笨拙的重写或一个过度热情的 factoid 可以让你丢一次检索，但永远造不出一个伪造的引用。**

这也干净地解决了 Meera–Ravi 的张力：**我们从来没有扔掉教科书。** Ravi 的抽认卡**索引**理解；Meera 的文本仍然**就是**理解。考前突击表没有取代学习 —— 它指回了学习。

### 还有那句要说出口的悄悄话

> **这场 bake-off 不是「用派生物取代 raw」，而是「派生物叠加在 raw 之上」。**

raw chunk 索引**永远不离开系统**。有些 query —— "§4.2 到底说了什么？" —— 由原段落来服务最好，而 raw 索引正是它们该落的地方。我们不是在拆掉 Week 03 的成果。**我们是在给它配同事。** 对每一种表示唯一要问的是：**它在付什么房租？**

---

## 第三幕：高度 —— Summary 与 RAPTOR

第二幕里的一切都是**局部的** —— factoid、rewrite、QA pair 都运作在单个段落的高度上。但有些问题无论抽取得多好，都不可能从任何单一段落里得到回答，**因为它们的答案不在文档「里面」；它是「关于」这份文档的。**

### Abstractive summarization 是高度的改变，不是压缩

「压缩」暗示同样的内容被更紧地塞进一个更小的盒子。摘要不是那样。**它是坐热气球上升：** 你升高，从地面上看不见的大结构浮现出来 —— 海岸线的形状、田野的纹理 —— 而在地面上占满你视野的细节消失了。**你用分辨率换取范围。哪个视角都不更真。**

所以 summary 是 factoid 的**互补**，永远不是它的替代：

```
Factoid  牺牲上下文  换取精度
Summary  牺牲精度    换取上下文
```

有些 query 在地面上无法回答 —— "这份报告讲什么？"、"主要发现是什么？"、"这版政策和上一版有什么不同？" **没有任何单个 chunk 包含答案，因为答案分布在整体之中。**

Philip Anderson 的 **"More Is Different"** 精确地命名了这个原理：在每一个尺度层级上，都会出现下一层级看不见的、性质上全新的属性。**一份文档的主题是它 chunk 的涌现属性 —— 在任何一个 chunk 里都不存在，只在高处可见。**

**三个工程决策：**

| 决策 | 选择 |
| --- | --- |
| **粒度（granularity）** | 按 chunk / 按 section / 按文档 / 按语料做摘要 —— 每一种都是不同的 artifact，有不同的检索行为 |
| **忠实性（faithfulness）** | abstractive summary 会幻觉，而**对 RAG 来说，一个自信的错误摘要比没有摘要更糟。** 必须靠 prompting、验证或引用要求来强制 |
| **索引方式（indexing）** | summary 通常住在**自己的 namespace** 里，因为它们的检索特性和 chunk 差别太大，混不到一起 |

一旦你接受**高度是一个旋钮**，问题就变成：为什么只选一档？按 section 回答"methods 部分覆盖了什么"；按文档回答"这篇论文的贡献是什么"；按语料回答"这整个集合讲什么"。每一种相对其价值都很便宜，而且每一种都能捕到其他档位漏掉的一整条主题型 query 带。而一旦你有了几个固定高度的摘要，**你离「把高度变成连续的」只差一小步。** 那一步就是 RAPTOR。

### RAPTOR：变焦镜头

Sarthi et al., *Recursive Abstractive Processing for Tree-Organized Retrieval.* 五行讲完：

```
1. 从 leaf 级 chunk 开始。
2. 按 embedding 相似度对邻近 chunk 做聚类。
3. 把每个簇摘要成一个新节点。
4. 重复：对摘要聚类，再对簇做摘要。
5. 停在单一根节点（或少数几个高层节点）。
```

结果是一棵树。叶子是细粒度 chunk；中间节点是逐级更抽象的摘要；根是整体的梗概。**检索时你同时搜索所有层级：**

| Query 类型 | 落在 |
| --- | --- |
| 事实型 —— "learning rate 是多少？" | **叶子** |
| 主题型 —— "整体方法论是什么？" | **中间节点** |
| 全局型 —— "这个集合是关于什么的？" | **根** |

> **Query 自己选放大倍数。索引是一个变焦镜头，不是一个固定焦段。**

想象一个星系。从内部看，你看到一颗颗恒星 —— 叶子。拉远，恒星模糊成旋臂 —— 中间节点。再拉远，整个星系变成一枚发亮的硬币 —— 根。**没有哪个放大倍数是"真的那个"；每一个回答的是关于同一个对象的不同问题。**

**Matryoshka 的类比是精确的**：Matryoshka embedding 是一个在多种维度下都有意义的向量；RAPTOR 是一个可以在多种分辨率下被检索的语料。Matryoshka 给你多分辨率的**向量**；RAPTOR 给你多分辨率的**文本**。

**要归档的那个细节：** RAPTOR 的聚类是在 **UMAP 降维后的 embedding 上做软的、可重叠的高斯混合（GMM）分配** —— 一个 chunk 可以属于多个簇，因为一个段落可以同时关于多件事。**这个软聚类就是通往 Week 05 的铰链。**

### 要带出教室的那个想法：definitive article（定稿式条目）

在**单篇文档**上跑 RAPTOR，它的上层节点是这篇文档的摘要。在**一个语料**上跑 —— 一百篇论文、一千张支持工单、某个主题下的所有内部备忘 —— **簇就不再尊重文档边界了。** 一个簇聚起的是**关于同一件事**的 chunk，不管它们住在哪里。于是它的摘要是某种全新的东西：不是任何单一来源的摘录，而是**跨全部来源的综合 —— 一篇任何单篇文档都不包含的、关于某个主题的定稿条目。**

设想去问一个书架 —— PRML 和 Hastie–Tibshirani–Friedman 的 *Elements of Statistical Learning* 放在一起 —— "什么是 overfitting？" 一个朴素系统返回 Bishop 的最佳 chunk **或者** ESL 的最佳 chunk。一个语料级 RAPTOR 节点返回**一个已经把两种处理方式调和进同一段规范文字的、连贯的答案。**

这就是 **definitive-article 属性**，也是为什么这件事不是「多几步的摘要」。它是 Anderson 的 *More Is Different* 在检索上的兑现：语料级条目是一个**涌现对象** —— 它在任何源文档里都不存在，而且**不可能**存在，因为它是这个集合的属性，不是任何成员的属性。我们是在字面意义上**制造这个语料从未为自己写过的那条百科条目。**

而这周**刻意**停在这里。要把那条条目做好，你最终会想按**关系结构**聚类，而不是按原始 embedding 邻近度 —— 哪些实体和想法在跨文档层面真正相连。那是图上的 community detection，值得单独一天。

---

## PRML bake-off：这周如何自证

Lesson plan 指定的那次测量，以及为什么 PRML 是「理想的反派」。

**语料：** Bishop 的 PRML，§1.1–3.2 —— 从多项式曲线拟合叙事一路到 model selection 与 bias–variance。

**问题：** *Why does polynomial regression overfit on a small dataset?*

**为什么这个问题很残忍：** Bishop 从来没用一句话回答它。他是**演示**它 —— 拟合 M = 0, 1, 3, 9；展示 M = 9 的曲线穿过每一个点地剧烈抖动；列表显示系数 **w\*** 爆炸到巨大量级；然后才引入正则化。因果性的答案**是整个 §1.1 的弧线**。你真正想要的那句话 ——

> "a high-degree polynomial has more free parameters than data points, so it fits the noise, and its coefficients blow up"

—— **在 Bishop 书里根本不以句子的形式存在。** 它分布在一张图、一张表和三个段落里。一本为 Meera 写的教科书，被问了一个 Ravi 式的问题。

**保持 bake-off 诚实的三条规则**（一个强 embedder 碰上词汇丰富的 query，能让朴素基线显得比实际更好；而一个注了水的 demo 什么也教不了）：

1. **用真正存在词汇错配的 query。** Bishop 写的是 "coefficients become large"；学生问的是 *"why do the weights blow up when the curve gets too wiggly?"* 派生路径已经把这种方言归一化了，raw chunk 没有。**差距就在那里被拉开。**
2. **要包含 synthesis（综合型）query。** *"What is the relationship between model complexity, dataset size, and overfitting here?"* 它的答案横跨三个 chunk。raw chunking 返回一个碎片；派生路径 —— 以及之后的 RAPTOR —— 把整体装配起来。
3. **打分要打 answer-ability，不是 topical relevance。** 问题不是「有没有返回一个相关的 chunk」，而是**「你能不能真的从返回的东西里，自足地写出答案」**。**这才是派生物能诚实取胜的那个指标。**

### Centroid Tug-of-War（质心拔河）

把稀释不等式用身体证明，而不是用白板。在地板上用胶带圈出一块作为 embedding space：

- **五个志愿者是事实顶点** —— "on the Spree"、"capital"、"most populous"、"six million"、"political center since 1990" —— 彼此站开，因为他们的含义彼此不同。
- **第六个学生是那个段落**，按游戏规则必须站在五个位置的**平均点**。他最后被孤零零地困在正中间，**离所有人一臂之远，离谁都不近。**
- **第七个学生是 query** —— "What is the population of Berlin?" —— 走进来伸手去找最近邻。**只索引段落时，房间里离他最近的就是那个被困在中间的质心学生。匹配很远；你能看见那个伸手的动作。**
- **然后我们做 factoid 抽取。** 段落溶解，五个顶点作为独立点各自站出来，query 直直地走到 "six million" 那个顶点前。**距离在全班面前坍塌。**

那个收缩的间隙就是 `cos(q, e_k) ≥ cos(q, e_para)` 的体感版。**那个方程，和那个从被困质心走向 "six million" 顶点的学生，是同一句话说了两遍。**

---

## 四个 Lab

| Lab | 要建什么 | 真正重要的指标 |
| --- | --- | --- |
| **1. 仪器化的 PRML bake-off** | 把 PRML 前三章用三种方式入库 ——（a）raw-chunk 索引、（b）factoid 索引、（c）QA-pair 索引。三者**全部保持在线**并**融合**结果。20 个 query 分三带：pointed factual / vocabulary-mismatch / synthesis | Recall@k、MRR，以及最重要的**人工 answer-ability 判断**。三条臂之间 embedding 模型、chunker、top-k 必须**固定**；唯一允许变的变量是表示本身 |
| **2. Factoid 与 QA 抽取 pipeline** | 在 50 个 chunk 的样本上建两个 LLM 抽取器：一个把 chunk 分解成 self-contained factoid，一个每 chunk 生成 3–8 个 QA pair | **去读那些 artifact。** 找出那个仍然写着 "it" 而不是 "Berlin" 的 factoid。找出那个源文本其实答不了的合成问题。**这些在聚合指标里看不见，在纸面上一目了然** |
| **3. 两个高度的 RAPTOR 树** | 在同样的章节上实现 2–3 层的 cluster–summarize–recurse；把 Lab 1 的 synthesis query 打向树的不同层级，看它们落在哪 | 树的深度到底有没有改善 synthesis 带的 recall？**成本账本要一直摊开** —— 两层花了多少次摘要调用，在语料规模上每晚重建一次要多少钱？ |
| **4. 多表示锦标赛** | 把 raw chunk、factoid、QA pair、RAPTOR 节点合到一个融合 retriever 后面。然后**做消融** —— 依次移除每一种表示，测量系统级的下降 | 一张诚实的表：一行一种表示，一列一个 query 带，显示每个 artifact 到底在哪里挣回了它的存储和入库成本。**某种表示会在你的语料上几乎毫无贡献；那是一个发现，不是一次失败** |

**预期的结果形状：** raw chunk 在 pointed 带上守得住，派生物在 mismatch 带上拉开，而 synthesis 带是所有人都吃力的地方 —— 那正是 RAPTOR 挣饭钱的地方。

---

## 这一天的节奏

> **先意外，再机制，最后原则：顺序本身就是教学法。**

```
Frame            为什么原始文本抗拒检索 —— 目的、受众、IMRaD、赤裸的 query
Toolkit 上半     factoid 作为原子；embedding dilution 作为敌人
Proof            PRML bake-off（可感知的差距）+ Centroid Tug-of-War（为什么）
Toolkit 下半     rewrite、QA pair、「检索打派生物，生成用源文本」
Altitude         abstractive summary；RAPTOR 的变焦镜头
Corpus           跨文档综合出的 definitive article —— 通往 GraphRAG 的桥
```

注意那个刻意的打断：先见工具箱，**立刻用证明把它打断**，等到没人怀疑「这东西确实需要」之后，才把工具箱补完。

---

## 我们实际建了什么 —— 以及诚实的缺口

我们 Week 04 的工作（T016、T017）在真实基础设施上把**第二幕的局部 artifact** 端到端做完了。**第三幕 —— RAPTOR —— 我们没建。**

### 已建：四种 artifact 对比 — `course/week_04/retrieval_artifact_comparison/`

在三个源上的真实（不是模拟）RAG demo —— PRML 第 2 章、PRML 第 3 章、Dense-X 论文 —— 把**四种 artifact 类型索引进同一个向量空间**。最终 SV embedding 索引：**49 条记录，1024 维**，通过课堂集群用 `Qwen/Qwen3-Embedding-0.6B` 生成。

| Artifact 类型 | 记录数 | | 来源 | 记录数 |
| --- | ---: | --- | --- | ---: |
| QA pair | 22 | | Dense-X | 24 |
| Abstractive summary | 11 | | PRML 第 2 章 | 13 |
| Proposition | 10 | | PRML 第 3 章 | 12 |
| Raw chunk | 6 | | | |

完整 pipeline，无 TF-IDF fallback：

```
raw chunks → SV chat 生成 QA → SV embedding 索引
→ SV query embedding → cosine top-k → SV chat grounded answer
```

两次查询，top hit 都是 QA pair：

- `What is a proposition in Dense-X?` → `qa_dense_x_002`，**0.8703**
- `What is the goal of proposition-level retrieval?` → `svqa_raw_dense_x_002_2`，**0.8795**

同体裁效应如预期在起作用 —— **同时也是一个警告。** 那些分数相对其他 artifact 类型是被抬高的，**恰恰因为**问句对问句比问句对证据更容易匹配。把四种 artifact 放在同一个不做区分的空间里排序，结果是 QA pair 在分数上赢，但不一定在 answer-ability 上赢。Lesson plan 的 Lab 4 消融正是对这件事的正确回应，**而我们没跑。**

那套 7 问的 eval（`artifacts/eval_questions.json`）值得读，因为每个问题都**事先写明了预期的 artifact 行为** —— 一份写下来的预测：

| 问题形态 | 预测赢家 |
| --- | --- |
| "What is a proposition in Dense-X?" | QA pair / proposition —— 原子定义 |
| "Why can proposition-level retrieval help RAG?" | QA pair / summary —— 要因果解释，不是定义 |
| "What does PRML Chapter 2 teach?" | Abstractive summary —— 章节级 query 没有任何 chunk 能答 |
| "What is the beta distribution used for in PRML Chapter 2?" | QA pair —— 直接事实 |

配套 artifact：`source_manifest.json`、`abstractive_summaries.json`、`dense_x_propositions.json`、`qa_pairs.json`、`generated_qa_pairs_sv.json`（用 `openai/gpt-oss-20b` 生成 12 对）、`raw_chunks_sample.json`、`local_retrieval_index.json`（37 条 TF-IDF 基线）、`sv_embedding_index.json`。构建脚本：`scripts/build_local_retrieval_index.py`。

### 已建：Xennials FactoidWiki — `course/week_04/task_02_xennials_factoid_wiki/`

同样的思路搬到线上源，小规模复现 FactoidWiki 的构建。Wikipedia "Xennials" → 6 个 section → **11 个 section-aware raw chunk** → **88 个 factoid**（`Qwen/Qwen3-VL-8B-Instruct`）→ **88 个 QA pair** → 一个覆盖全部三种 artifact 类型的 **187 条记录、1024 维**索引，外加一个做浏览、搜索和 grounded 合成的 Streamlit UI。

那个比例就是发现本身：**11 个 raw chunk 变成了 187 条索引记录（约 17 倍）。** 语料很小，但这个 fan-out 就是整周的成本面，而且和下面 Dense-X 的语料算术是同一条曲线。

这个 187 条记录的索引，后来成了我们 agentic RAG eval 基线的语料（`evals/`）—— **Week 04 造出了 Week 06–07 被考核时所用的那个测试语料。**

### 已建：chunking pipeline — `course/week_04/chunking_pipeline/`

基于 Docling，三个 notebook（`01-docling_chunking`、`02-contextual_and_late_chunking`、`03-chunking_pipeline`）—— 把 Week 03 的 contextual / late chunking 这条线收成可运行代码。

### 没建

| Lesson plan 里的项目 | 状态 |
| --- | --- |
| **Passage rewrite** | 未实现。**这是我们完全跳过的唯一一个局部 artifact** —— 也是对任何含法律或政策文字的语料最相关的那一个 |
| **Lab 1（按规格）** | 部分完成。我们用的是 PRML 第 2–3 章加自己的问题，而不是 §1.1–3.2 加那个 overfitting 问题；而且**从未给 vocabulary-mismatch 带和 synthesis 带打分** —— 而 lesson plan 说，派生物本该正是在那里拉开 |
| **Answer-ability 判断** | 未打分。我们测的是 cosine 分数，后来是 recall —— **从来没测「能不能从返回的东西里自足地作答」** |
| **Lab 3 —— RAPTOR 树** | 未建。没有 cluster–summarize–recurse，没有多高度检索，没有成本账本 |
| **Lab 4 —— 消融锦标赛** | 未跑。我们在一个索引里放了四种表示，而**对哪些在付房租毫无证据** |

按 `PROJECT_PLAN.md`，RAPTOR 是「可用的干预手段，不是默认里程碑」—— 所以跳过它是一个**决定**，不是疏漏。但 Lab 1、3、4 都还敞着，而 **Lab 4 是三者中最便宜、信息量最大的那个。**

---

## Dense X Retrieval：factoid 主张背后的数字

这周 factoid 想法的出处（Chen et al., EMNLP 2024）。值得把「它证明了什么」和「它没证明什么」分开。

**头条：** proposition 级索引在 unsupervised retriever 上比 passage 级高 **+10.1 Recall@20**（supervised 上 +2.7）。

**两个改变「谁该在意」的发现：**

1. **Unsupervised retriever 提升很大，supervised 很小。** SimCSE 和 Contriever 的 Recall@5 分别 +12.0 和 +9.3（相对 35.0% / 22.5%）。而 DPR —— 在 NQ、TQA、WebQ、SQuAD 上训练过 —— 在其中三个训练集上用 proposition 反而**略差**。**Proposition 是一个泛化修复，不是普适升级。** 如果你的 retriever 已经在自己的 query–passage 对上 fine-tune 过，收益会小得多。
2. **这是一个长尾收益。** proposition 在稀有实体上大幅领先，随实体频率上升差距收窄（20,000 条测试 query 里约 25% 的目标实体频率 ≤ 3）。**对头部实体，passage 检索本来就够用。**

**下游**，在 LLaMA-2-7B、固定 500 token 预算下，proposition 比 passage 高 **+4.1 / +3.2 / +2.7 / +2.8 EM**（SimCSE / Contriever / DPR / GTR）；sentence 大致居中。差距最大的是 **100–200 词**区间 —— 约 10 个 proposition、5 个句子、或 2 个 passage。超过约 500 词三种粒度收敛。*这就是信息密度机制，也是 lesson plan 为什么死抠 prompt 预算。*

**语料算术 —— 成本面：**

| 单元 | 数量 | 平均词数 |
| --- | ---: | ---: |
| Passages | 41,393,528 | 58.5 |
| Sentences | 114,219,127 | 21.0 |
| Propositions | 256,885,003 | 11.2 |

**Proposition 的索引记录数是 passage 的约 6.2 倍。** 任何要把企业语料 propositionize 的提案，都必须带上这个数字。

**生成 proposition 的质量**（人工分析，随机 50 个 passage）—— 注意弱点在哪：

| 错误类型 | GPT-4 | Propositionizer（Flan-T5-large） |
| --- | ---: | ---: |
| 不忠实 | 0.7% | 1.3% |
| 不够最小 | 2.9% | 2.0% |
| **不能独立成立** | **4.9%** | **3.1%** |

用 42k 个 GPT-4 生成对蒸馏出的 Flan-T5-large 已经很接近 GPT-4。**self-containment 是最弱的那根轴** —— 恰好是整个方法赖以成立的那个属性，也恰好是 Lab 2 叫你用眼睛去找的东西。

---

## 真正重要的结果：我们的第一次测量失败了

Week 04 写下了一个预测。`evals/cases/EV-001.json` 原话记录了它：

> "Week 04 predicted QA-pair and factoid artifacts outrank the raw chunk for query-shaped questions; this case measures whether that holds."

基线运行（`evals/results/latest.md`，2026-08-14，**lexical** retriever，k=5，187 条记录）：

| 指标 | 数值 |
| --- | ---: |
| 通过用例 | 6 / 10 |
| mean recall@5 | 0.3333 |
| mean nDCG@5 | 0.3773 |
| mean MRR | 0.6 |
| decision accuracy | 0.9 |
| negative rejection rate | 0.6667 |

**EV-001 —— "What is a Xennial?" —— recall@5 = 0.0。** 一个专门为回答它而建的语料，碰上最简单不过的问题。

那个显而易见的解释**被测过而且被否掉了**：在其他条件全部不变的情况下往 tokenizer 上加了个 stemmer，recall@5 仍然是 0.0 —— top-5 只是换成了另外几条同样不是定义的记录。

真实原因：去掉停用词后，query 就剩单个词 `xennial`。**43 条记录都含它，而且大多 term frequency 相同**，BM25 已经没有任何区分信号，排序坍缩到文档长度归一化上。gold 记录 `fact_xennials_lead_01_07` 本身就是单数形式，依然输了，**2.50 对 2.77，纯粹输在长度上**（24 token vs. 14）。

三个结论：

1. **artifact 做得再好，也救不了一个没有信号可排序的 retriever。** 单词 query 给 lexical scorer 留不下任何可区分的东西。解法指向 dense retrieval 或 query expansion，不是 tokenizer。
2. **把语料原子化让这件事变**糟**了。** 88 个 factoid 每个都含 `xennial` 且 term frequency 相近，**这正好是 BM25 退化的条件**。**细粒度索引放大了「大量近似记录」这个失败模式** —— 这是 lesson plan 没有讨论的成本，因为它全程假设用的是 dense retriever。
3. **这周的主张从来不是一个 lexical 主张。** Dense X 测的是 dense dual-encoder；我们测的是 lexical，拿到相反结果。不是矛盾 —— 是适用范围的修正，也是对 lesson plan 自己那条「除表示之外一切固定」的提醒。

最便宜的下一步已经就位：187 条记录全部带 `Qwen/Qwen3-Embedding-0.6B` 向量，`--retriever dense` 也已实现。缺的只有 query 向量，需要课堂 endpoint —— **趁课程网络还在，一次课就够**（`tasks/T025`）。

---

## 这周产出的工程约束

1. **索引期生成把 hallucination 挪到了上游。** query 期的 guardrail 抓不到一个在索引时就被编造出来的事实。任何 propositionizer 都需要在记录进索引**之前**对着源 span 做忠实性检查 —— 就是把 lesson plan 的 faithfulness 决策从 summary 推广到 factoid。
2. **约 3–5% 的 not-stand-alone 是实测比率，不是理论风险。** 在 Wikipedia 规模上是背景噪声；在小而高风险的语料上是一次事故。**我们需要的不只是生成器，还有 validator。**
3. **Summary 要有自己的 namespace。** 它们的检索特性和 chunk 差别太大，混不到一起 —— 而我们那个 49 条的索引就是混着的，这很可能是 QA pair 在分数上通杀的部分原因。
4. **回家的指针不是可选项。** Week 04 两个索引里每条记录都带 `source_pointer` / `source_url`。这就是限住爆炸半径的东西：派生物可以让你丢一次检索，但造不出伪造引用。
5. **每个派生索引都要过一次房租检查。** 生成成本、存储、过期都是真实的；6.2 倍 fan-out 意味着 6.2 倍的失效面。**Lab 4 的消融表是唯一诚实的取舍方式。**

---

## 留给团队的开放问题

1. 如果 QA pair 系统性地压过其他 artifact 类型（我们这几次 0.87–0.88），这些类型到底还该不该放在同一个空间里排序 —— 还是分 namespace 检索，再用 RRF 做类型感知加权融合？
2. 当一篇文章的 88 个 factoid 全都含同一个核心词时，去重 / 近重复策略是什么？EV-001 说明这是**主要**失败模式，不是边角情况。
3. QA-pair 生成器**没生成**的那些问题怎么覆盖？生成更多、查询时用 HyDE、还是加一条非 query-shaped 的支路？
4. 考虑到掉精度的风险，为我们自己的文字建一个 passage-rewrite 索引值得吗 —— 核心 pattern 在实践中真的能化解那个风险吗？
5. 源变更之后的重新生成策略是什么？factoid、rewrite、QA pair、summary 全都会过期。
6. LLM 生成的 factoid 是否需要存一个忠实性分数，检索能不能用它？
7. 最便宜的有用 RAPTOR 是什么：单文档上两层，还是直接跳到语料级聚类 —— 毕竟 definitive-article 属性只在那里才真的出现？

---

## 阅读材料

**必读：**

- **Chen et al.** —— *Dense X Retrieval: What Retrieval Granularity Should We Use?* factoid 想法的出处；确立了检索粒度是一个有可测后果的设计变量。
- **Sarthi et al.** —— *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.* 检索分辨率应当匹配 query 的抽象程度。**注意那个软聚类 —— 它是通往 Week 05 的铰链。**
- **Bishop** —— *PRML* §1.1–3.2。bake-off 语料。**专门把多项式曲线拟合那段当成一个检索问题**来重读。
- **Ma et al.** —— *Multi-Vector Retrieval as a Multi-Representation Learning Problem.* 把整周形式化了：一份文档应该由多个向量（或多段文本）表示，各自捕捉一个不同侧面。

**选读：** Gao et al.（HyDE）· Wang et al.（InPars / 合成 query 生成）· Dhuliawala et al.（Chain-of-Verification）· Asai et al.（Self-RAG）· Anderson, *More Is Different*（1972）—— 四页物理，解释为什么一个语料具有任何单篇文档都不具有的属性。

---

## 这周在整条主线上的位置

```
Week 01 —— RAG pipeline 的端到端全貌
Week 02 —— 向量空间为什么根本上能成立
Week 03 —— 源文档在进入这个空间之前，如何被切开或被保全
Week 04 —— 我们到底要不要索引源本身，还是索引从它制造出来的 artifact
Week 05 —— 从一本书到一座图书馆：软聚类以网络分析、community detection、
          GraphRAG 和 Memory-GraphRAG 的形式回来
```

有三周时间，我们把文档当作**要被索引的那个东西**。Week 04 把它当作**原材料** —— 一个用来制造更适合被索引的东西的底料。

> **文本是为读者写的；检索需要的是为 query 写的 artifact。所以我们制造那个 artifact，我们检索它 —— 与 raw chunk 并列，永不取代它 —— 然后我们把原文展示给读者。我们检索派生物。我们用源文本生成。**

---

## 后续动作

- `tasks/T025` —— 趁课程网络还能用，把 dense retriever 那条支路在 EV-001 上跑掉。最便宜的干预，它的结果决定 query expansion / hybrid / reranker 值不值得试。
- **Lab 4（未跑）** —— 对我们现有的四种表示做消融。索引有了，但**哪些表示挣回了成本，我们毫无证据。**
- **Lab 1 的两个带（未跑）** —— 给 vocabulary-mismatch 带和 synthesis 带打分，用 answer-ability 而不是 cosine。**这周的主张本该正是在那里才看得见。**
- `tasks/T027` —— Week 04 **和** Week 05 的课程笔记（`course/week_04/week-04.zh.md`、`course/week_05/week-05.zh.md`）。本文是给团队的总结，不是课程笔记。
- `tasks/T026` —— answerability / abstention gate。EV-006 以 confidence 1.0 回答了一个本该拒答的问题。
