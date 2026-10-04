# 第 10 周课堂笔记

日期：2026-08-15

状态：讲义（Week 10 Lesson Plan，*The Library of Many Catalogues*，Asif Qamar，SupportVectors，29 页）已读完并整理成完整精读笔记；开场 Prelude（*The Room as the Corpus*，20 页）**全部收齐并逐页记录**；正课 deck（*The Library of Many Catalogues*，125 页）**已逐页记录 p.3–p.87 的大部分**（缺页见第〇-B 节末的补课）。Lab 动手实现待课后补充。

来源：
- `summer-week-10-lesson-plan.pdf`（*Enterprise RAG: The Library of Many Catalogues — Retrieval Architecture, from the Representation to the Verdict*，29 页）
- `the-room-as-the-corpus.pdf`（开场 Prelude 幻灯，**20 页，完整**）
- `the-library-of-many-catalogues.pdf`（正课 deck，**125 页**）
- 实物教具：实验一发到手的航海图 `OTLETIA — Approaches to Otlet Harbour`（SupportVectors 自制，页脚标 *Week 10 prelude · Experiment I*）
- 讲义自述其来源：RetrievalCraft monograph（同名）及其配套 deck。**讲义是 refresher 和第一返回点，monograph 是完整解剖，book chapter 课后跟进** —— monograph 待补。

> **本周定位**：Week 09 是「温和的一周」——语料拿到了自己的档案（OKF），我们把那条被治理的通道诚实地放在一架**还没搭出来的**升级阶梯的最顶端。今天把那架梯子一级一级搭出来，而且**用整整一天**：上午十一点到晚上八点半，整个检索侧的房子。
>
> 种子是六月第一天就埋下的：**检索是 RAG 的承重墙，因为生成器无法引用检索从未浮出水面的东西。** 此后每一周都靠在这堵墙上——Week 04 的派生物、Week 05 的图、随后的护栏与评估——今天这堵墙终于拿到它的工程学。
>
> **唯一要留存的一句**：*A retrieval system is not a search over documents. It is a **portfolio of representations** and a **court of adjudication**.* ——一个检索系统不是「在文档上做搜索」，而是**一组表征的投资组合**加上**一座裁决的法庭**：对同一份语料做许多目的各异的投影，再用一串法官（先便宜后昂贵）决定该信哪一个投影。今天所有内容都是这句话的展开。

---


## 〇-A、开场体验：The Room as the Corpus（Prelude · 20 页 · 全部收齐）

**连续第三周的「先动手/先失败，再命名」开场**——而且形式在递进：

| 周 | Prelude 标题 | 形式 | 场地 |
|---|---|---|---|
| 08 | *The Personal Equation* | **七个你注定失败的小实验** | 你的神经系统 |
| 09 | *The Library in Your Head* | **四个思想实验** | 你的脑子 |
| 10 | *The Room as the Corpus* | **四个用手做的实验** | **这个房间** |

**从「在你体内测量」→「在你脑中设计」→「用你的手搭建」。** 前两周你是被测量的仪器、是设计者；今天你是**劳工**——亲手当一次 Otlet 的馆员。

> **全部 20 页已收齐**（完整 PDF `the-room-as-the-corpus.pdf`），以下逐页记录。


### 幻灯一 · 标题页

> **The Room as the Corpus**
> **Four experiments to run with your hands, before we build the library**
>
> *Today the corpus is not on a server. It is this room, these tables, and the paper on the floor. Everything we build this afternoon, you will have already done by lunch.*
>
> **中文**：**房间即语料库**——**在我们建图书馆之前，四个用手做的实验**。*今天语料不在服务器上。它就是这个房间、这些桌子、地上的纸。今天下午我们建的每一样东西，你在午饭前就已经做过了。*

- **标题的字面意思就是它的技术主张。** 今天讲义里那座 1895 年的 Mundaneum，用的就是纸卡、抽屉、走在抽屉之间的馆员——**一部没有电的检索系统**。把教室宣布为语料库，等于让你在无电条件下把整套架构跑一遍：**桌子是索引，地上的纸是文档，你的手是 I/O**。正对讲义那句边注——*His institution died because every projection and every query cost a clerk; **ours costs electricity**.* **上午你要亲自付一次「馆员」这个代价，下午才会明白 LLM 到底把什么变便宜了。**
- **"...you will have already done by lunch" 是整个教学法。** 这是 Week 09 那句核心倒转（*understanding happened at authoring time; the exam merely retrieved it*）的换装版本：**先让你在没有术语的情况下把事情做对，下午的讲义只负责给你已经做过的动作起名字。**
- **今天格外需要这个锚点**，因为正课极长（11:00–20:30，三幕）。讲义自己预告了这张幻灯的用途：*When the notation thickens — and by mid-afternoon it will — remember that **every equation describes something Otlet's clerks once did with fountain pens**.* **用手做过一遍 = 给下午每个公式预留一个身体记忆的挂钩**——DCL 的分母、RRF 的名次求和、光圈阈值，届时都能回指到上午某个具体动作。
- 页数比 Week 09 的 Prelude（31 页）短，符合「正课极长，开场克制」。


### 幻灯二 · **HOW THIS WORKS：Run it, then name it**

> **HOW THIS WORKS**
> # **Run it, then name it**
>
> *Each experiment is **run first** — with **bodies, objects, and paper, no theory**. Then we **harvest** what actually happened. Then we give **the seed a quiet name** and plant it for the afternoon.*
>
> ***Nothing this morning requires knowing what a retriever is. Everything this morning will be waiting for you when the main deck names it.***
>
> **中文**：**这套东西是怎么运作的**。**先做，再命名**。*每个实验**先被做一遍**——**用身体、实物和纸，不讲理论**。然后我们**收获**实际发生了什么。然后我们给**那颗种子一个安静的名字**，把它种下去，留给下午。* ***今天上午没有任何一件事需要你知道「retriever」是什么。而今天上午的每一件事，都会在下午主讲义给它命名时等着你。***

- **⭐ 这一页把三拍结构显式写出来了**：**Run it（做）→ Harvest（收获）→ The Seed（命名）**。此前我是从 Week 09 的体例推断出来的，这里是原文确认。
- **「用身体、实物和纸，不讲理论」** —— 与 p.1「房间即语料库」一致：**上午的算力单位是人和纸。**
- **⭐ 最后那句是整个 Prelude 的契约**：***上午不需要你懂任何术语；而上午的一切，会在下午被命名时等着你。*** ——**先有经验，后有词汇；词汇不是新知识，是给已有经验贴的标签。**

### 幻灯三 · **THE MAP FOR THIS PRELUDE：Four experiments**

> **THE MAP FOR THIS PRELUDE**
> # **Four experiments**
>
> **EXPERIMENT I** — *Many Maps* ｜ **EXPERIMENT II** — *Five Senses* ｜ **EXPERIMENT III** — *Five Catalogues* ｜ **EXPERIMENT IV** — *Scattered Sheets* ｜ **HARVEST** — *Four Seeds*
>
> **中文**：**这场序曲的地图 · 四个实验**：**实验一 · 许多地图**｜**实验二 · 五种感官**｜**实验三 · 五个目录**｜**实验四 · 散落的纸**｜**收获 · 四颗种子**

- 目录页，与 p.19（Harvest · Four Seeds）首尾呼应。**四个实验 + 一次收束，共五段。**


### 幻灯四 · Experiment I · Run it — Many maps of one country

> **Many maps of one country**
>
> Four maps of the same region are on the front table: a **nautical chart**, a **road atlas**, a **subway map**, a **topographic sheet**. Each of you takes one — **you may not trade.**
>
> ***Question one:*** How do I get from the station to the harbour? *Answer from your map only. Time yourself.*
> ***Question two:*** Where will the water go when it floods?
>
> **中文**：**一个国家的许多张地图**。前面桌上有同一片区域的四张地图：**航海图、公路地图册、地铁图、地形图**。你们每人拿一张——**不许交换**。**问题一**：我怎么从火车站到港口？*只准用你手上那张地图回答，给自己计时。* **问题二**：发洪水时水会往哪里流？

- **"Many maps of one country" 就是 "One corpus, many catalogues" 的换词**——**国家 = 语料，地图 = 索引**。四张画的是同一片疆域，**没有任何一张画了全部，也没有任何一张是错的**。讲义「仪器柜」一节开场引的 **Korzybski「地图不是疆域」**在这里**退回成字面**：真的发四张纸质地图。
- **每张地图扔掉了什么，才是它的身份**：

| 地图 | 保留 / 扔掉 | 对应车道 |
|---|---|---|
| **公路地图册** | 几何真实 + 街道网；粒度粗 | **通用 dense / chunk 索引**——什么都还行，什么都不精 |
| **地铁图** | **只保留连通关系，几何全扔**（Beck 1931 那张著名的图根本不按比例） | **QA pair / factoid 索引**——为一类问题牺牲其余，在那类问题上无敌 |
| **航海图** | 水深、潮汐、进港航道；**陆地基本空白** | **专科 / 稀疏车道**——领域内极精确，出了领域全瞎 |
| **地形图** | **等高线、海拔**——其他三张都没有的**一个维度** | **summary / community 索引**——回答关于**结构**的问题 |

- **两道题是设计过的高度对照**：**问题一（车站→港口）是点/语境查询**，地铁图与公路册答得又快又好；**问题二（洪水往哪流）是结构性/全局查询**，**只有地形图答得了**——因为答案**不在任何一个地点上，而在等高线的结构里**。另外三张不是答得差，是**在结构上不可能答**。这就是讲义那条：**落错高度不会报错，会给你一个自信的不相关答案**——而错答的人不会觉得自己在瞎猜，**因为他手上那张地图看起来很权威**。
- **三个藏在规则里的机关**：
  - **"you may not trade"（不许交换）才是实验的核心**——它把每个人**强制变成一个单一索引**：不能问隔壁、不能融合。这就是**全景敞视监狱**：一只眼睛宣称拥有全部视野。等禁令解除、全场合起来回答时，**融合就是重建**这句话就自证了。
  - **"Time yourself"（计时）不是走过场**——同一个问题，**对的表征答得快，错的表征要么慢、要么答不出**。这一笔计时晚上会变成：**延迟不是性能指标，它是一条决定「哪些法官有资格入席」的结构性约束。**
  - **缺席是静默的**——拿航海图的人**不会收到「火车站未收录」的报错**，他会盯着一张精美的图然后确信这里没有火车站。**这是召回天花板的手工演示：你的表征从没编码过的东西，你再盯多久也召不回来，而且不会有任何信号告诉你它漏了。**


### 实物 · 我抽到的那张：**OTLETIA — Approaches to Otlet Harbour**（航海图）

> 副标题：*Nautical chart · soundings in metres at chart datum · lights and shoals · **NO ROADS***
> 图右半边：***(land: not charted)***
> 页脚：*OTLETIA · SupportVectors · Week 10 prelude · Experiment I*

**注意国名与港名**：**OTLETIA、Otlet Harbour**——整个虚构地理都是用 **Paul Otlet** 命名的，**上午的 Mundaneum 已经埋在地名里了**。

**图上实际存了什么（精度高得离谱）**：

- **水深（soundings）**，精确到 0.1 米：`4.4` `1.3` `9.1` `3.9` `2.8` `5.7`…… 外加多条等深线
- **灯标特征**：`Iso 6s` · `Fl.R 4s` · `Fl.G 3s` · `Fl(2) 10s`——**这些是唯一标识符**，靠精确匹配闪光节奏来认灯
- **命名的危险物**：`Otlet Shoal (1.8 m)`，虚线红圈圈出
- **一条方位线**：`Leading Line 052°`
- **码头信息**：`OTLET HARBOUR quays 3–7 m`
- **西侧海域**：`OCEANUS OCCIDENTALIS`；罗盘玫瑰；0–5 km 比例尺

**对应车道**：**专科 / 稀疏车道的完美化身**——赢在**罕见词、标识符、精确数值、只出现一次的名字**（`Fl.R 4s` 就是一个只出现一次的名字），**光圈内精确到小数点，出了光圈一片空白**。

**两道题的实际结果**：

- **问题一：答不了，但失败方式很微妙。** 我手上**有目的地**，而且精度全场最高（Otlet Harbour、码头水深 3–7 m、进港航向 052°、进港前避开 1.8 m 的 Otlet Shoal）；**但没有起点**——火车站不在图上，路不在图上，陆地根本没被测绘。于是处在一个很具体的诱惑里：**半个 query 被极高置信度地满足了**，很容易输出「港口在东南岸，水深 3–7 米」这种**听起来很专业、却完全没回答问题**的答案。**这是「自信的不相关答案」的教科书范例，而它之所以可信，正是因为它带着小数点。** 诚实的答案是**明确弃权**。
- **问题二：几乎全瞎，但不是零贡献。** 没有陆地高程，答不了「水怎么流」；**但能贡献一条边界条件**——水最终**去哪里**（Oceanus Occidentalis 与那个天然内凹的海湾），以及**受纳水体有多深**。翻译成检索术语：**一条基本瞎掉的车道，仍然可以贡献一条高置信度的事实**——而 **RRF 的设计恰恰奖励这个**（「被**任何一条**车道排得高的文档都会上升」）。**你不需要每条车道都全能，你需要每条车道在自己擅长的那一点上把正确答案顶到高位。**

**三个藏在这张纸里的机关**：

1. **`NO ROADS` —— 这张图自报了自己的光圈。** 这是全场最重要的一句话，**因为生产环境里的索引不会这么做**：你的向量索引被问到光圈之外的问题时，**不会说 "land: not charted"**，它会**安静地返回一个余弦 0.71 的最佳匹配**，而你无从分辨那是答案还是沙子。这直接接上今天的**两栏账簿**（缺席的代价只能由测量来写）与 Week 09 OKF 那条「**覆盖在结构上是局部的，而我们如实说出这一点**」。**诚实的部分覆盖 > 沉默的全覆盖假象。**（对应本仓库 `tasks/T026-answerability-abstention-gate` —— **这张图就是一个印在纸上的 abstention gate**。）
2. **`soundings in metres at chart datum` —— 这是封存的标尺。** 水深不是绝对值，是**相对于一个约定基准面**（通常为最低天文潮位）测的；**离开这个基准，`1.8` 毫无意义**。这就是**光圈教条**的物理版（*一个模型上的 0.7 和另一个模型上的 0.7 是不同的光圈*）以及出口校准那条（*0.8 分在周二和上线那天必须意思相同*）。**Chart datum 就是海图界的封存标尺——航海界花了两百年统一它，而我们的向量检索还在到处用不可移植的绝对阈值。**
3. **`Leading Line 052°` —— 这是一件写时派生物。** **没有任何船长在进港时现场推导这条线**：某位测量员**测过一次**，算出能安全避开 Otlet Shoal 的方位，**印在图上**，此后每条船**白拿**。这就是 Week 09 Walk V Harvest 那笔账——***The card is expensive once***——以及今天的主线：**能花在「静止之物」上的智能就都花在那儿，算力的冰山属于水面之下。** 而 **`Otlet Shoal (1.8 m)` 那个虚线圈是它的对偶**：图不只告诉你该走哪，**还指名了陷阱在哪**。


### 幻灯五 · Experiment I · **HARVEST** — Whose map won — and when?

> **EXPERIMENT I · HARVEST**
> # **Whose map won — and when?**
>
> The **subway map** answered question one **in seconds**. The **nautical chart was useless for it**. The **road atlas was right, but slow**.
>
> Then question two — and the **topographic sheet**, **mute a moment ago**, was **the only map in the room that could speak**.
>
> ***Nobody held a bad map.*** Each held a map that had **decided what to attend to** — **and the deciding is what made it usable**. **Carroll's mile-to-the-mile map answers everything and can never be unfolded.**
>
> **中文**：**实验一 · 收获**。**谁的地图赢了——以及在什么时候赢的？** **地铁图**在**几秒之内**回答了第一问。**航海图对它毫无用处。** **公路地图册答对了，但很慢。** 然后是第二问——**地形图**，**刚才还哑口无言**，成了**全场唯一能开口的那张地图**。***没有人手里拿着一张坏地图。*** 每个人手里那张，都**做过一次「注意什么」的决定**——**而正是那个决定让它变得可用**。**Carroll 那张一英里比一英里的地图什么都能回答，却永远摊不开。**

- **⭐ 三条结果逐条印证了课前的推演**：
  - **航海图对第一问毫无用处** —— 正是我抽到的那张 `NO ROADS`：**有目的地、没有起点**。
  - **地形图在第一问哑口无言、在第二问成为唯一能开口的** —— **高度决定谁能说话**。
  - **⭐ 公路册「答对了，但很慢」** —— 这就是 p.4「**给自己计时**」那条指令的收成：**对的表征答得快；勉强能答的表征，慢**。它在这里第一次把**延迟**引入判据，晚上会变成「**延迟是一条决定哪些法官有资格入席的结构性约束**」。
- **⭐ `Nobody held a bad map` 是这一页的主句**：**失败不是质量问题，是匹配问题。** 而 **`the deciding is what made it usable`（正是那个决定让它可用）**——**有损不是代价，是可用性的来源。**
- **Carroll 在 Prelude 就已经出现**：正课 p.9（*Mein Herr's map*）不是新引入，是**把上午埋的这句展开成一整页**。

### 幻灯六 · Experiment I · **THE SEED** — A representation is a choice of what to ignore

> **EXPERIMENT I · THE SEED**
> # **A representation is a choice of what to ignore**
>
> Every map is a **lossy projection** of the country. **Its power comes from the loss.** The **subway map threw away geography and kept topology**; the **topographic sheet threw away roads and kept height**.
>
> *This afternoon: **BM25 keeps the words; the dense lane keeps the meaning; the factoid index keeps the claim; the summary keeps the theme. None is the country.** **We will build the atlas — and a court to decide which page to open.***
>
> **中文**：**实验一 · 种子**。**一个表征，是一次「选择忽略什么」的决定**。每一张地图都是这个国家的**有损投影**。**它的力量来自那份损失。** **地铁图丢掉了几何、留下了拓扑**；**地形图丢掉了道路、留下了高度**。
> *今天下午：**BM25 留下词；dense 车道留下意思；factoid 索引留下声明；summary 留下主题。没有一个是那个国家本身。** **我们将建起那本地图册——以及一座决定翻开哪一页的法庭。***

- **⭐ 这一页与正课 p.11 的右栏几乎逐字相同。** 也就是说 **p.2 那句承诺被字面兑现了**：*上午的一切会在下午被命名时等着你*——**等着你的不是「类似的意思」，是同一段话。**
- **`Its power comes from the loss.`** —— 比正课 p.11 的 `because of what it threw away` 更短、更硬。**这是全天关于「有损」的最凝练表述。**
- **两个丢弃的例子给得很准**：**地铁图丢几何留拓扑**（Beck 1931）、**地形图丢道路留高度**——**各自丢掉的正是对方保留的**，这就是 p.10「蜻蜓」那条推论（**失效不相关才有增益**）的实物版。


### 幻灯七 · Experiment II · Run it — Five senses, one object

> **Five senses, one object**
>
> Five volunteers. One covered object. Each volunteer gets **one channel only**: touch for ten seconds · listen while it is tapped and shaken · smell · ask three yes/no questions · **see** for two seconds.
>
> *Each reports to the room.* **Report only what your channel gave you.** *Then the room, together, writes one description on the board.*
>
> **中文**：**五种感官，一个物体**。五名志愿者，一个被盖住的物体。每人**只分到一条通道**：**触摸**十秒 · 在物体被**敲击和摇晃**时**听** · **闻** · **问三个是/否问题** · **看**两秒。*每人向全场报告。* **只报告你那条通道给了你的东西。** *然后全场一起，在白板上写出**一段**描述。*

- **实验一演的是「投影」，实验二演的是「重建」。** *CT 扫描仪从不给肿瘤拍照，它拍几百张有损投影，然后重建出没有任何单张曝光包含的东西。* **"Five senses, one object" 就是 "Many maps of one country" 的物体版**，而这次多了实验一没有的关键一步：**白板上那段合成的描述，就是融合（fusion is the reconstruction）。**
- **这是盲人摸象的反转。** 原寓言的落点是「**每个人都错了**」；今天的落点是「**每个人单独都不完整，但合起来能重建**」。**这个差别就是全景敞视监狱与断层扫描原理的差别**——组合**拒绝**「一只眼睛拥有全部视野」的宣称，而这个拒绝就是整个架构。
- **五条通道 ↔ 五条车道**（注意预算被刻意设计成不对称——**这本身就是一条教条**）：

| 通道 | 预算 | 拿得到 / 拿不到 | 对应 |
|---|---|---|---|
| **触摸 10 秒** | **最慷慨** | 形状、重量、质地、温度、材质；看不见颜色与文字 | **全维 dense 复评**——丰富、昂贵、慢 |
| **听（敲击+摇晃）** | 中等 | **内部结构**：空心？有散件？装了颗粒？**唯一能「看进去」的通道** | **结构/全局车道**（RAPTOR、community）——回答**不在任何表面上**的问题 |
| **闻** | 窄得可怜 | 多数时候近乎为零；**但一旦是咖啡、皮革、雪松、樟脑，直接给出答案** | **稀疏/罕见词车道**——大部分时候沉默，**罕见标识符一命中就是决定性的** |
| **问三个是/否** | **3 次，硬预算** | 不是感官，是**交互**；**质量完全取决于问题问得好不好** | **agentic turn / 多跳规划**——**3 次就是案卷深度预算** |
| **看 2 秒** | **带宽最高，时间最短** | 两秒足以拿到几乎一切 | **最高法院**：读得少、想得深、**单位时间最贵** |

  「问三个是/否」那条最值得盯——**它是唯一一条可以主动去补别人盲区的通道**（"它能吃吗？""上面有字吗？"）。这就是**路由器**与**问题侧**：**一半的架构站在 query 这一侧，而你只有三次机会，问坏了就浪费了。**

- **三条规则，三个机关**：
  1. **`one channel only`** —— 和实验一的 `you may not trade` 完全同构：**强制你变成一个单一索引**。你必然交出一份不完整的报告，**这不是失败，这是规格**。
  2. **`Report only what your channel gave you`** —— **最容易被违反的一条**。摸到冰冷金属圆柱的人**几乎一定会脱口而出「这是个保温杯」**；**那不是通道给你的，那是你的先验**。诚实的报告是「冷、金属、圆柱、约 15 厘米、光滑、靠一端有一圈凸起」。这一条同时踩中三处：**Week 08 实验 4 的参数泄漏**（只讲悉尼墨尔本的短文，半屋子答「首都是堪培拉」——**从证据回答，把先验清楚标注为先验**）；**今天的主模式**（报告是**派生物**，物体是**源**；抢先说「保温杯」等于**从派生物直接生成**，正是那份丢掉 `irrevocable` 的法律改写）；以及**摘要器纪律**（**摘要器是记者，不是法官**）。
  3. **`the room, together, writes ONE description`** —— **预测白板上会发生什么：看了两秒的那位会一家独大**，另外四人的报告沦为脚注，**闻的那位大概率被完全忽略**。**而这正是 RRF 存在的理由**——*k 阻尼头部，使得某一条车道的第一名不能一家独大*。各通道的「分数」**不可通约**（「冷」「空心的」「有雪松味」**不共享任何标度**），所以**不能加权求和，只能按名次融合**。**k=60 那个数字，就是为了防住白板上即将发生的这一幕。**
- **还有一个会被忽略的问题：白板上那段描述，还留得住出处吗？** 如果写成「一个中空的金属圆柱，带木质气味」，事后发现「中空」是错的，**你还能回溯到那是「听」那条通道报的吗？** 这是**出处回指针的第二项职责——失效键**。丢了归属，你手上就只有一段**无法失效的合成文本**：*a rumor mill with vector search*。
- **藏得最深的一条：白板的天花板 = 五条通道的并集。** 如果没有任何一条通道编码了某个属性（颜色、来历、归属），**全场讨论多久都变不出来**。白板那段描述的信息量被并集**死死封顶**；讨论、争辩、重排、润色**一个都不能增加信息，只能不丢信息**。**这是召回天花板换了个场景又演一遍**，也正好解释了参考级联的设计——**各车道发射深度要选得让「并集」很少漏掉一颗弹珠**：**铲子是并集，不是任何单独一条车道。**


### 幻灯八 · Experiment II · **Harvest** — Five confident shadows

> **Five confident shadows**
>
> Every report was **partial** and every report was **certain**. The toucher knew weight and texture; the listener knew hollowness; the two-second seer knew colour and shape — **and missed the weight entirely**.
>
> **The board's description was better than any single report.**
>
> 右栏：*Notice what did **not** happen: the seer was **not** the "best sensor" who made the others redundant. Each channel **lost different things** — and that is precisely why the fusion recovered more than any part.*
>
> **中文**：**五道自信的影子**。每一份报告都是**局部的**，而每一份报告都是**确信的**。摸的人知道重量和质地；听的人知道它是空心的；只看了两秒的人知道颜色和形状——**而完全错过了重量**。**白板上那段描述，比任何单独一份报告都好。**
> 右栏：*注意「没有发生」的那件事：看的人**并不是**那个让其余四人变得多余的「最佳传感器」。**每条通道丢失的东西各不相同**——而这恰恰是为什么融合恢复出的，比任何一个部分都多。*

- **标题是柏拉图洞穴的反转。** *shadows* = 墙上的影子 = **有损投影**；洞穴寓言的落点是「影子是要逃离的假象」，而这里的落点是——**你逃不出洞穴**（Korzybski：地图不是疆域，**每一种表征都必然有损**），**所以你改成从五个角度各取一道影子，然后重建**。**这和上一页把「盲人摸象」从「每个人都错了」反转成「合起来能重建」是同一个手法**：讲义把两个「单一视角必然失败」的经典寓言，**双双改写成断层扫描原理**。
- **`partial` 与 `certain` 并置，是这一页真正的刀。** 局部性和确信度**同时存在，且互不知情**——**报告里没有任何一个字告诉你它漏了什么**。这正好和我抽到的那张航海图形成对照：**海图在自己脸上印了 `NO ROADS` 和 `(land: not charted)`，而五位志愿者没有。** 生产环境里的索引属于后者：**被问到光圈之外的问题时，它不会说「未测绘」，它会安静地返回一个余弦 0.71 的最佳匹配。** 同时这也是 **Week 08 的过度自信/ECE 换了个场景**——**一份 20% 覆盖率、100% 置信度的报告**，其错误不在内容，在**校准**：**分数没有编码覆盖**。这就是讲义那句「**出口处的校准不是可选项**」的来由。
- **右栏那句 `Each channel lost different things` 才是全场最该抄下来的一句。** 断层扫描原理的**精确表述不是「每条车道都不如整体」，而是「各条车道的损失是去相关的（decorrelated）」**。**如果五条通道丢的是同一批东西，融合什么也恢复不出来。** 融合之所以有效，是因为**损失彼此正交**。这就是讲义那条边注的一般化——*sparse 赢在罕见词、dense 赢在改写与意图；**这正是为什么按名次融合的混合检索胜过任何单独一条***：**sparse 丢的是同义，dense 丢的是罕见标识符，两者丢的不是同一批东西。**
  - **可以直接拿去当工程规则的推论**：**新增一个索引时，别问「它能看见什么」，问「它丢的东西和现有索引丢的是否不同」。** 一个**和现有索引丢失同一批东西**的新索引，**再先进也加不了信息**——这就是 **Kitchen Sink** 的判据，也是**消融门**真正在测的东西。
- **`the seer was not the "best sensor"` —— 这一页明确预防了一个几乎人人都会有的直觉**（我在看 p.7 时的第一反应也正是「看两秒那位会一家独大」）。**而两件事必须分开看，它们的张力才是重点**：
  - **信息上**：看的人**不是超集**——他拿到了颜色和形状，**却完全错过了重量**。**没有任何一条通道包含另一条。**
  - **社交上**：他的报告**听起来最像答案**，所以在白板前**最容易主导讨论**。
  - **也就是说：主观上的支配 ≠ 信息上的支配。** 而这**恰恰就是 RRF 为什么要在名次上融合、并且用 k 阻尼头部**——*k damps the head so that one lane's first place cannot dominate*。**k=60 防的就是「那个听起来最权威的车道，把它并不拥有的信息也一并代表了」。**
- **`The board's description was better than any single report` —— CT 重建的主张在房间里被当场证实。** 但要接着上一页那条限制一起读：**融合的输出严格优于任何单一投影，同时又被五条通道的并集死死封顶。** 两句合起来才是完整的教条——**融合能恢复出没有任何单张曝光包含的东西，但恢复不出任何一张曝光都没有编码过的东西。**


### 幻灯九 · Experiment II · **The Seed** — The tomographic principle（正式命名）

> **The tomographic principle**
>
> A CT scanner never photographs the tumour. Hundreds of lossy shadows, each blind alone, **reconstruct** what no single exposure contains.
>
> **You just were the scanner. Five projections; the whiteboard was the reconstruction.**
>
> 右栏：*This afternoon: each index is a projection of the corpus at its own angle, and **fusion is the reconstruction**. The kin: the compound eye, the cubist portrait, Rashomon. What it is not: the panopticon — one eye claiming total sight.*
>
> **中文**：**断层扫描原理**。CT 扫描仪从不给肿瘤拍照。数百道有损的影子，**每一道单独看都是瞎的**，却**重建**出没有任何单张曝光包含的东西。**你们刚才就是那台扫描仪。五道投影；白板就是那次重建。**
> 右栏：*今天下午：每一个索引都是语料在它自己那个角度上的一次投影，而**融合就是重建**。同族：复眼、立体派肖像、罗生门。它不是什么：全景敞视监狱——一只眼睛宣称拥有全部视野。*

- **这一页是 Prelude 的第一个正式命名（The Seed）**，而且它**几乎逐字就是下午讲义 "The Tomographic Principle" 那一段**。也就是说，标题页那句 ***"Everything we build this afternoon, you will have already done by lunch"* 在这里第一次兑现**：**上午用五个人做的事，下午会以同样的措辞再讲一遍**——只不过那时它叫「架构」。
- **CT 的机制才是这个类比的钥匙（不是修辞）**：
  - 拍**一张** X 光，得到的是一张**压扁的影子**——所有器官叠在一起，肿瘤可能被骨头挡住，也分不出前后。
  - **CT 不是去拍一张更好的 X 光。** 它绕着病人转一圈，从**几百个角度**各拍一张**同样糟糕**的影子。
  - 然后用算法把这几百张影子**解出来**，重建成一张横截面。
  - **关键：那张横截面从来没有被拍到过。** 它是**算出来的**，**不存在于任何一张原始影子里**。
  - **翻译成检索**：没有任何一个索引「看见」了正确答案的全部理由；**正确答案是在融合那一步被算出来的**。
- **三个「同族」各自代表这条原则在一个不同领域里被独立发现**——这是这一页真正的野心，它在说：**这不是一个检索技巧，是一条更普遍的认识论原则**：
  - **复眼（compound eye）· 生物学**：苍蝇几千只小眼，每只都糊、视野都窄，**合起来对运动极其敏感**。**演化独立发现了这个方案。**
  - **立体派肖像（cubist portrait）· 艺术**：毕加索把同一张脸的正面与侧面**同时**画在一个平面上。单看「画错了」，**但它传达了任何单一视角都传达不了的东西**——讲义原话是 *one man, many simultaneous angles*。**人类主动放弃了单一视角。**
  - **罗生门（Rashomon）· 认识论/叙事**：同一桩事件，四个当事人四种互相矛盾的叙述，**电影不给你「正确版本」**。**真相（如果有）只存在于交叉处。** 这一个最狠——它把原则从「感知」推到了「事实本身」。
- **反面：全景敞视监狱（panopticon）。** 边沁设计的环形监狱，中心一座塔，**一个看守能看见所有牢房**——**一只眼睛宣称拥有全部视野**。**对比是精确的**：全景敞视 = **一个视角声称自己完备**；断层扫描 = **承认每个视角都不完备，靠数量与角度差异去重建**。而讲义把这句话收成全天最凝练的一击：
  > **A single index makes that claim; the portfolio refuses it, and the refusal is the whole architecture in one gesture.**
  > （**单一索引在做那个宣称；组合拒绝它——而这个拒绝，就是整个架构的一个手势。**）
- **我的一条补注（差异，值得课上问）**：**CT 的重建是有数学保证的**——Radon 变换与滤波反投影，角度够多就能保证还原。**检索的「重建」没有这种保证**：RRF 只是一个粗糙有效的启发式（*三个作者，一页纸*），我们**没有一条定理说「车道够多就能重建出正确答案」**。所以这个类比在**动机**上极准，在**保证**上是**借来的**——这也正是为什么讲义反复要求**用封存标尺 + 配对 bootstrap 去实测**，而不是相信架构本身。


### 幻灯十 · Experiment II · **A Quiet Corollary** — The dragonfly's eye（融合生效的**前提条件**）

> **The dragonfly's eye**
>
> Thirty thousand ommatidia, each nearly blind — and the dragonfly out-detects any human at the one thing that matters to it: **motion**. **Ninety-five percent of its hunts succeed.**
>
> Why does the fusion beat the parts? Because the facets **fail independently** — each blind spot is covered by a neighbour that is not blind there.
>
> 右栏：*Hold this for the afternoon: many projections beat one **only when their failures are uncorrelated**. **Five listeners would not have improved on one. Five different senses did.** That is the wisdom of crowds — and its fine print.*
>
> **中文**：**蜻蜓的眼睛**。三万个小眼（ommatidia），**每一个都近乎失明**——而蜻蜓在对它唯一要紧的那件事上胜过任何人类：**运动**。**它的捕猎成功率是百分之九十五。** 为什么融合胜过部分？**因为这些小面是独立失效的**——每一个盲点，都被一个**在那个位置不瞎的邻居**覆盖掉了。
> 右栏：*把这条留到下午：多投影胜过单投影，**只有当它们的失效互不相关时**。**五个「听」不会比一个「听」更好。五种不同的感官会。** 这就是群体智慧——**以及它的细则**。*

- **标题栏写的是 "A QUIET COROLLARY"（一条安静的推论），这个定位很关键。** 上一页（The Seed）是**响亮的原则**：断层扫描——要多投影。**这一页是它的使用条件**：**多投影什么时候才有用。** 没有这一页，上一页会被直接误读成「索引越多越好」——**而那正是 Kitchen Sink 的定义**。**它安静，但它是护栏。**
- **数字值得记住**：三万个小眼，**每一个都近乎瞎**（分辨率极低）；而蜻蜓的**捕猎成功率约 95%**——作为对比，狮子约 25%，大白鲨约 50%。**蜻蜓是地球上最成功的捕食者之一，而它的每一个传感器都极差。** 这是一个非常强的**存在性证明**：**极差的传感器 + 正确的组合方式 = 世界级性能。**
- **`fail independently` 是全页的技术核心。** 每个小眼都有盲点，**但盲点的位置各不相同**，所以**这一个的盲点落在另一个的清晰区里**。反过来：**如果三万个小眼在同一个方向上全都瞎**（比如被同一片薄膜挡住），**三万个和一个没有任何区别**。
- **右栏那句可以直接当工程判据**：***many projections beat one only when their failures are uncorrelated***。
  - **五个「听」= 高度相关的失效 = 没有增益**
  - **五种不同感官 = 不相关的失效 = 有增益**
- **「群体智慧的细则（fine print）」**：Galton 1906 年在集市上让 787 人猜一头牛的重量，**中位数 1207 磅，真值 1198 磅**——群体比任何单个专家都准。**但细则是：群体智慧要求判断彼此独立。** 一旦人们开始互相看答案（信息级联、羊群效应），**误差变成相关的，平均就不再消除它，群体智慧立刻崩溃。** 讲义用 *fine print*（合同里那种签的时候不看、出事才发现的小字条款）这个词，是在说：**人人都爱引「群体智慧」，没人读细则。**
- **跨周连接（这条最深）**：这就是 **Week 08 实验 1「偏差 vs 方差」的同一条数学，第二次出现**——
  - **不相关的误差 = 方差** → **聚合（平均/融合）可以消掉它**
  - **相关的误差 = 偏差** → **取多少次平均都不消失，只能测出来减掉**（*subtract, don't fire*）
  - **融合就是「取平均」这个动作。所以融合只能消掉方差，消不掉共同偏差。** 五个「听」之间的共同盲区，是**偏差**，融合无能为力。
- **落到检索上的操作判据（以及一条现实警告）**：
  - **加一个索引之前问的不是「它多先进」，而是「它的失效模式和现有索引是否相关」。**
  - **稀疏 vs 稠密：不相关**（一个丢同义，一个丢罕见标识符）→ **有增益**。这正是讲义那条边注——*hybrid retrieval, fused in ranks, beats either alone*，**断层扫描原理最简单的双投影形态**。
  - **⚠️ 两个不同厂商的 dense 模型：往往高度相关**——**相似的训练语料、相似的目标函数、甚至相似的基座**，**丢的是同一批东西**。「再加一个 embedding 模型」经常是**相关失效**，收益远小于预期。
  - **结论：portfolio 要按「类型」多样化（词面 / 语义 / 结构 / 图像 / 派生物），而不是按「品牌」多样化。**
- （旁注：这一页正好印证了课前我用「假设五个人都用手摸」做的那个推演——幻灯用 *five listeners* 说了同一件事。）


### 幻灯十一 · Experiment III · **RUN IT** — Five catalogues of one document

> **EXPERIMENT III · RUN IT**
> # **Five catalogues of one document**
>
> **Every table gets the same one-page document.**
> **Table 1** indexes it by **author and title**. **Table 2** by **subject headings**. **Table 3** by **every number in it**. **Table 4** by **every question it answers**. **Table 5** by **one sentence — what it is about**.
>
> Now **five queries, one at a time**. For each: **which table can answer it from its index alone — without re-reading the document?**
>
> **中文**：**实验三 · 动手做**。**同一份文档的五个目录**。**每一桌拿到同一份一页纸的文档。** **第 1 桌**按**作者与标题**建索引。**第 2 桌**按**主题词**。**第 3 桌**按**文档里的每一个数字**。**第 4 桌**按**它能回答的每一个问题**。**第 5 桌**按**一句话——它是关于什么的**。现在**五个查询，一次一个**。每一个都问：**哪一桌能仅凭自己的索引回答它——不许回头再读那份文档？**

- **⭐ 实验设计比我课前的推测更精确**：不是「把材料分到不同抽屉」，而是——**同一份文档，五桌各自建一个不同类型的索引**。**变量只有一个：索引的类型。**
- **⭐ 而那条约束才是把它变成检索实验的关键**：***不许回头再读那份文档。*** 只能用索引答。**这正是生产系统的真实处境**——查询时你面对的是索引，不是语料。
- **五种索引逐条对应今天的派生物清单**：

| 桌 | 索引方式 | 对应的真实表征 |
|---|---|---|
| **1** | 作者与标题 | **结构化元数据 / 前置过滤字段** |
| **2** | 主题词 | **UDC 式分类 / summary 索引** |
| **3** | **文档里的每一个数字** | **factoid（原子事实）** |
| **4** | **它能回答的每一个问题** | **⭐ QA pair —— 手工版** |
| **5** | 一句话：它是关于什么的 | **document 级 summary** |

  **第 4 桌尤其值得注意：那就是 QA pair 这件派生物，被一群人用纸手工造了一遍。**

### 幻灯十二 · Experiment III · **THE FIVE QUERIES** — Point, contextual, thematic, global, verbatim

> **EXPERIMENT III · THE FIVE QUERIES**
> # **Point, contextual, thematic, global, verbatim**
>
> 1. **Who wrote it?**
> 2. **What figure does it give for X?**
> 3. **What is it about?**
> 4. **Does it answer whether Y is true?**
> 5. **Quote its exact sentence on Z.**
>
> **Every query delighted one table and embarrassed four. No table answered all five.** And **query five — the verbatim one — embarrassed everyone but the table that had kept the words themselves.**
>
> **中文**：**实验三 · 五个查询**。**点、语境、主题、全局、逐字**。1. **是谁写的？** 2. **它给出的 X 的数值是多少？** 3. **它是关于什么的？** 4. **它有没有回答 Y 是否为真？** 5. **原文引用它关于 Z 的那句话。** **每一个查询都让某一桌欣喜、让另外四桌难堪。没有任何一桌能回答全部五个。** 而**第五个查询——逐字的那个——让所有人都难堪，除了那张保留了词本身的桌子。**

- **⭐⭐ 重要发现：这里是五种高度，不是四种。** 副标题写得清清楚楚——**point、contextual、thematic、global、以及 `verbatim`（逐字）**。**而正课 p.12 那页「四种查询高度」把第五种省掉了。**
  - **`verbatim`（逐字）是唯一一种「只有保留了词本身的索引才答得了」的查询**——原文引用、精确条款、法条编号、错误码。
  - **⭐ 这就是稀疏车道（BM25 / SPLADE）不可被替代的那条独家理由**：**不管 dense 做得多好，它保留的是「意思」，而逐字查询要的正是被它丢掉的那样东西。**
  - **建议把这一条补进自己的高度清单**——正课只讲四种，但**第五种在实践中最常见于合规、法务、故障排查场景**。
- **`Every query delighted one table and embarrassed four. No table answered all five.`** —— **组合的存在性证明**：不是「多个更好」，而是**任何单一索引在结构上都无法覆盖全部高度**。

### 幻灯十三 · Experiment III · **THE SEED** — The portfolio, and the altitude of a question

> **EXPERIMENT III · THE SEED**
> # **The portfolio, and the altitude of a question**
>
> Questions arrive at **different altitudes** — **a name, a fact, a theme, a truth-check, a quotation** — and **each altitude wants a different projection**. **Otlet's clerks kept five repertories for exactly this reason.**
>
> *This afternoon: the **portfolio of representations** — sparse, dense, factoids, QA pairs, summaries — and **the router that sends each question to its own height**.*
> ***You just were the Mundaneum: five drawers, one corpus, and no ranking.***
>
> **中文**：**实验三 · 种子**。**组合，以及一个问题的高度**。问题以**不同的高度**到达——**一个名字、一个事实、一个主题、一次真伪核对、一句引文**——**而每一种高度想要一种不同的投影**。**Otlet 的馆员维持五套档案，正是出于这个原因。**
> *今天下午：**表征的组合**——稀疏、dense、factoid、QA pair、summary——以及**那个把每个问题送到它自己高度的路由器**。*
> ***你们刚才就是 Mundaneum：五个抽屉，一份语料，而且没有排序。***

- **⭐⭐ 那句我一直在等的转折，原来在上午就已经落地了**：***You just were the Mundaneum: five drawers, one corpus, and **no ranking**.***
  - 我在正课 p.5–p.7 反复预测「他有组合、缺法庭」这句会出现——**它其实早在 Prelude 实验三的种子页就被交付了**，而且是以**第二人称**交付的：**不是「Otlet 缺法庭」，是「你们刚才自己就是那个缺法庭的系统」。**
  - 所以正课 p.7 那一页才可以直接把论点合起来说——**上午你已经亲身当过「有组合、没排序」的那半边。**
- **五种高度在这里被再次点名**：**名字 / 事实 / 主题 / 真伪核对 / 引文**——**再次是五种，含 verbatim。**
- **`Otlet's clerks kept five repertories for exactly this reason`** —— 把实验三直接钉到 Mundaneum 上：**五桌 = 五套档案**。正课 p.5「按主题、按作者、按分面、按事实本身」就是它的历史版本。


### 幻灯十四 · Experiment IV · **Run it（1 of 2）** — Twenty sheets, scattered（**铲子**）

> **Twenty sheets, scattered**
>
> Around the room are **twenty sheets of paper** — under chairs, on windowsills, taped beneath tables. **Twelve carry pieces of one argument. Eight are decoys: beautiful, plausible, and beside the point.**
>
> ***Ninety seconds. Teams of four. Collect as many sheets as you can. Do not read them yet. Go.***
>
> **中文**：**二十张纸，散落各处**。房间四处散着**二十张纸**——椅子底下、窗台上、用胶带贴在桌子背面。**其中十二张各自携带同一个论证的一块碎片。八张是诱饵：漂亮、看起来很像那么回事、但不在点上。**
> ***九十秒。四人一组。尽可能多地把纸收集起来。先别读。开始。***

- **这一页整场就是「铲子（the scoop）」，而且几乎每一个细节都对着一条教条**：

| 幻灯上的细节 | 对应的教条 |
|---|---|
| **九十秒** | **硬延迟预算**——*延迟不是性能指标，是一条决定「哪些法官有资格入席」的结构性约束* |
| **"Collect as many sheets as you can"** | **召回是神圣的**：铲得宽、铲得慷慨 |
| **"Do not read them yet."** | **不要在铲的阶段花精度**——*every stage narrows before the next spends*。**读 = 昂贵的法官**；九十秒内边捡边读，两头落空 |
| **二十张 / 十二真 / 八假** | **40% 的噪声率**——即使你全捡到，**精度上限也只有 60%**，必须靠筛子 |
| **椅子底下、窗台上、胶带贴在桌子背面** | **检索难度不均匀**：有些文档显眼（窗台），有些要蹲下去摸（桌底）。**而藏得深的那几张未必不重要**——时间压力会让你只捡容易的 |
| **四人一组** | **并行发射 + 并集**：四个人分头找，战利品合并——**铲子是并集，不是任何单独一条车道** |
| **"Twelve carry pieces of ONE argument"** | **答案分散，不在任何单张纸里**——这是**全局/多跳查询的形状**，也是断层扫描在文本上的版本 |

- **最重要的一行是 "Do not read them yet."** 它把**召回阶段**和**精度阶段**用一条禁令**物理隔开**。九十秒**不够你边读边挑**——一旦你蹲在桌底读第一张，其余十九张就都没了。**这就是为什么级联要把便宜的法官放在前面：不是为了省钱，是为了让昂贵的法官还有东西可审。**
- **同时这是召回天花板的字面演出**：**九十秒结束后没被你捡到的纸，第二部分你再也拿不到了。** 手上有什么，就只能用什么拼。*Only the scoop decides what is caught.*
- **"beautiful, plausible, and beside the point" 是「高余弦、低相关」的文字定义。** 这八张 decoy 之所以危险，不是因为它们劣质，**恰恰是因为它们优质**——它们和真材料**在表面特征上无法区分**。这直接对上**测度集中**那条：*top few 候选之间的绝对差异很小，所以 reranker 的辨别力比 retriever 更要紧，出口校准不是可选项*。**光靠阈值筛不掉它们。**
- **⚠️ 术语张力（值得留意）**：`decoy` 这个词在今天要**担两个相反的角色**：
  - **这里的 decoy = 坏东西**：语料里天然存在的、看起来极像答案的干扰项，**筛子必须滤掉它们**。
  - **下午讲义里的 decoy = 好东西**：QA pair 被明确称作 ***the decoy the retriever should find***——**我们故意制造**的、query 形状的替身，**目的就是让它被检索到，然后跳回源**。
  - **两者其实是同一机制的两面**：一个是**未受控的诱饵**（语料自带），一个是**受控的诱饵**（我们制造）。而下午那条教条 ***the decoy's job ends at retrieval*** 说的是后者——**受控诱饵负责被找到，但绝不能被送上重排的证人席**。**留意这个词第二次出现时的价号翻转。**
- **对 part 2（p.15）的预测**：现在开始**读**——丢掉八张 decoy，把十二张碎片拼成那个论证。这就是**筛子 + 重排 + 生成**。**落点大概率是两个之一（或都有）**：①「**你没捡到的那几张，现在拿不回来了**」（召回天花板）；②「**捡得最多的队伍未必拼得最好**」（铲得宽必然带进沙，**精度要在后一阶段单独付账**）。
- **待现场确认**：若多组同时抢这二十张纸，**没有任何一组能拿到全部十二张**——那么每组手里都是**不同的局部子集**，part 2 是否会让各组交换/合并？（若会，那就是**融合**再演一次。）


### 幻灯十五 · Experiment IV · **Run it（2 of 2）** — The synthesizing question（**筛子 + 生成**）

> **The synthesizing question**
>
> Back at your tables. **Now read.** The question every team must answer **on one page**:
>
> ***Show that softmax, the Boltzmann–Gibbs distribution, cross-entropy loss, and logistic regression are one thing wearing four costumes — and name the thing.***
>
> **Fifteen minutes. Use only the sheets on your table.**
>
> **中文**：**综合之问**。回到你们桌边。**现在开始读。** 每一组必须在**一页纸**上回答的问题：***证明 softmax、Boltzmann–Gibbs 分布、交叉熵损失、逻辑回归是同一样东西穿着四件戏服——并说出这样东西的名字。*** **十五分钟。只准用你们桌上那些纸。**

- **这个问题本身就是今天的论点，而且把箭头掉了个头。**
  - 实验一（一个国家 / 四张地图）、实验二（一个物体 / 五种感官）：**一 → 多**，你拿到许多投影，任务是**重建**那个「一」。
  - 实验四：**多 → 一**，你拿到四件戏服（softmax / Boltzmann–Gibbs / 交叉熵 / 逻辑回归），任务是**认出**那个「一」。
  - **"one thing wearing four costumes" 就是 "one corpus, many catalogues" 的另一种说法。**
- **这是一个教科书级的「全局查询（global query）」**：讲义的定义是——*a global query wants what lives in **the structure of the whole corpus and in no passage at all***。**答案（那样东西的名字）不写在任何一张纸上**，它活在十二张碎片**彼此的关系**里。**这正是 community summary / GraphRAG 存在的理由**，也是为什么这类问题**不能靠单点检索回答**。
- **三条约束各自是一条教条**：

| 约束 | 教条 |
|---|---|
| **"Now read."** | 上一页禁止的动作现在解禁——**精度阶段开始**。*Precision spent after recall is secured.* |
| **"Use only the sheets on your table."** | **RAG 的契约本身**：**只从检索到的证据生成**，不许用手机、不许用记忆。同时**召回天花板在此刻咬人**——九十秒没捡到的，现在拿不回来 |
| **"on one page" / "Fifteen minutes"** | **输出预算 + 生成预算**：必须**压缩**，不能堆料 |

- **两笔账在两个不同时刻分别付清**：**贪心捡得多的队伍，现在要在十五分钟里趟过八张 decoy**；**捡得谨慎的队伍，可能缺关键碎片**。**这就是召回/精度的取舍——而且它演示了一件容易被忽略的事：decoy 不只是往答案里掺噪声，它还在吃你的生成预算。** 对应讲义那句：*a system that retrieves reflexively pays for evidence it does not use*。
- **时间比例值得记**：**九十秒检索 : 十五分钟生成 ≈ 1 : 10**。**检索便宜而快，生成慢而贵**——这正是为什么**筛子必须在生成之前把候选收窄**，也是参考级联里「每一级都在下一级开销之前先收窄」的直觉来源。
- **⭐ 最狠的一点：这四件戏服本身就是「语域错配」的活体演示。**
  - **softmax** —— 机器学习工程的词汇
  - **Boltzmann–Gibbs 分布** —— 统计物理的词汇
  - **交叉熵损失** —— 信息论的词汇
  - **逻辑回归** —— 统计学的词汇
  - **四个学科、四套术语、一个对象。** 一个写着 "softmax" 的 query **在词面上永远匹配不到**一页写着 "Boltzmann distribution" 的文档——**倒排表永不相遇**，正是讲义里 "cardiac" 与 "heart" 那个例子的高阶版。
  - **能跨过这道鸿沟的只有两条路**：**捕捉意义的表征**（dense / SPLADE 的学习式扩展），或者**显式制造的派生物**（contextualized rewrite、factoid、QA pair）。**这道综合之问，等于把「为什么需要多表征组合」这件事，用一个真实的学术问题演了一遍。**
- **「那样东西」的名字（参考答案）**：**指数族 / Gibbs 测度，而生成它的原理是最大熵（Jaynes 1957）**；把四者缝在一起的那个数学对象是 **log-partition function（log-sum-exp）及其 Legendre 对偶（负熵）**。链条：

| 戏服 | 恒等式 |
|---|---|
| **Boltzmann–Gibbs** | `p(x) = exp(−E(x)/kT) / Z`，`Z = Σ exp(−E/kT)` |
| **Softmax** | `p_i = exp(z_i/T) / Σ_j exp(z_j/T)` —— 令 `E_i = −z_i`、`k=1`，**与上式逐字相同**。**logits 就是负能量，softmax 的分母就是配分函数 Z** |
| **交叉熵** | 把 softmax 代进 `−Σ q_i log p_i`，`q` 为 one-hot ⇒ `−log p_y` = **该 Gibbs 分布的负对数似然**。最小化交叉熵 = 最小化 `KL(q‖p)` = 最大似然；而物理里 `−log Z` 是**自由能**，所以这个目标就是**变分自由能** |
| **逻辑回归** | **二分类的 softmax**（对 `{z, 0}` 做 softmax 即得 `σ(z)`），损失即二元交叉熵；而它的经典推导正是**最大熵模型**——在匹配特征期望的约束下最大化熵，解出来就是 logistic / multinomial logit |

  **缝合点一句话**：**log-sum-exp 的梯度就是 softmax，它的凸共轭是单纯形上的负熵，由它生成的 Bregman 散度就是 KL**——**四件戏服都是同一个凸函数的不同侧面。**

- **（当时的预测，已被 p.16–p.18 证实）**：实验四的 Harvest 落点正是「**漏掉的救不回来**」与「**decoy 吃掉的是桌边的预算**」。


### 幻灯十六 · Experiment IV · **Harvest（1 of 2）** — Who missed a sheet?

> **EXPERIMENT IV · HARVEST · 1 OF 2**
> # **Who missed a sheet?**
>
> Some team came back **without the log-partition sheet**, or **without the sufficient-statistic sheet** — and **however hard they thought at the table, the argument had a hole exactly that shape**.
>
> **No amount of cleverness at the table recovered what the scoop had missed.**
>
> ***That is the recall ceiling.** What the first stage does not catch, **no later stage can restore**. **The bucket decides what is in the sieve.** **Recall first — get it right — then spend on precision.***
>
> **中文**：**实验四 · 收获（1/2）**。**谁漏掉了一张纸？** 有的组回来时**少了那张「配分函数（log-partition）」的纸**，或者**少了那张「充分统计量（sufficient statistic）」的纸**——**而无论他们在桌边想得多苦，那个论证上就有一个恰好是那个形状的洞。** **桌边的任何聪明才智，都救不回铲子漏掉的东西。** ***那就是召回天花板。** 第一阶段没捞到的，**任何后续阶段都无法恢复**。**桶决定了筛子里有什么。** **先把召回做对——然后再花钱买精度。***

- **⭐ 被点名的两张纸，反过来确认了那道综合之问的答案**：**「log-partition（配分函数）」和「sufficient statistic（充分统计量）」都是指数族的核心构件**。
  - **配分函数 Z** 正是 softmax 的分母、自由能的来源、Legendre 对偶的生成函数——**我在 p.15 记录里给出的「缝合点 = log-sum-exp 及其凸共轭」，在这里被实验材料本身证实了。**
  - **充分统计量**是指数族定义的另一半（$p(x)\propto\exp(\eta^\top T(x))$ 里的 $T(x)$）——**这一条我当时漏了，补上。**
- **⭐ 「洞的形状」这个说法很准**：***the argument had a hole exactly that shape*** —— **缺失不是「答案变差」，而是论证结构里出现了一个特定形状的空缺**，而且**你在桌边越想越补不上，因为缺的是一块事实，不是一次推理。**
- **`The bucket decides what is in the sieve.`（桶决定了筛子里有什么。）** —— 比正课 p.6 的表述更短。**桶 = 铲子 = 第一阶段。**
- **与 Harvest 2/2（p.17）合起来才是完整的一对**：

| | 教条 | 代价发生在 |
|---|---|---|
| **Harvest 1/2（本页）** | **漏掉的救不回来** → 铲要宽 | **铲阶段，永久** |
| **Harvest 2/2（p.17）** | **诱饵的代价在桌边** → 筛要狠 | **桌边，可延后** |


### 幻灯十七 · Experiment IV · **Harvest（2 of 2）** — Who wasted time on a decoy?（**级联的正当性证明**）

> **Who wasted time on a decoy?**
>
> Some team spent **five of their fifteen minutes** on the Gaussian written in full, or the lovely lemma from measure theory — **decoys that *sounded* right and cost table time.**
>
> But notice: **the decoys cost you at the table, not at the scoop. Grabbing them cost nothing. Reading them cost minutes.**
>
> 右栏：*That is why the pipeline is a **cascade**: scoop wide and cheap and tolerate sand; then sieve at leisure with an expensive judge. **Anyone who tried to be precise while scooping came back with fewer sheets.***
>
> **中文**：**谁在诱饵上浪费了时间？** 有的组把十五分钟里的**五分钟**花在了那张完整写出高斯分布的纸上，或者那条measure theory 里的漂亮引理——**这些诱饵「听起来」是对的，而它们消耗的是桌上的时间。** 但请注意：**诱饵的代价发生在桌边，不在铲的阶段。捡起它们不花什么；读它们要花掉几分钟。**
> 右栏：*这就是为什么这条流水线是一个**级联**：**铲得宽、铲得便宜、容忍沙子**；然后**从容地**用一位昂贵的法官去筛。**任何试图「一边铲一边求准」的人，带回来的纸都更少。***

- **这一页是整个级联架构的正当性证明，而且它是靠一条「成本不对称」推出来的**：

| 动作 | 成本 |
|---|---|
| **捡起一张 decoy** | **≈ 0**（弯个腰） |
| **读一张 decoy** | **分钟级** |

  **也就是说：假阳性的代价不是在检索时付的，是在判断时付的。** 推论直接得出——**铲的阶段要慷慨（假阳性在那里几乎免费），筛的阶段要严格（假阳性在那里很贵）**。这就是讲义那句 *every stage narrows before the next spends* 的成本学根据。

- **右栏那句反事实把论证闭合了**：***Anyone who tried to be precise while scooping came back with fewer sheets.***
  - 提前求准，**换来的是召回的损失**——而**召回是永久性的**（沙坑里漏掉的弹珠找不回来）。
  - 所以「在铲的阶段做筛选」是**双重错误**：**用一个不可逆的损失（漏掉弹珠），去省一件本来就便宜、而且可以延后做的事（除沙）。**

- **被点名的两张 decoy 选得极准**：**「完整写出的高斯分布」**和**「measure theory 里那条漂亮的引理」**。
  - 它们**不是错的，也不是低质量的**——**高斯分布本身就是指数族的一员**，所以它和今天那道综合之问**真的沾边**；测度论也确实是基础。
  - **正因如此它们才贵**：一个组可以花五分钟**说服自己它属于答案的一部分**。
  - **可以直接记下来的一条规律：最贵的 decoy 不是明显错的那种（三秒就丢了），而是「像到值得认真考虑」的那种——代价与似真度成正比。擦边球比远距离脱靶贵得多。**

- **在真实系统里，「桌上的时间」具体是三笔账**（这一页把它们合并成了「读」）：
  1. **cross-encoder 的算力**——每个候选一次前向
  2. **上下文窗口的 token**
  3. **生成器的注意力**——即 context rot；讲义那句 *a system that retrieves reflexively pays for evidence it does not use*

- **⚠️ 我的两条补注（值得课上问）**：
  1. **「捡起来不花钱」在房间尺度上成立，在生产尺度上只是「相对成立」**：发射深度要付索引存储、内存、以及深发射本身的延迟。讲义自己给的做法是**稀疏车道发得略深一点，因为它最便宜**——**也就是说，铲的深度是一个被调过的参数，不是无穷。** 更准确的说法是：**捡相对于读足够便宜，所以最优解是「深而有限」的发射深度。**
  2. **并不是所有过滤都该往后放。** 对照讲义两处：**ACL 必须前置过滤（pre-filter），绝不后置**；**查询变换级联也是「便宜的确定性修复最先做」**。**规律是：按成本排序，同成本时按确定性排序**——**便宜且确定性的过滤（拼写、ACL）往前放；昂贵且需要判断的过滤（相关性）往后放**。之所以 ACL 例外，是因为**它的假阳性是灾难性的（泄漏），而相关性的假阳性只是浪费**。

- （这一页确认了我在 p.15 对 Harvest 落点的预测之一——**decoy 吃掉的是生成预算**——并给出了比预测更精确的形式：**代价发生在桌边，不在铲的阶段。**）


### 幻灯十八 · Experiment IV · **The Seed** — Scoop wide, sieve hard（**派生物投资的诊断法**）

> **Scoop wide, sieve hard**
>
> Which sheets did **every** team need? **Those are your critical-path artifacts.**
> Which sheets did every team **find easily**? **Those are your cheap lanes.**
> Which were **hidden under chairs**? **Those are the ones a good portfolio manufactures on purpose.**
>
> 右栏：*This afternoon: the **judicial ladder** — cheap judges narrow the docket so the expensive judge can afford to be careful; **the archaeology of top-K** that asks which artifacts actually won; and **the exponential family, which you have now assembled by hand**.*
>
> **中文**：**铲得宽，筛得狠**。哪些纸是**每一组都需要**的？**那些是你的关键路径派生物。** 哪些纸是**每一组都很容易找到**的？**那些是你的便宜车道。** 哪些是**藏在椅子底下**的？**那些正是一个好的组合会特意去制造的东西。**
> 右栏：*今天下午：**司法阶梯**——便宜的法官缩小案卷，好让昂贵的法官负担得起「仔细」；**top-K 的考古学**——去问到底是哪些派生物真的赢了；以及**指数族，你们刚刚已经用手把它拼出来了**。*

- **三个诊断问题构成一个隐含的 2×2，而全部投资只该落在其中一格**：

| | **容易找到** | **藏在椅子底下** |
|---|---|---|
| **每组都需要（关键路径）** | 现有**便宜车道**已经够了——**什么都不用建** | **⭐ 这里才是该制造派生物的地方**（factoid / QA pair / rewrite / summary） |
| **不是每组都需要** | 无所谓 | **别管它** |

- **这就是讲义那条 Artifact ROI 公式的手工版**：
  `ROI ≈（该粒度在查询分布中的权重）×（实测质量提升）−（构建成本 + 存储成本）`
  - **「每组都需要」= 查询分布权重高**
  - **「藏在椅子底下」= 质量提升高**（因为不制造它就会被漏掉）
  - **两个条件同时成立，才值得花钱制造。**
- **⭐ 而这一页真正的方法论在于：诊断是「观察」出来的，不是「猜」出来的。** 你不去凭直觉判断哪些纸关键——**你回头数：刚才那一轮里，哪些纸每组都用到了。** 这正是讲义的 **top-K 考古学**：*记录一周内每一条最终结果的家谱，然后数*；*让家谱——而绝不是热情——决定哪些镜头留下*。**房间刚跑完一轮真实流量（四个组、一个真实问题），这一页就是在这批流量上做考古。**
- **右栏三个预告，第三个是妙笔**：
  1. **司法阶梯**——便宜法官缩小案卷（Act III）
  2. **top-K 考古学**——数哪些派生物真的赢了（Act II 经济学）
  3. **「指数族，你们刚刚已经用手把它拼出来了」** —— **实验的「内容」而不只是「形式」，直接喂给下午。**
- **⭐ 为什么综合之问偏偏选了那四件戏服（这条值得单独记）**：**因为 InfoNCE 就是那四件戏服同时穿在身上**——

$$
\mathcal{L}_{\text{InfoNCE}} = -\log \frac{\exp\!\big(s(q,d^{+})/\tau\big)}{\sum_j \exp\!\big(s(q,d_j)/\tau\big)}
$$

  - 这是**一个以「相似度」为负能量、以 `τ` 为温度的 Gibbs 分布**（softmax），
  - 配上一个 **one-hot 目标的交叉熵**（= 该分布的负对数似然），
  - 而分母 `Σ exp(·)` **就是配分函数 Z**。
  - **于是 DCL 的全部内容，用上午拼出来的语言讲，就只有一句话：把正例从配分函数 Z 里拿出去。**
  - **上午用手拼出的那个对象，下午会直接变成损失函数的骨架。** 综合之问不是随便挑的题目。
- **标题 "Scoop wide, sieve hard" 几乎就是讲义全天的收束句**：*Scoop wide and sieve hard; manufacture what the examiner will ask; let cheap judges spend their pennies so the supreme court can afford its verdict; and let every index earn its place, or let it go.* —— **Prelude 的最后一个 Seed，直接命名了全天的最后一句话。**


### 幻灯十九 · **Harvest · Four Seeds** — What you did before lunch（整场 Prelude 的收束）

> **What you did before lunch**
>
> - **Many maps** — *a representation is a choice of what to ignore*
> - **Five senses** — *projections fuse into more than their parts, **when their blind spots differ***
> - **Five catalogues** — *one corpus, many drawers; each question has an **altitude***
> - **Scattered sheets** — *recall first; precision is spent afterward*
>
> 右栏：*Four seeds. This afternoon the main deck names them: **the tomographic principle, the portfolio, the recall ceiling, and the court**. You will recognize each one — **you were standing in it.***
>
> **中文**：**你在午饭前做过的事**。**许多地图**——*一个表征，是一次「选择忽略什么」的决定*。**五种感官**——*多个投影融合出的东西多于它们各部分之和，**前提是它们的盲区各不相同***。**五个目录**——*一份语料，许多抽屉；**每个问题都有它的高度***。**散落的纸**——*先召回；精度是事后才花的*。
> 右栏：*四颗种子。今天下午主讲义会给它们命名：**断层扫描原理、组合、召回天花板、法庭**。你会认出每一个——**因为你当时就站在它里面。***

- **⭐ 这一页点明了实验三的主题**（当时尚未截到，后已补齐）：**Experiment III = "Five catalogues"**（*一份语料，许多抽屉；每个问题都有它的高度*）。**幻灯十一 / 十二 / 十三已补齐（见上）**——动手形式是「同一份文档，五桌各建一种索引」，对应讲义的 **Mundaneum 与查询高度**。
- **四个实验 ↔ 四颗种子 ↔ 下午的四条教条**（**注意不是严格一一对应**，是互相咬合）：

| 实验 | 这一页给的一句话 | 下午的名字 |
|---|---|---|
| **I 许多地图** | **表征 = 选择忽略什么** | 仪器柜：**每种表征都是有损投影** |
| **II 五种感官** | **盲区不同，融合才有增益** | **断层扫描原理** |
| **III 五个目录** | **一份语料，许多抽屉；问题有高度** | **组合（portfolio）+ 四种高度** |
| **IV 散落的纸** | **先召回，精度事后花** | **召回天花板 + 法庭** |

- **⭐ 全页最锋利的一句是第一条：*a representation is a choice of what to ignore*。**
  - **它比讲义里 "every representation is a lossy projection" 更狠。** *Lossy*（有损）听起来像**意外、像遗憾**；*a choice of what to ignore*（一次选择忽略什么的决定）**把它变成了主动的设计行为**。
  - **地铁图不是「不小心」丢了几何，是故意丢的**——**只有丢掉几何，连通关系才画得清楚。** 我那张航海图不是「忘了」画陆地，是**明确宣布不画**（`NO ROADS`）。
  - **推论直接得出**：既然每个表征都**必须**选择忽略某些东西，那么**单一表征必然有一整类问题结构上答不了**——**这就是组合存在的理由**，而不是「多个总比一个好」这种模糊直觉。
- **四颗种子串起来是一条完整的推理链**：
  1. **表征 = 选择忽略什么**（I）
  2. **忽略的东西不同，融合才有增益**（II + 蜻蜓那条推论）
  3. **所以要一份语料、多个抽屉，并按问题的高度分**（III）
  4. **而检索的执行顺序必须先宽后准**（IV）
- **右栏最后一句 *"you were standing in it"*（你当时就站在它里面）是整套教学法的最后一击**，也**兑现了 p.1 那句承诺**——*Everything we build this afternoon, you will have already done by lunch*，而这一页的标题就叫 **"What you did before lunch"**。**下午听到「断层扫描原理」时，你不是在学一个新概念，而是在给一个你上午身体所在的位置起名字。**


### 幻灯二十（终页）· **Now — the library**

> **Now — the library**
>
> *Otlet built this architecture **by hand** in 1895, with clerks and index cards, and **had every drawer but the court**. This afternoon we **mechanize** his library, and we build **the half he never had**.*
>
> **中文**：**现在——图书馆**。*Otlet 在 1895 年**用手**建成了这套架构，用的是馆员和索引卡片，**他拥有每一个抽屉，唯独没有法庭**。今天下午我们把他的图书馆**机械化**，并且建起**他从未拥有的那一半**。*

- **框架在这里闭合。** p.1 的副标题是 *Four experiments to run with your hands, **before we build the library***（在我们建图书馆之前）；终页就叫 ***Now — the library***。**Prelude 从一开始就把自己定义成序章，二十页走完，序章结束。**
- **"by hand" 这个词在首尾各出现一次，是刻意的**：p.1 说**你们**用手做四个实验，p.20 说 **Otlet** 用手建了这套架构。**你们上午做的，正是他用手做了四十年的事。** 这也解释了整场 Prelude 为什么必须发生在**没有电**的房间里——纸、桌子、地板、亲手走动。**先当一次馆员，才知道机械化省掉的到底是什么。**
- **⭐ "had every drawer but the court" 与四个实验精确对应**：
  - **实验一（许多地图）、实验二（五种感官）、实验三（五个目录）= 抽屉**，也就是**表征的组合与投影**——**Otlet 全都有**（书目卡、分类卡、剪报、图像库、百科摘要，五种目的各异的投影）。
  - **实验四（散落的纸：先召回、后精度）= 法庭**——**这一样他没有**。一个 UDC 类目**要么包含某张卡、要么不包含**；抽屉之内，**卡片按入藏顺序排列**。**他有铲子，没有筛子；有召回，没有排序。**
  - 讲义原句逐字对应：*The Mundaneum had the portfolio and lacked the court.* / ***Half of today is the half Otlet never built.***
- **"mechanize" 是这一页的关键动词**，对应讲义那条边注：***His institution died because every projection and every query cost a clerk; ours costs electricity.***（他的机构之所以死去，是因为每一次投影、每一次查询都要付一个馆员的代价；我们的只要电费。）**机械化 = 把馆员换成算力**——而 LLM 让派生表征的制造变便宜、六十年的索引结构让搜索次线性，就是那两台引擎。
- **人称值得注意**：*"**we** mechanize his library, and **we** build the half he never had."* ——**第一人称复数**把整个房间纳入了一项跨越 131 年、尚未完成的工程。**这不是在凭吊一个失败者，是在接手他的工作。** 呼应讲义的祝祷：*烧掉我们的 Mundaneum，我们就把它重新推导出来*——**语料是唯一不可替代的东西。**
- **排版上这一页没有右栏、没有列表、字极少、大量留白——它是一个呼吸点与转场。二十页的 Prelude 到此结束，正课开始。**


### 现场待记录 / 待补

- [x] ~~幻灯逐页记录~~ —— **20 页已全部收齐并记录完毕**
- [ ] 实验二：**看两秒那位的报告在白板上占了多少字**（「一家独大」的现场量化，晚上讲 RRF 的 k 时可直接引用）
- [ ] 实验二：**有几个人违反了「只报通道给你的东西」**；**闻的那位是否一句话锁定物体**（稀疏车道罕见词命中的现场演示）；**三个是/否问题问得好不好**（问题侧六病理的现场版）
- [ ] **白板上有没有出现任何一条「没有任何通道提供过」的信息** —— 若有，**幻觉当场发生**
- [ ] 远程学员（Zoom）在动手实验里的替代做法（Week 08 用过「举手／纸条／半个房间」的匿名聚合手法，可能复用）

---

## 〇-B、正课 deck 逐页记录：*The Library of Many Catalogues*（125 页，已记录 p.3–p.87）

> **Prelude 结束、正课 deck 开始。** 前者最后一页是 *Now — the library*，后者的 Prologue 就叫 **The Library**——**交接是字面的**。
> 已记录 **p.3–p.87** 中的大部分；**缺页清单与补课见本节末尾**；**p.88–125 尚未截取**。

### 正课 p.3 · **Prologue — The Journey Begins：The Library**

> **PROLOGUE · THE JOURNEY BEGINS**
> # **The Library**
>
> *A century before RAG, a Belgian lawyer **decomposed** the world's knowledge onto index cards — and built a **portfolio of catalogues** by hand.*
>
> **中文**：**序章 · 旅程开始**。**图书馆**。*在 RAG 出现的一个世纪之前，一位比利时律师把全世界的知识**分解**到索引卡片上——并且**用手**建起了一整套**目录的组合**。*

**左侧视觉**：一整片**卡片形状的方格阵列**（约 8 列 × 11 行以上，每格中间一个小圆点）——**Mundaneum 那一千六百万张索引卡的图像化**。绝大多数格子是暗的，少数被点亮成**珊瑚红**与**蓝色**两种颜色，分散在不同位置、彼此**部分重叠又不重合**。

- **这张图基本可以确定是「组合」这条论点的视觉版**：**同一片卡片阵列（一份语料），被不同的目录点亮出不同的子集**。红与蓝各自命中一批卡片、位置不同——**正是「每个索引是语料在自己那个角度上的一次投影」**。（也可能是一个 build 动画的中间帧，或是「相关的卡片 vs 实际被检索到的卡片」这种召回示意；**待现场确认**。）
- **无论哪种读法，它都在讲义写下任何一个字之前，先把论点画了出来。**

**三个措辞值得单独记**：

1. **`decomposed`（分解）** —— 这是**单篇原则（monographic principle）的准确动词**。讲义原文：*his monographic principle directed that documents be **decomposed** — each fact copied onto its own standard 3-by-5 card*。**Otlet 判定「书」是错误的单位**，因为**问题几乎从来不长成一本书的形状**。
2. **`a portfolio of catalogues`（目录的组合）** —— **全天论点的核心词，在正课的第一句话里就出现了**。讲义的完整论点是「**表征的组合 + 裁决的法庭**」，而这一页**只给了前半句**。
3. **`by hand`（用手）** —— **这是这个词第三次出现**：Prelude p.1（*四个用手做的实验*）→ Prelude p.20（*Otlet 用手建了这套架构*）→ 正课 p.3（*用手建起目录的组合*）。**一条贯穿的线索：今天所有要机械化的东西，都曾经是手工完成过的。**

**⭐ 注意这一页故意没说的那一半**：讲义的转折是——***The Mundaneum had the portfolio and lacked the court.***（有组合，缺法庭）。**这一页只夸他建成了什么，还没说他缺了什么。** 按讲义的顺序，接下来几页大概率是：**卡片规模与检索服务的细节（1912 年起电报提问、每千张卡 27 法郎、每年约 1,500 次查询）→ 1934 年撤资、1940 年六十三吨被毁 → 然后才是那记转折：他没有排序（ranking），抽屉之内卡片按入藏顺序排列。**


### 正课 p.4 · **Otlet's Mundaneum**

> Otlet and La Fontaine set out to catalogue **everything humanity had published** — the **monographic principle**: **one atomic fact per 3×5 card**. **Sixteen million cards** at the peak.
>
> *Queries arrived by telegraph; clerks walked the drawers; answers went back by mail — **a retrieval service with a latency of days**.*
>
> 图注：*Otlet at his desk. (Mundaneum archives)*
>
> **中文**：Otlet 与 La Fontaine 立志给**人类出版过的一切**编目——**单篇原则**：**一张 3×5 卡片装一个原子事实**。**巅峰时期一千六百万张卡片。**
> *提问通过电报到达；馆员在抽屉之间行走；答案通过邮件寄回——**一项延迟以「天」计的检索服务**。*

**配图**：Otlet 本人坐在书桌前的褐色旧照，**身后是整面墙的卡片抽屉柜**，桌上堆满纸张——**抽屉 = 索引，桌面 = 工作集**。

- **`one atomic fact per 3×5 card` 是今天 factoid 的直系祖先。** 讲义把这条线画得很直：**单篇原则 → Dense X 的 proposition-level retrieval → FactoidWiki 的 2.57 亿条命题**。Otlet 判定「书」是错误的单位，因为**问题几乎从来不长成一本书的形状**；今天我们把一个五声明的段落拆成 factoid，理由**一字不差**——段落 embed 在五种意义的质心附近，而尖锐的问题落在某一个顶点上。
- **⭐ 用工程师的耳朵听第二段**（讲义边注明确要求这么听）：**一个远程客户端、一个多索引知识库、带出处的检索证据，以及以「天」为单位的延迟。**

| Mundaneum（1895–1934） | 今天 |
|---|---|
| 电报提问 | API 请求 |
| 馆员在抽屉之间行走 | 索引查找（次线性） |
| 邮寄回答 | 响应 |
| **延迟：天** | **延迟：毫秒** |
| **一卡一事实** | **factoid / proposition** |
| UDC 分类的连接符号（可从多方向寻址） | 多索引 + 元数据过滤 |
| **每次投影、每次查询 = 一个馆员的工资** | **每次投影、每次查询 = 电费** |

- **幻灯没给、但讲义补充的运营细节**（值得一并记住）：**从 1912 年起提供该服务，每千张卡 27 法郎，每年约 1,500 次查询**；1934 年 Otlet 的 *Traité de documentation* 已经画出了由桌面与屏幕组成的 **réseau**——**一个联网终端，写于 Turing 还在读本科那年**。
- **⭐ 转折仍未到来。** p.3 讲他建成了组合，p.4 讲规模与服务，**都还是在夸**。讲义的那记转折——***他没有排序：一个 UDC 类目要么包含某张卡、要么不包含；抽屉之内，卡片按入藏顺序排列***——**还没出现**。按顺序，接下来大概率是**1934 年撤资 / 1940 年六十三吨被毁 / 1944 年去世**，然后才是那句 ***had the portfolio and lacked the court***。


### 正课 p.5 · **One corpus, many catalogues**（全天标题句本身）

> **Many projections of one corpus**: **by subject, by author, by facet, by the facts themselves.** In 1940 the occupiers cleared the halls — **sixty-three tonnes destroyed**; the surviving drawers reached **Mons**.
>
> *A **multi-representation retrieval system, by hand** — **factoids a century before FactoidWiki**. Today we **mechanize** his library.*
>
> **中文**：**一份语料的许多投影**：**按主题、按作者、按分面（facet）、按事实本身**。1940 年占领者清空了展厅——**六十三吨被摧毁**；幸存的抽屉最终抵达**蒙斯（Mons）**。
> *一套**用手做成的多表征检索系统**——**比 FactoidWiki 早了一个世纪的 factoid**。今天我们把他的图书馆**机械化**。*

**配图**：Mundaneum 工作大厅的黑白照——**一排排卡片柜沿墙铺开，馆员（多为女性）坐在桌前作业**，吊灯垂下，桌上堆着卡片盒。**这张照片就是「每一次投影、每一次查询都要付一个馆员的代价」的图像证据**——那套系统的算力单位是人。

- **标题即全天论点**：*One corpus, many catalogues* 是讲义反复出现的那句，也是整堂课标题（*The Library of Many Catalogues*）的来源。
- **⭐ 四种投影被逐一点名，且可以逐条映射到今天**：

| Otlet 的投影 | 今天的对应 |
|---|---|
| **by subject**（按主题） | UDC 分类 / **summary 索引**（section、document、corpus 三种高度） |
| **by author**（按作者） | **结构化元数据字段 / 前置过滤** |
| **by facet**（按分面） | **UDC 的连接符号**——`statistics : agriculture : India : 1895`，一张卡同时坐在多个维度的交点上；今天是**多索引 + 多维过滤** |
| **⭐ by the facts themselves**（按事实本身） | **factoid 索引 / proposition-level retrieval** |

  **最后一条是这一页的重点**：*"by the facts themselves"* 就是**单篇原则的检索形态**——不是按书找，是**按事实找**。而下一句直接把话挑明：***factoids a century before FactoidWiki***。**Dense X / FactoidWiki 的 2.57 亿条命题，是这张卡片的工业化版本。**（这条印证了 p.4 记录里的推断。）

- **`by hand` 第四次出现**（Prelude p.1 / Prelude p.20 / 正课 p.3 / 这里），且这次和 **`multi-representation retrieval system`** 这个技术名词直接并置——**「多表征检索系统」这个词，第一次被用在一套纯手工系统上。**
- **`Today we mechanize his library` 与 Prelude 终页逐字重复**（*This afternoon we mechanize his library*）——**deck 在明确接续 Prelude 的最后一句话，交接是设计好的。**
- **⭐ 六十三吨这个数字会在今天结束时再回来一次。** 讲义的收尾祝祷是：
  > **1940 年被摧毁的不是知识，是知识的表征**——目录、摘要、卡片本身——**而让那次损失不可逆的，是 Otlet 的推导管线是由馆员和四十年做成的。我们的可以重跑。**
  > **烧掉我们的 Mundaneum，我们就把它重新推导出来**：一座算力冰山、几天的管线时间、一套回归测试来证明重建是诚实的。**语料是唯一不可替代的东西。**

  **也就是说：现在听到的是悲剧，晚上再听到时是论证**——**所有索引都是派生物，可从「语料 + 配方」重新生成；唯有语料不可替代。**
- **转折依然未到。** 三页讲完组合、规模、毁灭，讲义里那句 ***他没有排序（ranking）*** 仍未出现。**下一页大概率就是它**——*had every drawer but the court*。


### 正课 p.6 · **Prologue — The Load-Bearing Wall：The recall ceiling**

> **PROLOGUE · THE LOAD-BEARING WALL**
> # **The recall ceiling**
>
> A child loses her marbles in a sandbox; she recovers them with **a bucket and a sieve**. **Scoop wide, scoop generously, tolerate sand** — the sieve removes sand **at leisure**.
>
> But **if the scoop misses a marble, no sieve can recover it.**
>
> 右栏：*Whatever recall you have at the scoop is a **ceiling**. **No reranker, no prompt, no bigger model raises it** — **generation cannot cite what retrieval never surfaced**. **Only the scoop decides what is caught.***
>
> **中文**：**序章 · 承重墙**。**召回天花板**。一个孩子把弹珠丢在沙坑里，用**桶和筛子**找回来。**铲得宽、铲得慷慨、容忍沙子**——筛子可以**从容地**把沙子除掉。**但如果铲子漏掉了一颗弹珠，任何筛子都救不回来。**
> 右栏：*你在铲的阶段拿到多少召回，那就是一个**天花板**。**没有 reranker、没有 prompt、没有更大的模型能把它抬高**——**生成器无法引用检索从未浮出水面的东西**。**只有铲子决定什么被捞起。***

- **这一页是实验四的正式命名**（对照 Prelude p.14「九十秒，尽可能多地捡，先别读」与 p.17「诱饵的代价在桌边，不在铲的阶段」）。**两半合起来才完整**：**铲得宽，因为漏掉是永久的；筛得狠，因为沙子便宜且可延后。**
- **⭐ 全页最关键的是那条不对称性**（幻灯没直说，但整段论证都建立在它上面）：

| 错误类型 | 发生在 | 性质 |
|---|---|---|
| **铲进沙子**（假阳性） | 铲阶段 | **可逆、便宜、可延后处理** |
| **漏掉弹珠**（假阴性） | 铲阶段 | **不可逆、永久** |

  **召回之所以「神圣」，不是因为它比精度重要，而是因为只有召回的错误是不可逆的。**

- **⭐ 右栏点名的三样「抬不高天花板」的东西，恰好是团队最爱伸手去拿的三个补救措施**——值得逐条说清为什么无效：
  1. **reranker** —— 它**只能重排递给它的东西**。没进候选集的文档，它见都没见过。
  2. **prompt** —— 它只作用于生成器，而**生成器只看得见被检索出来的上下文**。
  3. **更大的模型** —— **这一条最危险**。更大的模型**看起来**像是修好了问题，因为它会**用参数化知识把答案编出来**——**这正是 Week 08 的参数泄漏**。**它没有提高召回，它把「检索失败」转换成了「无据回答」**，而且**这个答案还引用不了任何来源**。
- **`generation cannot cite what retrieval never surfaced` 是六月第一天就埋下的那颗种子**，整个夏天每一周都靠在这堵墙上——今天这堵墙终于拿到它的工程学。
- **⚠️ 一条实务推论（讲义在评估周已经铺垫过）**：**假阳性你看得见，假阴性你看不见。** 沙子进了候选集，你一眼就能发现；**而漏掉的那颗弹珠不会留下任何痕迹**——没有报错、没有低分、没有任何信号。**所以召回只有靠封存的 gold set 才能测量**，这就是为什么「先有标尺，再建基线」这个顺序不能颠倒。
- **`at leisure`（从容地）这个词与 Prelude p.17 右栏逐字相同**（*then sieve at leisure with an expensive judge*）——**deck 与 Prelude 共用同一套措辞，是刻意的复现。**
- **📝 记录一下我的一次预测偏差**：p.5 之后我预计紧接着是「他有组合、缺法庭」那记转折；deck 实际先跳到了**承重墙（召回天花板）**。**「lacked the court」这句仍未出现**，按讲义结构它应当在论点陈述附近——**待后续几页确认。**


### 正课 p.7 · **Prologue — The Governing Thesis：Portfolio, and court**（⭐ 全天论点）

> **PROLOGUE · THE GOVERNING THESIS**
> # **Portfolio, and court**
>
> **A retrieval system is not a search over documents.** It is:
>
> **A portfolio of representations** — many **purpose-built** projections of one corpus.
> **A court of adjudication** — a cascade where cheap judges narrow the field so expensive judges can afford to be careful.
>
> 右栏：*Architecture is deciding **which representations to manufacture** and **how to adjudicate among them**. **Scale decides how much of each you can afford.** **Every slide today is a footnote to this thesis.***
>
> **中文**：**序章 · 统辖性论点**。**组合，与法庭**。**一个检索系统不是「在文档上做搜索」。** 它是：**一组表征的投资组合**——同一份语料的许多**为特定目的而造的**投影；**一座裁决的法庭**——一个级联，便宜的法官缩小战场，好让昂贵的法官负担得起「仔细」。
> 右栏：*架构就是在决定**制造哪些表征**、以及**如何在它们之间裁决**。**规模决定你各自负担得起多少。** **今天每一张幻灯，都是这条论点的一个脚注。***

- **⭐ 论点在这里补全了，法庭终于到场。** deck 的实际顺序是：**p.3–5 用 Otlet 给出「组合」→ p.6 用弹珠给出「承重墙 / 召回天花板」→ p.7 把两半合起来命名。** Otlet 那句 *had the portfolio and lacked the court* 到此已**不必再说**——**他有第一条，没有第二条**，前四页就是它的注脚。
- **开头那句否定式很重要**：***not a search over documents***。它先**拆掉默认心智模型**（查询进去、文档出来、一条排序列表），再给替代模型。**很多团队的架构问题，根源就在于他们从没离开过被否定的那句。**
- **`purpose-built`（为特定目的而造）是这一页的关键限定词。** 不是「索引越多越好」——**每一个投影之所以存在，是因为某一类问题恰好需要它**。对应讲义派生物清单那条纪律：***没有任何一件派生物靠「有趣」赢得位置；它靠指出「没有它，检索会以哪种具体方式死掉」来赢得位置。***
- **⭐ 右栏把「架构」定义成两个决定，而这两个决定就是今天剩下部分的目录**：

| 决定 | 对应 |
|---|---|
| **制造哪些表征**（which representations to **manufacture**） | **Act II · 第二语料库**——派生物清单七件 |
| **如何在它们之间裁决**（how to **adjudicate** among them） | **Act III · 法庭**——RRF、去重、cross-encoder |
| **（约束）规模决定你各自负担得起多少** | **Playbook**——伽利略的平方立方律、蟑螂尺度 vs 内骨骼、消融门 |

  **注意动词是 `manufacture`（制造），不是 choose 或 use。** 这已经预告了 Act II 的立场：**不要等 query 来匹配文档，去制造匹配 query 的文档。**

- **⭐ `Every slide today is a footnote to this thesis`** —— 化用 Whitehead 那句「整个西方哲学传统不过是柏拉图的一系列脚注」。它在告诉你：**当后面的东西开始模糊时，回到这一页。**
- **⭐ 一条结构性观察：序章交付的，正好就是讲义《校准说明》要求你今晚唯一握住的两件东西。**
  > 讲义原话：*那超过了一天的量，也没期待你今晚就全部握住。**握住论点和召回天花板。** 其余的，回到这里来取。*

  **论点 = p.7，召回天花板 = p.6。** 也就是说——**Prologue 一结束，及格线就已经交付完毕；后面九个小时全部是可以事后再取的深度。**
- **措辞复现**：*cheap judges narrow the field so expensive judges can afford to be careful* 与 Prelude p.18 右栏（司法阶梯）逐字同源——**Prelude 的四颗种子正在被逐一兑现成正课的术语。**


### 正课 p.8 · **The tomographic principle**（Prelude p.9 的正课版）

> # **The tomographic principle**
>
> A CT scanner never photographs the tumor: hundreds of **lossy projections**, each blind alone, **reconstruct** what no single exposure contains. **Each index is one projection; fusion is the reconstruction.**
>
> *The kin: the cubist portrait (right), the compound eye, Rashomon. **Not the panopticon** — one eye claiming total sight. **The portfolio refuses that claim.***
>
> 图注：*Juan Gris, **Portrait of Picasso**, 1912. Public domain.*
>
> **中文**：**断层扫描原理**。CT 扫描仪从不给肿瘤拍照：数百道**有损投影**，每一道单独看都是瞎的，却**重建**出没有任何单张曝光包含的东西。**每个索引都是一道投影；融合就是那次重建。**
> *同族：立体派肖像（右）、复眼、罗生门。**不是全景敞视监狱**——一只眼睛宣称拥有全部视野。**组合拒绝那个宣称。***

> 📌 这条原理的完整拆解（CT 机制、三个同族各自代表什么、全景敞视的对比、以及「检索没有 Radon 重建定理」那条补注）见 **Prelude p.9**。以下只记正课版**新增**的东西。

- **⭐ 配图是真迹：Juan Gris《Portrait of Picasso》（1912）。** 这个选择有三层机锋：
  1. **画的是毕加索本人，用的是毕加索发明的技法**——立体主义的共同创始人，被一位追随者用立体主义画了下来。**同一张脸的正面与侧面被同时压在一个平面上。**
  2. **这不是「画坏了的肖像」**，而是一幅**携带了单一视点无法携带的信息**的肖像——正是 *many simultaneous angles* 的字面演示。
  3. **⭐ 年代**：Mundaneum 始于 **1895**（布鲁塞尔），立体主义成型于 **1907–1912**（巴黎），Gris 这幅正是 **1912**。**同一个历史时刻，欧洲在「信息科学」和「绘画」两个毫不相干的领域，各自独立地推出了同一个主张：把对象分解，从多个角度同时表征它。** 这和 Prelude p.9 那三个「同族」的用意一致——**这不是一个检索技巧，是一条更普遍的认识论转向。**
- **⭐ 新增的最后一句：*The portfolio refuses that claim.*** Prelude 版只说了「不是全景敞视」，正课版**把它接回了 p.7 的论点词**：
  - **p.7 从正面定义 portfolio**：*许多为特定目的而造的投影*
  - **p.8 从反面定义 portfolio**：**它是那个「拒绝『一只眼睛拥有全部视野』」的东西**
  - **两个定义缺一不可。** 讲义的完整句是：***单一索引在做那个宣称；组合拒绝它——而这个拒绝，就是整个架构的一个手势。***
- **`Each index is one projection` 这半句是 Prelude 版没有的直接翻译**：Prelude 说「你们刚才就是那台扫描仪」（体验），正课说「**每个索引都是一道投影**」（术语）。**又一次「先站在里面，再给它起名字」。**


### 正课 p.9 · **Prologue — A map on the scale of a mile to the mile：Mein Herr's map**

> **PROLOGUE · A MAP ON THE SCALE OF A MILE TO THE MILE**
> # **Mein Herr's map**
>
> *"And then came the grandest idea of all! We actually made a map of the country, **on the scale of a mile to the mile**!"*
> *"Have you used it much?" I enquired.*
> *"**It has never been spread out, yet**: the farmers objected — it would cover the whole country, and **shut out the sunlight**! So we now **use the country itself, as its own map**, and I assure you **it does nearly as well**."*
>
> 右栏：*Lewis Carroll, **Sylvie and Bruno Concluded**, 1893. **The perfect map is no map**: a representation that keeps everything **has chosen nothing**, and **cannot be unfolded**. Every useful projection is a decision about **what to attend to** — and **what to leave in the dark**.*
>
> **中文**：**序章 · 一张一英里比一英里的地图**。**Mein Herr 的地图**。*「然后来了最伟大的主意！我们真的做了一张这个国家的地图，比例尺是**一英里比一英里**！」「你们常用它吗？」我问。「**它还从来没被摊开过**：农民们反对——它会盖住整个国家，**把阳光挡掉**！所以我们现在**直接拿这个国家本身当它自己的地图**，我向你保证，**效果几乎一样好**。」*
> 右栏：*Lewis Carroll，《西尔维与布鲁诺 · 续篇》，1893。**完美的地图就是没有地图**：一个保留了一切的表征，**等于什么都没有选择**，而且**摊不开**。**每一个有用的投影，都是一次关于「注意什么」——以及「把什么留在黑暗里」——的决定。***

- **这一页在回答一个必然会被问出来的反问**：*既然每个表征都有损，那为什么不干脆做一个不丢任何东西的表征？* **Carroll 的笑话就是答案。**
- **⭐ 它把「有损」从缺陷升级为定义性质。** 和 Prelude p.19 那句合起来，论证就完整了：
  1. **表征 = 一次「选择忽略什么」的决定**（Prelude p.19）
  2. **而一个什么都不忽略的表征，等于没有做任何选择**（本页）
  3. **所以：有损不是表征的缺陷，是表征之所以成立的条件。**
- **⭐ 工程上的翻译（这一页最硬的一条）**：**`cannot be unfolded`（摊不开）= 没有压缩。**
  - 一个和语料**一样大**的索引，**不提供任何导航优势**——你要扫完它，等于扫完语料本身。
  - **检索之所以能次线性，正是因为索引是有损压缩。无损 = 无压缩 = 无加速。**
  - 这也解释了 Otlet 为什么选卡片而不是复制整本书：**单篇原则本身就是一次激进的压缩决定。**
- **⭐ *"use the country itself, as its own map … it does nearly as well"* —— 这是长上下文幻象，早了 130 年。**
  - **把整个语料塞进百万 token 窗口，字面上就是「拿国家本身当自己的地图」。**
  - 而 **"it does nearly as well"（效果几乎一样好）正是那个诱惑的原话**——讲义在 Act II 幕间会用 **NoLiMa** 来回答它：**去掉词面重叠，十二个前沿模型里有十一个在 32K 处丢掉一半准确率。**
  - 讲义的图书馆论证也是同一句：***你不会为了回答一个问题去读整座图书馆；你查目录。而 Otlet 的馆员——他们本来可以读到任何答案——之所以建那些目录，恰恰是因为「读」不 scale。***
  - **（这是我的读法，待现场确认是否被明确点出；但从措辞看，这一页大概率是 Act II 幕间的伏笔。）**
- **两个小细节**：
  - **修辞是贯通的**：引文里农民反对是因为地图会**挡住阳光（shut out the sunlight）**；右栏说每个投影都要决定**把什么留在黑暗里（leave in the dark）**。**光与暗这条线从笑话一路接到教条。**
  - **`attend to`（注意什么）** —— 在一门刚讲过 attention 的课上，这个用词很难说是巧合：**一个投影决定「注意什么、忽略什么」，正是注意力权重在做的事。**
- **年代**：**1893**，比 Mundaneum（1895）**早两年**。同族的更著名版本是 **Borges《论科学的精确性》（1946）**——一个帝国的制图师造出了与帝国等大的地图。**Carroll 是更早的那个。**
- （📌 这一页兑现了我在 Prelude p.9 记录里埋的那条预测：*「也很可能顺手埋一个反向的种子：那为什么不直接印一张什么都有的地图？」*）


### 正课 p.10 · **To the sun and the winters：Borges — the map of the Empire**

> **TO THE SUN AND THE WINTERS**
> # **Borges: the map of the Empire**
>
> Borges **retold Carroll's joke as history**: the Cartographers Guild struck a map of the Empire **the size of the Empire, point for point**. Later generations found it **useless** and **left it to the sun and the winters** — **tattered ruins in the western deserts**.
>
> *"On Exactitude in Science," 1946. **The map that omits nothing is abandoned by everyone. A representation earns its use by what it leaves out.***
>
> **中文**：**交给太阳与冬天**。**博尔赫斯：帝国的地图**。博尔赫斯**把 Carroll 的笑话重讲成了历史**：制图师公会造出了一张**与帝国等大、点对点**的帝国地图。后世发现它**毫无用处**，**把它丢给了太阳和冬天**——**西部沙漠里的残破遗迹**。
> *《论科学的精确性》，1946。**一张什么都不省略的地图，会被所有人抛弃。一个表征，靠它省略掉的东西挣得自己的用途。***

**配图**：一张做旧的世界地图（`MAPPA MUNDI ANTIQUA`），**图面本身正在龟裂、风化成沙漠地形**——字面意义上的「地图烂在沙漠里」。
> 🔍 **细节**：图上标着 **`OCEANUS OCCIDENTALIS`**——**和实验一发到手的那张 OTLETIA 航海图是同一个海名**。**Prelude 与正课共用一套虚构地理，整天是被当作一件作品设计的。**

- **⭐ Carroll → Borges 不是重复，是升级，因为两者失败在不同的时间点上**：

| | 失败方式 | 工程对应 |
|---|---|---|
| **Carroll（1893）** | 地图**从未被摊开过**（农民反对） | **部署阶段就不可行**——无损表征没有压缩，摊开等于扫全量 |
| **Borges（1946）** | 地图**被造出来了、被用过**，然后**被抛弃、风化成残骸** | **运营阶段不可持续**——它被建成、被维护、然后没人查询，只剩账单 |

  **合起来才是完整论证：无损表征在部署上不可行，在运营上不可持续。**

- **⭐ 「留给太阳和冬天的残骸」有一个非常具体的现代对应：一个没人查询、却仍在计费的索引。**
  - 讲义的成本账簿说：**存储字节与每索引的边际美元是 CFO 读的那份，组合里每一个索引都必须向它记账。**
  - 而 Playbook 点名的两种病理里，**Sacred Cow（神牛）**就是这张帝国地图——**因为它很贵、或者当初有人力荐，所以留着**。
  - **判据仍然是那一句**：***如果拿掉它什么都没变，那头牛就是牛肉。***
- **`earns`（挣得）这个动词值得记**：右栏说*一个表征**挣得**它的用途*，而 Playbook 的规则是***每一个索引都必须通过消融挣得它的位置***——**同一个动词，序章埋、终章收。**
- **一句可以直接背的**：***The map that omits nothing is abandoned by everyone.***（一张什么都不省略的地图，会被所有人抛弃。）与 p.9 的 ***The perfect map is no map*** 配成一对——**前者讲它没用，后者讲它不成其为地图。**


### 正课 p.11 · **Prologue — One country, many maps：Every map is a choice of what to ignore**（实验一的命名）

> **PROLOGUE · ONE COUNTRY, MANY MAPS**
> # **Every map is a choice of what to ignore**
>
> The **naval chart** keeps depth soundings, shoals, and lights — **and erases every road**. The **road map** keeps junctions and distances — and erases the sea floor. The **political map** keeps borders and capitals — no contour lines. The **geological map** keeps strata — no cities at all.
>
> **Same country. Four maps. Each one useful *because* of what it threw away.**
>
> 右栏：*A **representation is a choice of attention**. **BM25 attends to the words; the dense lane to the meaning; the factoid to the claim; the summary to the theme. None is the country. The portfolio is the atlas — and the court decides which page to open.***
>
> **中文**：**每一张地图都是一次「选择忽略什么」**。**航海图**保留水深、浅滩和灯标——**并抹掉每一条路**。**公路图**保留路口与距离——抹掉海床。**政治地图**保留边界与首都——没有等高线。**地质图**保留地层——完全没有城市。**同一个国家。四张地图。每一张之所以有用，正是**因为**它丢掉的那些东西。**
> 右栏：*一个表征就是**一次注意力的选择**。**BM25 注意的是词；dense 车道注意的是意思；factoid 注意的是声明；summary 注意的是主题。没有一个是那个国家本身。组合是那本地图册——而法庭决定翻开哪一页。***

- **🎯 直接命中你手里那张图**：幻灯说航海图 ***erases every road***——而实验一发到你手上的那张 `OTLETIA — Approaches to Otlet Harbour`，**副标题上就印着 `NO ROADS`、图右半边写着 `(land: not charted)`**。**你上午握在手里的那个「盲区」，现在成了正课的第一个例子。**
- **⭐ 这是「有损」论证的第三级、也是最强的一级**：

| 阶段 | 主张 | 语气 |
|---|---|---|
| **Prelude p.19** | 表征 = 一次「选择忽略什么」的决定 | **中性描述** |
| **正课 p.9 / p.10**（Carroll / Borges） | 什么都不忽略 = 什么都没选 = 摊不开、被抛弃 | **反证** |
| **正课 p.11** | **每一张之所以有用，正是「因为」它丢掉的东西** | **正面主张** |

  幻灯把 **`because`** 单独标了色——**不是「虽然有损但仍然有用」，而是「有用性来自丢弃本身」。**

- **⭐ 右栏那四行是全天组合的一句话版本，值得直接背下来**：

| 车道 | 它注意的是 |
|---|---|
| **BM25** | **词**（纸面上印出来的那些字） |
| **dense 车道** | **意思**（词背后的语义） |
| **factoid** | **声明**（原子事实） |
| **summary** | **主题**（贯穿全文的东西） |

  **`None is the country.`** —— Korzybski 又一次：**没有任何一条车道是疆域本身。**

- **⭐ 一个新的、更好用的比喻：*The portfolio is the atlas — and the court decides which page to open.***
  - **组合 = 地图册（atlas）**：一本装订好的、由不同地图组成的册子。
  - **法庭 = 决定翻开哪一页。**
  - **这比「便宜法官/昂贵法官的级联」更容易向非专业同事解释**，而且**把 p.7 的两半装进了同一个实物**。
  - ⚠️ **小小的不精确（值得自己心里记住）**：地图册的比喻**略微低估了融合**——实际的法庭不是「只翻开一页」，而是**同时读几页、再按名次把它们合起来（RRF）**。**准确说法应该是：法庭决定翻开哪几页、以及各页的话该算多重。**
- **结构观察**：正课序章正在**把四个实验逐一兑现成教条**——**p.6 = 实验四（召回天花板）→ p.7 = 论点 → p.8 = 实验二（断层扫描）→ p.9–10 = 地图插曲（Carroll / Borges）→ p.11 = 实验一（许多地图）**。**按此推断，下一页大概率是实验三——「一份语料，许多抽屉；每个问题有它的高度」，即四种查询高度。**


### 正课 p.12 · **Prologue — Not all questions live at the same height：The four query altitudes**（实验三的命名）

> **PROLOGUE · NOT ALL QUESTIONS LIVE AT THE SAME HEIGHT**
> # **The four query altitudes**
>
> **Point** — *"what is the notice period in clause 12(b)?"*
> **Contextual** — *"what does **this** section mean for my renewal?"*
> **Thematic** — *"how has our flood-risk stance evolved?"*
> **Global (sensemaking)** — *"what are the major regulatory concerns across the portfolio?"*
>
> 右栏：***Misjudging a query's altitude is the most reliable way to build the wrong system.** Hold the optics in mind all day: **microscope, zoom lens, telescope** — a well-equipped laboratory owns all three.*
>
> **中文**：**序章 · 不是所有问题都住在同一个高度**。**四种查询高度**。**点**——「第 12(b) 条里的通知期是多久？」**语境**——「**这一**节对我的续约意味着什么？」**主题**——「我们对洪水风险的立场是怎么演变的？」**全局（sensemaking）**——「整个投资组合里的主要监管关切有哪些？」
> 右栏：***误判一个查询的高度，是把系统建错的最可靠方式。** 全天都把这套光学器械记在心里：**显微镜、变焦镜头、望远镜**——**一间装备齐全的实验室三件都有。***

- **⭐ 四个例子刻意取自同一个领域**（保险/合同：通知期、续约、洪水风险、监管组合）——**同一个用户、同一份语料，四种高度**。这说明：**高度是「问题」的属性，不是领域或语料的属性。** 你不能靠「我们是法律行业」来决定架构，只能靠**实测的查询分布**。
- **`this` 被单独标了蓝色**，这不是排版随意：**「这一节」里的「这」就是内指（endophora）**——**它的含义取决于用户此刻站在哪里**。这正是**语境化改写（contextualized rewrite）**这件派生物要治的那具尸体：**把代词解析掉，让 chunk 脱离上下文也能被检索到。**
- **四种高度 → 四种表征**（讲义的对应表）：

| 高度 | 想要什么 | 对应表征 |
|---|---|---|
| **Point** | 一个事实 | **factoid** |
| **Contextual** | 一整段、周边完好 | **chunk** |
| **Thematic** | 贯穿一份文档的东西 | **summary** |
| **Global** | 活在整个语料结构里、不在任何一段里 | **community summary / 图 sidecar** |

- **⭐ 右栏第一句是很重的一句**：***误判高度是把系统建错的最可靠方式***——注意它说的不是「效果会变差」，而是**「会建错系统」**。因为**高度决定你要制造哪些派生物**：以为流量是点查询，你就去建 factoid 索引；结果流量其实是主题查询，那个索引**再优化也答不了**。
  - 配套的失效表现是讲义那条：**落错高度不会报错，会给你一个自信的不相关答案**——点查询淹死在摘要里，全局查询被三条关于一种药的引文糊弄过去。
- **⭐ 光学三件套（the optical triad）**——讲义的完整版比幻灯多半句：
  > **factoid 是显微镜，RAPTOR 是变焦镜头，GraphRAG 是望远镜。一间运转良好的实验室三件都有，*并且知道自己手里握的是哪一件*。**
  - **「三件都有」= 组合**；**「知道手里握的是哪一件」= 路由器。** 幻灯只给了前半句，后半句在 Act III。
  - 🔍 **注意：四种高度，却只有三件光学器械。** 缺的那一件是 **Contextual/chunk**——**它是肉眼**，不需要器械，是默认视野。**三件仪器都是为了「肉眼看不到的高度」而配的。**
- **落地含义**：**权重来自你实测的查询分布**（讲义：*用例的暴政，写成账簿的形式*）。参考数字：**全局 sensemaking 约占企业流量 5–15%，而本课的路由器只送 1–2% 走图 sidecar**——**它定义智能的天花板，但不被允许承载高速公路。**
- （📌 兑现了 p.11 记录里的预测：序章正在把四个实验逐一兑现成教条，**p.12 = 实验三**。至此四个实验全部命名完毕：p.6=实验四、p.8=实验二、p.11=实验一、p.12=实验三。）


### 正课 p.14 · **ACT I · The Cabinet Opens：Every representation is a lossy projection**

> ⚠️ **p.13 未截到**（大概率是 Act I 的分幕标题页）。**序章到此结束（p.3–12），Act I 开始。**

> **ACT I · THE CABINET OPENS**
> # **Every representation is a lossy projection**
>
> An **inverted index** keeps **the words** and discards **the meaning**. A **dense vector** keeps **the gist** and discards **the words**. A **ColBERT matrix** keeps **both** — **and charges you storage for it**.
>
> **There is no faithful projection — only *different chosen losses*.**
>
> 右栏：*The design question of Act I is **never** "which representation is best?" It is: **which information can this query class not afford to lose?** Choose the projection **whose loss you can live with**.*
>
> **中文**：**第一幕 · 仪器柜打开**。**每一个表征都是一次有损投影**。**倒排索引**保留**词**、丢掉**意思**。**dense 向量**保留**要旨**、丢掉**词**。**ColBERT 矩阵**两者都保留——**并为此向你收取存储费**。**不存在忠实的投影——只有*不同的、被选择的损失*。**
> 右栏：*第一幕的设计问题**从来不是**「哪个表征最好？」它是：**这一类查询「输不起」哪些信息？** 选那个**你能承受其损失**的投影。*

- **⭐ 三行给出三种损失画像，可以直接背**：

| 表征 | 保留 | 丢弃 |
|---|---|---|
| **倒排索引（BM25/SPLADE）** | **词** | **意思**（同义、改写） |
| **dense 向量** | **要旨** | **词**（罕见标识符、精确短语） |
| **ColBERT 矩阵** | **两者** | **——换成了存储账单** |

- **⭐ 第三行才是这一页真正的转折**：**ColBERT 并没有逃出取舍，它把损失换了一种货币**——**从「信息损失」换成了「存储/成本损失」**。
  - 这条推论很重要：**有损是必然的，但损失可以被兑换成另一种货币（钱、延迟、内存）。**
  - 也正因为如此，**MUVERA 与 WARP 才是架构级事件而不只是工程优化**：它们**降低了那种货币的价格**，于是 ColBERT 在锦标赛里的位置就变了。讲义原话：***现在决定 ColBERT 坐在哪里的是锦标赛，不是成本反对意见。***
- **`different chosen losses`（不同的、被选择的损失）—— `chosen` 这个词把整条论证收口了**：

| 页 | 主张 |
|---|---|
| Prelude p.19 | 表征 = 一次**选择**忽略什么的决定 |
| 正课 p.9 / p.10 | 什么都不忽略 = 什么都没选 → 摊不开、被抛弃 |
| 正课 p.11 | **因为**丢弃了，才有用 |
| **正课 p.14** | **不存在忠实的投影，只有不同的、被选择的损失** |

  **损失是设计决定，不是意外。**

- **⭐ 右栏那句是目前为止最可操作的一条重构**：

  ❌ **错误的问题**：「哪个表征最好？」——**这个问题没有答案**，因为「最好」取决于查询。
  ✅ **正确的问题**：「**这一类查询输不起哪些信息？**」——**按 query class 提问，而且是反着问的：先说清你不能丢什么，再挑一个「损失落在别处」的投影。**

- **把 p.10 + p.12 + p.14 合起来，可以得到一个可执行的选型流程**：
  1. **列出你的 query class**（用实测分布，不是猜的）
  2. 对每一类问：**丢了什么就答不了？**（罕见编号？否定？跨段落关系？某个高度？）
  3. **选一个「损失落在别处」的投影**
  4. 多个 class → 多个投影，**并且检查它们的损失是否互不相关**（p.10 的蜻蜓推论：**失效相关的两个索引，加起来等于一个**）
  5. **最后用消融证明每一个都挣得了自己的位置**


### 正课 p.15 · **ACT I · Sparse lineage · 1972 to now：BM25 — the words on the page**

> **ACT I · SPARSE LINEAGE · 1972 TO NOW**
> # **BM25 — the words on the page**
>
> Robertson and Spärck Jones's lineage: term frequency **saturates** (**the 30th mention is not thirty times the relevance**), long documents are **normalized**, **rare terms carry more information**.
>
> **Fifty years old, and still the baseline every modern method is measured against.**
>
> 右栏：*Its failure mode is **exact-match brittleness**: **"convolution filters"** in the document, **"convolutional neural networks"** in the query — **one inflection, and the match dies**. **This is not theory. This is Tuesday.***
>
> **中文**：**第一幕 · 稀疏谱系 · 1972 至今**。**BM25——纸面上的那些词**。Robertson 与 Spärck Jones 的谱系：词频**会饱和**（**第 30 次提及并不等于三十倍的相关性**）、长文档被**归一化**、**罕见词携带更多信息**。**五十岁了，至今仍是每一种现代方法用来对照的基线。**
> 右栏：*它的失效模式是**精确匹配的脆性**：文档里写的是 **"convolution filters"**，查询里写的是 **"convolutional neural networks"**——**一个词形变化，匹配就死了**。**这不是理论。这是周二。***

- **`1972` 是 Spärck Jones 那篇 IDF 论文的年份**（*A statistical interpretation of term specificity...*）；Robertson & Spärck Jones 的概率检索模型在 1976；BM25 本身成型于 1994 年前后的 Okapi 项目（*Best Matching* 第 25 号迭代）。**「1972 to now」= 五十四年。**
- **幻灯点名的三条性质，就是 BM25 公式里的三块**：

| 幻灯用词 | 公式中的位置 | 含义 |
|---|---|---|
| **saturates** | `k₁`（典型 1.2） | **第 30 次提及不等于三十倍相关**——词频贡献递减 |
| **normalized** | `b`（典型 0.75） | 长文档天然更容易含任何词，要惩罚长度 |
| **rare terms carry more information** | **IDF** | 罕见词更值钱 |

- **⭐ 第三条其实就是 Week 02 的「surprise」**：**IDF ≈ −log P(term)**——**罕见 = 意外 = 信息量大**。**同一个 `−log p`，Week 02 用来定义训练损失，这里用来给词加权。** 两周之间最直接的一条数学连线。
- **「五十年了还是基线」= 讲义 Playbook 里那条**：***朴素基线（BM25 + 一个 LLM）是神圣的；它是零假设，而你加的每一个组件都是一次「零假设不够用」的声明。*** 升级阶梯的 **L1**。
- **⭐ 右栏这个失效例子比讲义正文的 `cardiac / heart` 更狠**：
  - `cardiac` vs `heart` 是**同义词问题**——两个不同的词。
  - `convolution` vs `convolutional` 是**同一个词的不同词形**——**连「换个说法」都算不上，只是一个后缀**，倒排表就已经不相遇了。**脆性比同义问题更基础。**
  - ⚠️ **一条补注（值得心里有数）**：**词干化（stemming / lemmatization）正是历史上针对这一类失效的补丁**——Porter stemmer 会把 `convolution` 和 `convolutional` 都归到 `convolut`。所以这个具体例子在**带词干化的管线里可能不会发生**。但结论不变：**词面匹配的脆性是结构性的**，而词干化本身也是一种**有损投影**（过度归并会把本该区分的词合成一个）——**你只是把损失从一个地方挪到了另一个地方**，正好呼应 p.14 的「不同的、被选择的损失」。
- **⭐ `This is not theory. This is Tuesday.`** —— 全天最好的一句俏皮话之一：**这不是论文里的边角案例，这是你生产日志里一个平常工作日就会发生的事。**
- **接下来**：按讲义顺序，下一页大概率是 **SPLADE**——**它正是为了修这一页点名的这个失效而存在的**：用 MLM 头学出词表上的稀疏扩展，让讲 `convolution` 的文档在自己从没印过的 `convolutional` 上也带权重，**同时保住倒排索引的全部运维美德**。


### 正课 p.16 · **ACT I · A cautionary tale, part one：BM42 — the launch**

> ⚠️ 顺序修正：p.15 之后**没有**接 SPLADE，而是插入了 **bm42 警世故事（分两部分）**。

> **ACT I · A CAUTIONARY TALE, PART ONE**
> # **BM42 — the launch**
>
> **July 2024**: Qdrant announces **BM42** — replace BM25's **term statistics** with **transformer attention weights**. **No fine-tuning needed.** The launch benchmarks show it **beating BM25 and even SPLADE**.
>
> **The idea is not absurd**; it is **UniCOIL's learned-reweighting instinct with attention as the teacher**.
>
> 右栏：*The benchmark of choice: **Quora** — a duplicate-question dataset averaging about **1.6 relevant items per query**. **Hold that number. It is about to end the story.***
>
> **中文**：**第一幕 · 一个警世故事，第一部分**。**BM42——发布**。**2024 年 7 月**，Qdrant 发布 **BM42**——用 **transformer 的注意力权重**替换 BM25 的**词频统计量**，**无需微调**。发布时的基准显示它**打败了 BM25，甚至打败了 SPLADE**。**这个想法并不荒谬**；它就是 **UniCOIL 那种「学习式重加权」的直觉，只不过把注意力当作老师。**
> 右栏：*所选的基准是 **Quora**——一个重复问题数据集，**平均每个查询约 1.6 个相关项**。**记住这个数字。它马上就要终结这个故事。***

- **⭐ 幻灯先替对方说好话：*The idea is not absurd*。** 这一点很重要，讲义也强调过：**教训不是关于某一家厂商**。**BM42 处在一条正当的谱系里**——**UniCOIL** 就是「学习式稀疏检索」（给每个词学一个权重，而不是用 IDF 这种统计量），**BM42 只是把老师换成了注意力权重**。**先把对方的想法讲成合理的，再讲它为什么没站住——这才是可复现的批评方式。**
- **⭐ 破绽在基准，不在想法**：**Quora 重复问题数据集，平均每查询约 1.6 个相关项。** 为什么这个数字会「终结故事」：
  1. **分辨力极低**：每个查询只有约 1.6 个正确答案，`recall@10` 这类指标**几乎所有方法都接近满分**，差异被压进噪声。
  2. **⭐ 它恰好没有语域错配**：Quora 是**问题对问题**——**query 和 document 是同一体裁、同样短、同样口语**。而**稀疏检索最吃亏、学习式扩展最该发光的场景恰恰是语域错配**（问题 vs 散文、口语 vs 法律腔）。**这个基准把被测方法最关键的能力维度整个抹掉了。**
  3. 所以这不是「数据作假」的故事，是**「用了一把量不出差异的尺」**的故事。
- **讲义给出的、要带走的那条反射**（不是关于厂商）：
  > **把每一次产品发布当作一篇你打算复现的论文来读，并让你自己封存的标尺去批改这份作业。**
- **`A CAUTIONARY TALE, PART ONE`** —— 分两部分，**第二部分讲翻车**：讲义原文是*一位细心的读者在几天内重算了算术，那个宣称没能存活*。
- **📌 这一页在全天结构里的作用**：它是 **Act I 的第一个「怎么读证据」的示范**，也预告了 Act III 的方法论——**配对 bootstrap 区间、封存 gold set、公开排行榜只是冒烟测试不是仪器**。


### 正课 p.18 · **ACT I · Sparse lineage · The destination：SPLADE — the words the page means**

> ⚠️ **p.17 未截到**——按标题推断是 **bm42 警世故事的第二部分（翻车）**：*一位细心的读者在几天内重算了算术，那个宣称没能存活*。

> **ACT I · SPARSE LINEAGE · THE DESTINATION**
> # **SPLADE — the words the page means**
>
> $$w_j = \max_i \log\big(1 + \mathrm{ReLU}(z_{ij})\big)$$
>
> Project each token through the **MLM head**; keep the **sparse max over positions**. *"The cow jumped over the moon"* activates **cattle, bovine, leaped, lunar** — **expansion terms the author never typed**, stored in **an ordinary inverted index**.
>
> 右栏：***BM25 sees only the words on the page; SPLADE sees the words the page means.*** *UniCOIL **reweights without expanding** — the conservative stop on the same line. **The house sparse lane is SPLADE.***
>
> **中文**：**第一幕 · 稀疏谱系 · 终点站**。**SPLADE——页面所「指」的那些词**。把每个 token 投过 **MLM 头**；在各位置上取**稀疏的最大值**。*"The cow jumped over the moon"* 会激活 **cattle、bovine、leaped、lunar**——**作者从未打出过的扩展词**，而且**存在一个普通的倒排索引里**。
> 右栏：***BM25 只看见纸面上印着的词；SPLADE 看见的是页面所指的词。*** *UniCOIL **只重加权、不扩展**——同一条线上更保守的那一站。**本课的稀疏车道默认是 SPLADE。***

- **标题是刻意与 p.15 对仗的**：**BM25 — the words on the page** ／ **SPLADE — the words the page means**。**纸面上的词 vs 页面所指的词。**
- **⭐ 公式逐项拆解**（这是这一页最值得带走的东西）：

| 项 | 作用 |
|---|---|
| $z_{ij}$ | **MLM 头**在**位置 i** 上对**词表第 j 个词**的 logit——「这个位置有多倾向于预测出这个词」 |
| $\mathrm{ReLU}(\cdot)$ | **把负值压成 0** —— **稀疏性就是在这里产生的**：绝大多数词表项直接归零 |
| $\log(1+\cdot)$ | **饱和**，与 BM25 的 `k₁` 同一种精神——不让某个被强烈激活的词一家独大，也把权重压在倒排索引好打分的量级上 |
| $\max_i$ | **在位置上池化**：只要**任何一个**位置强烈预测出 "cattle"，整份文档就在 "cattle" 上带权重。**用 max 而不是 sum**——只提一次但提得很重的词照样算数，也避免长文档权重膨胀 |
| $w_j$ | 结果：**整个词表上的一个权重向量，绝大多数为 0** → **一个稀疏向量，直接塞进倒排索引** |

  > 📎 **幻灯没写但值得知道**：SPLADE 训练时还会加一项 **FLOPS 正则**来压制非零项数量——**否则扩展会失控，倒排表被撑爆**。稀疏不是自动的，是被罚出来的。

- **⭐ 例子选得很准**：`cow → cattle, bovine`（同义/上位）、`jumped → leaped`（同义）、**`moon → lunar`（词形/派生）**。
  - **最后一个正好治的是 p.15 点名的那个失效**——`convolution` vs `convolutional`，**一个词形变化就让匹配死掉**。**SPLADE 同时补上了「同义鸿沟」和「词形脆性」两个洞。**
- **`stored in an ordinary inverted index` 是运营上的重点**：**倒排索引的全部美德都保住了**——精确过滤、增量更新、可解释（能看见是哪些词命中的）、成熟的基础设施、查询时不需要向量库。**这就是为什么它是「稀疏车道的终点站」而不是「另一条 dense 车道」。**
- **⭐ 稀疏谱系是一条连续的线，这一页把三站排好了**：

| 站点 | 权重来自 | 是否扩展 |
|---|---|---|
| **BM25** | **统计量**（TF/IDF） | ❌ |
| **UniCOIL** | **学出来的** | ❌ —— *保守的那一站* |
| **SPLADE** | **学出来的** | ✅ —— **终点站** |

  **而 p.16 的 BM42 正是想站在这条线上**（用注意力当老师做重加权）——**所以幻灯才说「这个想法并不荒谬」。UniCOIL 就是那个想法站得住的版本。**

- **⭐ `The house sparse lane is SPLADE.`** —— 和 DCL 是 house loss 一样，**本课在明确给出默认选项**：**稀疏车道选 SPLADE。**
  - ⚠️ **代价（幻灯未列，实务需知）**：扩展会**拉长倒排表** → 索引体积与查询延迟都高于纯 BM25；索引时和查询时都需要跑模型（BM25 不需要）。有若干 efficiency 变体在做这个取舍。**又一次「不同的、被选择的损失」。**


### 正课 p.19 · **ACT I · Dense geometry · THE LICENSE：Concentration of measure**

> **ACT I · DENSE GEOMETRY · THE LICENSE**
> # **Concentration of measure**
>
> $$\Pr\big[\,|\langle u,v\rangle| > \varepsilon\,\big] \;\le\; 2\,e^{-d\varepsilon^2/2}$$
>
> In high dimensions, random unit vectors are **almost surely near-orthogonal** — **the sphere's surface huddles at the equator of any pole you pick**.
>
> So **a high cosine is exponentially unlikely *by chance***.
>
> 右栏：*Anything found in the polar cap **got there for a reason** — **training pulled it there**. **Signal survives concentration; noise is annihilated by it. That is the real theorem behind semantic search.***
>
> **中文**：**第一幕 · 稠密几何 · 许可证**。**测度集中**。在高维中，随机单位向量**几乎必然近乎正交**——**无论你挑哪个极点，球面的面积都挤在它的赤道上**。所以**一个高余弦在「偶然」的意义上是指数级不可能的**。
> 右栏：*任何出现在**极冠**里的东西，**都是有原因才到那儿的**——**是训练把它拉过去的**。**信号在集中性中幸存；噪声被集中性消灭。这才是语义搜索背后真正的定理。***

- **⭐ 这一页把「测度集中」翻了个面。** 讲义正文里它是**危害**（阈值不可移植、top few 差异极小、reranker 辨别力更要紧）；这一页的分幕标题却是 **THE LICENSE（许可证）**——**它是「余弦到底凭什么能用」的理由。**
- **公式怎么读**：对 $d$ 维随机单位向量 $u,v$，它们内积绝对值超过 $\varepsilon$ 的概率**随维度指数衰减**。代几个数就有体感：

| 维度 $d$ | 阈值 $\varepsilon$ | 偶然超过的概率上界 |
|---|---|---|
| **1024** | 0.5 | $2e^{-128}\approx 5\times10^{-56}$ —— **实际等于零** |
| **1024** | 0.3 | $2e^{-46}\approx 2\times10^{-20}$ |
| **128** | 0.5 | $2e^{-16}\approx 2.3\times10^{-7}$ |

  **所以：你检索到一份余弦 0.8 的文档，它几乎不可能是碰巧撞上的。它在那儿，是因为训练把它放在那儿。**——这就是「许可证」。

- **⭐ 两副面孔怎么统一**（这一点值得想清楚，否则会觉得前后矛盾）：

| | 说的是哪个分布 | 结论 |
|---|---|---|
| **许可证（本页）** | **随机向量的零分布** | 零分布是一条极窄的带；**离 0 很远的东西不可能是零假设** |
| **危害（讲义正文）** | **训练过的 embedder 在真实语料上的实测分布** | 实测分布**并不像随机向量**（典型挤在 0.2–0.9），**所以绝对阈值不可移植、顶部差异极小** |

  **一句话：集中性保证了「背景噪声」被压成极窄的一条带；但你的 embedder 有没有把信号推出那条带，是训练的问题，不是几何的问题。**

- **⭐ 与 Week 02 的直接连线（这条最有用）**：**定理预测「随机文本对的余弦应当接近 0」。而 Week 02 那个 cosine histogram 实验实测到的是——**

| 模型 | 随机对 `mean` | 离定理预测（≈0）的距离 |
|---|---|---|
| **Raw BERT** | **0.722** | **极远** —— 这就是各向异性 |
| **MiniLM** | **0.169** | 接近 |
| **Fine-tuned** | `inter` = **−0.213** | 已经把无关项推到负相关 |

  **也就是说：各向异性的定义，就是「实测的随机对相似度」偏离「定理预测的 0」的程度。**
  **定理给出目标，Week 02 的直方图测量你离目标有多远。** 两周在这里合上了。

- **⚠️ 我的一条补注（对 128 维铲子的量化辩护）**：上表显示，**128 维在 0.5 阈值处的偶然碰撞概率约 $2\times10^{-7}$**——在**一千万份文档**的语料上，**期望约有 2 个纯属偶然的「高相似」邻居**；而**全宽 1024 维时这个数字实际是零**。
  **这正好量化了「铲—复评」模式为什么必要**：**128 维的铲子会放进一些偶然噪声（可接受，因为筛子在后面），而全宽复评把它们清掉。** 讲义那句「用 128 维在数百万候选上铲，再对幸存者用全宽复评」，在这条不等式里有精确的数值理由。


### 正课 p.20 · **ACT I · Dense geometry · THE DISCIPLINE：The aperture doctrine**

> **ACT I · DENSE GEOMETRY · THE DISCIPLINE**
> # **The aperture doctrine**
>
> A similarity threshold is a **cone of light** on the sphere: **0.5 opens the aperture to 60°, 0.7 to 45°, 0.8 to 37°, 0.9 to 26°.**
>
> **The house recipe is never a bare top-K. It is "up to 20, all above 0.7."**
>
> 右栏：*A bare top-20 is a promise to return twenty things **whether or not twenty relevant things exist**. **Forgetting the threshold is how irrelevance leaks into the context window — silently, politely, every query.***
>
> **中文**：**第一幕 · 稠密几何 · 纪律**。**光圈教条**。相似度阈值是球面上的**一束光锥**：**0.5 把光圈开到 60°，0.7 到 45°，0.8 到 37°，0.9 到 26°。** **本课的配方从来不是裸的 top-K，而是「最多 20 个，且全部高于 0.7」。**
> 右栏：*一个裸的 top-20 是一句承诺：**不管存不存在二十个相关的东西，都要还你二十个**。**忘掉阈值，就是无关内容渗进上下文窗口的方式——无声地、礼貌地、每一次查询。***

- **⭐ 分幕标题是刻意配对的**：**p.19 = THE LICENSE（许可证）**，**p.20 = THE DISCIPLINE（纪律）**。
  - **许可证说：高余弦不可能是偶然，所以你「可以」信任它。**
  - **纪律说：你仍然必须自己决定「多高才算高」，并且强制执行它。**
  - **两页是一对：几何给你授权，工程要你自律。**
- **角度换算全部正确**（阈值 = cos θ）：`arccos 0.5 = 60°`、`arccos 0.7 ≈ 45.6°`、`arccos 0.8 ≈ 36.9°`、`arccos 0.9 ≈ 25.8°`。**阈值不是一个数，是围绕 query 方向的一个立体角**——**开大进沙，收小丢弹珠。**
  - 🔍 与 p.19 合读会有一个反直觉的体感：**45° 的锥听起来很宽**（像是球面上很大一块），**但在 1024 维里，落在任一固定方向 45° 之内的随机向量比例约 $10^{-111}$**——**「宽」的锥其实极度挑剔。** 这正是为什么高余弦值得信任。
- **⭐ 「本课配方」值得直接抄下来：`最多 20 个，且全部 > 0.7`。** 它有**两个约束**，而裸 top-K 只有一个：

| 约束 | 作用 | 裸 top-K 有吗 |
|---|---|---|
| **上限（至多 20）** | 控成本、控延迟 | ✅ 有 |
| **下限（全部 > 0.7）** | **控无关内容** | ❌ **没有** |

- **⭐ 右栏那句是生产环境最常见的 bug 的精确描述**：**top-K 是一份「固定尺寸」的合同。** 如果语料里只有 3 份相关文档，**它照样还你 20 份**——**其余 17 份直接进上下文窗口。**
  - **`silently, politely`（无声地、礼貌地）才是关键**：**没有报错、没有告警、没有任何信号。** 这与 Prelude 那张 `NO ROADS` 航海图正好相反——**海图声明了自己的光圈，裸 top-K 从不声明。**
  - **它同时是「弃权（abstention）」问题**：**一个无法返回少于 K 个结果的系统，结构上就说不出「我没有」。**
  - **代价还要按 p.17 那条算**：多出来的无关项**不只是掺噪声，还在吃生成预算**（cross-encoder 前向、context token、注意力）。
- **⚠️ 必须配套记住的一条（否则会误用 0.7）**：**这个 0.7 不是普适常数。** 同一份讲义明确说过——***绝对相似度阈值在不同 embedder 之间不可移植：一个模型上的 0.7 和另一个模型上的 0.7 是不同的光圈。***
  - **可移植的是配方的「形状」（上限 + 下限），不是那个数字。**
  - **下限怎么定**：在**封存的 gold set** 上，看已知相关 / 已知不相关的分数分布，选一个你能接受其召回-精度取舍的位置；**逐 embedder、逐车道地定，并在换模型时重定。**


### 正课 p.21 · **ACT I · One embedding, many budgets：Matryoshka — dimensionality as a cost knob**

> 📌 **当时截图被弹窗遮挡，做过括号补全；后据完整 deck PDF 校正——四处补全全部有误，下面已换成原文**（原补全：`aperture` / `matches` / `polar cap` / `128 vs 1024 … rack`）。
> 📌 顺带记下：**PDF 页码指示器显示正课 deck 共 125 页。**

> **ACT I · ONE EMBEDDING, MANY BUDGETS**
> # **Matryoshka — dimensionality as a cost knob**
>
> $$\mathcal{L} \;=\; \sum_{k \in \{128,\,256,\,512,\,1024\}} \lambda_k \, \mathcal{L}_{\text{contrastive}}\big(e^{(k)}\big)$$
>
> Kusupati 2022: **train the loss at every nested prefix**, and the **first 128 dimensions become a usable coarse embedding** — **a scoop 8× cheaper than the full vector**, **rescored later at full width**.
>
> 右栏：*The compact vector is **a coarser net**: it **catches everything the full vector catches, plus some false positives** — **a giraffe may occasionally wander into the Arctic cap**. **At 100M chunks, 128 vs 4096 dims is one server versus a cluster.***
>
> **中文**：**第一幕 · 一个 embedding，多种预算**。**Matryoshka——把维度变成一个成本旋钮**。Kusupati 2022：**在每一个嵌套前缀上都施加损失**，于是**前 128 维本身就成了一个可用的粗粒度 embedding**——**一把比全宽向量便宜 8 倍的铲子**，**稍后再用全宽复评**。
> 右栏：*那个更紧凑的向量是**一张更粗的网**：**全宽向量能捞到的它都能捞到，外加一些假阳性**——**偶尔会有一只长颈鹿溜进北极冠**。**在一亿个 chunk 的规模上，128 维对 4096 维，是「一台服务器」对「一个集群」的差别。***

- **⭐ 公式在说什么**：**训练一个 embedding，但把对比损失同时施加在它的每一个嵌套前缀上**（128 / 256 / 512 / 1024），$\lambda_k$ 是各宽度的权重。
  **这就是为什么「前缀本身也是好 embedding」不是巧合，而是被训练出来的**——套娃的每一层都被单独要求过。
- **`dimensionality as a cost knob` 是这一页的重构**：**维度本来是一个固定的架构选择，MRL 把它变成了一个「运行时」旋钮**——**同一份索引，你可以按预算选择用多少维去铲。**
- **⭐ 长颈鹿那句是本页最关键的性质**：**更紧凑的向量 = 更粗的光圈**，而且是**超集**关系——
  - **全宽能捞到的，128 维都能捞到**（**不丢弹珠**）
  - **只是额外多进一些沙子**（长颈鹿溜进极冠）
  - **正因为是「只多不少」，铲—复评才是安全的**：**铲的阶段不损失召回，只增加噪声，而噪声由全宽复评清掉。**
- **⭐ 这一页用文字说的，正是 p.19 那条不等式的数值后果**（对照我在 p.19 记录里的补注）：

| 维度 | 偶然超过 0.5 的概率 | 一亿 chunk 上的期望误配数 |
|---|---|---|
| **1024** | $\approx 5\times10^{-56}$ | **实际为 0** |
| **128** | $\approx 2.3\times10^{-7}$ | **约 23 只「长颈鹿」** |

  **「a giraffe may occasionally wander into the polar cap」就是 $2e^{-d\varepsilon^2/2}$ 在 d=128 时的口语版。**

- **成本数字（按幻灯的 128 vs 4096 重算）**：一亿 chunk × **4096** 维 × 4 字节 ≈ **1.6 TB**；换成 **128** 维 ≈ **51 GB**。**32 倍差距 = 一台服务器 vs 一个集群**——幻灯的 *one server versus a cluster* 是准确的。
  - ⚠️ **幻灯自身有一处不自洽**：左栏说铲子「**便宜 8 倍**」（对应 128 vs 1024），右栏却说「**128 vs 4096**」（32 倍）。**两者不能同时成立。** 本课白板上写的是 **D = 4096**（见本节白板记录），所以**右栏更可信**；左栏的「8×」大概率沿用了 1024 维的旧算例。
- **⚠️ 必须配套的一条纪律（幻灯未写，讲义写了）——MRL–DCL 不变式**：
  > **在 Matryoshka 的求和内部、在每一个前缀宽度上，都施加「解耦」损失（DCL）**，这样 **128 维的铲子和全宽的复评是被同一套纪律训练出来的**；并且**在任何 embedder 更换之前，对这条不变式做回归测试**（在封存集上测「铲深处的召回」）。
  - **为什么必须测**：幻灯断言的「超集」性质**在实践中只是近似**。**一把悄悄腐烂的铲子，等于筛子还没看见就已经丢了六颗弹珠**——**而这种损失是静默的**（又一次：假阴性看不见）。


### 正课 p.23 · **ACT I · 2025–26 · THE OBJECTION FALLS：The late-interaction cost collapse**

> ⚠️ **p.22 未截到**——按位置推断是 **ColBERT / 后期交互本身的介绍页**（MaxSim、每 token 一个向量）。

> **ACT I · 2025–26 · THE OBJECTION FALLS**
> # **The late-interaction cost collapse**
>
> **ColBERTv2** — residual compression, **16–32× smaller**. **PLAID**, then **WARP** — **41× faster than XTR**. **MUVERA** — fixed-dimensional encodings make multi-vector search run on **ordinary ANN engines**.
>
> And **mxbai-edge-colbert**: **17M parameters** matching ColBERTv2.
>
> 右栏：*Within two years, late interaction went from a **luxury** to **a lane you must justify excluding**. **When a cost objection is the entire argument, re-audit the argument annually — costs are the fastest-moving part of this field.***
>
> **中文**：**第一幕 · 2025–26 · 反对意见倒下**。**后期交互的成本坍塌**。**ColBERTv2**——残差压缩，**体积缩小 16–32 倍**。**PLAID**，随后是 **WARP**——**比 XTR 快 41 倍**。**MUVERA**——固定维编码让多向量检索**跑在普通的 ANN 引擎上**。还有 **mxbai-edge-colbert**：**1700 万参数**即可匹敌 ColBERTv2。
> 右栏：*两年之内，后期交互**从一种奢侈品，变成了一条「你必须论证为什么要排除它」的车道**。**当一个反对意见的全部内容就是「太贵」时，请每年重审这条论证——成本是这个领域里变动最快的部分。***

- **⭐ 四项进展各自打掉账单的一个不同部分**，这个结构值得记住：

| 进展 | 打掉的是哪一项成本 |
|---|---|
| **ColBERTv2**（残差压缩） | **存储**——每 token 一个向量的体积，缩小 16–32 倍 |
| **PLAID → WARP** | **查询延迟**——比 XTR 快 41 倍 |
| **MUVERA**（固定维编码） | **基础设施**——把多向量检索归约成单向量 MIPS，**普通 ANN 引擎就能跑，不需要专用多向量设施** |
| **mxbai-edge-colbert** | **模型体积**——1700 万参数 |

  **「太贵」从来不是一个成本，是四个。四个各自被单独攻破。**

- **⭐ 全页最该记的一句是举证责任的反转**：***from a luxury to a lane you must justify **excluding**.***
  - **以前**：你要论证**为什么要加** ColBERT
  - **现在**：你要论证**为什么不加**
  - **这是「默认值」的迁移，不是「效果」的迁移。**
- **⚠️ 但要和 Playbook 一起读，否则会误用**：**成本不再是「排除的理由」，但它也不是「加入的理由」。** 讲义那句是——***现在决定 ColBERT 坐在哪里的是锦标赛（tournament），不是成本反对意见。*** **每一个索引仍然必须通过消融挣得自己的位置**；否则你只是把 Sacred Cow 换成了 Kitchen Sink。
- **与 p.14 的呼应**：p.14 说 **ColBERT「两者都保留，并为此向你收取存储费」**——**它没有逃出取舍，只是把损失换成了另一种货币**。**这一页说的是：那种货币的汇率崩了。** 取舍还在，只是价格变了。
- **⭐ 一条可以直接变成流程的方法论（右栏第二句）**：
  > **当一个反对意见的全部内容就是「太贵」时，每年重审它。成本是这个领域里变动最快的部分。**
  - **推论**：架构决策要**记录「拒绝的理由」，而且要按理由分类**——
    - 因**能力**拒绝（「它做不到 X」）→ 老化较慢
    - 因**成本**拒绝（「太贵/太慢/太占内存」）→ **老化最快，必须挂年度复审**
  - **落到本仓库**：`decisions/` 里的每条否决记录都应带一个 `rejected_because: capability | cost` 字段，**cost 类的自动进年度复审队列**。这和 Week 09 OKF 的 `stale_after` 是同一条设计直觉——**被治理的判断必须能回答「这是什么时候的快照」。**
- **分幕标题 `2025–26` 本身就在示范这条纪律**：**它给这个结论打了时间戳**，等于承认「这句话会过期」。


### 正课 p.26 · **POP QUIZ · ACT I：Quiz 1 — the cap that wasn't full**

> ⚠️ **p.24–25 未截到。**

> **POP QUIZ · ACT I**
> # **Quiz 1 — the cap that wasn't full**
>
> *Your dense lane is configured as a **bare top-20**. For one query, **exactly 6** chunks in the corpus lie inside the **0.7 cone (45° aperture)**.*
> ***(a)** How many of the 20 returned chunks came from the **equatorial band**?*
> ***(b)** What is the **best possible precision@20** here?*
> ***Then say back the house recipe that prevents this.***
>
> **中文**：**随堂测验 · 第一幕**。**测验一——那个没被装满的「冠」**。*你的 dense 车道配置成一个**裸的 top-20**。对某个查询，语料中**恰好有 6 个** chunk 落在 **0.7 的锥（45° 光圈）之内**。**(a)** 返回的 20 个 chunk 里，有多少来自**赤道带**？**(b)** 这里**最好可能的 precision@20** 是多少？**然后把能防住这件事的「本课配方」背出来。***

**答案：**

- **(a) 14 个。** 极冠里只有 6 个，而 top-20 承诺凑满 20 个 → **其余 14 个只能从赤道带里抓**。
  - **⭐ 关键在于「赤道带」这个词有多重**：按 p.19 的测度集中，**赤道带正是随机向量所在的地方**。所以这 14 个**不只是「相关性较低」——它们在几何上与随机文档没有区别**。**你把 14 份噪声礼貌地送进了上下文窗口。**
- **(b) 0.30（6/20）。** 「最好可能」是因为**语料里总共只存在 6 个相关项**——**哪怕排序完美无缺，20 个格子里也最多只能有 6 个是对的**。**上限由语料决定，不由模型决定。**
- **配方**：***"up to 20, all above 0.7"***（**最多 20 个，且全部高于 0.7**）。
  - 加上下限之后：**返回 6 个，precision 从 0.30 变成 1.00**，同时**省下 14 个 context 槽位与 14 次 cross-encoder 前向**。

**标题是一个双关**：**`cap`** 既是 **p.19/p.21 的「极冠（polar cap）」**——它只装了 6 个、**没被装满**；也是 **top-K 的那个「上限（cap）」**——**它偏要装满**。**病根就在这两个 cap 的错配：上限是固定的，而相关项的数量不是。**

**这道题把 Act I 的三页缝在了一起**：

| 页 | 提供了什么 |
|---|---|
| **p.19** 许可证 | **赤道带 = 随机向量所在处**——所以那 14 个是噪声，不是「弱相关」 |
| **p.20** 纪律 | **裸 top-K 只有上限没有下限**；配方是「至多 20 且全部 > 0.7」 |
| **p.17** 级联的经济学 | 那 14 个**不只是掺噪声，还在吃生成预算** |


### 正课 p.27 · **POP QUIZ · ACT I · ANSWER：Fourteen strangers in the context window**

> **POP QUIZ · ACT I · ANSWER**
> # **Fourteen strangers in the context window**
>
> **(a)** $20 - 6 = \mathbf{14}$ — **chunks the geometry never endorsed, promoted because the contract said "return twenty."**
>
> **(b)** $6/20 = \mathbf{0.30}$ — **a ceiling no retriever can beat, because only six relevant chunks exist.**
>
> 右栏：*The recipe: **"up to 20, all above 0.7."** A top-K without a threshold is **a promise to fill the bucket with sand whenever the marbles run out** — and **the generator downstream cannot tell sand from marble**.*
>
> **中文**：**答案 · 上下文窗口里的十四个陌生人**。**(a)** 20 − 6 = **14**——**几何从未背书过的 chunk，仅仅因为合同写着「还我二十个」而被提拔上来。** **(b)** 6/20 = **0.30**——**一个任何检索器都打不破的天花板，因为相关的 chunk 总共就只有六个。**
> 右栏：*配方：**「最多 20 个，且全部高于 0.7」**。**一个没有阈值的 top-K，是一句承诺：弹珠一旦用完，就拿沙子把桶填满**——**而下游的生成器分不出沙子和弹珠。***

- **两个答案与推导均与课前预判一致**（14 / 0.30 / 配方），但幻灯的**措辞**补了三处关键的东西：
- **⭐ (a) `the geometry never endorsed` / `promoted because the contract said "return twenty"`**
  - **「几何从未背书」**——那 14 个不是「弱相关」，是**测度集中意义上的随机邻居**（p.19 的赤道带）。
  - **「合同」= top-K 的固定尺寸承诺**；**「提拔（promoted）」**这个动词很准：**它们不是被选出来的，是被制度性地晋升上来的**——**因为有空位，不是因为有资格。**
- **⭐ (b) 出现了今天的第二个「天花板」，与 p.6 构成对称**：

| | 天花板是什么 | 谁定的 | 下游能不能救 |
|---|---|---|---|
| **召回天花板**（p.6） | 铲子捞上来的召回 | **第一阶段** | **不能** |
| **精度天花板**（本页） | 语料里相关项的数量 | **语料本身** | **不能** |

  **两者都不是模型问题，都是「在你调任何参数之前就已经确定」的上界。** 而且都无法靠 reranker、prompt、更大的模型抬高。

- **⭐ 右栏那句是全页最狠的，而且它把 p.6 的隐喻拿回来用在了精度上**：
  - **「弹珠用完就拿沙子填桶」**——p.6 的桶与筛子本来讲的是**召回**；这里同一套器物被用来讲**精度**。**同一个沙坑，两种失败。**
  - **⭐ `the generator downstream cannot tell sand from marble` 才是「为什么这要紧」的答案**：**检索器知道分数，生成器不知道。** 上下文窗口一旦拼好，**那 14 个陌生人和 6 个真材料长得完全一样**——**余弦 0.2 这条信息在交接的那一刻就被丢掉了。**
  - **推论**：要么**在检索阶段就用阈值挡住**（本课的配方），要么**把分数/置信度一起传给生成器让它自己权衡**——**而本课选前者**，因为后者不可靠。这也正是机房那条「**给检索到的证据打聚光灯（spotlight）**」和「**出口处必须校准**」的同一条动机。


### 正课 p.28 · **MILESTONE · ACT II OF VII：The Trained Instrument**（分幕卡）

> **MILESTONE · ACT II OF VII**
> # **The Trained Instrument**
>
> *The embedder is **not a commodity**. It is **a scientific instrument** — and **it must be calibrated to your domain**.*
>
> **中文**：**里程碑 · 第二幕（共七幕）**。**被训练的仪器**。*embedder **不是一种大宗商品**。它是**一台科学仪器**——**而且必须针对你的领域做校准**。*
>
> 配图：同心圆弧 + 一个发光的点——**一台仪器的刻度盘 / 声呐扇面**。

- **⭐ 重要结构信息：`ACT II OF VII`——正课 deck 分成七幕，而讲义只有三幕。** 也就是说 **deck 把讲义的小节展开成了独立的幕**：

| deck 分幕 | 对应讲义位置 |
|---|---|
| **Act I · The Cabinet Opens**（p.14–27） | 讲义 Act I 前半：**表征组合**（BM25 / SPLADE / dense / MRL / ColBERT / 测度集中 / 光圈） |
| **Act II · The Trained Instrument**（p.28–） | 讲义 Act I 后半：**DCL、负例课程表、MRL–DCL 不变式** |
| **剩余五幕（推测）** | 第二语料库与派生物 · 长上下文幻象 · 法庭（融合/去重/重排） · 问题侧与机房 · Playbook |

- **`not a commodity … a scientific instrument`** —— 呼应讲义那句：***embedder 不是玻璃，是镜子；而镜子是为某个目的打磨的。*** **「大宗商品」的意思是「随便下载一个就行」——这一幕就是要拆掉这个假设。**

---

### 正课 p.29 · **ACT II · The sorting machine and the scale：Two forces, one geometry**

> **ACT II · THE SORTING MACHINE AND THE SCALE**
> # **Two forces, one geometry**
>
> Every contrastive loss is **the same physics**: an **attractive force** pulling positives together, a **repulsive force** pushing negatives apart. **The embedding space your database searches at midnight is the cooled, frozen residue of that argument.**
>
> **The pipeline is only as good as the vectors that enter it.**
>
> 右栏：*A generic **MTEB download** was trained on **someone else's argument, on someone else's data**. **Fine-tuning re-opens the argument on your terms** — and **everything downstream inherits the improvement for free**.*
>
> **中文**：**第二幕 · 分拣机与天平**。**两种力，一个几何**。每一个对比损失都是**同一套物理**：一种**吸引力**把正例拉到一起，一种**排斥力**把负例推开。**你的数据库在半夜里检索的那个 embedding 空间，就是那场角力冷却凝固之后的残留物。** **整条流水线的上限，就是进入它的那些向量。**
> 右栏：*一个通用的 **MTEB 下载模型**，是在**别人的争论、别人的数据**上训练出来的。**微调等于在你自己的条件下重开这场争论**——**而下游的一切都免费继承这份改进。***

- **两种力就是 Week 02 讲过的 alignment / uniformity**：**吸引力**把 query 拉向正例，**排斥力**把其余一切铺开在球面上，好让任何区域都不拥挤。**只有吸引力而没有排斥力，空间就会各向异性**——**什么都像什么**。
- **⭐ 全页最好的一句：*the cooled, frozen residue of that argument*（那场角力冷却凝固后的残留物）。**
  - **训练结束的那一刻，几何就冻住了。** 你此后每一次检索，都是在**向一块化石提问**。
  - **推论：查询时无法修复训练时的错误。** 这构成今天的**第三个天花板**——

| 天花板 | 由谁在什么时候决定 | 下游能救吗 |
|---|---|---|
| **召回天花板**（p.6） | **第一阶段的铲子** | ❌ |
| **精度天花板**（p.27） | **语料里相关项的数量** | ❌ |
| **⭐ 几何天花板**（本页） | **训练时那场角力** | ❌ |

  **三者的共同点：上界在你调任何参数之前就已经确定了。**

- **⭐ 右栏是 bm42 教训的推广**：**「别人的争论、别人的数据」**——**一个通用 embedding 模型的几何，是照着别人的查询分布打磨的镜子。**
- **⭐ 而 Week 02 的实验就是这句话的数值证明**：

| 模型 | `gap = intra − inter` |
|---|---|
| Raw BERT | 0.107 |
| MiniLM（通用句向量） | 0.179 |
| **领域微调后** | **1.072** |

  **「在你自己的条件下重开这场争论」= gap 从 0.179 涨到 1.072，六倍。**

- **`everything downstream inherits the improvement for free`** —— **因为 embedder 坐在级联的最前面**：改进它，**每一条车道、每一级、每一次查询都受益**。**这就是微调 embedder 的杠杆率论证。**
- **⚠️ 必须配套的纪律（讲义有，幻灯这页还没给）——48 小时教条与「什么时候拒绝微调」**：
  > 用**从你自己语料制造的合成对** + **负例课程表** + **DCL**，领域微调是**一件两天的活**；
  > **而当语料是通用的、领域很小、或者「用来证明这次更换诚实的标尺还不存在」时，你拒绝做它。**
  - **最后一条最要紧**：**先有标尺，再谈微调。** 否则你无法证明换上去的模型真的更好——**只能证明它不一样。**


### 正课 p.30 · **ACT II · The default loss, and its flaw：InfoNCE — the line-up tournament**

> **ACT II · THE DEFAULT LOSS, AND ITS FLAW**
> # **InfoNCE — the line-up tournament**
>
> $$\mathcal{L}_{\text{InfoNCE}} \;=\; -\log \frac{e^{\,u^\top v_+/\tau}}{e^{\,u^\top v_+/\tau} \;+\; \sum_{j\neq+} e^{\,u^\top v_j/\tau}}$$
>
> **The field's default.** Differentiate it and **the attraction on the positive is $(1-P_+)/\tau$** — **throttled by the model's own confidence**. Late in training, when positives are easy, $P_+ \to 1$ and **the learning signal chokes**.
>
> 右栏：*The positive **sits in its own denominator**: **attraction and repulsion are wired in series when they ought to run in parallel**. **Easy positives gag the gradient exactly when hard negatives still need pushing.***
>
> **中文**：**第二幕 · 默认的损失，以及它的缺陷**。**InfoNCE——列队指认锦标赛**。**这是这个领域的默认选择。** 对它求导，**正例上的吸引力是 $(1-P_+)/\tau$**——**被模型自己的置信度扼住**。训练后期，当正例已经很容易时，$P_+ \to 1$，**学习信号就噎住了**。
> 右栏：*正例**坐在它自己的分母里**：**吸引与排斥被串联了，而它们本该并联。** **容易的正例恰恰在难负例还需要被推开的时候，把梯度捂住了嘴。***

- **⭐ 幻灯把分母拆开写成 $e^{s_+/\tau} + \sum_{j\neq+}$，是刻意的——它让缺陷「肉眼可见」**：**正例既是被评的对象，又是评分标准的一部分。**
- **⭐ 梯度的精确形式（这是全页的技术核心）**。记 $s_j=u^\top v_j$、$P_j = e^{s_j/\tau}/Z$：

$$\frac{\partial \mathcal{L}}{\partial s_+} = -\frac{1-P_+}{\tau}\quad(\text{吸引}) \qquad\qquad \frac{\partial \mathcal{L}}{\partial s_j} = +\frac{P_j}{\tau}\quad(\text{排斥}, j\neq+)$$

  - **$P_+ \to 1$ 时，吸引力 $\to 0$** —— 幻灯左栏说的就是这个。
  - **⭐ 但更狠的是右栏那句「串联」**：$P_+ \to 1$ 意味着**所有 $P_j \to 0$**，于是**作用在难负例上的排斥力也一起归零**。
  - **也就是说：模型一旦对正例有信心，它就同时停止了「把难负例推开」这件事**——***easy positives gag the gradient exactly when hard negatives still need pushing***。**这才是「串联」的准确含义：两股力共用同一个 softmax 归一化，一个熄火，另一个跟着熄火。**
- **「串联 / 并联」是电路比喻**：**串联时，一处的电流限制了另一处；并联时两者独立。** **DCL 要做的就是把它们改成并联。**
- **DCL 的修法与它为什么有效（下一页大概率讲）**：把正例逐出分母 ⇒
  $$\mathcal{L}_{\text{DCL}} = -\frac{s_+}{\tau} + \log\sum_{j\neq+} e^{\,s_j/\tau}$$
  - **吸引项的梯度变成常数 $-1/\tau$**——**不再被置信度扼住**；
  - **排斥项只在负例之间归一化**——**不会因为正例太自信而集体归零**。
  - **两股力就此解耦（decoupled），这就是 DCL 名字的由来。**
- **顺带解释了讲义那句「小 batch 不再是一种税」**：batch 越小，分母里的负例越少，**正例在 $Z$ 里的占比就越大 → $P_+$ 越大 → 梯度越早噎住**。**把正例踢出分母，这个惩罚就消失了。**
- **与今天其他部分的连线**：
  - **InfoNCE = softmax（以 $\tau$ 为温度）+ one-hot 交叉熵**——**正是实验四那道综合之问的「四件戏服」**。**上午用手拼出的指数族，这一页变成了损失函数的骨架，而 DCL 改的正是那个配分函数 $Z$。**
  - **Week 02** 已经给过 InfoNCE 的公式与「温度控制对相似度差异的敏感度」；**今天补上的是它的缺陷与修法。**


### 🖊 现场白板（Excalidraw）· 配合 p.21 / p.30：softmax 的实算演示

> 白板上同时出现三块内容（讲师手写，部分字迹不确定，标 `?`）：

**① 上方一条轴：`1 ——[红色涂满的一小段]—— D`，`D` 旁标 `4k`**
- **这是 Matryoshka 的图示**：**全宽 D = 4096 维**，**红色那一小段是前缀**（铲子实际用的那几百维）。
- 右上另有 `y₁ … yₙ` 与 `D` ——各前缀宽度的输出。

**② 中间手写目标函数**（字迹部分不清）：
$$\arg\min_{\Theta}\Big(\;\mathcal{L}_{\text{cont}}^{(D)} \;+\; \lambda\,\mathcal{L}^{(2^d)} \;+\; \cdots\Big)$$
- 即 **MRL 目标的手写版**：**全宽 D 上的对比损失，加上各个 $2^d$ 前缀宽度上的损失**（128/256/512/1024… 都是 2 的幂），对参数 $\Theta$ 取最小。**与幻灯 p.21 的公式一致。**

**③ 下方：softmax 的实算演示（本次白板的重点）**

> `(−∞, ∞) ⟶ [0, 1]`
>
> | 候选 | A | B | C | D | E |
> |---|---|---|---|---|---|
> | **logit** | **43** | **25** | **−10** | **−45** | **−1000** |
> | **exp** | $e^{43}$ | $e^{25}$ | $e^{-10}$ | $e^{-45}$ | $e^{-1000}$ |

- **⭐ 这组数字当场把 p.30 的毛病算了出来**。约掉 $e^{43}$：

$$P_A = \frac{1}{1 + e^{-18} + e^{-53} + e^{-88} + e^{-1043}} \approx 1 - 1.5\times10^{-8}$$

  **也就是 $P_+ \approx 0.999999985$，于是 $1-P_+ \approx 1.5\times10^{-8}$。**
  **InfoNCE 在正例上的梯度是 $(1-P_+)/\tau$ ——它现在等于一亿分之一点五。学习信号实际上已经死了。** 这就是 p.30 说的 ***the learning signal chokes*** 的数值版本。

- **⭐ 副产品一：为什么必须减最大值。** $e^{43}\approx4.7\times10^{18}$ 还撑得住，但 logit 一旦到 100，$e^{100}\approx2.7\times10^{43}$ **就超出 float32 上限（约 $3.4\times10^{38}$）**。**减掉最大值后**指数变成 `0, −18, −53, −88, −1043`，**永不上溢**——这就是 Week 02 讲的数值稳定 softmax。
- **⭐ 副产品二：`e^{−1000}` 在数值上等于「不存在」。** float64 最小正规数约 $2.2\times10^{-308}$，而 $e^{-1000}\approx10^{-435}$ → **直接下溢成 0**。**分数低到 −1000 的候选，对分母毫无贡献，也拿不到任何梯度。**
- **⭐ 副产品三：温度会放大这一切。** 若 $\tau=0.05$，所有 logit 先乘 20 → **43 与 25 的差距从 18 变成 360** → $e^{-360}$ 直接归零。**温度越低，「赢家通吃」越极端，梯度噎住得越早。**
- **`43 → 25` 的差距只有 18，但概率之比是 $e^{18}\approx6.6\times10^{7}$（六千六百万倍）** —— **指数函数的残忍：logit 上的小差距 = 概率上的天壤之别。**


### 正课 p.31 · **ACT II · THE HOUSE SURGERY：DCL — the positive leaves the denominator**

> **ACT II · THE HOUSE SURGERY**
> # **DCL — the positive leaves the denominator**
>
> $$\mathcal{L}_{\text{DCL}} \;=\; -\,\frac{u^\top v_+}{\tau} \;+\; \log \sum_{j\neq+} e^{\,u^\top v_j/\tau}$$
>
> **Yeh et al. 2022: evict the positive term — nothing else.** Attraction becomes a **constant $1/\tau$ that cannot be throttled**; **repulsion still self-paces over the negatives.**
>
> **Freedom from the batch-size tax.**
>
> 右栏：***Honesty**: the big public embedder recipes **still ship InfoNCE variants** — **at batch 8,192 the coupling barely binds**. **We fine-tune at batch 32 on rented GPUs.** **DCL is the small-batch house choice, not a universal law.***
>
> **中文**：**第二幕 · 本院手术**。**DCL——正例离开分母**。**Yeh et al. 2022：把正例那一项逐出去——除此之外什么都不改。** 吸引力变成**一个不会被扼住的常数 $1/\tau$**；**排斥力仍然在负例之间自我调节。** **从此摆脱 batch 尺寸税。**
> 右栏：***说句实话**：大厂公开的 embedder 配方**仍然在用 InfoNCE 的各种变体**——**在 batch 8,192 的规模上，那个耦合几乎不起作用**。**而我们是在租来的 GPU 上用 batch 32 做微调。** **DCL 是「小 batch 情形下」本课的选择，不是一条普适定律。***

- **⭐ `evict the positive term — nothing else`（只改这一处）** —— DCL 的全部内容就是**从分母里删掉一项**。**没有新超参、没有新模块、没有新数据。** 这也是为什么它值得当默认。
- **⭐ 手术前后，两股力各自变成什么**：

| | InfoNCE | **DCL** |
|---|---|---|
| **吸引（拉正例）** | $(1-P_+)/\tau$ ——**被模型自己的信心扼住** | **常数 $1/\tau$ —— 扼不住** |
| **排斥（推负例）** | $P_j/\tau$，**在含正例的池子里归一化** → 正例一自信，**全体归零** | $P'_j/\tau$，**只在负例之间归一化** → **最像的那个照样被重点推开** |
| **接线方式** | **串联** | **并联** |

  **注意保留下来的那份自适应性**：***repulsion still self-paces over the negatives*** —— **难负例仍然拿到更大的推力**，这是好的自适应；被去掉的只是**有害的那一种**（正例一自信就全体熄火）。

- **⭐⭐ 右栏的「诚实声明」是全页最该记住的东西**，它给这条建议标注了**适用范围**：
  - **大厂配方仍用 InfoNCE 变体，因为在 batch 8,192 上「那个耦合几乎不起作用」。**
  - **为什么大 batch 能掩盖这个毛病**：$P_+ \approx 1/\big(1+\sum_j e^{(s_j-s_+)/\tau}\big)$。**负例越多，分母里的项越多，$P_+$ 就越难爬到 1。** batch 8,192 时永远有足够多的负例把 $P_+$ 压住，**梯度就不会噎住**；batch 32 时只有 31 个负例，**$P_+$ 很快逼近 1**。
  - **⭐ 于是一句话：DCL 是穷人的大 batch。** 大 batch 靠**显存**解决这个问题，DCL 靠**改公式**解决同一个问题——**而显存要花钱，改公式不要。**
  - **`not a universal law`** —— **本课明确给自己的 house choice 标了适用条件。** 这和 bm42 那条「把发布公告当作要复现的论文来读」是同一种诚实：**给建议标注边界，比宣称普适可信得多。**
- **可直接使用的判据**：

| 你的 batch 能开到 | 用什么 |
|---|---|
| **几十（租 GPU / 单卡微调）** | **DCL** |
| **几千（有大显存集群）** | InfoNCE 变体也可以 |

  **判据是 batch size，不是「哪个更先进」。**

- **分幕小标题 `THE HOUSE SURGERY`（本院手术）** —— 与 house loss / house recipe / house sparse lane 同一系列：**本课在明确交付一套「默认值」，并逐一说明它们的理由与边界。**


### 正课 p.32 · **ACT II · WHAT DOES MOST OF THE REAL WORK：The hard-negative curriculum**

> **ACT II · WHAT DOES MOST OF THE REAL WORK**
> # **The hard-negative curriculum**
>
> The house ordering, **easy to hard**: **random** negatives → **BM25-mined** lexical look-alikes → **in-batch** negatives (**free with the loss**) → **model-mined hard** negatives from **your own retriever's near-misses**.
>
> 右栏：***A mediocre loss with brilliant negatives beats a brilliant loss fed easy ones.*** The machine, like a student, **learns most from the contrasts that sting** — **easy negatives are pushing on doors that are already shut**.
>
> **中文**：**第二幕 · 真正干活最多的是什么**。**难负例课程表**。本课的排序，**由易到难**：**随机负例** → **BM25 挖出来的词面近似** → **同批次内负例**（**随损失免费附赠**）→ **模型挖出来的难负例**，取自**你自己 retriever 的「差一点就对」**。
> 右栏：***一个平庸的损失配上出色的负例，胜过一个出色的损失配上简单的负例。*** 机器和学生一样，**从「刺痛的对比」里学到最多**——**简单负例是在推一扇早就关上的门。**

- **⭐ 分幕小标题本身就是结论**：***WHAT DOES MOST OF THE REAL WORK***（真正干活最多的是什么）——**答案是负例，不是损失函数。** 讲完 DCL 那套精巧的手术之后，这一页立刻说：**数据比公式重要。**
- **⭐ 与前两页的关系：三页在解同一个问题（梯度噎住），但从两个方向下手**：

| 页 | 角色 | 动的是 | 比喻 |
|---|---|---|---|
| **p.30 InfoNCE** | **诊断** | —— | **题太简单，学生不学了** |
| **p.31 DCL** | **修法 A** | **改公式** | **改评分规则** |
| **p.32 课程表** | **修法 B** | **改数据** | **出更难的题** |

  **两条路可以、也应该同时用。** 而这一页明确表态：**如果只能选一样，选负例。**

- **四级课程表逐条**：

| 级 | 负例来源 | 成本 | 为什么更难 |
|---|---|---|---|
| **1 随机** | 语料里随便抓 | 极低 | 几乎全是「一眼就不对」 |
| **2 BM25 挖** | 用 BM25 搜 query，取词面像但不对的 | 低 | **词面相似**，逼模型看意思 |
| **3 in-batch** | **同一 batch 里别人的正例** | **免费**（本来就在显存里） | 数量随 batch 涨 |
| **4 模型挖的难负例** | **用你当前的 retriever 去搜，取排名高但其实不对的**（near-miss） | 高（要跑一遍检索） | **专挑模型现在的弱点** |

- **⭐ `easy negatives are pushing on doors that are already shut` 与 p.30 的梯度分析严丝合缝**：**简单负例的 $P_j$ 已经接近 0，排斥梯度 $P_j/\tau$ 也就接近 0——推它没有任何效果。** 只有**分数排在正例附近**的负例才拿得到可观的梯度。**「刺痛」在数学上就是「$P_j$ 不小」。**
- **用法要点**：
  1. **按顺序上，不要一开始就喂第 4 级。** 模型还没学会基本区分时，最难的负例只会淹没它——**而且更容易踩假负例陷阱。**
  2. **第 4 级是自举循环**：用当前模型挖负例 → 训一轮 → 用新模型再挖 → 再训。**模型越强，它的 near-miss 越难，课程自动加码。**
  3. **⚠️ 第 4 级也最危险**：**挖得太狠，「负例」其实是未标注的正例**——**损失会因为模型答对而惩罚它**。对策（下一页大概率讲）：**positive-aware mining**（丢掉分数离正例太近的候选）+ **cross-encoder 当去噪法官**。


### 正课 p.34 · **ACT II · THE INVARIANT THAT GUARDS THE SCOOP：The MRL–DCL invariant**

> ⚠️ **p.33 未截到**——按讲义顺序，大概率是**假负例陷阱**（positive-aware mining + cross-encoder 去噪法官），即我在 p.32 记录里预告的那一页。

> **ACT II · THE INVARIANT THAT GUARDS THE SCOOP**
> # **The MRL–DCL invariant**
>
> **House rule: the DCL loss is applied *inside the Matryoshka summation, at every prefix length* — 128, 256, 512, 1024.**
>
> **Fine-tune at full width only, and the full-dim metrics *improve* while the 128-d prefix quietly *degeometrizes*.**
>
> 右栏：*This is **silent scoop rot**: **the cheap scoop that feeds your whole cascade rots while every dashboard you watch turns greener**. **Regression-test recall@500 at 128 dimensions on every fine-tune. No exceptions.***
>
> **中文**：**第二幕 · 守卫铲子的那条不变式**。**MRL–DCL 不变式**。**本课规则：DCL 损失要施加在 *Matryoshka 求和的内部、每一个前缀长度上*——128、256、512、1024。** **只在全宽上做微调，你会看到全维指标*变好*，而 128 维前缀在悄悄地*失去几何*。**
> 右栏：*这就是**铲子的静默腐烂**：**供养你整条级联的那把便宜铲子正在烂掉，而你盯着的每一块仪表盘都在变绿。** **每一次微调，都要在 128 维上回归测试 recall@500。没有例外。***

- **⭐ 规则本身**：不是「训 MRL」和「用 DCL」两件事各做各的，而是**把 DCL 嵌进 Matryoshka 的求和里，逐个宽度施加**。**铲子和复评必须被同一套纪律训练出来。**
- **⭐ 失效机制（为什么只在全宽微调会毁掉铲子）**：**套娃性质不是模型的固有属性，是被损失函数强制出来的。**
  - 只在全宽算损失 → **梯度只约束整个 1024 维向量整体表现好**
  - **没有任何东西要求「前 128 维单独拿出来也要好」**
  - 于是优化器会**自由地把信息重新摊到所有维度上**（那样更容易优化）
  - **结果：前缀不再是可用的粗粒度 embedding —— 它「失去了几何（degeometrizes）」**
  - **一句话：撤掉那个强制，套娃就散了。**
- **⭐⭐ `silent scoop rot` 为什么是「静默」的——三重静默叠加**：
  1. **你看的仪表盘是全维指标 → 变绿**
  2. **你生产上线的路径是 128 维铲子 → 在烂**
  3. **而召回的失效本来就不留痕迹**——铲子漏掉的弹珠，**筛子从来没见过，所以下游不会报任何错**
  - 讲义那句配套的：***一把悄悄腐烂的铲子，等于筛子还没看见就已经丢掉六颗弹珠。***
  - **⭐ 可迁移的一般原则：测量你实际上线的那条路径，不是最方便测的那条。** 仪表盘与服务路径不一致，是一整类 bug 的模板。
- **⭐ 处方给得异常具体，逐项都有理由**：

| 处方 | 为什么是这个 |
|---|---|
| **recall**，不是 precision/nDCG | 铲子阶段**召回是神圣的**，且**召回的错误不可逆** |
| **@500**，不是 @10 | **要在铲子实际工作的深度上测**。top-10 可能还好好的，而**尾部（融合与重排要用的那一段）已经烂了** |
| **at 128 dimensions**，不是全宽 | **测你真正服务的那条路径** |
| **every fine-tune** | 这是**门禁**，不是偶尔抽查 |
| **No exceptions** | 全篇少见的措辞 —— 讲义在这里不留余地 |

- **收口**：这条不变式我在 p.21（Matryoshka）与 p.29（两种力）的记录里都标注过「讲义有、幻灯尚未给」——**到这一页幻灯给了，而且比讲义更具体**（讲义只说「在封存集上测铲深处的召回」，幻灯直接给出 **recall@500 @ 128d**）。


### 正课 p.35 · **ACT II · THE ECONOMICS OF CALIBRATION：The 48-hour doctrine**

> **ACT II · THE ECONOMICS OF CALIBRATION**
> # **The 48-hour doctrine**
>
> A domain fine-tune of a strong open embedder — **curriculum, DCL, MRL-aware** — is **about two days of work on modest GPUs**, and it is **among the highest-leverage components in the whole architecture**.
>
> **When *not* to fine-tune: small corpus, generic domain, no eval set to gate the swap.**
>
> 右栏：***Never swap embedders without the yardstick** — an embedder upgrade is an **index migration (Act VI)**, and **an unmeasured migration is a leap of faith with your recall ceiling in hand**.*
>
> **中文**：**第二幕 · 校准的经济学**。**48 小时教条**。对一个强开源 embedder 做领域微调（**课程表、DCL、套娃感知**）**大约是两天的活，用中等配置 GPU 即可**，而且它是**整个架构里杠杆率最高的组件之一**。**什么时候*不该*微调：语料小、领域通用、没有 eval set 来给这次更换把关。**
> 右栏：***绝不要在没有标尺的情况下换 embedder**——换 embedder 是一次**索引迁移（第六幕）**，而**一次没被测量的迁移，等于攥着你的召回天花板往下跳。***

- **这一页回答的是「那到底该不该做」**——前面几页教了怎么做（DCL / 课程表 / 不变式），这一页给决策。
- **`no eval set to gate the swap` 里的 `gate`（门禁）是关键词**：**eval set 不是用来「看看效果」的，是用来决定「准不准换」的闸门。**
- **⭐ 右栏三重风险**：换 embedder ①**是一次完整的索引迁移工程**（所有向量重算、索引重建）；②**它动的是不可逆的那个上限（召回天花板）**；③**失败是静默的**。**这三条叠加，使它成为所有改动里风险最高的一种。**
- **结构信息**：右栏点名**索引迁移在第六幕**——七幕结构里，**Act VI ≈ 机房 / 运维**。

---

### 正课 p.36 · **POP QUIZ · ACT II：Quiz 2 — the throttled spring**

> **POP QUIZ · ACT II**
> # **Quiz 2 — the throttled spring**
>
> *Late in a fine-tune, a typical positive pair scores **$P_+ = 0.98$** under InfoNCE, with **$\tau = 0.05$**.*
> ***(a)** Compute the InfoNCE attraction magnitude $(1-P_+)/\tau$ and the DCL attraction $1/\tau$.*
> ***(b)** By what factor is InfoNCE's pull throttled?*
> ***Then say back, in one sentence, what "decoupled" decouples.***
>
> **中文**：**测验二——被扼住的弹簧**。*微调后期，一个典型的正例对在 InfoNCE 下得分 $P_+ = 0.98$，$\tau = 0.05$。**(a)** 计算 InfoNCE 的吸引力大小 $(1-P_+)/\tau$ 与 DCL 的吸引力 $1/\tau$。**(b)** InfoNCE 的拉力被扼住了多少倍？**然后用一句话说回来：「解耦」到底解开了什么？***

**答案：**

- **(a)**
  - **InfoNCE**：$(1-0.98)/0.05 = 0.02/0.05 = \mathbf{0.4}$
  - **DCL**：$1/0.05 = \mathbf{20}$
- **(b)** $20 / 0.4 = \mathbf{50}$ 倍。**等价地就是 $\dfrac{1}{1-P_+} = \dfrac{1}{0.02} = 50$。**
  - **⭐ 注意：节流倍数 $=1/(1-P_+)$，与温度 $\tau$ 无关**——$\tau$ 同时放大两者，约掉了。**扼住拉力的完全是模型自己的信心。**
  - **⭐ 这道题就是讲义里那句「在 monograph 的算例里弱五十倍」的原始算例。**（我在笔记开头曾把这处出处从「讲义」更正为「monograph」，这里得到印证。）
- **(c) 一句话**：**「解耦」解开的是「正例的吸引力」与「正负例共用的那个分母」之间的耦合——从此吸引力恒为 $1/\tau$，不再被模型对正例的信心扼住。**
  - 更口语的一句：**它把「还要学多少」和「已经学得多好」解耦了。**


### 正课 p.38 · **POP QUIZ · ACT II：Quiz 3 — the silent scoop rot**

> ⚠️ **p.37 未截到。**

> **POP QUIZ · ACT II**
> # **Quiz 3 — the silent scoop rot**
>
> *After a **full-width-only fine-tune**, full-dim **NDCG@10 rises 0.71 → 0.76**. Your nightly job also reports **recall@500 at 128 dimensions: 0.97 → 0.81**. A query has **40 relevant chunks**.*
> ***(a)** How many marbles does the 128-d scoop now miss, on average?*
> ***(b)** Can the full-dim rescore recover them?*
> ***Name the invariant that was violated.***
>
> **中文**：**测验三——铲子的静默腐烂**。*在一次**只在全宽做的微调**之后，全维 **NDCG@10 从 0.71 升到 0.76**。你的夜间任务同时报告 **128 维上的 recall@500：0.97 → 0.81**。某个查询有 **40 个相关 chunk**。**(a)** 现在这把 128 维的铲子平均漏掉多少颗弹珠？**(b)** 全宽复评能把它们捞回来吗？**说出被违反的那条不变式。***

**答案：**

- **(a)**
  - **微调后漏掉**：$40 \times (1-0.81) = \mathbf{7.6}$ 颗
  - **相比微调前多漏**：$40 \times (0.97-0.81) = 40\times0.16 = \mathbf{6.4}$ 颗
  - **⭐ 这道题的数字是被反推设计过的**：**6.4 ≈ 六颗**，正是讲义那句原话——***a silently rotting scoop is six marbles gone before the sieve ever sees them***（一把悄悄腐烂的铲子，等于筛子还没看见就已经丢掉六颗弹珠）。
- **(b) 不能。**
  - **全宽复评只对「铲子交上来的候选」打分。没被铲上来的，复评从来没见过它。**
  - **这就是召回天花板：第一阶段漏掉的，任何后续阶段都无法恢复。**
- **(c) 被违反的是 MRL–DCL 不变式** —— **DCL 损失必须施加在 Matryoshka 求和的内部、每一个前缀宽度上（128/256/512/1024）**。只在全宽微调 → 前缀失去几何 → 铲子腐烂。

**⭐ 这道题真正的教学点在两个指标的错位：**

| 指标 | 变化 | 它测的是什么 | 结论 |
|---|---|---|---|
| **全维 NDCG@10** | **0.71 → 0.76**（+0.05） | **在「已经捞上来的东西」里排得好不好** | ✅ 仪表盘变绿 |
| **128 维 recall@500** | **0.97 → 0.81**（−0.16） | **到底能捞上来多少** | ❌ 天花板塌了 |

- **NDCG@10 在结构上测不到漏掉的那 6.4 颗** —— **它只在幸存者里排序。**
- **净效果几乎肯定是负的**：**上限掉了 16%，而你只是在剩下的东西里排得好了 5%。**
- **一句话：你把排序提高了 5%，把能排的东西减少了 16%。**


### 正课 p.40 · **MILESTONE · ACT III OF VII：The Derivative Corpus**（分幕卡）

> ⚠️ **p.37、p.39 未截到**（p.39 大概率是 Quiz 3 的答案页）。

> **MILESTONE · ACT III OF VII**
> # **The Derivative Corpus**
>
> ***Do not wait for the query to match your documents. Manufacture documents that match your queries.***
>
> **中文**：**里程碑 · 第三幕（共七幕）**。**派生语料库**。***不要等着 query 来匹配你的文档。去制造匹配你 query 的文档。***
>
> 配图：**顶部一个高亮（珊瑚红）的盒子，向下辐射出十几条细线，连到十几个更小的盒子**——**一个源，许多派生物。**

- **⭐ Act II（被训练的仪器）结束，Act III 开始。七幕结构目前已知**：

| deck 分幕 | 内容 | 对应讲义 |
|---|---|---|
| **Act I** · The Cabinet Opens | 表征组合（BM25/SPLADE/dense/MRL/ColBERT） | 讲义 Act I 前半 |
| **Act II** · The Trained Instrument | DCL、课程表、MRL–DCL 不变式、48 小时教条 | 讲义 Act I 后半 |
| **Act III** · **The Derivative Corpus** | **派生物清单、主模式、经济学** | **讲义 Act II** |
| Act VI（由 p.35 得知） | **索引迁移 / 机房** | 讲义 Act III 后半 |
| Act IV / V / VII | 待定（推测：法庭、问题侧、Playbook） | |

- **⭐ 这一幕的口号就是全天的「主倒转」**，与讲义逐字相同。它把检索的重心**从查询时搬到了创作时**：
  - **正统做法**：变换 query 去凑文档（query rewriting、HyDE……）——**在查询时花力气**
  - **这一幕**：**离线制造匹配 query 的文档**——**在创作时花力气**
  - **理由是经济学**：**离线时算力便宜、时间充裕；查询时又贵又赶。** 讲义原句：***能花在「静止之物」上的智能就都花在那儿——算力的冰山属于水面之下，在查询时不可见。***
- **配图是「一个源 → 许多派生物」**，正好是正课 p.3 那张卡片阵列的对偶：**p.3 是「一份语料，许多目录」（多个索引）；这张是「一份文档，许多派生物」（多个衍生对象）**——rewrites / factoids / QA pairs / summaries / 树节点 / 社区摘要 / 被治理的 concept。
- **⭐ 三幕连起来看，是一条很干净的递进**：

| 幕 | 你在改什么 |
|---|---|
| **Act I** | **什么都不改**——用现成的表征 |
| **Act II** | **改模型**（把仪器校准到你的领域） |
| **Act III** | **改语料本身**（制造新的文档） |

  **而 p.32 已经预告了这条精神：「真正干活最多的是负例，不是损失函数」——数据 > 模型。这一幕把同一条原则从训练侧搬到了语料侧。**

- **接下来这一幕会讲什么（据讲义 Act II 预告）**：
  1. **用户即考官**（IIT「四十道题」的故事）——语域错配是永久的
  2. **主模式**：***retrieve the derivative, generate from the source***
  3. **出处回指针的两项职责**：引用 + 失效键
  4. **派生物清单七件**，每一件对着一具指名的尸体
  5. **经济学**：Artifact ROI 公式、sidecar 教条、千元实习生发票、**top-K 考古学**、churn calculus
  6. **幕间：长上下文幻象**（NoLiMa）
- **⚠️ 听的时候留意一条**：讲义在 ColBERT 那段留了一句预警——***我们今天下午亲手制造的一些派生物，正在变成编码器的原生输出***（contextual retrieval → late chunking → 整文档语境编码器）。**这一幕要教你手工建的东西，有一部分正在被模型内化。** 留意讲师会不会把这条挑明。


### 正课 p.41 · **ACT III · A STORY FROM AN EXAMINATION HALL：The classmate with forty questions**

> **ACT III · A STORY FROM AN EXAMINATION HALL**
> # **The classmate with forty questions**
>
> Applied electrodynamics, IIT. **I studied the subject.** A **soccer-playing** classmate visited the seniors and collected the question banks: **roughly forty questions, recycled across years with small mutations**. He memorized beautiful answers, **topped the exam**, **took a long shower, and never opened a physics book again**.
>
> 右栏：*I had optimized on **learning the subject**. He had optimized on **answering the examiner**. A retrieval system faces **a stream of questions** — and **the corpus was written with no examiner in mind at all**. **The user is the examiner.***
>
> **中文**：**第三幕 · 一个来自考场的故事**。**那个有四十道题的同学**。应用电动力学，IIT。**我在学这门学科。** 一个**踢足球的**同学去找学长收集了题库：**大约四十道题，逐年循环出现，只有小幅变异**。他背下了漂亮的答案，**考了第一**，**洗了个长长的澡，从此再没打开过物理书**。
> 右栏：*我优化的是**学会这门学科**。他优化的是**回答这位考官**。一个检索系统面对的是**一条问题流**——**而语料在被写下时，心里根本没有任何考官**。**用户就是考官。***

- **⭐ 这不是道德故事，是规格说明书。** 讲义原句：***In retrieval architecture that is not a tragedy. It is the specification.***（在检索架构里这不是悲剧，这是规格说明书。）
- **两种优化目标的对照**：

| | 优化目标 | 对应到系统 |
|---|---|---|
| **「我」** | **学会整门学科** | 让模型/语料"理解一切" |
| **踢足球的同学** | **回答这位考官** | **按实际查询分布来造派生物** |

- **⭐ 语域错配是结构性的、且永久**：**语料是为别的读者写的**——教科书为教学、论文为审稿人、合同为对方律师；**没有一份是为「你的用户此刻的问法」写的。**
- **⭐ 一个容易被略过、但很关键的细节：那四十道题是「去找学长要来的往年真题」，不是他自己猜的。**
  - **对应到系统里：真题 = 你自己的查询日志。**
  - 这就是 Act II 经济学里那条 **top-K 考古学**的另一面——**权重来自你实测的查询分布，不是你的直觉。**
- **⭐ 「逐年循环出现，只有小幅变异」这句还预告了下周**：**如果问题会以小幅变异重复出现，那么「语义缓存」就有价值**——下周的主题正是**语义缓存：这栋房子的前门**。
- **⚠️ 一条诚实的边界（讲义未明说，但值得自己记住）**：那位同学**「再没打开过物理书」——他并没有学会这门学科**。对应的风险是：**只按已知问题优化，遇到没见过的问题会崩。**
  - 所以 **QA pair 是加在基础检索之上的一条车道，不是替代**。
  - 而且讲义的 **Say 定律**警告过：**供给创造需求**——**系统一旦变好，用户就会开始问更难的问题**，你的"四十道题"会失效。**这正是「gold set 必须是活的」那条纪律的来由。**


### 正课 p.42 · **ACT III · THE MASTER PATTERN：Retrieve the derivative, generate from the source**

> **ACT III · THE MASTER PATTERN**
> # **Retrieve the derivative, generate from the source**
>
> Rewrites, factoids, QA pairs, summaries — **searched**. The original passage — **cited and generated from**. **Every artifact carries a provenance back-pointer to its source chunk.**
>
> **The rewrite is the bait; the original is the evidence.**
>
> 右栏：***Learn it once; you will use it everywhere.*** And the back-pointer is **not only the citation** — it is the **invalidation key**: ***summaries are materialized views***, and **when the source changes, provenance tells you what went stale**.
>
> **中文**：**第三幕 · 主模式**。**检索派生物，从源生成**。改写、factoid、QA pair、摘要——**它们是被搜索的**。原始段落——**它是被引用、并被拿来生成的**。**每一件派生物都携带一个指回其源 chunk 的出处回指针。** **改写是诱饵；原文才是证据。**
> 右栏：***学一次，你会到处用到它。*** 而回指针**不只是引用**——它还是**失效键**：***摘要就是物化视图（materialized views）***，**当源发生变化时，出处会告诉你什么东西过期了。**

- **⭐⭐ `summaries are materialized views`（摘要就是物化视图）是幻灯相对讲义新增的一句，也是给工程师最好用的一个类比**：
  - **物化视图 = 预先算好、存起来的查询结果。** 底层表一变，视图就必须失效。
  - **数据库有成熟的失效机制；而你的派生语料库没有——你必须自己建一套。**
  - **而 back-pointer 就是那张依赖关系表。**
- **`The rewrite is the bait; the original is the evidence.`** —— 诱饵与证据的配对。（注意 `bait` 在这里是**受控的、好的**那种诱饵，与 Prelude 实验四里语料自带的 `decoy` 价号相反。）

**完整例子（HR 政策）**

源 chunk `#4471`：
> 「员工在终止雇佣关系后，最后一期薪酬应于离职生效日起 **15 个工作日**内结清，**包括未休年假折算**。」

从它派生出：

| 派生物 | 内容 | 回指针 |
|---|---|---|
| **QA pair** | Q:「离职后多久发最后一笔工资？」A:「15 个工作日内」 | → `#4471` |
| **factoid** | 「离职薪酬结算期限为 15 个工作日。」 | → `#4471` |
| **rewrite** | 「员工离职后，公司会在 15 个工作日内把最后一笔工资发完。」 | → `#4471` |
| **section summary** | 「本节规定离职相关的薪酬与福利结算。」 | → `#4460–4480` |

**检索时**：用户问「换工作后工资什么时候到账」→ **命中那条 QA pair**（因为它是问题形状的）→ **但送进生成器的是 `#4471` 的原文**。

**⭐ 为什么必须回到原文**：上表那条 rewrite **丢掉了「包括未休年假折算」**。若直接拿 rewrite 生成，用户会以为只有工资、没有年假折现。**这就是讲义那个「法律改写丢掉 irrevocable」的同构失效——它不是证据，它是诱饵。**

**⭐ 现在政策改了：15 个工作日 → 10 个工作日。**

| | 没有回指针 | 有回指针 |
|---|---|---|
| 你更新了原文 | ✅ | ✅ |
| factoid「15 个工作日」 | **❌ 仍躺在索引里** | 反查出处图 → **删除重生成** |
| QA pair 的答案 | **❌ 仍是 15** | **删除重生成** |
| section summary | **❌ 可能已过期** | **标脏，稍后重建** |
| 后果 | **系统以高置信度返回一个已作废的数字，还带着「引用」——这就是 authority failure** | 可控 |

**两种失效模式（讲义）**：

| 类型 | 派生物 | 做法 | 为什么不同 |
|---|---|---|---|
| **本地失效** | chunks、factoids、rewrites、QA pairs | **按 document id 删除、重新推导** | 一条 factoid 只来自**一个** chunk |
| **传递性过期** | summaries、树节点、社区摘要 | **写时标脏，懒惰地、自底向上、异步重建** | 一条语料级摘要来自**成千上万个** chunk——改一个 chunk 就全量重建，成本不可接受 |

> **讲义原话**：***分层新鲜度不是妥协，而是对「信息在不同高度上以不同速率衰减」这件事的正确读法。***

- **一句话收口（讲义）**：***一个没有出处的派生语料库不是索引，是一间装了向量搜索的谣言工厂。***


### 正课 p.43 · **ACT III · THE GEOMETRY OF THE PROBLEM：The Berlin experiment**

> **ACT III · THE GEOMETRY OF THE PROBLEM**
> # **The Berlin experiment**
>
> Query: *"What is the population of Berlin?"*
> Cosine against the **full paragraph: 0.64 — an angle of 50°**. Against the **extracted factoid: 0.81–0.90**.
>
> **At a production threshold of 0.7, the paragraph containing the answer is *silently dropped*.**
>
> 右栏：*A paragraph embedding is the **centroid of its distinct meanings — near none of them**. **The answer was there. The geometry hid it.** **Factoid extraction is the antidote to embedding dilution.***
>
> **中文**：**第三幕 · 这个问题的几何**。**柏林实验**。查询：「柏林的人口是多少？」对**整段**的余弦：**0.64——角度 50°**。对**抽出来的 factoid**：**0.81–0.90**。**在 0.7 的生产阈值下，那个装着答案的段落被*静默丢弃*了。**
> 右栏：*一个段落的 embedding 是**它各个不同意思的质心——离其中任何一个都不近**。**答案就在那里。是几何把它藏起来了。** **factoid 抽取，就是 embedding 稀释的解药。***

- **⭐ 幻灯新增了「角度」，正好接上 p.20 的光圈教条**——把这两页合起来看，失效变得极其直观：

| | 余弦 | 角度 | 相对 0.7 阈值（**45° 光圈**） |
|---|---|---|---|
| **整段（含答案）** | **0.64** | **50°** | ❌ **在光圈外 5 度** |
| **抽出的 factoid** | **0.81–0.90** | **26°–36°** | ✅ **舒服地在圈内** |

  **差五度，答案被丢掉。**（换算核对：`arccos 0.64 ≈ 50.2°`、`arccos 0.7 ≈ 45.6°`、`arccos 0.81 ≈ 35.9°`、`arccos 0.90 ≈ 25.8°`——幻灯的数字准确。）

- **⭐ 机制：质心（centroid）。** 一个段落若含五个不同的声明，它的向量就是这五个意思的**平均**；而**平均值离每一个顶点都有相当大的角度**。
  - 直觉版：两个相距 60° 的意思，归一化质心离**每一个**都是 30°。意思越多、越分散，质心离**全部**都越远。
  - **而你的问题只指向其中一个顶点。**
- **⭐⭐ `The answer was there. The geometry hid it.`（答案就在那里。是几何把它藏起来了。）**
  - **这不是数据问题，不是模型质量问题，是几何问题。**
  - **推论（很重要）：换一个更强的 embedding 模型救不了这个。** 因为**质心效应是「取平均」这个动作的必然结果**——更好的模型让每个意思的向量更准，但**平均仍然是平均**。
  - **唯一的修法是改变「索引单元的粒度」**——这就是 factoid 存在的全部理由，也是 Dense X / FactoidWiki（**从 1.14 亿个句子得到 2.57 亿条命题**）把它工业化的原因。
- **`silently`（静默地）—— 今天第 N 次出现**：没有报错、没有告警。**那个装着答案的段落，就是铲子漏掉的一颗弹珠**，而**筛子从来没见过它**。
- **这一页也解释了 factoid 在清单里的位置**：它治的那具尸体叫 **embedding dilution（embedding 稀释）**。

**具体例子（还原那一段）**

> 「柏林是德国的首都，位于该国东北部、施普雷河畔。它是欧盟人口第二多的城市，**约有 380 万居民**。柏林在两德统一后重新成为首都，如今是重要的文化与创业中心，拥有三所主要大学和多家世界级博物馆。」

这一段里有**五件事**：①首都地位 ②地理位置 ③**人口** ④历史 ⑤文化机构。
**它的向量是这五个意思的平均**，而查询「柏林的人口是多少」**只指向第 ③ 个顶点**。

**抽出来的 factoid**：「柏林约有 380 万居民。」——**只有一个意思，向量就落在那个顶点上。**

**纪律（讲义）**：**自足性**（factoid 必须脱离上下文也成立）、**NLI 忠实性过滤**（防止抽取时编造）、**每 chunk 设上限**（防止索引爆炸）。


### 正课 p.44 · **ACT III · THE INVENTORY：What the derivative corpus contains**（派生物清单）

> **ACT III · THE INVENTORY, EACH ARTIFACT AGAINST ITS FAILURE MODE**
> # **What the derivative corpus contains**
>
> - **Contextualized rewrites** — cure **endophora** and **legalese**; **the source's understudy, auditioning for the retriever**
> - **Factoids / propositions** — cure **centroid dilution** on point queries; Dense X industrialized this: **FactoidWiki, 257M propositions from 114M sentences**
> - **QA pairs, 3–8 per chunk** — **the only artifact that puts a query-shaped object in the index**: **question as vector, answer in payload**
> - **Summaries** — **section, document, corpus** altitudes; **thematic queries stop drowning in detail**
> - **RAPTOR nodes and community summaries** — **the zoom lens and the telescope**, next two slides
> - **Governed concepts** — last week's guest; **its seat here in four slides**
>
> 右下：*Each artifact exists to prevent **a specific failure**. **Factoids sacrifice context for precision; summaries sacrifice precision for context. Neither is superior — that is the complementarity.***
>
> **中文**：**第三幕 · 清单：每一件派生物，对着它自己的失效模式**。**派生语料库里装着什么**。**语境化改写**——治**内指**与**铠甲语域**（法律腔）；**它是源的替身演员，正在为 retriever 试镜**。**Factoid / 命题**——治点查询上的**质心稀释**；Dense X 把它工业化：**FactoidWiki，从 1.14 亿个句子得到 2.57 亿条命题**。**QA pair，每 chunk 3–8 个**——**唯一把「query 形状的对象」放进索引的派生物**：**问题进向量，答案放 payload**。**摘要**——**节、文档、语料**三种高度；**主题查询不再淹死在细节里**。**RAPTOR 节点与社区摘要**——**变焦镜头与望远镜**，后两页。**被治理的 concept**——上周的客人；**四页之后落座**。
> 右下：*每一件派生物的存在，都是为了防住**一个特定的失效**。**factoid 用上下文换精度；summary 用精度换上下文。没有哪个更优越——这正是互补性。***

- **⭐ 分幕标题就是纪律**：***EACH ARTIFACT AGAINST ITS FAILURE MODE***（每一件对着它的失效模式）——**没有任何一件靠「有趣」赢得位置。**

| 派生物 | 它治的那具尸体 |
|---|---|
| **语境化改写** | **内指（endophora）+ 铠甲语域**（法律腔、临床速记） |
| **Factoid** | **质心稀释**（p.43 柏林实验） |
| **QA pair** | **跨体裁错配**（问题 vs 散文） |
| **Summary** | **主题查询碎在 chunk 之间 / 淹死在细节里** |
| **RAPTOR** | 缺**变焦镜头** |
| **Community summary** | 缺**望远镜** |
| **Governed concept** | **权威失效** |

**同一个源 chunk，五件派生物长什么样（例）**

源（保险条款，故意带内指与法律腔）：
> 「4.2 节 · 保单续期。**本条款**所述之通知期为三十（30）日。**该期间**自续期基准日起算，且不因投保人变更通讯地址而中断。**前述**通知未依约送达者，视为自动续期。」

| 派生物 | 内容 |
|---|---|
| **语境化改写** | 「**保单续期**的通知期是 **30 天**，从**续期基准日**开始算。投保人换地址不会中断这 30 天。如果公司没按约定把续期通知送到，**保单就自动续期**。」<br>→ **「本条款/该期间/前述」全部解析掉，法律腔换成用户的说法** |
| **Factoid ×4** | ①「保单续期通知期为 30 日。」②「续期通知期自续期基准日起算。」③「变更通讯地址不中断续期通知期。」④「续期通知未依约送达的，保单自动续期。」<br>→ **一句一个原子事实，各自落在自己的顶点上** |
| **QA pair ×3** | Q「续保要提前多久通知？」A「30 天」／ Q「我搬家了会影响续保通知期吗？」A「不影响」／ Q「公司没通知我会怎样？」A「自动续期」<br>→ **问题进向量，答案放 payload** |
| **Section summary** | 「第 4 节规定保单续期的通知期、起算方式与未通知的后果。」 |
| **RAPTOR / community / governed** | 后续几页 |

- **⭐ 右下角那段是这一页真正的论点，而且它把 Prelude 的蜻蜓推论接了回来**：

| | 牺牲 | 换来 | 擅长 |
|---|---|---|---|
| **Factoid** | **上下文** | **精度** | **点查询** |
| **Summary** | **精度** | **上下文** | **主题查询** |

  **「没有哪个更优越——这正是互补性。」**
  **翻译成 Prelude p.10 的话：它们丢的不是同一批东西，所以融合才有增益。** 如果两件派生物牺牲的是同一样东西，**加起来等于一件**。

- **`the source's understudy, auditioning for the retriever`（源的替身演员，正在为 retriever 试镜）** —— 与 p.42 主模式一致：**替身负责被选中，正主负责上场作证。**
- **路线信息**：**RAPTOR 与社区摘要在后两页；被治理的 concept 在四页之后。**


### 正课 p.45 · **ACT III · THE ZOOM LENS：RAPTOR — the query finds its own level**

> **ACT III · THE ZOOM LENS**
> # **RAPTOR — the query finds its own level**
>
> **Cluster, summarize, recurse** — a **discovered** hierarchy, **1.3–1.5× the leaves**. **Retrieve over the collapsed tree**: **the query lands at its own altitude.**
>
> *Bacon's tree (right) was **decreed**; RAPTOR **grows** one from the geometry. **Warning: garbage clusters yield confident garbage summaries** — **RAPTOR amplifies embedder quality, both ways.***
>
> **中文**：**第三幕 · 变焦镜头**。**RAPTOR——查询自己找到它的层级**。**聚类、摘要、递归**——一个**被发现出来的**层级，节点数约为**叶子的 1.3–1.5 倍**。**在坍缩树上做检索**：**查询自己落到它该在的高度。**
> *右图培根的知识树是**被钦定的**；RAPTOR 则是**从几何里长出来**一棵。**警告：垃圾聚类会产出自信的垃圾摘要**——**RAPTOR 会放大 embedder 的质量，双向放大。***
>
> 配图：**培根/百科全书派的「人类知识体系树」**（根部 MÉMOIRE / RAISON / IMAGINATION，主枝 HISTOIRE / PHILOSOPHIE / POÉSIE）。

- **机制**：从 chunk（叶子）出发 → **聚类** → 每簇**生成摘要**，摘要成为上一层节点 → 对摘要**再聚类再摘要** → **递归**直到收敛。**总节点约 1.3–1.5 倍叶子数**（10 万 chunk → 多出 3–5 万个摘要节点，**存储代价其实很温和**）。
- **⭐ `collapsed tree`（坍缩树）是这一页最关键的检索技巧**：
  - **不是**自顶向下遍历树；
  - 而是**把所有层级的节点（叶子 + 各层摘要）全部放进同一个索引**，查询时一次性检索。
  - **于是查询自己会命中它该在的高度**——**判断高度这件事被从路由器手里拿走，交给了相似度本身。**
- **⭐ `decreed` vs `grows`（钦定 vs 长出来）**：
  - 培根/百科全书派的知识树是**人先验规定**的分类学（记忆→历史、理性→哲学、想象→诗歌）；
  - **RAPTOR 的层级是从数据的几何里涌现出来的**。
  - **顺带：Otlet 的 UDC 也是「钦定」的。** 所以这一页也在说——**Mundaneum 的抽屉是人定的，RAPTOR 的抽屉是算出来的。**
- **⚠️⚠️ 警告是这一页最该记的部分**：***garbage clusters yield confident garbage summaries*** ／ ***RAPTOR amplifies embedder quality, both ways***。
  - embedding 空间不好（各向异性、`gap` 小）→ **聚类是乱的**
  - 而**摘要器会认真地给一个乱簇写出一段通顺的摘要**
  - **结果：一个流畅、自信、但主题根本不成立的节点，混在索引里**
  - 讲义还给了它的名字——**幻影簇（phantom cluster）**：**它能通过每一项逐 chunk 的出处检查**（因为每个 chunk 确实存在），**却在主题上根本不成立**；**只有主题一致性检查（topical-coherence check）抓得住它。**
  - **⭐ 可执行的前置条件：上 RAPTOR 之前，先用 Week 02 的 cosine histogram 量一下你的 `gap`。gap 小的空间上建 RAPTOR，等于放大噪声。**

**具体例子（500 篇客户访谈）**

**叶子（原始 chunk）**：
> ①「……我们最担心的是数据出境合规……」 ②「……跨境传输要额外审批，流程三周……」 ③「……法务不批我们就没法用海外 SaaS……」 ④「……价格倒可以接受，主要是审批周期……」 ⑤「……上季度换了三个供应商，都卡在安全评估……」

**第 1 层（聚类 + 摘要）**：
> **簇 A**（①②③）→「客户普遍将**数据出境合规与跨境审批**视为采购阻碍。」
> **簇 B**（④⑤）→「采购周期受**安全评估与供应商更替**影响，**价格并非主要障碍**。」

**第 2 层**：
> 「**合规与安全审批**是主导采购决策的因素，**优先于价格**。」

**三种查询，一次检索，各自落到自己的高度**：

| 查询 | 命中 |
|---|---|
| 「跨境审批要多久？」 | **叶子②**（"三周"） |
| 「客户对合规的顾虑是什么？」 | **第 1 层 · 簇 A 摘要** |
| 「影响采购决策的主要因素是什么？」 | **第 2 层顶层摘要** |

**⚠️ 幻影簇长什么样**：若 embedder 不好，可能把「价格可以接受」和「数据出境」聚成一簇（只因为它们出现在同一批访谈、句式相近），摘要器会写出——
> 「客户在**成本与合规之间存在权衡**。」

**听起来很像回事，但没有任何一条原始记录支持这个结论。** 而且**逐条查出处全都对得上**（每个 chunk 都真实存在）——**这就是为什么只有主题一致性检查才抓得住它。**


### 正课 p.46 · **ACT III · THE TELESCOPE：GraphRAG — asking the city, not the shelves**

> **ACT III · THE TELESCOPE**
> # **GraphRAG — asking the city, not the shelves**
>
> **Extract entities and relationships, detect communities (Leiden), summarize each community.** *"Major regulatory concerns across 500 earnings calls"* **exists in no document — it lives in the structure.**
>
> **Embeddings say: these passages *sound alike*. Triplets say: these passages are *about the same things*.**
>
> 右栏：*Some questions can only be answered by the **structure** of a corpus, **never by any passage within it**. The community summary is **the highest-value derivative artifact we have met** — **a mini-textbook written by the whole corpus**.*
>
> **中文**：**第三幕 · 望远镜**。**GraphRAG——问这座城市，而不是问书架**。**抽取实体与关系，检测社区（Leiden 算法），为每个社区生成摘要。**「这 500 场财报电话会里的主要监管关切有哪些」——**这个答案不存在于任何一份文档中，它活在结构里。** **embedding 说的是：这些段落「听起来像」。三元组说的是：这些段落「是关于同一些东西的」。**
> 右栏：*有些问题只能由语料的**结构**来回答，**永远不会由其中任何一个段落来回答**。社区摘要是**我们见过的价值最高的派生物**——**一本由整个语料写成的小教科书。***

- **⭐ 全页最核心的一句是那组对照**：
  - **embedding：这些段落「听起来像」**（表面语义相似）
  - **三元组：这些段落「是关于同一些东西的」**（指向同一批实体）
  - **两者会分歧，而且分歧的方向刚好相反**：
    - **两段文字可以毫不相似，却关于同一个东西**（A 公司的年报 与 B 公司的诉讼文件，通过同一个监管机构相连）→ **embedding 抓不到**
    - **两段文字可以非常相似，却关于完全不同的东西**（两家公司的季度业绩段落，句式几乎一样）→ **embedding 会错误地拉近**
- **⭐ `asking the city, not the shelves`（问这座城市，不是问书架）** —— 书架 = 一本本文档；城市 = 它们之间的关系网络。**你问的是城市的形状，而不是某一栋楼里写了什么。**
- **`a mini-textbook written by the whole corpus`（一本由整个语料写成的小教科书）** —— 对社区摘要最好的定义。
- **⚠️ 但要和讲义的两条经济学一起读，否则会误用**：
  - **sidecar 教条**：**图是 sidecar，永远不是主路**。**全局 sensemaking 约占企业流量 5–15%，而本课的路由器只送 1–2% 走它**——**它定义智能的天花板，但不被允许承载高速公路。**
  - **千元实习生发票**：抽取任务接到前沿 API 而非本地集群 → 成本悬崖。**LazyGraphRAG 与 HippoRAG 2 此后废掉了这张发票的大部分**，所以**这条教条现在是关于流量，不是关于价格**。

**RAPTOR vs GraphRAG（并列对照）**

| | **RAPTOR（变焦镜头）** | **GraphRAG（望远镜）** |
|---|---|---|
| **建出来的东西** | **一棵树** | **一张图 + 社区摘要** |
| **靠什么建** | **向量相似度聚类** | **LLM 抽取实体与关系（三元组）+ Leiden 社区检测** |
| **回答的问题** | **「关于 X 的整体情况」**——主题明确，只是**散在很多 chunk 里** | **「整个语料的结构是什么」**——**你事先不知道有哪些类别** |
| **答案在哪** | 在若干段落的**汇总**里 | **不在任何段落里，在结构里** |
| **成本** | 中（**1.3–1.5×** 叶子数） | **高**（每份文档都要跑抽取） |
| **流量占比** | 中 | **5–15%，而路由只送 1–2%** |
| **失败模式** | **幻影簇**（乱聚类 → 自信的垃圾摘要） | 抽取质量差 → 图是错的；**成本悬崖** |

**例子对照**

- **RAPTOR 擅长**：「客户对合规的顾虑是什么？」→ 把散在 50 篇访谈里的合规段落聚起来摘要。**主题是已知的，只是分散。**
- **GraphRAG 擅长**：
  - 「这 500 场财报电话会里的**主要监管关切有哪些**？」→ **你事先不知道有几类**。答案形如「有五类，分别是 A/B/C/D/E」，**而没有任何一个段落说过这句话。**
  - 「**A 公司和 B 公司有什么关系？**」→ **可能没有任何一份文档同时提到两者**，关系是通过第三方 C 中转的。**embedding 完全做不到——两份文档不「像」，但它们通过同一个实体相连。**


### 正课 p.47 · **ACT III · THE INVOICE ARRIVES：The sidecar doctrine, and the cost cliff**

> **Sensemaking is 5–15% of enterprise queries; in our production routing, 1–2% of traffic actually enters the graph sidecar.** One intern once wired extraction to a **frontier API** instead of the local cluster: **$1,000 overnight, for two Dostoevsky novels**.
>
> 右栏：*The 2024–26 correction: **LazyGraphRAG indexes at ~0.1% of full cost**; **HippoRAG 2** keeps **factoid parity while winning multi-hop**. **Graph RAG is now a specialized instrument, not a default** — **a sidecar, never the main road.***
>
> **中文**：**第三幕 · 账单到了**。**sidecar 教条与成本悬崖**。**Sensemaking 占企业查询的 5–15%；在我们的生产路由里，实际只有 1–2% 的流量真正进入图 sidecar。** 有个实习生曾把抽取任务接到**前沿 API** 而不是本地集群：**一夜一千美元，而处理的不过是两本陀思妥耶夫斯基的小说。**
> 右栏：*2024–26 年的修正：**LazyGraphRAG 的索引成本约为完整版的 0.1%**；**HippoRAG 2 在 factoid 上打平、在多跳上取胜**。**Graph RAG 如今是一件专用仪器，不是默认选项**——**sidecar，永远不是主路。***

- **「两本陀思妥耶夫斯基小说 = 一千美元一夜」**——约一百万字。**成本悬崖被量化成了一个有画面的换算。**
- **⭐ 右栏是诚实的更新**：**成本悬崖已经被大幅填平（0.1%）**。**所以这条教条现在的理由变了：不再是「太贵」，而是「流量只有 1–2%」。** 便宜了，但仍然是 sidecar。（同 p.23 的方法论：**因成本而拒绝的论证，每年要重审。**）

---

### 正课 p.48 · **ACT III · THE AUDIT THAT SETTLES THE ARGUMENT：The archaeology of top-K**

> **ACT III · THE AUDIT THAT SETTLES THE ARGUMENT**
> # **The archaeology of top-K**
>
> **Trace every winner in your top-K back through its provenance**: raw chunk, factoid, QA decoy, rewrite, summary node?
>
> **The reproducible finding: *most of your top results, most of the time, are not raw chunks*.**
>
> 右栏：*This is **the single strongest argument for the multi-representation architecture** — **no new hardware, no bigger model, spectacularly better retrieval**. **Run it offline as an audit; keep it running online as telemetry.***
>
> **中文**：**第三幕 · 那次了结争论的审计**。**top-K 的考古学**。**把你 top-K 里的每一个胜出者，顺着它的出处回溯**：它是原始 chunk、factoid、QA 诱饵、改写、还是摘要节点？**可复现的发现：*大多数时候，你的大多数 top 结果都不是原始 chunk。***
> 右栏：*这是**支持多表征架构的最强单一论据**——**不需要新硬件，不需要更大的模型，检索质量却显著提升**。**离线跑一次当审计；在线一直跑当遥测。***

- **⭐ 为什么标题叫「了结争论的审计」——因为这是唯一的「事后」证据。**
  - 其他论据都是**事前的、预测性的**：**柏林实验**说 factoid *应该*有用（几何论证）；**用户即考官**说 QA pair *应该*有用（语域论证）。
  - **top-K 考古学是唯一在「你自己的真实流量」上给出事后计数的东西**——**这些派生物到底赢了多少次。**
  - **争论到此了结：不靠热情，靠家谱。** 讲义原话：***让家谱——而绝不是热情——决定哪些镜头留下。***
- **成本低到没有借口**：讲义说 ***it costs one week of logging to run on your own traffic***（在你自己的流量上跑，只需要一周的日志）。
- **⭐ 两种用法（幻灯明确区分）**：

| 用法 | 何时 | 回答什么 |
|---|---|---|
| **离线审计** | 跑一次 | **该不该建这些派生物 / 建哪些** |
| **在线遥测** | 一直跑 | **哪些该留下 / 哪些该砍掉** |

**怎么实施（落到代码）**

```python
# 检索返回后，记录每个胜出者的家谱
for i, hit in enumerate(final_top_k):
    log_genealogy({
      "query_id": qid,
      "rank": i,
      "artifact_type": hit.payload["type"],       # chunk|factoid|qa_pair|rewrite|summary|raptor|community
      "source_chunk_id": hit.payload["source_chunk_id"],
      "lane": hit.lane,                           # 由哪条车道发射
      "score": hit.score,
      "cited_in_answer": ...,                     # 可选：生成器实际引用了吗
    })
```

一周后：

```sql
SELECT artifact_type, COUNT(*) AS wins
FROM genealogy WHERE rank <= 10
GROUP BY artifact_type ORDER BY wins DESC;
```

- **⚠️ 一条必须补的纪律：出现频率高 ≠ 不可或缺。**
  - **考古学是「观察」**：谁赢了。
  - **消融是「干预」**：关掉它会怎样。
  - **一件派生物可能经常出现在 top-K，但关掉它答案照样对**（因为有冗余车道覆盖）——**那它仍然该砍。**
  - **正确用法：考古学负责初筛（便宜、连续），消融负责定论（严格、间歇）。**


### 正课 p.49 · **ACT III · THE SEVENTH ARTIFACT — LAST WEEK'S GUEST RETURNS：Knowledge with papers**

> **ACT III · THE SEVENTH ARTIFACT — LAST WEEK'S GUEST RETURNS**
> # **Knowledge with papers**
>
> **Last Saturday, knowledge got its papers.** Today **OKF takes its seat here: the governed concept, the seventh artifact.** Its corpse: the **authority failure** — **text no one currently stands behind**.
>
> *Chunks answer **what is similar**; concepts answer **who says so, as of when** — **as queryable fields**. The plate's cartouche (right): **frontmatter in ink, c. 1930**.*
>
> **中文**：**第三幕 · 第七件派生物——上周的客人回来了**。**带着证件的知识**。**上周六，知识拿到了它自己的证件。** 今天 **OKF 在这里落座：被治理的 concept，第七件派生物。** 它的尸体是**权威失效**——**当前没有任何人站在其背后的文本**。
> *chunk 回答的是**「什么是相似的」**；concept 回答的是**「谁这么说的、截至什么时候」——而且是作为可查询的字段**。右图图版底部的题签：**用墨水写的 frontmatter，约 1930 年。***

- **`Last Saturday` = Week 09（2026-08-08）的 OKF。** **「知识拿到了自己的证件」**——谁写的、谁核实过、什么时候过期。
- **⭐ 全页最锋利的是那组对照**：

| | 回答什么 | 形式 |
|---|---|---|
| **chunk** | **什么是相似的**（what is similar） | 相似度 |
| **governed concept** | **谁这么说的、截至什么时候**（who says so, as of when） | **可查询的字段** |

  **`as queryable fields`（作为可查询的字段）是关键限定**：这些信息**不是写在散文里，而是写在结构化字段里**——所以**可以过滤、可以机械判断**。
  **工程上的差别**：你可以写 `WHERE verified_by IS NOT NULL AND stale_after > now()`；**对一个 chunk 你写不出这句话。**

- **⭐⭐ 配图才是这一页真正的论证**：一张 **1930 年前后的 Mundaneum 图版**（*L'ÉCLAIRAGE*，照明史，19 种灯具编号排列，从火把、亚述/埃及/罗马油灯，到 Davy 安全灯、煤气灯、电灯）。**底部的题签（cartouche）就是用墨水手写的 frontmatter**：

| 图版上的字段 | 值 | 今天的对应 |
|---|---|---|
| `Mat:` **628.9** | UDC 分类号（照明工程） | `type` / `subject` |
| `Lieu:` **(∞)** | 地点 = 普适 | 作用域字段 |
| `Temps:` **∞** | 时间 = 全时 | `valid_from` / `stale_after` |
| `Pers:` | 人物（此处空） | 实体字段 |
| `Source:` | **出处** | `sources[]` |
| `Doc. N° **8055**` | 文档编号 | `id` |
| `H. ROYNETTE` | 制图者 | `author` |
| `PALAIS MONDIAL, BRUXELLES` | 机构 | 命名空间 |

  **Otlet 的卡片早就有 frontmatter——只是写在纸上、用墨水。**
  **这正是全天那句话的图像证据**：***Otlet 的卡片今年夏天回来了，以带着出处写在 frontmatter 里的 typed markdown 的形式。***

- **闭环**：正课从 p.3–5 的 Otlet 开始，绕过 Act I 的表征、Act II 的训练、Act III 的六件派生物，**在第七件这里回到了同一张卡片**——**同一个设计，绕了 130 年。**
- **接下来几页（据讲义）**：**governed concept 的三条独有性质**（修复便宜、支持导航式检索、评审门结构上原生）、**幻影概念（phantom concept）**及其防御、以及**阶梯纪律**（这一层只为被治理的核心而建）。


### 正课 p.50 · **ACT III · THE ONLY GATED DERIVATION：Extract → review → merge**

> **ACT III · THE ONLY GATED DERIVATION**
> # **Extract → review → merge**
>
> **Every other artifact is derived by pipeline. This one's derivation passes through a human review gate** — **extraction lands as a pull request; merge is the promotion event**. **Repair is a one-line diff, not a re-ingestion.**
>
> Its seat: **the top rung of the ladder** — **the governed core only (glossary, metrics, policies, runbooks), where an owner will actually review.**
>
> 右栏：*An unreviewed bundle is **chunks wearing a suit** — **worse than chunks, because the suit reads as authority**. And beware the phantom cluster's descendant: the **phantom concept**, **a fluent interpolation wearing the review gate's own seal**. **Fidelity review, not form review.***
>
> **中文**：**第三幕 · 唯一一件带门禁的推导**。**抽取 → 评审 → 合并**。**其他每一件派生物都由管线自动推导出来。只有这一件的推导要经过一道人类评审门**——**抽取落地为一个 pull request；合并就是那个晋升事件**。**修复是一行 diff，不是重新摄取。** 它的座位：**阶梯的最顶一级**——**只为被治理的核心（术语表、指标定义、政策、runbook），也就是真的有一位主人会去评审的那些。**
> 右栏：*一个未经评审的 bundle 是**穿了西装的 chunk**——**比 chunk 更糟，因为那身西装会被读成权威**。还要提防幻影簇的后代：**幻影概念**，**一段流畅的插值，穿着评审门自己的印章**。**要做忠实性评审，不是形式评审。***

- **⭐ Git 工作流三步，每一步都有精确含义**：

| 步 | 是什么 |
|---|---|
| **Extract** | agent 抽取 → **落地为一个 pull request**（候选，不是事实） |
| **Review** | **人类审** ——**这是全清单里唯一的人类门禁** |
| **Merge** | **晋升事件（promotion event）** ——**这条知识从「候选」变成「权威」的那一刻** |

- **`Repair is a one-line diff, not a re-ingestion`** —— 讲义那句的浓缩：**其他每一件我们重建（rebuild），只有这一件我们修复（repair）。** 一个错事实在 embedded 语料里要等季度重摄取；在 bundle 里是**一行 diff，几分钟合并，`git blame` 记下谁修的**。
- **`top rung / governed core only`** —— **不是给整个语料用的**。只给**术语表、指标定义、政策、runbook**这**几百到几千个**、**且有主人愿意握笔**的 concept。

- **⭐⭐ 右栏第一条警告：`chunks wearing a suit`，而且「比 chunk 更糟」。**
  - **为什么更糟**：***the suit reads as authority***（**西装本身会被读成权威**）。
  - 一个 chunk 至少诚实地宣告「我只是一段文本」；**一个未经评审的 bundle 带着 frontmatter、带着 `verified` 字段，看起来像是被治理过的**——**下游（路由器、生成器、用户）会把它当作已核实。**
  - **失效的本质：元数据在撒谎，而元数据的可信度本来就高于正文。**

- **⭐⭐ 第二条警告：幻影概念（phantom concept）。**
  - **幻影簇的后代**，但**更危险**——**因为通过评审的幻影会被晋升**：盖上 human-reviewed 的戳，**被抬进那些分层机制原本就是为了保护的高风险查询路径**。

**幻影概念长什么样（例）**

源文件里实际有的：
> 政策 A（2024）：「差旅住宿标准每晚 800 元。」
> 政策 B（2025）：「一线城市可上浮 20%。」

抽取 agent 产出的 concept：
```yaml
title: 差旅住宿标准
verified: true
sources: [policy-A.md, policy-B.md]
---
一线城市差旅住宿标准为每晚 960 元。
```

- **每个字段都合法，两个 source 都真实存在，960 = 800×1.2 算得也对。**
- **但没有任何一份政策说过「960」——它是插值出来的。**
- 而 B 可能另有限定（只适用于某些岗位），或 A 已被更新政策取代。**这条 concept 现在带着 `verified: true` 躺在最高信任层里。**

| 评审类型 | 会怎样 |
|---|---|
| **形式评审（form review）** | ✅ **放行**——YAML 合法、source 存在、链接可点 |
| **⭐ 忠实性评审（fidelity review）** | ❌ **拦下**——「960 这个数字出现在哪份源文件里？找不到 → 打回」 |

- **讲义补充的两条防御，正好治这个**：
  1. **蕴含（NLI）检查在 CI 里跑**——每一个 knowledge pull request 都过一遍，和过滤 factoid 用的是同一套机器。
  2. **⭐ 数字一律不配得到散文**——**一个定量声明必须放进「被证明的计算（attested computation）」，在那里插值在结构上不可能发生。**


### 正课 p.53 · **POP QUIZ · ACT III：Quiz 5 — the telescope and the wristwatch**

> ⚠️ **p.51–52 未截到。**

> **POP QUIZ · ACT III**
> # **Quiz 5 — the telescope and the wristwatch**
>
> *Your system serves **100,000 queries/month**. **Five percent** are sensemaking, routed to the graph sidecar at **$0.20–0.60 per query**.*
> ***(a)** Monthly sidecar bill?*
> ***(b)** The router breaks and routes **everything** through the graph — new bill?*
> ***Say back the sidecar doctrine, and name the anti-pattern in (b).***
>
> **中文**：**测验五——望远镜与手表**。*你的系统每月服务 **10 万次查询**。其中 **5%** 是 sensemaking，被路由到图 sidecar，**每次查询 $0.20–0.60**。**(a)** 每月 sidecar 账单是多少？**(b)** 路由器坏了，把**所有**流量都送进图——新账单是多少？**把 sidecar 教条背出来，并说出 (b) 里那个反模式的名字。***

**答案：**

- **(a)** 10 万 × 5% = **5,000 次** → **$1,000 – $3,000 / 月**
- **(b)** 10 万次全走图 → **$20,000 – $60,000 / 月**
  - **20 倍。**
- **(c) sidecar 教条**：**图是 sidecar，永远不是主路。** 全局 sensemaking 占企业流量 **5–15%**（本课路由器只送 **1–2%**），且**不成比例地是高管问的那些问题**——**它定义智能的天花板，但不被允许承载高速公路。**
- **(d) 反模式的名字：标题就是答案——「用望远镜看手表」。** 讲义原话：***telescopes are not for wristwatches***（望远镜不是给手表用的）。**拿一件为全局问题设计的昂贵仪器，去处理点查询。**

**三条值得补的**：

1. **⭐ 20 倍的还不只是钱——延迟会先崩。** 图 sidecar 的 map-reduce 是**秒级到十秒级**，而点查询期待的是**百毫秒**。**用户体验当天就崩，账单第二天才到。**
2. **⭐ 但请注意：这是今天少见的一个「响亮」的故障。** 账单会叫、延迟会叫、告警会响。**对比今天一路走来的那些静默失效**（铲子静默腐烂、赤道带静默填充、幻影概念带着 `verified` 静默晋升）——**这个反而是幸运的。**
   > **可带走的一般规律：成本类故障是响的，质量类故障是哑的。所以你会自动修好前者，而后者只能靠纪律。**
3. **⭐ 防御是路由器的 fail-safe 默认值**：**路由器坏掉时，应该退回「高速公路」（便宜的主路），而不是退回 sidecar。** **默认值要选「便宜且够用」的那条**——这道题演的正是默认值选错方向的代价。
4. **与 p.47 的成本更新对照**：**LazyGraphRAG 把「索引时」成本降到约 0.1%**，但**这道题算的是「查询时」成本**——那部分还在。**所以「图很贵」这条如今主要贵在查询时，不是索引时。**


### 正课 p.54 · **POP QUIZ · ACT III · ANSWER：$1,000 well spent — or $60,000 on fire**

> **(a)** 5,000 × $0.20–0.60 = **$1,000–3,000** — **buying answers no other instrument can produce.**
> **(b)** 100,000 × $0.20–0.60 = **$20,000–60,000** — **mostly spent answering point queries.**
>
> 右栏：*The doctrine: GraphRAG is a **sidecar** for the small fraction of queries that need structure — **disproportionately the ones executives ask**. The anti-pattern is **the point query through the graph: using a telescope to read your own wristwatch.***
>
> **中文**：**(a)** $1,000–3,000——**买的是没有任何其他仪器能产出的答案。** **(b)** $20,000–60,000——**而这些钱大部分花在了回答点查询上。**

- **⭐ 同样的单价、同样的工具，一个「值」一个「烧」——差别完全在路由。**

| | 花费 | **第二栏（缺席的代价）** | 判语 |
|---|---|---|---|
| **(a) 全局问题走图** | $1,000 | **满的**——没有它这类问题**根本答不了** | **值** |
| **(b) 点查询走图** | $60,000 | **空的**——便宜车道也能答，还更快 | **烧** |

- **⭐ 由此得到一条比「两栏账簿」更精确的东西**：前面问的是「**这个组件值不值**」；**这道题说明那个问法是错的**。
  > **正确的问法是：「这个组件，对这一类查询，值不值。」**
  > **成本从来不是组件的属性，是「组件 × 查询类别」这个配对的属性。**

---

### 正课 p.56 · **INTERLUDE · THE EVIDENCE AGAINST THE MIRAGE：NoLiMa, and context rot**

> ⚠️ **p.55 未截到**（大概率是幕间的开场页）。**Act III 结束，幕间「长上下文幻象」开始。**

> **INTERLUDE · THE EVIDENCE AGAINST THE MIRAGE**
> # **NoLiMa, and context rot**
>
> **Million-token windows tempt a simple heresy: *just put the corpus in the prompt*.** Then **remove the lexical overlap between needle and question — NoLiMa** — and **11 of 12 frontier models fall below 50% of their short-context performance by 32K tokens**.
>
> 右栏：***Chroma's context rot report** ran **eighteen models** — GPT-4.1, Claude 4, Gemini — and found degradation **well inside the advertised window**. **Lost-in-the-middle is mitigated in new models, not solved.** **Test cures with NoLiMa-style probes, not marketing decks.***
>
> **中文**：**幕间 · 反驳幻象的证据**。**NoLiMa 与上下文腐烂**。**百万 token 窗口诱惑出一条简单的异端：*把语料直接塞进 prompt 就好了*。** 然后**去掉「针」和「问题」之间的词面重叠——这就是 NoLiMa**——**十二个前沿模型里有十一个，在 32K token 处就跌破了它们短上下文表现的 50%。**
> 右栏：***Chroma 的 context rot 报告**跑了**十八个模型**——GPT-4.1、Claude 4、Gemini——**发现退化远在「广告标称的窗口」之内就已发生**。**「中间迷失」在新模型上被缓解了，但没有被解决。** **要用 NoLiMa 式的探针去检验号称的修复，而不是看营销材料。***

- **⭐ NoLiMa 的方法论贡献（这才是重点，而不是那个数字）**：
  - **标准的 needle-in-a-haystack**：把一句话藏进长文本，再问一个**与那句话共享词汇**的问题 → **模型只要做词面匹配就能找到，根本不需要理解** → 于是所有模型都「通过」，「百万 token 已解决」。
  - **NoLiMa 去掉词面重叠** → **现在必须推断，不能匹配** → **12 个里 11 个在 32K 就腰斩。**
  - **⭐ 这是一条「基准设计」的教训，不只是长上下文的教训：一个允许被走捷径的基准，测的就是那条捷径。**
  - **而这和上午 bm42 用 Quora（每查询 1.6 个相关项）是同一个错误**——**用了一把量不出你关心的东西的尺。** 两个案例，同一条教训。
- **⭐ `well inside the advertised window` 带出一个很有用的区分**：

| | 是什么 |
|---|---|
| **广告窗口（advertised）** | 模型技术上**接受**多少 token |
| **可用窗口（usable）** | 模型在多少 token 内**还能可靠地推断** |

  **两者可以差一个数量级，而只有第二个对你有意义。**

- **`mitigated, not solved`（被缓解，不是被解决）** —— 所以**每换一次模型都要重测，不能假设它已经好了**。
- **`Test cures with NoLiMa-style probes, not marketing decks`** —— 与 bm42 那条反射一字不差的同源：***把每一次发布当作一篇你打算复现的论文来读，让你自己封存的标尺去批改。***

**怎么给自己做一个 NoLiMa 式探针（便宜、可执行）**

1. 从**你自己的语料**取一个事实
2. **用完全不重合的词**写一个问题（换同义词、换句式、用上位词——**故意不让它能被词面匹配**）
3. 把那段埋进**不同长度**的上下文：8K / 32K / 128K / 全窗口
4. 测准确率随长度的曲线
5. **⭐ 曲线开始掉的地方，就是你的「可用窗口」——用它，而不是用厂商标称的数字。**

- **讲义的诚实结论**：**在蟑螂尺度上（一万份文档、单一语域），长窗口是一个正当的器官**；**往上，检索不是在和窗口竞争，检索是让窗口值得被填满的那个东西。** ***The window is for holding evidence, not for finding it.***


### 正课 p.57 · **INTERLUDE · THE ECONOMICS：The meter is running**

> **INTERLUDE · THE ECONOMICS**
> # **The meter is running**
>
> **Attention re-reads every token, *every query*** — you pay **O(n) per token served**, at **tens of seconds of latency**. **Retrieval pays O(log n)-ish per query against a pre-built index.**
>
> Corpus-in-the-prompt versus a tuned cascade: roughly a **1,250-fold per-query cost gap**.
>
> 右栏：***The number will age; the asymmetry will not.*** **Indexing is a one-time capital cost, amortized over every future query.** **Prompt-stuffing is an operating cost you pay again, in full, forever.**
>
> **中文**：**幕间 · 经济学**。**跑表还在走**。**注意力会重读每一个 token，*每一次查询都重读一遍***——你为**每个被服务的 token 付出 O(n)**，代价是**数十秒的延迟**。**而检索针对一个预先建好的索引，每次查询只付大约 O(log n)。** 「把语料塞进 prompt」对比「一条调好的级联」：**每次查询的成本差距约 1,250 倍。**
> 右栏：***那个数字会过时；这个不对称不会。*** **建索引是一次性的资本支出，被未来每一次查询摊薄。** **而塞 prompt 是一笔运营支出——你要一次又一次、全额、永远地付下去。**

- **⭐⭐ `The number will age; the asymmetry will not.` 是全页最该带走的一句，而且它是方法论级别的。**
  - **1,250 倍这个数字会变**（模型变便宜、硬件变快）。
  - **但「一次性 vs 每次全额再付」这个结构性差异不会变。**
  - **所以论证要建立在「不对称」上，不要建立在「数字」上。**
- **⭐ 把它和 p.23（ColBERT 成本坍塌）并排，就得到一条完整的判据**：

| 论证类型 | 例子 | 会不会过期 | 该怎么办 |
|---|---|---|---|
| **价格论证** | 「ColBERT 太贵」 | **会**——成本是这个领域变动最快的部分 | **每年重审**（p.23） |
| **结构论证** | 「长上下文每次都要全额再付」 | **不会**——它是成本的**形状**，不是成本的**数值** | **可以依赖**（p.57） |

  **这就解释了为什么讲义敢在 ColBERT 上改口（反对意见倒下了），却不敢在长上下文上改口。**

- **资本支出 vs 运营支出（CapEx vs OpEx）是给预算会用的语言**：
  - **索引 = CapEx**：付一次，**被未来每一次查询摊薄**
  - **塞 prompt = OpEx**：**每次查询全额重付**
  - **推论：查询量涨十倍，索引方案的账单涨 `log`，塞 prompt 方案的账单涨十倍。**
  - **⭐ 在预算会上不要说「长上下文更贵」**（对方会回「价格在降」）；**要说「它是运营成本，我们是资本成本」**——**这句话不会被降价打败。**
- **延迟同样是数量级差距**：幻灯说塞满窗口是**数十秒**；而 p.20 的时钟预算里，**cross-encoder 一到几百毫秒就已经算「昂贵的法官」了**。**差两个数量级以上。**
- **技术脚注**：幻灯写的是「每个被服务的 token 付 O(n)」——即生成每个 token 都要对 n 个上下文 token 做注意力；**而 prefill 阶段实际是 O(n²)**。**无论按哪种算，结论方向一致：成本随语料规模增长，且每次查询重付。**
- **与 p.56 合起来，幕间的两半就完整了**：**p.56 给证据（NoLiMa：它做不到），p.57 给经济学（就算做得到，你也付不起）。**


### 正课 p.58 · **INTERLUDE · THE HONEST SYNTHESIS：You do not read the library**

> **INTERLUDE · THE HONEST SYNTHESIS**
> # **You do not read the library**
>
> **You do not read the library to answer a question; *you consult its catalogues*.**
>
> **What long context genuinely bought us**: the **retrieved-evidence window grew from 4K toward 100K** — **bigger top-K, whole-document stuffing at small scale, rerankers that read 32K**.
>
> 右栏：***Long context raised the ceiling on what retrieval may return — not on whether retrieval is needed.*** That is the **mid-2026 consensus**, and it is **a hybrid's consensus, not a partisan's**.
>
> **中文**：**幕间 · 诚实的综合**。**你不会去读整座图书馆**。**你不会为了回答一个问题去读整座图书馆；*你查它的目录*。** **长上下文真正给我们买来了什么**：**被检索证据的窗口从 4K 长到了 100K**——**更大的 top-K、小规模下可以整文档塞入、reranker 能读 32K**。
> 右栏：***长上下文抬高的是「检索可以返回多少」的天花板——而不是「是否还需要检索」。*** 这是**2026 年年中的共识**，而且它是**混合派的共识，不是党派的共识**。

- **幕间三页的结构在这里完整了**：**p.56 给证据**（NoLiMa：它做不到）→ **p.57 给经济学**（就算做得到你也付不起）→ **p.58 给诚实的综合**（但它确实买到了这些东西）。
- **⭐ 这一页不是全盘否定——它明确列出长上下文「确实买到了什么」，而且四条全都发生在「检索之后」**：

| 买到了什么 | 具体 | 发生在哪一段 |
|---|---|---|
| **证据窗口 4K → 100K** | 能塞给生成器的证据变多 | **筛子之后** |
| **更大的 top-K** | 以前只能给 5 条，现在能给二三十条 | **筛子之后** |
| **小规模整文档塞入** | 蟑螂尺度上直接塞整篇 | **筛子之后** |
| **reranker 能读 32K** | cross-encoder 输入窗口变大，能处理长文档 | **筛子内部** |

  **⭐ 用今天的词说：长上下文放松了「筛子及其之后」的约束，一点也没有动「铲子」。** 而**铲子才是那个不可逆的天花板。**

- **⭐⭐ 右栏那句是整个幕间最精确的一句**：
  > ***它抬高的是「检索可以返回多少」的天花板，不是「是否还需要检索」。***

  这是「**窗口装证据，不负责找证据**」的更精确版本——**它扩大了下游的容量，没有触及上游的召回。**

- **⭐ `a hybrid's consensus, not a partisan's`（混合派的共识，不是党派的共识）—— 这是一句关于「如何持有一个立场」的方法论注解。**
  - 它在说：**这个结论不是「RAG 阵营 vs 长上下文阵营」的胜负，而是两边都承认的地方。**
  - **这是今天反复出现的一个习惯**：**每给出一个立场，同时标注它的认识论地位**——
    - p.31：**「DCL 是小 batch 情形下本课的选择，不是普适定律」**
    - p.23：**「当反对意见的全部内容是『太贵』时，每年重审」**
    - Week 09 OKF：**「agent 改变策展经济学这个赌注仍然敞开——目前还没有生产环境的事后复盘，我们如实说出这一点」**
    - **本页：「这是混合派的共识，不是党派的共识」**
  - **一门给自己每条结论都标注确定性与边界的课，比一门只给结论的课有用得多。**
- **回到 Otlet**：***Otlet 的馆员本来可以读到任何答案，之所以建那些目录，恰恰是因为「读」不 scale。***

**可以直接拿去做决策的对照表**

| 你想干什么 | 长上下文帮不帮 |
|---|---|
| **省掉检索** | ❌ **不行** |
| 给生成器更多证据 | ✅ |
| top-K 从 5 提到 20–30 | ✅ |
| 一万份文档、单一语域、直接塞整篇 | ✅ |
| 让 reranker 处理长文档 | ✅ |


### 正课 p.59–p.60 · **POP QUIZ · INTERLUDE：Quiz 6 — the million-token bid** 与答案

> ⚠️ **p.55 未截到**（幕间开场页）。以下两页当时在课上讨论过，记录据完整 deck PDF 复原。

> **POP QUIZ · INTERLUDE**
> # **Quiz 6 — the million-token bid**
>
> *A vendor proposes **skipping retrieval**: stuff **~800K corpus tokens into every prompt at $2.50 per million input tokens**. Your cascade currently costs **$0.002–0.005 per query**.*
> ***(a)** Vendor's per-query cost, and the ratio to yours?*
> ***(b)** Even if cost were zero, **which measured phenomenon still argues against the bid**?*
> ***Say back the library argument in one sentence.***
>
> **中文**：**测验六——百万 token 的竞标**。*一家供应商提议**跳过检索**：**把约 80 万语料 token 塞进每一个 prompt，按每百万输入 token $2.50 计价**。你现在的级联是**每次查询 $0.002–0.005**。* **(a)** 供应商的单次查询成本，以及和你的比值？**(b)** **即使成本为零，仍然有哪个被测量出来的现象反对这个方案？** ***用一句话把图书馆论证说回来。***

**答案页（p.60）原文**：
> # **Two dollars a question, and the model stops reading**
>
> **(a)** **$2.00 per query — 400–1,000× the cascade, in line with the ~1,250× reference gap.**
> **(b)** **Context rot**: **NoLiMa shows most models losing half their performance by 32K once lexical overlap is gone — long before 800K.**
>
> 右栏：*You do not read the library to answer a question; you consult its catalogues. **The window is where retrieved evidence goes — it was never a substitute for deciding what deserves to be there.***
>
> **中文**：**一个问题两美元，而模型已经不再读了**。**(a) 每次查询 $2.00——是级联的 400–1,000 倍，与 ~1,250 倍这个参考差距一致。** **(b) context rot**：**NoLiMa 显示，一旦去掉词面重叠，多数模型在 32K 处就已经损失一半表现——远在 800K 之前。**
> 右栏：*你不会为了回答一个问题去读整座图书馆；你查它的目录。**窗口是被检索到的证据的去处——它从来不是「决定什么东西配待在那里」的替代品。***

**算一遍**：$800\text{K} \times \dfrac{\$2.50}{1\text{M}} = \mathbf{\$2.00}$；比值 $2.00 \div 0.005 = \mathbf{400}$、$2.00 \div 0.002 = \mathbf{1000}$。

- **⭐ (b) 这一问的设计意图：它在告诉你「成本论证是较弱的那个论证」。** 价格会降，而**质量的证据在价格归零之后依然成立**。由此可以把论证分成三个耐久度等级：

| 论证类型 | 例子 | 耐久度 |
|---|---|---|
| **结构论证** | 「运营成本 vs 资本成本，每次全额重付」（p.57） | **最耐久**——它是成本的**形状** |
| **证据论证** | 「NoLiMa 上 32K 就腰斩」 | **中等**——经验性的，**会随模型改善，必须重测** |
| **价格论证** | 「现在一次两美元」 | **最不耐久** |

- **⭐ 右栏最后那句是幕间最精确的收束之一**：***窗口是被检索到的证据的去处——它从来不是「决定什么东西配待在那里」的替代品。*** 这是「窗口装证据，不负责找证据」的升级版——**它把「找」重新定义成「决定什么配进来」。**
- **真要回应这样一个供应商，三层一起上**：① **结构**——「你是运营成本，我们是资本成本；查询量涨十倍，我们的账单涨 log，你涨十倍」；② **证据**——「请给我看你**在 NoLiMa 式探针上的准确率-长度曲线**，不是大海捞针的成绩」；③ **图书馆论证**。**并且要求在我们自己封存的 gold set 上跑，不是在你的 demo 上跑。**

### 正课 p.65 · **ACT IV · THE PROBLEM WITH TUNING THE COURT：The staircase you cannot differentiate**

> ⚠️ **p.59–64 未截到**（含 Quiz 6 答案页、**Act IV 分幕卡**、以及 RRF / 融合的开头几页）。**Act IV = 法庭。**

> **ACT IV · THE PROBLEM WITH TUNING THE COURT**
> # **The staircase you cannot differentiate**
>
> Once lanes have **weights $w_r$** and **emission depths $k_r$**, someone must choose them. But **NDCG as a function of weights is piecewise-constant** — **a staircase**: nudge a weight, **no rank flips, the metric does not move**; nudge again, **a flip, a jump**.
>
> **No gradient. Nothing to descend.**
>
> 右栏：*Grid search over a dozen lanes is **combinatorially hopeless**, and **hill-climbing on a staircase walks in circles**. The house answer is to **stop optimizing the staircase — and optimize a surrogate of it**.*
>
> **中文**：**第四幕 · 调这座法庭时遇到的麻烦**。**那道你无法求导的阶梯**。一旦每条车道有了**权重 $w_r$** 和**发射深度 $k_r$**，就得有人来选它们。但 **NDCG 作为权重的函数是分段常数的**——**一道阶梯**：轻推一下权重，**没有任何名次翻转，指标纹丝不动**；再推一下，**发生一次翻转，指标跳一格**。**没有梯度。无处可降。**
> 右栏：*在十几条车道上做网格搜索是**组合上无望的**，而**在阶梯上爬山只会原地打转**。**本课的答案是：不要去优化那道阶梯——去优化它的一个代理（surrogate）。***

- **⭐ 为什么是阶梯（机制）**：**NDCG 只依赖结果的「排序」**。权重连续变化时**分数连续变化，但排序只在离散的交叉点上改变**。所以：
  - **交叉点之间**：排序不变 → **指标完全不动 → 导数 = 0**
  - **交叉点上**：两个结果换位 → **指标跳变 → 导数不存在**
  - **⇒ 处处不是 0 就是无穷。没有可用的梯度。**

**一个具体例子**

两条车道，当前 `w_sparse = 0.50`：

| `w_sparse` | 文档 A 得分 | 文档 B 得分 | 排序 | NDCG |
|---|---|---|---|---|
| 0.50 | 0.72 | 0.70 | A > B | **0.81** |
| 0.52 | 0.73 | 0.71 | A > B | **0.81**（一模一样） |
| 0.55 | 0.74 | 0.735 | A > B | **0.81**（还是没动） |
| **0.58** | 0.75 | **0.76** | **B > A** | **0.78**（**跳了**） |

**在 0.50–0.57 之间你怎么调都没反应；到 0.58 突然跳一下。这就是那道阶梯。**

- **两条朴素的路都堵死了**：
  - **网格搜索**：十几条车道，每条有权重和深度两个参数 → **组合爆炸**（每参数取 5 个值、12 条车道就是 $25^{12}$），**而且每个点都要在 gold set 上跑一遍完整级联**。
  - **爬山法**：**平台上到处零梯度，你会原地打转。**
- **⭐ 本课的答案：代理曲面法（surrogate-surface method）**——**阶梯不可微，但「阶梯的一个光滑近似」可微。**

```
1. 在参数网格上「采样」若干点（不是穷举）
2. 每个点：在封存 gold set 上实测 NDCG
3. 用这些 (参数 → NDCG) 数据拟合一个光滑代理曲面（高斯过程 / 贝叶斯优化）
4. 在这个可微的代理上做优化，得到「下一个最值得试的点」
5. 去实测那个点，把结果加回数据集，重复
6. 全程带「配对 bootstrap 区间」——防止把 0.02 的差异当成信号
```

- **为什么贝叶斯优化正好合适**：**维度低**（十几个参数）、**每次评估很贵**（跑完整级联 + gold set）、**目标不可微**——**这三条正是 BO 的适用条件**，也正是随机搜索/网格搜索的不适用条件。
- **⚠️ 两条硬约束**：**必须在封存集上做**（否则过拟合到调参集）；**必须带配对 bootstrap 区间**（否则把噪声当改进）。
- **⭐ 与 RRF 那条「宪法」的关系**：讲义说**在 gold set 存在之前，RRF k=60 + 各车道等权就是宪法，只在有证据时修宪**。
  **这一页讲的正是「修宪的程序」**——**而修宪的前提是先有标尺。没有 gold set，这一整页都无从谈起。**


### 正课 p.66 · **ACT IV · HOUSE PRACTICE, TOLD AS METHOD：The surrogate-surface method**

> **ACT IV · HOUSE PRACTICE, TOLD AS METHOD**
> # **The surrogate-surface method**
>
> **Sample** weight vectors and per-lane depths $\theta = (w_1..w_R,\; k_1..k_R)$ at random. **Evaluate** $L(\theta) = 1 - \mathrm{NDCG@10}$ on the train split. **Fit** a linear surface $L \approx a + b^\top\theta$. **Walk** downhill on the plane; **sample again around the landing zone**. **Confirm on held-out.**
>
> 右栏：***A poor man's Bayesian optimization*** — today you would hand the same **mixed space** to **Optuna/TPE**. The permanent warning: **with a dozen lanes and a few hundred queries, the surrogate will happily overfit the sample**. ***Held-out confirmation is not optional.***
>
> **中文**：**第四幕 · 把本课的做法讲成方法**。**代理曲面法**。**采样**：随机取权重向量与各车道深度 $\theta = (w_1..w_R,\;k_1..k_R)$。**评估**：在训练划分上算 $L(\theta) = 1 - \mathrm{NDCG@10}$。**拟合**：拟一个线性曲面 $L \approx a + b^\top\theta$。**行走**：在这个平面上往下走；**在落点附近重新采样**。**确认**：在留出集上确认。
> 右栏：***这是穷人版的贝叶斯优化***——**今天你会把同样的「混合空间」直接交给 Optuna/TPE**。**长期有效的警告：十几条车道加上几百个查询，代理会很乐意地过拟合样本。** ***留出集确认不是可选项。***

- **五个动词就是五个步骤**：**Sample → Evaluate → Fit → Walk → Confirm**，循环执行。
- **`L(θ) = 1 − NDCG@10`** —— 转成「越小越好」，因为优化器习惯最小化。
- **⭐ 为什么一个「线性」代理就够用（这是最反直觉、也最实用的一点）**：
  - 阶梯在**局部**看是噪声，**但趋势是存在的**。
  - **线性拟合抓的不是曲面的精确形状，而是「哪个方向大体上更好」。**
  - **代理不需要准确，只需要有方向性**——它只负责告诉你**下一步该往哪走**，然后你**在落点附近重新采样、重新拟合**。
  - 这就是为什么它敢自称 **poor man's（穷人版）**——粗糙，但方向对。
- **`mixed space`（混合空间）指的是**：**权重 $w_r$ 是连续的，深度 $k_r$ 是整数的**。**TPE（Tree-structured Parzen Estimator）原生支持这种混合参数空间**，这正是幻灯点名 **Optuna** 的原因。
- **⚠️ 那条「长期有效的警告」为什么严重**：
  - 参数维度约 **24 个**（12 条车道 × 2 个参数），而 gold set 只有**几百个查询**。
  - **每个采样点的 NDCG 本身带噪声** → **线性拟合会把噪声当成趋势**。
  - **`Held-out confirmation is not optional.`** —— 这门课很少用这种措辞（上一次是 p.34 的 **recall@500 … No exceptions**）。**出现这种句式的地方，都是它认为「省掉就会静默失效」的地方。**
- **📝 一处自我更正**：我在 p.65 的记录里把这套方法描述成了「高斯过程 / 贝叶斯优化」——**幻灯给出的 house method 其实更简单：一个线性曲面**；**贝叶斯优化（Optuna/TPE）是它点名的「现代替代品」，不是 house method 本身。** 结论方向一致，但精度上以幻灯为准。

**落到代码的形状**

```python
import optuna

def objective(trial):
    theta = {
      **{f"w_{r}": trial.suggest_float(f"w_{r}", 0.0, 2.0) for r in lanes},
      **{f"k_{r}": trial.suggest_int(f"k_{r}", 50, 800) for r in lanes},   # ← 混合空间
    }
    return 1 - ndcg_at_10(run_cascade(theta), train_split)

study = optuna.create_study(direction="minimize")   # TPE 是默认采样器
study.optimize(objective, n_trials=200)

# ★ 不可省略的一步
confirm(run_cascade(study.best_params), held_out_split, paired_bootstrap=True)
```


### 正课 p.67 · **ACT IV · BEFORE ANY JUDGE SPEAKS：Parent-level dedup — then MMR**

> **ACT IV · BEFORE ANY JUDGE SPEAKS**
> # **Parent-level dedup — then MMR**
>
> After fusion, the docket holds **the same source photocopied**: its factoid, its QA decoy, its rewrite, its summary — **all children of one chunk**. **Cosine dedup and MMR compare surface forms; a question and its paragraph do not look alike.**
>
> So **collapse by source-chunk id first**, keeping the best-ranked representative.
>
> 右栏：***MMR diversifies surface forms; parent-level dedup collapses identities.*** **You need both, and dedup goes first** — ***it is also the archaeology of top-K, performed at runtime on every query.***
>
> **中文**：**第四幕 · 在任何法官开口之前**。**先做父级去重——然后才是 MMR**。融合之后，案卷里装着**同一个源的许多份复印件**：它的 factoid、它的 QA 诱饵、它的改写、它的摘要——**全都是同一个 chunk 的孩子**。**余弦去重和 MMR 比的是「表面形态」；而一个问题和它对应的段落，长得一点都不像。** 所以**先按 source-chunk id 折叠**，只保留排名最好的那一个代表。
> 右栏：***MMR 让「表面形态」多样化；父级去重折叠的是「身份」。*** **两个都要，而且去重在前**——***它同时也是 top-K 考古学，只不过是在运行时、对每一次查询执行的。***

- **⭐ 为什么余弦去重救不了这个（关键，且很容易想错）**：

| | 文本 |
|---|---|
| **QA pair** | 「续保要提前多久通知？」 |
| **源 chunk** | 「本条款所述之通知期为三十（30）日。该期间自续期基准日起算……」 |

  **这两者的余弦可能只有 0.4** —— **余弦去重完全不会认为它们重复。** 但**它们指向同一个源，却各占一个席位。**
  **一个问题和它的答案，在向量空间里本来就不该长得像**（那正是 QA pair 有用的原因）——**所以恰恰是最有用的那件派生物，最躲得过相似度去重。**

- **⭐ 解法是用「身份」而不是「相似度」**：**按 `source_chunk_id` 折叠。**
  - **这给了 back-pointer 第三项职责**（p.42 只说了两项）：

| 职责 | 用在哪 |
|---|---|
| ① **引用** | 生成时可点击、可审计 |
| ② **失效键** | 源变更时反向走出处图 |
| **③ 运行时去重键** | **本页：折叠同一个源的多个化身** |

- **⭐ 右栏那组区分要背下来**：

| | 比什么 | 消除什么 |
|---|---|---|
| **MMR** | **表面形态** | **内容冗余**——两段不同的文字在讲同一件事 |
| **父级去重** | **身份** | **同一个源的多个化身** |

- **⭐ 为什么顺序不能反**：**如果先跑 MMR，MMR 会把那几种不同形态当作「多样性」而主动保留它们**——**它会保护冗余。** 必须**先按身份折叠**，MMR 才能在**真正不同的源之间**做多样化。
- **⭐⭐ 最后一句是全页最妙的**：***它同时也是 top-K 考古学，只不过在运行时执行。***
  - **离线的考古学（p.48）**：追溯是为了**统计**——哪类派生物赢得多。
  - **运行时的父级去重（本页）**：追溯是为了**折叠**——同一个源只留一个席位。
  - **同一个机制，两种用途。**
  - **⭐ 实用推论：只要你实现了父级去重，考古学的数据就已经在手里了**——你每次查询都已经拿到了 `artifact_type` 和 `source_chunk_id`，**只差把它们写进一条日志。考古学几乎是免费的。**
- **成本论证**：讲义原话——**一个被塞了同一段落五套戏服的 reranker，浪费了五个席位**；而 **cross-encoder 的席位是整条级联里最贵的资源**（p.20 时钟预算：一到几百毫秒）。


### 正课 p.68 · **ACT IV · WHICH TEXT FACES THE SUPREME COURT：The decoy's job ends at retrieval**

> **ACT IV · WHICH TEXT FACES THE SUPREME COURT**
> # **The decoy's job ends at retrieval**
>
> The QA decoy **was manufactured to resemble questions** — so a cross-encoder scoring query-vs-decoy **certifies only that the bait resembles the hook**. **A verdict on the decoy is void.**
>
> **Every derivative candidate is resolved to its source text before reranking. The cross-encoder judges evidence, never bait.**
>
> 右栏：***One honest exception**: a summary retrieved **for a thematic query** is **genuinely the evidence at its altitude** — **rerank it as itself**. **Granularity needs quotas or routing; a passage-relevance judge misjudges altitude.***
>
> **中文**：**第四幕 · 哪一段文本站上最高法院**。**诱饵的任务在检索环节就结束了**。那个 QA 诱饵**本来就是为了像问题而被制造出来的**——所以让 cross-encoder 去给「query 对 诱饵」打分，**它只能证明「饵像钩」**。**对诱饵作出的判决是无效的。** **每一个派生候选在重排之前，都要被解析回它的源文本。cross-encoder 审判的是证据，永远不是饵。**
> 右栏：***一个诚实的例外***：一段为**主题查询**而检索到的摘要，**在那个高度上它本身就是证据**——**就按它自己重排**。**粒度需要配额或路由；一个「段落相关性」的法官会误判高度。**

- **⭐ 论证比讲义更精确。** 讲义说的是「一座在盘问自己下的饵的法庭」（比喻）；**幻灯给出了机制**：
  > **那个 decoy 是「为了像问题」而被制造的。所以它当然像问题。这个分数不携带任何关于「这份文档能不能回答问题」的信息。**
  - **所以 `A verdict on the decoy is void` 不是说「不准确」，是说「结构上无意义」**——**同义反复。**
- **做法**：**每个派生候选在重排前解析回源文本。**
  - **⭐ 注意这和上一页（父级去重）其实是同一步的两面**：先按 `source_chunk_id` 折叠，然后**取那个 source 的原文**送去重排。**back-pointer 又一次是承重件。**
- **⭐⭐ 右栏那个「诚实的例外」是讲义里没有的，很值得记**：

> **一段为主题查询检索到的摘要，本身就是那个高度上的证据——按它自己重排。**

  - **为什么是例外**：**QA decoy 是替身**，它指向别处；**而摘要对一个主题查询来说，就是答案本身**。用户问「客户对合规的顾虑是什么」，**答案就是那段摘要，不是任何单个 chunk**——**把它解析回源反而是错的**（你会用一个段落去回答一个需要汇总的问题）。
  - **判据是「高度」**：

| 派生物 | 面对什么查询 | 重排什么 |
|---|---|---|
| **QA pair / factoid / rewrite** | 任何 | **解析回源** |
| **summary** | **主题查询** | **⭐ 就按它自己** |
| summary | 点查询（已经落错高度） | 应当被路由挡在外面 |

  - **一句话判据：如果它「在这个查询的高度上就是证据」，按自己重排；如果它只是「指向证据的替身」，解析回源。**

- **⭐ 最后一句是一条独立且很实用的警告**：***Granularity needs quotas or routing; a passage-relevance judge misjudges altitude.***
  - **cross-encoder 是被训练来判断「这个段落和这个问题相关吗」的。** 它**没有**被训练来比较「一段摘要」和「一个段落」**哪个高度更适合这个问题**——它对**文本长度与形态**有偏好。
  - **如果你把 5 个 chunk 和 3 个摘要混在一起丢给它排，它给出的顺序反映的是「它更偏好哪种文本形态」，不是「哪个高度更对」。**
  - **两条解法**：
    1. **配额（quotas）**：top-10 里硬性保留 N 个摘要位、M 个 chunk 位
    2. **路由（routing）**：在检索之前就决定这次查询走哪个高度
  - **不要指望 reranker 自己搞定粒度——它不是为这件事训练的。**


### 正课 p.70 · **ACT IV · MAKING THE VERDICT MEAN SOMETHING：Calibration at the exit**

> ⚠️ **p.69 未截到。**

> **ACT IV · MAKING THE VERDICT MEAN SOMETHING**
> # **Calibration at the exit**
>
> **The moment anything downstream thresholds on the final score** — a "sufficient evidence" gate, an abstention rule — **you are betting the number means what it says. Raw reranker logits do not.**
>
> **Platt scaling or isotonic regression on a held-out set turns scores into probabilities you may threshold.**
>
> 右栏：***Decisions first, probabilities only if calibrated.*** **An uncalibrated 0.92 waving a hallucinated answer through the grounding gate is *the cascade's last and quietest failure mode*.**
>
> **中文**：**第四幕 · 让判决真的意味着什么**。**出口处的校准**。**只要下游有任何东西开始拿这个最终分数去卡阈值**——一道「证据是否充分」的门、一条弃权规则——**你就是在赌「这个数字真的是它字面的意思」。而原始的 reranker logit 并不是。** **在留出集上做 Platt 缩放或保序回归，才能把分数变成「可以拿来卡阈值的概率」。**
> 右栏：***先谈决策，只有校准之后才谈概率。*** **一个未经校准的 0.92 挥着一个幻觉答案通过了 grounding gate——这是整条级联*最后、也最安静*的失效模式。**

- **⭐ 什么时候需要校准，什么时候不需要（幻灯的第一句就是判据）**：

| 你拿分数干什么 | 需要校准吗 |
|---|---|
| **只用来排序**（top-10 交给生成器） | **❌ 不需要**——排序只需要单调性 |
| **拿去卡阈值**（充分性门、弃权规则、`if score > X`） | **✅ 必需**——你在把分数当概率用 |

  **校准是在你开始「把分数当概率」的那一刻才成为必需的。**

- **⭐ 为什么原始 logit 不行**：cross-encoder 的输出是训练目标的副产品，**它只保证「更相关的排更前」（单调性），不保证「0.92 意味着 92% 的可能性相关」**。**不同模型、不同版本、不同领域，同一个 0.92 含义完全不同**——**这就是 p.20 那条「0.7 在不同模型上是不同的光圈」在出口处的版本。**
- **两个方法怎么选**：

| 方法 | 做什么 | 何时用 |
|---|---|---|
| **Platt 缩放** | 拟一个 sigmoid：$p = \sigma(a\cdot s + b)$，**只有两个参数** | **数据少**；假设分数分布近似 logistic |
| **保序回归（isotonic）** | 拟一个**单调非减的阶梯函数**，不假设形状 | **数据多**；更灵活，但**容易过拟合** |

- **⭐⭐ 右栏是全页最重的一句，也是今天「静默失效」清单的最后一条**：
  > **一个未经校准的 0.92 挥着幻觉答案通过 grounding gate——最后、也最安静的失效。**
  - **为什么「最后」**：它发生在级联的**最末端**，所有法官都已判完。
  - **为什么「最安静」**：**没有任何东西会报错。** 分数 0.92，门槛 0.8，通过。**系统认为一切正常。**

- **⭐ 全天的静默失效清单（到这里齐了）**：

| 页 | 静默失效 |
|---|---|
| p.27 | **赤道带静默填满 top-K**——14 个陌生人进了上下文 |
| p.34 | **铲子静默腐烂**——仪表盘变绿，128 维召回塌了 |
| p.43 | **装着答案的段落静默被丢弃**——0.64 vs 阈值 0.7 |
| p.45 / p.50 | **幻影簇 / 幻影概念带着 `verified` 静默晋升** |
| **p.70** | **未校准的 0.92 静默放行幻觉** |

  **⭐ 而 p.53 的成本爆炸是今天唯一「响亮」的失效。**
  **规律：成本类故障是响的，质量类故障是哑的——所以前者你会自动修好，后者只能靠纪律。**

**实操**

```
1. 在留出集上跑完整级联，收集 (最终分数, 是否真的相关) 数据对
2. 拟 Platt 或 isotonic
3. 之后所有阈值都设在「校准后的概率」上，不再设在原始分数上
4. ⚠️ 换模型 / 换版本 / 换领域 → 重新校准
5. 定期重测校准曲线，监控漂移
```

- **和「弃权」的关系**：**弃权规则要求「我有多确定」这个数字可信。** 没有校准，**你的弃权门槛就是任意的**——你不知道 0.7 到底意味着「大概率对」还是「五五开」。


### 正课 p.71 · **ACT IV · THE WHOLE COURT, WITH NUMBERS：The reference cascade**（⭐ 参考级联全表）

> **ACT IV · THE WHOLE COURT, WITH NUMBERS**
> # **The reference cascade**

| STAGE | COURT | INSTRUMENT | EMITS |
|---|---|---|---|
| **1a** | **district**（地区法院） | **SPLADE sparse scoop** | **100** |
| **1b** | **district** | **Matryoshka-128 dense scoop** | **500** |
| **2** | **appeals**（上诉法院） | **full-dim rescore of 1b** | **250** |
| **3** | **high**（高等法院） | **ColBERT MaxSim filter** | **100** |
| **4** | **—** | **RRF fusion of lanes** | **~150** |
| **5** | **—** | **parent-level dedup, then MMR** | **~100** |
| **6** | **supreme**（最高法院） | **cross-encoder on *source text*** | **20–30** |

> 底部：*The numbers are illustrative; **the architecture is the invariant, the numbers are the variables** — retuned by the surrogate surface against **your own gold set**. Output: **20–30 seats in the generator's context window**.*
>
> **中文**：*这些数字只是示意；**架构是不变量，数字是变量**——由代理曲面法针对**你自己的** gold set 重新调出来。输出：**生成器上下文窗口里的 20–30 个席位。***

- **⭐ 法院层级的命名很精确，而且第 4、5 级「没有法院」这件事本身是信息**：
  - **有法院的**（1a/1b 地区、2 上诉、3 高等、6 最高）= **在做相关性判断**
  - **没有法院的**（4 融合、5 去重+MMR）= **不判断，只整理案卷**——**合并与折叠，不评判相关性**
  - **这条区分很有用**：**融合与去重是「行政程序」，不是「审判」。**
- **⭐⭐ 数字里最值得琢磨的一点：级联是「嵌套」的。**
  - 表面上看 SPLADE 只发 100、而 dense 发 500，似乎与讲义那句「稀疏车道发得略深，因为它最便宜」矛盾。
  - **实际上 1b → 2 → 3 是 dense 车道自己内部的一条三级级联**：

```
Matryoshka-128 铲   500   （极便宜，所以敢铲 5 倍深）
  → 全维复评        250   （中等成本，砍一半）
  → ColBERT MaxSim  100   （贵，只留 100）
```

  - **也就是说：到融合时，稀疏贡献 ~100，dense 也贡献 ~100——两条车道在融合处是平衡的。**
  - **dense 车道之所以能从 500 起步，正是因为它的铲子（128 维）便宜到离谱**——**这就是 Matryoshka 那条「维度是成本旋钮」在架构上的兑现。**
- **⭐ 融合后是 ~150 而不是 200，这个数字本身是诊断信号**：**两条车道重叠了约 25%。**
  - **如果重叠 90%，其中一条就没有存在必要**（p.10 蜻蜓推论：**失效相关的两个索引，加起来等于一个**）。
  - **⇒ 可以把「融合前后的候选数比值」当作一个廉价的车道冗余度指标。**
- **⭐ 底部那句是本页的教条，也直接接上 p.65–66**：
  > **架构是不变量，数字是变量。**
  - **哪些级、什么顺序 = 给定的**（这一页）
  - **每级发多少 = 调出来的**（p.65 的阶梯问题 + p.66 的代理曲面法）
  - **而调的依据必须是你自己的 gold set。**
- **与 p.58 的连接**：长上下文把「被检索证据的窗口」从 4K 推到 100K——**也就是说它放宽了 stage 6 的输出可以有多大，而前面五级一点没变。**
- **延迟预算对照（p.20 的时钟）**：**1a/1b 并行，各数十毫秒；4/5 个位数毫秒；2 数十毫秒；3 中等；6 一到几百毫秒 → p95 保持在一到两秒以内。**


### 正课 p.72 · **POP QUIZ · ACT IV：Quiz 7 — the incommensurable scoreboard**

> *Three top-hit scores: **SPLADE 12.4, cosine 0.83, MaxSim 41.7**. Which normalization lets you sum them into one fused score?*
> *(a) min–max to [0,1] (b) z-score per lane (c) divide by lane max (d) softmax per lane*
> ***Decide — and defend your choice.***

**答案：以上皆不。不要归一化——按名次融合（RRF）。** 标题就是提示：***incommensurable***（不可通约）。

- **⭐ 最深的一层：这道题根本算不出来。** 四种归一化各自还需要「整条车道的分布」（min/max、均值与标准差、最大值、全部分数 + 一个温度），**而你只有三个孤立的数字**。**RRF 只需要名次——这才是它真正的优势：它不需要你知道分布。**
- **逐条**：
  - **(a) min–max**：**把每条车道的最好那个强行拉到 1.0** —— 一条车道这次**完全没找到好东西**，它的第一名照样是 1.0。**抹掉了「这条车道这次靠不靠谱」。**
  - **(c) 除以最大值**：同病，更脆——**整条车道被单个异常高分压扁。**
  - **(d) softmax per lane**：**① 温度 τ 是凭空选的**（未调超参）；**② softmax 强制每车道分数和为 1 → 候选越多每个分数越小**，而参考级联里 **1a 发 100、1b 发 500** → **结构性不可比。**
  - **(b) z-score**：**四个里最站得住的**，但假设分数近似正态（**检索分数是重尾的**），且均值/标准差随查询漂移。
- **RRF 实算**：三条车道都排第一 → $3 \times \frac{1}{61} = 0.0492$；另一份排 1/5/10 → $\frac{1}{61}+\frac{1}{65}+\frac{1}{70} = 0.0461$。**全第一只高 7%——这就是 k=60 在阻尼头部。**
- **分阶段立场**：**没有 gold set → RRF k=60 等权是宪法**；**有 hold-out → 学习式融合（归一化 + 凸权重）可以打败 RRF**（Bruch et al. 2023 正是研究这个的，且讲义引了它）。**要选一个配学习式融合，选 (b)。**

---

### 正课 p.74 · **POP QUIZ · ACT IV：Quiz 8 — the decoy that testified**

> *A QA decoy — **"What is the notice period for termination?"** — wins retrieval, **answer and source-chunk id in its payload**. **What goes to the cross-encoder against the user's query?***
> *(a) the decoy question (b) the payload answer (c) decoy + answer concatenated (d) the contextualized rewrite of the clause*
> ***Choose, and justify with the doctrine.***

**答案：仍然是「以上皆不」。应当送去的是 `source_chunk_id` 指向的那段原始条款文本。**

- **⭐ 连续两道题，正确答案都不在选项里——这是刻意的：四个选项全都是「听起来很合理的派生物」。**
- **逐条为什么错**：

| 选项 | 它是什么 | 为什么错 |
|---|---|---|
| **(a) 诱饵问题本身** | 派生物 | **p.68**：诱饵是「为了像问题」而造的，**评它只证明「饵像钩」——判决无效** |
| **(b) payload 里的答案** | 派生物 | 抽取出来的短答案，**不是源，也不能被引用** |
| **(c) 诱饵 + 答案拼接** | 两个派生物 | **拼起来还是派生物** |
| **(d) ⭐ 条款的语境化改写** | **派生物（最像证据的那个）** | **这是陷阱**——rewrite 读起来最像原文，**但它是被制造的**；讲义那个「**丢掉了 `irrevocable` 的法律改写**」正是它，**「那不是证据，那是饵」** |

- **教条依据（p.68 + p.42）**：***每一个派生候选在重排之前都被解析回它的源文本。cross-encoder 审判的是证据，永远不是饵。***
- **p.68 那个「诚实的例外」在这里不适用**：例外只给**「为主题查询检索到的摘要」**；而这里是**点/语境查询**，胜出的是 **QA 诱饵**，不是摘要。
- **⭐ 完整的数据流（两边都要回到「原件」）**：

```
用户原话:  「员工离职的通知期是多久？」
  ↓ 检索（各车道拿到的是「规范化后的 query」）
命中 QA decoy #8801
     text  = "What is the notice period for termination?"   ← 被 embed 的那个
     payload.answer         = "30 days"
     payload.source_chunk_id = chunk_4471                    ← ★ 承重件
  ↓ 父级去重（按 source_chunk_id 折叠）
  ↓ 解析回源，取出 chunk_4471 的原文
  ↓ cross-encoder( 用户原话 , chunk_4471 原文 )
```

  - **文档侧回到「源文本」**（本页）
  - **查询侧回到「用户原话」**（讲义：*规范化 query 送给各车道，原始 query 用于 cross-encoder 审判*）
  - **⭐ 两条合起来才是完整教条：`Transform for retrieval; judge against the truth.`（为检索而变换；对着真相审判。）**


### 正课 p.78 · **MILESTONE · ACT V OF VII：The Question Side**（分幕卡）

> **MILESTONE · ACT V OF VII**
> # **The Question Side**
>
> ***Half the architecture stands on the query's side of the glass.***
>
> **中文**：**里程碑 · 第五幕（共七幕）**。**问题这一侧**。***有一半的架构，站在玻璃的「查询」那一侧。***
>
> 配图：**一个点向下扇形散开成许多分支的倒置树**——**一个查询扇出成多个子查询**（对应 p.79 的 decompose / multi-query fan-out）。

- **七幕结构现在已知六幕**：Act I 仪器柜 · Act II 被训练的仪器 · Act III 派生语料库 · Act IV 法庭 · **Act V 问题侧** · Act VI 机房/索引迁移（由 p.35 得知）· Act VII 待定（大概率是 **Playbook**）。

---

### 正课 p.79 · **ACT V · THE PARETO FRONT OF BROKEN QUERIES：Six pathologies, six verbs**

> **ACT V · THE PARETO FRONT OF BROKEN QUERIES**
> # **Six pathologies, six verbs**
>
> - **Surface errors** — typos degrade subword embeddings → **correct**
> - **Context starvation** — the follow-up **equidistant from everything, close to nothing** → **inject**
> - **Jargon opacity** — "CCAR" goes searching for its own meaning → **expand**
> - **Compositional complexity** — **three questions wearing one trench coat** → **decompose**
> - **Semantic vagueness** — **a wish, not a query** → **sharpen**, or HyDE
> - **Temporal ambiguity** — "the latest policy": **as of when?** → **resolve**
>
> 底部：*Each pathology gets a verb, each verb a stage. **The pipeline is complete when every pathology has a stage that addresses it.***
>
> **中文**：**第五幕 · 坏查询的帕累托前沿**。**六种病理，六个动词**。**表层错误**——拼写错误会破坏子词切分 → **纠正**。**上下文饥饿**——那句追问**对一切都等距，因而离一切都不近** → **注入**。**术语不透明**——「CCAR」自己出门去找自己的含义 → **展开**。**复合复杂度**——**三个问题穿着同一件风衣** → **拆解**。**语义含糊**——**这是一个愿望，不是一个查询** → **锐化**，或者用 HyDE。**时间歧义**——「最新的政策」：**截至什么时候？** → **解析**。
> 底部：*每一种病理配一个动词，每一个动词配一个阶段。**当每一种病理都有一个阶段在处理它时，这条流水线才算完整。***

- **⚠️⚠️ 重要：幻灯这六个和讲义那六个不完全一样。** 对照表：

| # | **讲义的六种** | **幻灯的六种** | 变化 |
|---|---|---|---|
| 1 | Misspelled → **correct** | **Surface errors** → **correct** | 同 |
| 2 | Underspecified → **expand** | **Jargon opacity** → **expand** | **收窄成「缩写/术语」这个具体子类** |
| 3 | Overloaded → **decompose** | **Compositional complexity** → **decompose** | 同 |
| 4 | Ambiguous → **disambiguate** | **Semantic vagueness** → **sharpen / HyDE** | 换了角度：从「歧义」变成「含糊」 |
| 5 | Register-mismatched → **rewrite** | — | **⚠️ 幻灯没有** |
| 6 | Multi-hop → **plan** | — | **⚠️ 幻灯没有** |
| — | — | **Context starvation → inject** | **⭐ 新增** |
| — | — | **Temporal ambiguity → resolve** | **⭐ 全新，讲义完全没有** |

  **⇒ 记住两套：幻灯的六个 + 讲义额外的两个（rewrite、plan），合起来是八种。**

- **⭐⭐ `Context starvation` 是「查询侧的质心稀释」——这是全页最漂亮的一个连接**：
  - 那句 ***equidistant from everything, close to nothing***（对一切都等距，因而离一切都不近）**在几何上，和 p.43 的柏林实验是同一个现象**：
    - **p.43 文档侧**：一段话包含五个意思 → 向量落在**质心** → **离每一个顶点都远**
    - **p.79 查询侧**：一句空洞的追问（「那第二种情况呢？」）→ 向量落在**质心** → **离每一份文档都不近**
  - **同一个几何病，两侧对称。文档侧的解药是 factoid（拆细）；查询侧的解药是 inject（注入会话上文、用户身份、当前所在文档）。**
- **逐条例子**：

| 病理 | 例子 | 机制 / 修法 |
|---|---|---|
| **Surface errors** | `recieve` / `retreival` | **拼写错误会改变 subword 切分** → embedding 位置漂移；稀疏车道更惨（倒排表直接不匹配）。**最便宜、确定性、最先做。** |
| **Context starvation** | 「那第二种情况呢？」 | 信息几乎全在**会话历史**里，不在句子里 → **注入上文** |
| **Jargon opacity** | 「CCAR」（= Comprehensive Capital Analysis and Review） | 用户打缩写，语料里写全称 → **展开缩写** |
| **Compositional complexity** | 「A 政策什么时候生效、适用哪些岗位、和 B 政策冲突吗？」 | **三个问题一个问号** → 拆开分别检索再合并（**p.78 那张扇形图**） |
| **Semantic vagueness** | 「我想让审批流程快一点」 | **这是诉求，不是问题** → **锐化**成可检索的问题，或用 **HyDE** 捏一个假想答案去 embed |
| **Temporal ambiguity** | 「最新的政策」 | 语料里有 2024/2025/2026 三版；而且「最新」可能指**文档最新**，也可能指**某事件发生时最新** → **解析时间锚点** |

- **⭐ `Temporal ambiguity` 直接连到 Week 09 的 OKF**：`stale_after`、`verified` 时间戳、「这是什么时候的快照」。**时间锚点在查询侧（本页）和语料侧（governed concept）都需要——两边都要能回答「as of when」。**
- **⭐ 分幕标题 `THE PARETO FRONT OF BROKEN QUERIES`（坏查询的帕累托前沿）用词很准**：**帕累托前沿意味着这六种互不支配**——**你不能用一种病理的解法去覆盖另一种**。**它们各自占据一个不可替代的维度。**
- **⭐ 底部那句是完整性判据，也是一张检查表**：
  > **当每一种病理都有一个阶段在处理它时，这条流水线才算完整。**
  - **不是「我们做了 query rewriting」**，而是**「六种病理，逐一点名，每一种都有归属」**。
  - **这和讲义的「消融门」是同一种精神**：**用「它防住了哪具尸体」来证明一个阶段的存在合理性。**


### 正课 p.80 · **ACT V · THE PIPELINE OF UNDERSTANDING：The transformation cascade**

> **ACT V · THE PIPELINE OF UNDERSTANDING**
> # **The transformation cascade**
>
> **Stages ordered cheap to expensive, with short-circuiting**: **spell → context injection → acronym expansion → rewrite/expand → decomposition → HyDE as last resort.**
>
> **Two passes around the guardrails: deterministic fixes *before*, LLM-assisted rewriting *after*** — **never amplify adversarial content pre-screening.**
>
> 右栏：*The output is the **canonized query** — and **it, not the raw string, is the semantic-cache key**. **"WFH policy" and "remote work policy" must converge *before* the cache, or the second user misses.***
>
> **中文**：**第五幕 · 理解的流水线**。**变换级联**。**各阶段按由便宜到昂贵排序，并且可以短路**：**拼写 → 上下文注入 → 缩写展开 → 改写/扩展 → 拆解 → HyDE（最后手段）。** **围绕护栏要分两趟走：确定性修复在护栏*之前*，LLM 辅助的改写在护栏*之后***——**绝不要在预筛之前放大对抗性内容。**
> 右栏：*它的输出叫**规范化查询（canonized query）**——**而作为语义缓存的键的，是它，不是原始字符串。** **「WFH policy」和「remote work policy」必须在进缓存*之前*就收敛，否则第二个用户就会 miss。***

- **六级流水线，成本递增，且每级都能短路**：

| 级 | 动作 | 成本 | 类型 |
|---|---|---|---|
| 1 | **拼写纠正** | 极低 | **确定性** |
| 2 | **上下文注入** | 低 | **确定性**（拼接会话上文） |
| 3 | **缩写展开** | 低 | **确定性**（查表） |
| 4 | **改写 / 扩展** | 中 | **LLM** |
| 5 | **拆解** | 高 | **LLM** |
| 6 | **HyDE** | **最高** | **LLM**，最后手段 |

  **讲义的配套原则：*每一级都应该能短路掉其余各级——大多数 query 只需要第一级。***
  **前三级确定性 / 后三级需要 LLM，这就是成本的分界线。**

- **⭐⭐ 「围绕护栏的两趟」是这一页最重要、也最容易被漏掉的工程细节**：

```
原始 query
  → ① 确定性修复（拼写 / 缩写表 / 上下文拼接）—— 纯查表，不可被注入
  → ★ 护栏预筛（检测注入、恶意、越权意图）
  → ② LLM 辅助改写（此时输入已经被审查过）
  → 检索
```

  - **为什么顺序不能反**：如果先让 LLM 去改写一段注入攻击，**LLM 可能「执行」它而不是改写它**；即便不执行，**改写也会把一段模糊的恶意输入变成一段清晰、通顺、更有效的恶意输入。**
  - **`amplify`（放大）这个动词很准**——**危险不在于 LLM 会漏掉恶意内容，而在于它会把恶意内容「优化」得更好用。**
  - 这条直接接上护栏那几周：**把每一份被摄取/输入的内容当作不可信的代码。**

- **⭐ 输出的名字是 `canonized query`（规范化 / 正典化查询）**，而它有**两个**用途；**原始 query 有一个**：

| 送什么 | 送到哪 | 为什么 |
|---|---|---|
| **canonized query** | **各条检索车道** | 让所有车道**对同一个问题**投票 |
| **⭐ canonized query** | **语义缓存的键** | **本页新增** |
| **原始 query（用户原话）** | **cross-encoder 审判** | 让一次漂离用户意图的变换**无法通过法庭把自己洗白** |

  **合起来仍是那句：`Transform for retrieval; judge against the truth.`**

- **⭐ 右栏的缓存论证很具体，而且是一个非显然的架构决定**：

| 缓存键放在哪 | 后果 |
|---|---|
| **原始字符串** | **命中率极低**——每个人措辞都不一样 |
| **⭐ 规范化查询** | **不同措辞收敛后命中同一个键** |

  **例子**：「WFH policy」与「remote work policy」——**必须在进缓存之前收敛**，否则**第二个用户会 miss**，你为同一个问题付两次钱。
  **这直接预告了下周的主题：语义缓存——这栋房子的前门。**

- **📝 与讲义的一处差异**：讲义的变换级联里有一个**显式的「分类」阶段**（*再分类——哪种病理、哪个高度、哪条路由*），**幻灯这六级没有列出来**。它可能被并进了 rewrite/expand，也可能出现在下一页（路由）。**待后续页确认。**


### 正课 p.81 · **ACT V · THE LAST RESORT, AND ITS GEOMETRY：HyDE — the document-shaped probe**

> **ACT V · THE LAST RESORT, AND ITS GEOMETRY**
> # **HyDE — the document-shaped probe**
>
> **Ask an LLM to *answer* the question first; embed the *fabricated answer*; search with that.** **The hallucinated answer lands in Seattle — the real documents are in the nearby suburbs. Wrong in the particulars, right in the register.**
>
> 右栏：*HyDE crosses the **query–document register gap** by **generating the missing side** — **the online twin of the offline QA pair: one principle, two timings**. It is also **the costliest stage** and **playing with fire on factual precision: last resort, not default.***
>
> **中文**：**第五幕 · 最后手段，以及它的几何**。**HyDE——文档形状的探针**。**先让 LLM 把这个问题「答」一遍；把那个*捏造出来的答案* embed；用它去检索。** **那个幻觉出来的答案落在了西雅图——而真正的文档在附近的郊区。细节全错，但语域对了。**
> 右栏：*HyDE 通过**生成缺失的那一侧**来跨越**「查询—文档」的语域鸿沟**——**它是离线 QA pair 的在线孪生兄弟：一条原理，两个时机。** 它同时也是**最昂贵的一级**，而且是**在事实精度上玩火：最后手段，不是默认选项。***

- **机制**：`用户问题 → 让 LLM 先「编」一个答案 → embed 那个编造的答案 → 用它去检索`
  - **为什么管用**：**你的索引里装的是文档（散文形状），而查询是问题形状。** 用一个**文档形状的探针**去探一个**文档形状的索引**——**形状对上了。**
- **⭐⭐ 「西雅图 / 郊区」这个比喻把机制说透了**：
  - LLM 编的答案里，**具体事实可能全是错的**（编了不存在的条款号、错的数字）——**这是「细节全错」**。
  - **但它的措辞、句式、术语、语域是对的**——**所以它在向量空间里落在了正确的邻域，只是不在正确的那个点上。**
  - **⭐ 而检索要的正是「邻域」，不是「点」。** **你不需要探针本身是正确答案，你只需要它落在正确答案附近**——最近邻搜索会把你从市中心带到郊区的那栋房子。
- **⭐⭐ 右栏最好的一句：`the online twin of the offline QA pair`（离线 QA pair 的在线孪生兄弟）——一条原理，两个时机。**

| | **QA pair（写时）** | **HyDE（读时）** |
|---|---|---|
| **生成哪一侧** | **生成「问题」侧** | **生成「文档」侧** |
| **放在哪** | **放进索引** | **用作探针** |
| **何时执行** | **离线，每个 chunk 一次** | **在线，每次查询一次** |
| **成本类型** | **⭐ 资本支出（一次性）** | **⭐ 运营支出（每次全额重付）** |

  - **两者是镜像：都在「通过生成缺失的那一侧来消除语域错配」。**
  - **⭐ 而这直接接上 p.57 的经济学论证**：**同一个原理，一个付一次，一个每次都付。**
  > **能用 QA pair（离线）解决的，就不要用 HyDE（在线）解决。**

- **两条警告**：
  1. **最贵的一级**——必须先跑一次完整的 LLM 生成才能开始检索，**延迟和成本都在关键路径上**。
  2. **在事实精度上玩火**——讲义原话：***一个捏造的探针可以捏造出一整个邻域。*** 如果 LLM 编的答案**连语域都偏了**（把一个法律问题编成了医学口吻的答案），**它会把你带到完全错误的邻域，而且你不会知道。**
- **`last resort, not default`** 与 p.80 的变换级联一致：**HyDE 是第六级，也是最后一级。前五级都短路不掉时才动它。**
- **可直接使用的判据**：

| 语域鸿沟的性质 | 用什么 |
|---|---|
| **结构性的、可预见的**（法律 / 临床 / 内部黑话） | **离线造 QA pair、rewrite** —— **资本支出** |
| **偶发的、无法预见的** | **HyDE** —— **运营支出，最后手段** |


### 正课 p.82 · **ACT V · THE FRONT DOOR：The semantic cache — E and τ**

> **ACT V · THE FRONT DOOR**
> # **The semantic cache — E and τ**
>
> $$\text{hit} \iff \max_i \ \text{sim}\big(E(q),\, e_i\big) > \tau$$
>
> **One embedder $E$, one threshold $\tau$ — *every cache failure you will ever debug traces to one of them*.** Two tiers: **above $\tau_{\text{full}}$, serve; between $\tau_{\text{partial}}$ and $\tau_{\text{full}}$, *do not serve* — use as a retrieval hint.**
>
> 右栏：*$\tau$ is an aperture; ***never KNN without a threshold*** — **the type-1 vs type-2 diabetes collision is one careless cone away**. Production hit rates run **20–45%** (**folklore — measure your own**), and **invalidation must track index versions**.*
>
> **中文**：**第五幕 · 前门**。**语义缓存——E 与 τ**。**一个 embedder $E$，一个阈值 $\tau$——*你将来会调试的每一个缓存故障，都能追溯到这两者之一*。** 两档：**高于 $\tau_{\text{full}}$，直接服务；介于 $\tau_{\text{partial}}$ 与 $\tau_{\text{full}}$ 之间，*不要服务*——把它当作检索提示用。**
> 右栏：*$\tau$ 是一个光圈；**绝不做没有阈值的 KNN**——**「1 型 vs 2 型糖尿病」的碰撞，只差一个粗心的锥。** 生产环境的命中率大致在 **20–45%**（**这是江湖经验——测你自己的**），而且**失效必须跟踪索引版本**。*

- **⭐ 两档设计是最实用的部分**，且与讲义那句 ***serve、hint、或 miss，绝不 guess*** 完全对上：

| 相似度 | 行为 |
|---|---|
| **> $\tau_{\text{full}}$** | **serve**——直接返回缓存的答案 |
| **$\tau_{\text{partial}}$ ~ $\tau_{\text{full}}$** | **⚠️ hint**——**不给答案**，但把那条历史查询检索到的文档拿来**预热/提示**本次检索 |
| **< $\tau_{\text{partial}}$** | **miss**——走完整流程 |

  **中间档的价值**：相似但不够相似的历史查询，**它当初捞到的文档很可能也相关**——**可以用它省掉一部分检索，但绝不能用它替代答案。**

- **⭐⭐ 那个反例极狠：「1 型 vs 2 型糖尿病，只差一个粗心的锥」**
  - 「**1 型**糖尿病的治疗方案」与「**2 型**糖尿病的治疗方案」——**在向量空间里极其接近**（几乎所有词都相同，只差一个数字），**但答案完全不同，给错会害人。**
  - **$\tau$ 稍微松一点，缓存就会把 1 型的答案返给问 2 型的人。**
  - **⭐ `never KNN without a threshold` 的机制**：**KNN 永远会返回「最近的那个」，不管它有多远。** **没有阈值，缓存就永远命中——命中的是最近的那个错误答案。**
- **⭐ 这和 p.20 的「裸 top-K」是同一个病，而且更严重**：

| | 承诺什么 | 后果 |
|---|---|---|
| **p.20 裸 top-20** | **凑满 20 个**，不管存不存在 20 个相关的 | **掺噪声**进上下文 |
| **p.82 裸 KNN 缓存** | **返回最近邻**，不管它有多近 | **⚠️ 直接给出错误答案** |

  **同一条教条：上限必须配下限。** **而缓存这一侧的后果更重——top-K 只是浪费席位，缓存是直接答错。**

- **`20–45%`，但标注了 `folklore`（江湖传说）** —— **讲师又一次给数字标注了认识论地位**（同 p.31 「不是普适定律」、p.58 「混合派的共识」）。**这不是研究结论，是行业口耳相传的经验值——测你自己的。**
- **⭐ `invalidation must track index versions`（失效必须跟踪索引版本）是最容易被漏掉的一条**：
  - **缓存里存的是「旧索引下算出来的答案」。** 一旦你**换了 embedder / 重建了索引 / 更新了语料**，**那些条目就全过期了——而它们不会自己知道。**
  - **所以缓存条目必须带索引版本号**；版本一变，**整片缓存失效或标脏**。
  - **⭐ 换个角度看会更清楚：语义缓存其实就是「查询—答案对」这件派生物。** 它和 factoid、summary 一样是从语料派生出来的，**所以同样受「源变了就要失效」的约束**——**back-pointer 那套纪律在这里第四次出现。**
  - 同时这也对应机房的**版本偏斜**教条：**一次查询绝不可跨 embedder 版本**——缓存是最容易违反这条的地方。
- **这一页就是下周的预告**：讲义说**语义缓存「值得拥有自己的一天，而它下周就会拿到」。**


### 正课 p.83 · **ACT V · SENDING THE QUERY TO THE RIGHT MACHINE：Routing, and the head/tail split**

> **ACT V · SENDING THE QUERY TO THE RIGHT MACHINE**
> # **Routing, and the head/tail split**
>
> **Classify by altitude (point / thematic / global) and modality** — structured questions go to the **text-to-SQL sidecar**, because ***you cannot retrieve your way out of a schema problem***.
>
> **Instacart's split**: the **head precomputed and cached (~98% precision)**, the **tail served by a distilled 8B model at ~300 ms**.
>
> 右栏：***Routing is also the maturity path for fusion**: **one global weight vector is a compromise across altitudes**. **The mature system classifies first, then reweights its lanes per query class.***
>
> **中文**：**第五幕 · 把查询送到正确的机器**。**路由，与头/尾分割**。**按高度分类（点 / 主题 / 全局），并按模态分类**——**结构化问题送去 text-to-SQL sidecar**，因为***你没法靠检索绕开一个 schema 问题***。**Instacart 的分割法**：**头部预计算并缓存（约 98% 精度）**，**长尾由一个蒸馏过的 8B 模型现场服务，约 300 毫秒**。
> 右栏：***路由同时也是融合的成熟路径**：**一个全局的权重向量，是跨所有高度的一个妥协**。**成熟的系统先分类，然后按查询类别给各条车道重新加权。***

- **📝 注意这里高度只列了三档**（point / thematic / global），**少了 contextual**；而正课 p.12 是四档、Prelude p.12 是五档（含 verbatim）。**路由用的是粗分类——分类器需要少而分得开的类别，不是完整的高度学。**
- **⭐ `you cannot retrieve your way out of a schema problem` 是本页最锋利的一句。**
  - 「**上季度华东区的退货率是多少？**」——**这个答案不在任何文档里，它在数据库里。** 你再怎么优化检索，也检索不出一个需要 `GROUP BY` 才能算出来的数字。
  - **这是「表征组合」的边界**：今天讲的所有派生物**都是从文本派生的**；**而有些问题的答案根本不在文本里。**
  - **⇒ 路由不只是「送到哪个索引」，还包括「送出这个系统」。**
- **Instacart 的头/尾分割，是「查询分布是重尾的」这一事实的架构兑现**：

| | 做法 | 指标 | 理由 |
|---|---|---|---|
| **head（头部）** | **离线预计算 + 缓存** | **~98% 精度** | **少数查询占大部分流量**，值得精算 |
| **tail（长尾）** | **蒸馏的 8B 模型现场服务** | **~300 ms** | **大量各不相同、每个只出现几次**，不值得预计算 |

  - **⭐ 这正是「四十道题」的工业化版本**（p.41）：那位同学收集的**四十道真题就是 head**；**Instacart 把 head 预计算到 98% 精度并缓存起来。**
  - **head 用「预计算 + 缓存」，正好接上 p.82 的语义缓存**——**缓存服务的就是 head。**

- **⭐⭐ 右栏才是这一页真正的洞见，而且它回过头去修正了 Act IV**：
  > **一个全局的权重向量，是跨所有高度的一个妥协。**

  - **p.65–66 教的是：调「一组」权重 $w_r$ 和深度 $k_r$。**
  - **这一页说：那本身就是个折中**——因为
    - **点查询**该重仓 **factoid 车道 + 稀疏车道**
    - **主题查询**该重仓 **summary 车道**
    - **全局查询**该走**图 sidecar**
    - **用同一组权重服务这三类，对每一类都不是最优。**
  - **⭐ 可执行的升级：代理曲面法要跑 N 次——每个 query class 一次，得到 N 组权重。**

- **⭐ 由此可以提炼出一条融合的成熟度阶梯**：

| 阶段 | 做法 | 前提 |
|---|---|---|
| **1** | **RRF k=60，各车道等权** | **没有 gold set 时的宪法** |
| **2** | **一组全局调优的权重**（代理曲面法） | 有 gold set |
| **3** | **⭐ 先分类，每个 query class 一组权重** | 有 gold set **且**有可靠的分类器 |

  **注意第 3 阶段的额外前提：分类器本身要够准**——**分错类的代价是「用错的权重去检索」，而且它是静默的。**


### 正课 p.84 · **ACT V · RETRIEVAL LEARNS TO REASON：The agentic turn**

> **ACT V · RETRIEVAL LEARNS TO REASON**
> # **The agentic turn**
>
> **Search-R1** trains the LLM by **RL** to **interleave reasoning with search** — **+41% over prompting**. On **BRIGHT**, the reasoning-retrieval benchmark, launch SOTA was **~18 nDCG@10 in 2024**; the leaderboard reads **66.9 by 2026**.
>
> ***Retrieval learned to reason* — marketing in 2023, a measured fact now.**
>
> 右栏：*And yet: **the loop pays its latency bill on every hop**. For most enterprise traffic — **point queries, cached heads** — **the single-shot cascade still wins**. **Route the hard residue to the agent; do not make every query pay agent prices.***
>
> **中文**：**第五幕 · 检索学会了推理**。**Agentic 转向**。**Search-R1** 用**强化学习**训练 LLM，让它**把推理与检索交错进行**——**比纯 prompting 高 41%**。在**推理-检索基准 BRIGHT** 上，**2024 年发布时的 SOTA 是约 18 nDCG@10；到 2026 年排行榜已经是 66.9。** ***「检索学会了推理」——2023 年这是营销话术，现在它是一个被测量出来的事实。***
> 右栏：*然而：**这个循环在每一跳上都要付它的延迟账单**。对大多数企业流量——**点查询、被缓存的头部**——**单发式级联仍然获胜**。**把难啃的残余送给 agent；不要让每一个查询都付 agent 的价钱。***

- **机制**：**不是「先想好，再搜一次」，而是「想一点、搜一点、再想、再搜」**——**Search-R1 用 RL 把这个交错循环训进模型里**，而不是靠 prompt 引导。
- **BRIGHT 的两年变化很陡**：**~18 → 66.9（约 3.7 倍）**。**BRIGHT 是「推理密集型检索」基准**——那些**必须先推理才能知道该搜什么**的查询。
- **⭐⭐ `marketing in 2023, a measured fact now` 是在给一个宣称重新分级**：从「厂商吹的」升到「有基准数字支撑的」。
  - **和上午 bm42 那条反射是同一个动作，方向相反**：bm42 是**发布公告被证伪**，这里是**营销话术被证实**。
  - **⭐ 两者合起来才是完整的态度：不是「不信厂商」，而是「等测量」。测量来了就改口。**
  - **这门课今天改口/不改口共三次，程序完全一致**：

| 宣称 | 证据 | 结果 |
|---|---|---|
| ColBERT「太贵」（p.23） | MUVERA / WARP / 压缩 | **改口**——反对意见倒下 |
| 长上下文「取代检索」（p.56） | **NoLiMa** | **不改口**——被证伪 |
| agentic「学会推理」（本页） | **BRIGHT** | **改口**——被证实 |

- **⭐ 右栏立刻踩刹车，而且踩得很具体**：
  - **`the loop pays its latency bill on every hop`** —— **agentic 的成本结构不是「贵一次」，是「每一跳都贵」**。想→搜→想→搜，每轮都是一次 LLM 调用 + 一次检索，**延迟线性累加**。
  - **`the single-shot cascade still wins`** —— 对**点查询与被缓存的头部**，**一次检索走完级联仍然更好**。
  - **`the hard residue`（难啃的残余）这个词很准**：**先用便宜的方式处理掉绝大部分，剩下的那一小撮才给 agent。**
- **⭐ 这与今天所有其他「sidecar 论证」是同一个模式**：

| 组件 | 流量占比 | 教条 |
|---|---|---|
| **图 sidecar**（p.47） | **1–2%** | **sidecar，永远不是主路** |
| **HyDE**（p.81） | 变换级联最后一级 | **last resort, not default** |
| **agentic loop**（本页） | **hard residue** | **不要让每个查询付 agent 的价** |

  **同一条结构：能力最强的那一档，恰恰是流量占比最小的那一档。**
  **而且都是「阶梯上的一级，不是异端」**——讲义原话：***agentic turn 是路由器最昂贵的一档，是阶梯上的一级，而不是异端。***

- **⭐ 「什么算 hard residue」有一个具体的判定入口，而且今天已经铺好了**：
  1. **单发级联跑完 → 出口校准（p.70）→ 分数低于弃权阈值**
  2. **或路由器识别出这是多跳查询**（讲义第六种病理：**multi-hop → plan**）
  3. **⇒ 升级到 agent**
  - **也就是说：agent 是「弃权规则」的下游。p.70 的校准正是为这个服务的**——**校准后的分数决定了便宜路径是否成功；失败了才升级。**


### 正课 p.86–p.87 · **POP QUIZ · ACT V：Quiz 10 — the fortune teller's suburb** 与答案

> ⚠️ **p.85 未截到。** 以下两页当时在课上讨论过，记录据完整 deck PDF 复原。

> **POP QUIZ · ACT V**
> # **Quiz 10 — the fortune teller's suburb**
>
> *Cache thresholds: **$\tau_{\text{full}} = 0.92$, $\tau_{\text{partial}} = 0.80$**. Three canonized queries arrive with nearest-neighbor similarities **0.95, 0.86, 0.74**.*
> ***(a)** State the front door's action for each.*
> ***(b)** One careless colleague proposes **"just return the nearest cached answer, always."** **Name the doctrine that forbids it, and the analogy that made it famous.***
>
> **中文**：**测验十——算命先生的郊区**。*缓存阈值：**$\tau_{\text{full}} = 0.92$、$\tau_{\text{partial}} = 0.80$**。三个规范化查询到达，最近邻相似度分别是 **0.95、0.86、0.74**。* **(a)** 说出前门对每一个的动作。**(b)** 有位粗心的同事提议「**就永远返回最近的那条缓存答案**」。**说出禁止它的那条教条，以及让这条教条出名的那个类比。**

**答案页（p.87）原文**：
> # **Serve, hint, miss — never guess**
>
> **(a)** **0.95 > 0.92: serve** the cached answer. **0.80 < 0.86 < 0.92: do not serve** — **pass downstream as a retrieval hint**. **0.74 < 0.80: miss**; run the full cascade.
> **(b) Never KNN without a threshold.**
>
> 右栏：*The famous collision: **type-1 and type-2 diabetes — nearest neighbors, clinically opposite answers**. **Every team that thinks the semantic cache is easy builds one, annoys its users, and rips it out.** **Built with $E$ and $\tau$ treated seriously, it is magic.***
>
> **中文**：**serve、hint、miss——绝不 guess**。**(a)** **0.95 > 0.92：serve**，直接返回缓存答案。**0.80 < 0.86 < 0.92：不要服务**——**作为检索提示传给下游**。**0.74 < 0.80：miss**，跑完整级联。**(b) 绝不做没有阈值的 KNN。**
> 右栏：*著名的碰撞：**1 型与 2 型糖尿病——在向量空间里是最近邻，在临床上答案完全相反**。**每一个认为语义缓存很简单的团队，都会建一个、把用户惹毛、然后把它拆掉。** **而如果 $E$ 和 $\tau$ 被认真对待，它就是魔法。***

- **标题本身就是答案的一半**：**没有阈值的 KNN 就是一个算命先生——你问什么它都答得上来，因为它只需要找「最近的」，而「最近的」永远存在。** 而**「郊区」是它答案所在的地方：在附近，但不是那里**（呼应 p.81 HyDE 的「真正的文档在附近的郊区」）。
- **那位同事错在哪，说得再准一点**：**KNN 的返回是「相对的」（最近的那个），而决策需要「绝对的」（够不够近）。阈值就是把相对变成绝对的那一步。** 去掉阈值，你得到的是一个 **100% 命中率的缓存——而它命中的是「最近的错误答案」。**
- **⭐ 这是今天第三次同一个病**：

| 页 | 承诺什么 | 缺什么 | 后果 |
|---|---|---|---|
| **p.20** | 裸 top-20 凑满 20 个 | **下限** | 掺噪声 |
| **p.27** | 同上（14 个陌生人） | **下限** | 吃生成预算 |
| **p.82 / p.86** | 裸 KNN 返回最近邻 | **下限** | **⚠️ 直接答错** |

  **同一条教条：上限必须配下限。而缓存这一侧后果最重——它后面没有任何一级会检查它。**
- **⭐ 右栏第二句是组织行为观察，不是技术观察**，它描述了一个完整的失败周期：**看起来简单 → 建了 → 用户被惹毛 → 拆掉 → 结论被记成「语义缓存不靠谱」**。**而真正的问题不是「缓存这个想法」，是「$E$ 和 $\tau$ 被草率对待了一次」。**
  - **这是「神牛」的对偶**（见第四幕 4.9 的补注）：**两者都是用历史代替测量。**
- **怎么避免那个周期**：① **上线前先造负例集**——你领域里那些「差一个词、答案相反」的对（1 型/2 型、税前/税后、试用期/正式、2024 版/2025 版），**这就是全部工作量所在**；② **$\tau_{\text{full}}$ 保守起步**，**假阴性只是多花几毫秒，假阳性是答错**；③ 记录每一次 serve，定期抽样人工核；④ **⭐ 给用户一个「这不对」的按钮**——**缓存的失效是静默的，唯一的探测器是用户。**

### 📕 缺页补课（用讲义全文回填，标注可信度）

> 标注：**【确认】**= 由其他幻灯明确证实 ｜ **【重建】**= 依据讲义原文回填，措辞可能不同 ｜ **【推测】**= 仅由位置推断

**缺页清单**

| 来源 | 已截 | 缺 |
|---|---|---|
| **Prelude（20 页）** | **全部 20 页（已补齐）** | **无** |
| **正课 deck（125 页）** | 3–12、14–16、18–21、23、26–32、34–36、38、40–50、53–54、**56–60**、65–68、70–72、74–75、78–84、**86–87** | **1–2、13、17、22、24–25、33、37、39、51–52、55、61–64、69、73、76–77、85、88–125** |

---

**① 正课 p.22 · ColBERT / 后期交互本体**【重建 · 内容损失最大的一页】

p.23 讲的是「成本坍塌」，所以 p.22 必然是**后期交互本身**：

- **它拒绝池化。** 其他 dense 车道把一整段压成**一个**向量；**ColBERT 让每个 token 保留自己的向量。**
- **MaxSim**：相关性 = **对每个 query token，取它与任意 document token 的最大相似度，再求和**。

$$\text{score}(q,d) \;=\; \sum_{i \in q} \max_{j \in d} \; E_{q_i} \cdot E_{d_j}$$

- **⭐ 它治的那具尸体**：**池化会把罕见词平均掉**。讲义原话——***那个池化向量会平均掉的罕见词，保住了自己的一票。*** 一段话里只出现一次的产品编号、人名、术语，在单向量里被稀释，在 ColBERT 里**仍然能单独命中**。
- **代价**：**每 token 一个向量** → 存储与算力爆炸。**这正是 p.23 那句「成本反对意见」的内容**，也是 p.14 说的「ColBERT 两者都保留，并为此向你收取存储费」。

---

**② 正课 p.24–25 · 语境化谱系（合上仪器柜）**【重建 · 第二重要】

讲义在 ColBERT 之后紧接着写的就是这一段（*The contextualization lineage closes the cabinet*）：

- **Anthropic 的 contextual retrieval**：在做 embedding 和 BM25 **之前**，给每个 chunk **前置一段生成的定位语境**（说明这一段在整份文档里的位置与背景）。
- **效果**：**top-20 检索失败率削掉 35–67%**（取决于 reranker）。**代价约为每百万 token 一美元。** 讲义称它是***目录里收益最高、最不炫目的升级***。
- **late chunking**：先对**整份文档**编码，再切分——**把语境从 prompt 搬进了编码器本身**。
- **whole-document contextual encoders**：进一步让整文档语境成为编码器原生输出。
- **⭐ 讲义在这里给了一句预警，值得单独记**：
  > **盯住这个趋势：我们今天下午亲手制造的一些派生物，正在变成编码器的原生输出。**

  **也就是说：Act II 教你手工制造的东西，有一部分正在被模型内化。** 这条对「该不该自建派生物管线」的长期判断很关键。

---

**③ Prelude p.11–13 · 实验三整场** ✅ **已补齐（见本节 幻灯十一/十二/十三）**，以下保留当时的重建推断以供对照

- **种子（由 p.19 确认）**：***Five catalogues — one corpus, many drawers; each question has an altitude.***
- **正课 p.12 就是它的命名**：**四种查询高度**（point / contextual / thematic / global），以及**光学三件套**（显微镜 / 变焦镜头 / 望远镜）。
- **动手形式【推测】**：大概率是**卡片抽屉**的实物版——同一批材料按不同方式归档成多个「抽屉」，然后拿不同高度的问题去查，体验「问题落错抽屉」的感觉。
- **缺失的是体验，不是教条**——**教条在正课 p.12 已经完整给到了。**

---

**④ 正课 p.17 · bm42 警世故事 · 第二部分**【重建】

p.16 埋的伏笔是「Quora，平均每查询约 1.6 个相关项……记住这个数字」。讲义的落点是：

> **一位细心的读者在几天内重算了算术，那个宣称没能存活。**

**要带走的不是厂商八卦，是那条反射**：
> **把每一次产品发布当作一篇你打算复现的论文来读，并让你自己封存的标尺去批改这份作业。**

---

**⑤ Prelude p.5–6 · 实验一的 Harvest 与 Seed** ✅ **已补齐（见本节 幻灯五/六）**

**种子（由 p.19 确认）**：***Many maps — a representation is a choice of what to ignore.***
**正课 p.11 是它的完整命名**（四张地图各自抹掉什么、`because of what it threw away`、四条车道各自「注意」什么）。

---

**⑥ Prelude p.16 · 实验四的 Harvest 第一部分** ✅ **已补齐（见本节 幻灯十六）**

p.17 是 Harvest 2/2（诱饵的代价在桌边）。**1/2 大概率讲的是召回侧**：**九十秒结束后没捡到的纸，第二部分再也拿不到了**——即正课 p.6 命名的**召回天花板**。

---

**⑦ Prelude p.2–3 / 正课 p.1–2 / 正课 p.13**【推测 · 无实质内容损失】

- Prelude p.2–3：开场规则与实验一的布置
- 正课 p.1–2：封面 + 全天路线图
- **正课 p.13：Act I 的分幕卡**——按 p.28（`MILESTONE · ACT II OF VII`）的体例，应为 **`MILESTONE · ACT I OF VII — The Cabinet Opens`**

---

## 一、全天地图与「必须带走的能力清单」

讲义在开头给了一份自检清单（*What Must You Carry Forward*）。它同时也是全天的目录，先抄在这里当作导航——读完笔记回来对一遍，**能不含糊地做到，才算过关**：

1. 陈述论点（表征组合 + 裁决法庭），并用 Mundaneum 解释**为什么 Otlet 有组合、缺法庭**。
2. 用「铲子与筛子」解释**召回天花板**，说清为什么下游任何组件都抬不高它。
3. 陈述**断层扫描原理**，说出单一索引宣称了什么、而组合拒绝了什么。
4. 按**高度**（point / contextual / thematic / global）给查询分类，并说出每种高度需要的表征。
5. 把 BM25、SPLADE、单向量 dense、Matryoshka、ColBERT 对照成**有损投影**，各自防住哪种失效——并讲 **bm42 的故事**作为「怎么读产品发布」的教训。
6. 写出 InfoNCE 和 **DCL**，说明**什么离开了分母、以及为什么小 batch 不再是一种税**，并陈述 **MRL–DCL 不变式**。
7. 描述**难负例课程表**与**假负例陷阱**，给出 **48 小时微调教条**以及**拒绝微调的理由**。
8. 背出主模式——**retrieve the derivative, generate from the source**——并说出出处**回指针的两项职责**。
9. 走一遍**派生物清单**（rewrites、factoids、QA pairs、summaries、RAPTOR、community summaries、governed concepts），每一件对应**它防住的那具尸体**。
10. 解释**长上下文幻象**（NoLiMa、context rot、跑表），并给出诚实的综合结论。
11. 写出 **RRF（k=60）**，解释为什么用**名次**而不是分数，并描述**代理曲面法**（surrogate surface）如何调不可微的东西。
12. 陈述 **which-text-to-rerank 教条**（诱饵的任务在检索环节就结束了）与**父级去重规则**。
13. 说出**六种查询病理**、变换级联、HyDE 与语义缓存的位置，以及**什么时候干脆不检索**。
14. 给出**版本偏斜教条**、**ACL 前置过滤规则**、**PoisonedRAG 的数字**。
15. 应用**升级阶梯**与 **Shapley 纪律**，点名 **Kitchen Sink** 与 **Sacred Cow**，并解释为什么是**规模**——而不是时尚——决定架构。

> 做得到这十五条，就为下周的**语义缓存**（今天这栋房子的前门）做好了准备。

**三幕结构（讲义）**：Act I 图书馆（上午，基础 + 表征组合）→ Act II 第二语料库（早下午，派生物 + 长上下文幻象）→ Act III 法庭（晚下午到晚上，裁决 + 问题侧 + 机房 + Playbook）。

> ⚠️ **注意**：**正课 deck 分成七幕**，与讲义的三幕不是同一套编号。对照见第〇-B 节 p.28 的记录。

**两句贯穿全天的引语**（讲义边注）：

> *Knowledge is of two kinds. We know a subject ourselves, or we know where we can find information upon it.* —— Samuel Johnson, 1775
>
> *Everything in the universe, and everything of man, would be registered at a distance as it was produced. In this way a moving image of the world will be established, a true mirror of his memory.* —— Paul Otlet, *Monde*, 1935

---


## 二、Act I · 图书馆 —— 基础与表征组合

> *We open in Brussels, and we stay there longer than you might expect.*

### 2.1 布鲁塞尔，1895：Mundaneum

**两个比利时律师决定给一切编目。** 1895 年 9 月，Paul Otlet 与 Henri La Fontaine 召开第一届国际书目大会，启动 *Répertoire Bibliographique Universel*——一部意图记录人类产出的每一份文档的卡片目录。他们把 Dewey 十进分类改造成 **UDC（国际十进分类法）**，其**连接符号**让一张卡可以同时坐在多个维度的交点上：`statistics : agriculture : India : 1895`——**可以从许多方向被寻址**。

然后 Otlet 做了真正与我们相关的那件事：**他判定「书」是错误的单位**。他的**单篇原则（monographic principle）** 要求把文档**分解**——每一个事实抄到自己那张标准 3×5 卡上，分类、归档，好让任何未来的问题都能找到它。到 1930 年代，抽屉里有约 **一千六百万张卡**。

> 边注（用工程师的耳朵听）：从 1912 年起研究所开了检索服务——**邮寄或电报提问，馆员在抽屉间行走，答案邮寄回去，每千张卡 27 法郎，每年约 1,500 次查询**。翻译成今天的术语：**一个远程客户端、一个多索引知识库、带出处的检索证据，以及以「天」为单位的延迟。**

1934 年，Otlet 的 *Traité de documentation* 勾勒了一张由桌面与屏幕组成的 **réseau**，通过电缆查询一个通用索引——一个**联网终端**，写于 Turing 还在读本科的那一年。然后世界拒绝合作：1934 年政府撤资；1940 年占领者为了办一场艺术展清空展厅，**摧毁了约六十三吨藏品**。Otlet 1944 年去世，相信自己一生的工作已经失败。幸存的抽屉最终在 **Mons** 找到归宿，至今仍在。

**承重的教训不是「先知预见了互联网」**，而是这一条：

> **Otlet 建的不是「在文档上的搜索」，他建的是一组表征的投资组合。**

同一个事实以五种形态活着——按作者的书目条目、按主题交叉点的分类卡、卷宗里的剪报、图像资料库里的一幅图、百科式摘要里的一行——**同一个源的五个目的各异的投影**，每一个之所以被制造，是因为**某一类未来的问题恰好需要那个投影**。而它们之下是单篇原则：**把文档分解成原子事实，因为问题几乎从来不长成一本书的形状。**

**缺了一样东西：Otlet 没有排序（ranking）。** 一个 UDC 类目要么包含某张卡、要么不包含；抽屉之内，卡片按**入藏顺序**排列。**Mundaneum 有组合，缺法庭。今天有一半的内容，正是 Otlet 从未建成的那一半。**

> 与 Week 09 的衔接：上周的 Prelude（*The Library in Your Head*）已经把 Mundaneum 当作「你在脑子里设计的卡片系统真的被建成过」的历史揭晓（那里给的数字是 1,200 万张以上，本周讲义给的是 1930 年代约 1,600 万张——**同一个机构在不同年份的规模，不冲突**）。上周它证明的是「按卡片规格制造知识可行」，本周它证明的是**「光有卡片不够，还得有排序」**——两周用同一个故事推出了两条互补的教条。

### 2.2 论点：把故事兑换成一句话

**检索系统是两样东西的连接**：

- **表征的投资组合（portfolio of representations）**——同一份语料的许多**目的各异的、有损的**投影，每一个之所以被制造，是因为某一类查询恰好需要那个投影；
- **裁决的法庭（court of adjudication）**——一个级联，**便宜的法官缩小战场，好让昂贵的法官负担得起「仔细」**。

> **检索架构 = 决定「制造哪些表征」+ 决定「如何在它们之间裁决」这门学科。**
> **规模决定你负担得起多少；测量决定它们中哪些配留下来。**
> *One corpus, many catalogues.*

### 2.3 召回天花板：沙坑里的弹珠

为什么检索是承重墙？因为**召回天花板（recall ceiling）**。

一个孩子把弹珠丢在沙坑里，用**铲子和筛子**找回来：铲得宽、铲得慷慨、容忍沙子——筛子可以从容地把沙子除掉。**但如果铲子漏掉了一颗弹珠，任何筛子都救不回来。**

> **第一阶段拿到多少召回，就是一个下游任何东西都抬不高的天花板：不是 reranker，不是更好的 prompt，不是更大的模型。**
> **Generation cannot cite what retrieval never surfaced.**

这就是为什么**铲子调召回、筛子调精度**，也是为什么 Act III 整座级联本质上是**「在召回被锁定之后再花精度」的机器**。讲义要求写在眼皮内侧的一句：***only the scoop decides what is caught.***

> 边注（为什么现在能跑 Otlet 的架构）：**两台引擎**——LLM 让**派生表征的制造变便宜**（一座在水面之下的离线算力冰山，查询时不可见），以及六十年的索引结构让搜索**次线性**。*His institution died because every projection and every query cost a clerk; ours costs electricity.*

### 2.4 断层扫描原理与四种查询高度

**为什么要许多目录，而不是一个更好的目录？**

**CT 扫描仪从不给肿瘤拍照。** 它拍数百张有损投影——每一张单独看都是瞎的——然后**重建出没有任何单张曝光包含的东西**。组合里的每个索引都是语料在**自己那个语义角度**上的投影：稀疏车道看**纸面上的词**，dense 车道看**词背后的意思**，factoid 索引看**原子声明**，summary 索引看**主题**。**融合就是重建。**

同族的比喻：**立体派肖像**（一个人，许多同时的角度）、**复眼**、**罗生门**。而它**不是**什么：**不是全景敞视监狱（panopticon）**——一只眼睛宣称拥有全部视野。**单一索引做出那个宣称；组合拒绝它，而这个拒绝就是整个架构的一个手势。**

之所以需要这些投影，是因为**问题以不同的高度到达**：

| 高度 | 想要什么 | 例子 | 对应表征 |
|---|---|---|---|
| **Point（点）** | 一个事实 | "III 期入组人数是多少？" | **factoid** |
| **Contextual（语境）** | 一整段、周边完好 | 需要上下文才成立的条款 | **chunk** |
| **Thematic（主题）** | 贯穿一份文档的东西 | "这家供应商怎么看数据驻留？" | **summary** |
| **Global（全局）** | 活在整个语料的结构里、不在任何一段里 | "这五百份访谈里的主要监管关切是什么？" | **community** |

**落错高度 = 一个自信的不相关答案**：点查询淹死在摘要里；全局查询被三条关于一种药的引文回答掉。**下午大部分路由与融合机器，存在的目的就是把每个问题送到它自己的高度——或者更好，让查询自己找到自己的水平面。**

> ⚠️ **补充（来自 Prelude p.12）**：实际上是**五种高度**，第五种是 **verbatim（逐字）**——「原文引用它关于 Z 的那句话」。**只有保留了词本身的索引答得了它**，这是稀疏车道不可替代的独家理由。正课 p.12 把它省掉了。

### 2.5 仪器柜：每一种表征都是有损投影

> Korzybski：**地图不是疆域**。每一个索引都是**为一次旅程画的地图**。

**稀疏谱系**保留一个**词表大小**的坐标系：文档是一袋带权重的词，倒排索引让查找次线性。

- **BM25**：按词频加权、对文档长度做饱和；两个常数 `k1`、`b` 存活三十年，因为它们编码了「证据如何累积」这条**耐久的真理**。
- **BM25 做不到的**：看见**同义**。查询说 "cardiac"，页面写 "heart"，倒排表永不相遇。
- **SPLADE**：**学会扩展**——一个 MLM 头为每份文档预测**整个词表上的稀疏分布**，于是那页讲心脏的文档在自己从未印过的 "cardiac" 上带了权重。**一条读过同义词典的稀疏车道**，且**保留倒排索引和随之而来的每一项运维美德**。

**Dense 谱系**丢掉词表坐标，只留几百个学出来的坐标。双编码器把 query 和 document 映到同一空间，相关性是余弦。**这条车道关掉了 paraphrase gap**——同时继承了高维几何，六月见过，现在必须在**运维上**尊重它。

> 边注（两条谱系是互补而非竞争）：**稀疏赢在罕见词、标识符、精确短语、只出现一次的名字；dense 赢在改写和意图。这正是为什么按名次融合的混合检索胜过任何单独一条——断层扫描原理最简单的双投影形态。**

### 2.6 测度集中与光圈教条

在一千维里，**几乎每一对随机向量都近乎正交**；真实语料的余弦相似度**远非填满 [−1, 1]**，而是**挤进一条窄带**——典型地在 0.2 到 0.9 之间（取决于 embedder），且大部分质量集中在其中很薄的一片。这是**测度集中（concentration of measure）**，它有**三条实践后果**，你设定的每一个阈值都必须带上：

1. **绝对相似度阈值在不同 embedder 之间不可移植。** 一个模型上的 0.7 和另一个模型上的 0.7 是**不同的光圈**，因为分布不同。
2. **top few 候选之间的差异在绝对值上很小**，所以 **reranker 的辨别力比 retriever 更要紧**，且**出口处的校准不是可选项**。
3. **光圈教条（the aperture doctrine）**：阈值是**围绕 query 方向的一个锥形光圈**。开大 → 进更多沙；收小 → 丢弹珠。**在封存集上设定，逐 embedder、逐车道地设定，并在 embedder 变更时重新审视。**

> Act II 的 Berlin 实验（0.64 对 0.81–0.90，跨过 0.7–0.8 的阈值）**就是测度集中在咬一个真实的生产系统。**

### 2.7 Matryoshka、后期交互与成本旋钮

两个想法补完仪器柜，而它们改变的是 dense 谱系的**成本结构**而非精度——**这正是它们属于一堂架构课而不只是建模课的原因**。

- **MRL（Matryoshka 表征学习）**：训练**单个** embedding，使其**前缀本身就是好的 embedding**——1024 维向量的**前 128 维**是同一意义的一个**可用的、更便宜的投影**。于是**维度变成一个运行时旋钮**：用 128 维在数百万候选上**铲**，再对幸存者用全宽**复评**。
- **ColBERT 的后期交互（late interaction）**：**拒绝池化**。每个 token 保留自己的向量，相关性是「对每个 query token 取其对任意 document token 的最大相似度，再求和」（**MaxSim**）。**池化向量会平均掉的那个罕见词，保住了自己的一票。**
  - 多年来的反对意见是**成本**（每 token 一个向量）；**到 2026 年这条反对意见基本倒了**：**MUVERA** 把多向量检索**带保证地**归约成单向量 MIPS，**WARP** 和小型 ColBERT 压垮了服务账单。
  - **现在决定 ColBERT 坐在哪里的是锦标赛（tournament），不是成本反对意见。**

**语境化谱系（contextualization）合上柜门**：Anthropic 的 **contextual retrieval** 在 embedding 和 BM25 之前，给每个 chunk **前置一段生成的定位语境**，把 **top-20 检索失败率削掉 35–67%**（取决于 reranker）；**late chunking** 以及随后的**整文档语境编码器**把那段语境从 prompt **搬进了编码器本身**。

> **盯住这个趋势：我们今天下午亲手制造的一些派生物，正在变成编码器的原生输出。**

**bm42 的故事（读发布公告的反射）**：2024 年一次发布宣称新的稀疏方法**决定性地**打败了 BM25；一位细心的读者在几天内**重算了算术**，那个宣称没能存活。**教训不是关于某一家厂商，而是一个反射：把每一次产品发布当作一篇你打算复现的论文来读，让你自己封存的标尺去批改这份作业。**

### 2.8 被训练的仪器：DCL、课程表与不变式

> **The embedder is not the glass; it is the mirror — and mirrors are ground for a purpose.**
> （embedder 不是玻璃，是**镜子**；而镜子是**为某个目的打磨**的。）

两股力量塑造几何：**alignment** 把 query 拉向它的正例；**uniformity** 把其余一切铺开在球面上，好让任何区域都不拥挤。**InfoNCE 把两者实现为一场列队指认（line-up）**：对 query `q`、正例 `d+` 和一批 `N` 个候选，

$$
\mathcal{L}_{\text{InfoNCE}} = -\log \frac{\exp\!\big(s(q, d^{+})/\tau\big)}{\sum_{j=1}^{N} \exp\!\big(s(q, d_j)/\tau\big)}
$$

**分母包含正例自身**。念出声就是：**让正例赢下这场列队指认。**

**微妙之处**：正例留在分母里时，**正例上的梯度恰恰在模型已经做得好的时候被扼住**——在 **monograph 的算例**里**弱五十倍**（讲义转述），而那正是它最要紧的时刻。修法是 **DCL（解耦对比学习）**：**把正例逐出分母**，

$$
\mathcal{L}_{\text{DCL}} = -\frac{s(q, d^{+})}{\tau} + \log \sum_{j \neq +} \exp\!\big(s(q, d_j)/\tau\big)
$$

**正例离开了列队，小 batch 也不再是一种税**——**这正是本课把 DCL 定为 house loss 的原因。**

**负例按课程表到达（curriculum）**：先易（随机负例）→ **BM25 挖掘的负例** → **dense 挖掘的负例**，每一级都更刺一点；严肃的配方里，**从 cross-encoder 蒸馏 margin（Margin-MSE）是承重信号**。

> **假负例陷阱（false-negative trap）**：负例挖得太狠，「负例」往往其实是**未标注的正例**，损失函数会**因为模型答对而惩罚它**。对策是 **positive-aware mining**——丢弃那些分数**离正例太近**的候选——外加一个**去噪法官**（cross-encoder）在难负例被信任之前先审一遍。

**上午两个想法在一条规则里相遇——MRL–DCL 不变式**：

> **在 Matryoshka 的求和内部、在每一个前缀宽度上，都施加解耦损失**，这样 **128 维的铲子和全宽的复评是被同一套纪律训练出来的**；并且**在任何 embedder 更换之前，对这条不变式做回归测试**（在封存集上测「铲深处的召回」）——因为**一把悄悄腐烂的铲子，等于筛子还没看见就已经丢掉六颗弹珠**。

**48 小时教条**：用**从你自己语料制造的合成对**、一份课程表、加 DCL，**领域微调是一件两天的活**——而当**语料是通用的、领域很小、或者用来证明这次更换诚实的标尺还不存在**时，**你拒绝做它**。

---


## 三、Act II · 第二语料库 —— 派生物与幻象

> 上午建的是**我们被给予的那份语料**的投影。早下午**制造第二份语料**——派生物，Otlet 的卡片被机械化——然后正面回应那个想彻底废掉检索的诱惑：**百万 token 窗口**。
> **两半转在同一个问题上：文本是谁的形状——读者的，还是考官的？**

### 3.1 用户即考官（The User Is the Examiner）

讲义里最个人化的一段：**在 IIT，作者应用电动力学考了第二名，而这件事的方式教了他四十年。** 考第一的同学去找学长收集**题库**——这位考官实际问过的**大约四十道题**，带着小幅变异循环出现。他为那四十道题写出漂亮答案、背下来、考了第一，**此后再没打开过一本物理书**。

> **我优化的是「学会这门学科」；他优化的是「回答这位考官」。**
> **在检索架构里这不是悲剧，这是规格说明书（It is the specification）。**

**用户就是考官**：检索系统面对的是**一条它不控制其语域（register）的问题流**，而**语料在被写下时心里根本没有考官**——教科书为教学而写、论文为审稿人而写、合同为对方律师而写。**这就是语域错配，而且它是永久的。**

正统的回应是**变换查询直到它像那些散文**——我们也会做（Act III 的问题侧）。**但更深的一步走向相反方向**：

> **不要等 query 来匹配你的文档；制造匹配你 query 的文档。**
> 把语料**离线**处理——那时算力便宜、时间充裕——把每个 chunk **重铸成问题能抓住的形状**。
> **能花在「静止之物」上的智能，就都花在那儿——算力的冰山属于水面之下，在查询时不可见。**

### 3.2 主模式与出处回指针

**一条规则统治我们制造的每一件派生物**：

> ### **Retrieve the derivative, generate from the source.**
> **检索派生物，从源生成。**

Rewrites、factoids、QA pairs、summaries、树节点、社区摘要——**这些是被搜索的**。**原始段落才是生成器看见并引用的东西。** 派生物存在是为了**被找到**；源存在是为了**被引用**。

> 一份丢掉了 "irrevocable"（一个背后挂着判例法的行话）的法律改写，**不是证据，是诱饵（bait）**。

**承重的推论**：**每一件派生物都携带一个指回其来源的指针**，这**不是礼节，是机器**。这枚**出处回指针**的职责在今天被用到了**四处**：

1. **它是引用**——那条可点击、可审计的声明；
2. **它是失效键（invalidation key）**——当源变化时，你**反向走出处图**，就能准确知道**哪些 factoid 死了、哪些 summary 已经传递性地过期、哪些树节点必须被标脏**；
3. **它是运行时去重键**——父级去重按 `source_chunk_id` 折叠同一个源的多个化身（正课 p.67）；
4. **它是「解析回源」的键**——重排之前把派生候选换回源文本（正课 p.68）。

> **一个没有出处的派生语料库不是索引，是一间装了向量搜索的谣言工厂。**
> （*A derivative corpus without provenance is not an index; it is a rumor mill with vector search.*）

> 边注：**回到布鲁塞尔——这一整部分就是穿着时代戏服的单篇原则。卡片是派生语料库；上架的书是源；馆员检索卡片、引用原书。其余一切只是机械化。**

### 3.3 派生物清单：一个源、许多表征，每一件对着一具指名的尸体

> **清单的纪律是：没有任何一件派生物靠「有趣」赢得位置；它靠指出「没有它，检索会以哪种具体方式死掉」来赢得位置。**

| 派生物 | 治的那具尸体 | 关键做法 / 数字 |
|---|---|---|
| **Contextualized rewrites（语境化改写）** | **endophora（内指）与铠甲语域**（法律腔、临床速记） | 用问题的语域重述 chunk、代词解析完毕：**源的替身演员，为 retriever 试镜** |
| **Factoids（原子事实）** | **embedding 稀释（dilution）** | 五个声明的段落 embed 在五种意义的**质心**附近、离**每一个顶点**都远；尖锐的 query 落在**某一个顶点**附近 |
| **QA pairs** | **跨体裁错配** | **唯一把「query 形状的对象」放进索引的派生物**；每 chunk 3–8 个问题，**embed 问题**，answer 与 source id 放 payload |
| **Summaries（摘要）** | **主题查询碎在 chunk 之间** | section / document / corpus 三种高度，**各自成索引** |
| **RAPTOR 节点** | 缺**变焦镜头** | 聚类、摘要、递归：**被发现的层级**，约叶子数的 **1.3–1.5×**；**在坍缩树上检索**，让 query 自己找到高度 |
| **Community summaries** | 缺**望远镜**（活在任何段落之外的 sensemaking 问题） | 实体 → **Leiden 社区** → 多分辨率摘要 → 查询时 map-reduce |
| **Governed concepts（被治理的概念）** | **authority failure（权威失效）** | 上周的客人回归；**唯一一件推导过程要经过人类评审门的派生物** |

**逐条的关键细节**：

- **Factoids · Berlin 实验**（📎 **讲义写的是「河流」查询，正课 p.43 改成了「柏林的人口是多少」——同一个实验，两处措辞不同**）：包含答案的那**段**对着该查询打 **0.64**，抽出来的 **factoid 打 0.81–0.90**——而在 **0.7–0.8 的生产阈值**下，**那个装着答案的段落被静默丢弃**。**Dense X 把这件事工业化**：**FactoidWiki，从 1.14 亿个句子里得到 2.57 亿条 proposition**。纪律：**自足性、NLI 忠实性过滤、每 chunk 设上限**。
- **QA pairs**：**retriever 应该找到的那个诱饵（the decoy）**。（记住这个词——Act III 会回来审它。）
- **Summaries**：**摘要器是记者，不是法官——逐条列出分歧，绝不调和它。**
- **RAPTOR 警告**：**垃圾聚类产出自信的垃圾摘要**；而**幻影簇（phantom cluster）**——一个偶然抱团、却能通过每一项**逐 chunk 出处检查**的簇——**是一种只有主题一致性检查（topical-coherence check）才抓得住的出处失效**。
- **Community summaries**：**embedding 告诉你这些段落听起来像；三元组告诉你它们是关于同一些东西的。**

> **光学三件套（the optical triad）组织了整份清单：factoid 是显微镜，RAPTOR 是变焦镜头，GraphRAG 是望远镜。一间运转良好的实验室三件都有，并且知道自己手里握的是哪一件。**

### 3.4 第七件派生物：被治理的 concept，正式落座

上周的客人回来了，并在清单里**坐下**。**被治理的 concept** 是被打磨到**不再是源的投影、而成为一个被撰写的知识对象**的派生物：**authored、typed、sourced、verified、expiring**。它的尸体是 **authority failure**——**检索返回了当前没有任何人站在其背后的文本，那份被取代的政策在余弦 0.91 上**。

**三条把它和清单里其他住户区分开的性质**：

1. **修复是便宜的，而便宜改变行为。** 一个错事实在 embedded 语料里要**等季度重摄取**；一个错事实在 bundle 里是**一行 diff，几分钟内合并，`git blame` 记下谁修了什么**。**其他每一件派生物我们都是重建（rebuild）；只有这一件我们是修复（repair）。**
2. **它服务于 embedding 之外的第二种检索机制——导航（navigation）：** agent 走 bundle 的 index 文件、跟随它的链接，**像馆员走书架一样**——一次**在被策展对象上的图遍历**，与 GraphRAG 的社区同族，但这张图是**被撰写和被评审的**，而不是**被聚类诱导出来的**。
3. **评审门是结构上原生的（structurally native）。** 幻影簇教我们「合成需要一个一致性门」，于是我们**外挂**了一个；**在这里，门就是这个格式自己的工作流**。抽取落地为一个 **pull request**，**合并就是晋升事件**，**修复是 diff 而不是重新摄取**。

**这道门有一个黑暗的孪生兄弟——幻影概念（the phantom concept）**：一个抽取 agent 可以铸造出一个**每个字段都格式良好、每条引用的源都真实存在、而定义却是任何版本的政策都从未包含过的流畅插值**的概念。**它比它的祖先（幻影簇）更危险，因为一个通过了评审的幻影会被晋升**——盖上 human-reviewed 的戳，**被抬进那些分层机制原本是为了保护的高风险查询路径**。

**防御是上周那套，只是瞄准早一个阶段**：

- **评审者检查的是 claim-to-source 的忠实度，不是 YAML 卫生**；
- **一道蕴含（entailment）检查——过滤 factoid 用的同一套 NLI 机器——在每一个 knowledge pull request 的 CI 里跑**；
- **数字一律不配得到散文**，因为**一个定量声明属于一次被证明的计算（attested computation），在那里插值在结构上不可能发生**。

**阶梯纪律**：**被治理的这一层是最顶一级**，昂贵在**持续的人类注意力**上，**只为被治理的核心赢得**——术语表、指标定义、政策、runbook，那**几百到几千个** authority failure 真的会致命、且**有一位领域主人愿意握笔**的 concept。

> **An unreviewed bundle is chunks wearing a suit, and the suit makes it worse.**
> （一个未经评审的 bundle 是穿了西装的 chunk，而那身西装让情况更糟。）

> 这条通道**诚实的借方栏**（讲义边注）：**策展成本真实且反复发生；`stale_after` 是一个闹钟，不是一支维护队伍；覆盖在结构上是局部的；转换本身也会幻觉。「agent 会改变策展的经济学」这个赌注仍然敞开——目前还没有生产环境的事后复盘——而我们如实说出这一点。**

### 3.5 派生语料库的经济学

**Enthusiasm for lenses is not a budget.**（对镜头的热情不是预算。）

**只是原始 chunk 一项**，在参考架构里就已经背了**四个索引**：**SPLADE、128 维的铲子、全维 dense、ColBERT**；而**每个派生物家族又各自带来自己的索引**——**总数轻易过十二个，而没人注意到里程表**。

**于是纪律，作为规则陈述、作为门禁执行**：

> **每一个索引都必须通过消融（ablation）赢得它的位置。**
> 把每个索引关掉；在 gold set 上测那道台阶；**一个「缺席后没人测得出来」的索引，是没有价值的复杂度。**

**建不建的经验法则**：

$$
\text{Artifact ROI} \approx (\text{query-mix 在该粒度上的权重}) \times (\text{实测质量提升}) - (\text{构建成本} + \text{存储成本})
$$

**按查询量摊销**。Factoid 在**事实密集语料 + 尖锐流量**上发光；rewrite **只在存在语域鸿沟的地方**才划算；RAPTOR **对一个小 FAQ 是杀鸡用牛刀**；**图 sidecar 需要 sensemaking 流量来记账**。**权重来自你实测的查询分布——用例的暴政，写成账簿的形式。**

**两条经济学统治清单**：

- **Sidecar 教条**：**图是 sidecar，永远不是主路**。**全局 sensemaking 占企业流量的 5–15%**（本课的路由器**只送 1–2% 走它**），却**不成比例地是高管问的那些问题**——所以**它定义了智能的天花板，但不被允许承载高速公路**。
- **千元实习生发票**：一个抽取任务接到了**前沿 API** 而不是本地集群，教会了**成本悬崖**；**LazyGraphRAG 与 HippoRAG 2 此后已经废掉了这张发票的大部分**——所以**这条教条现在是关于流量，不是关于价格**。

**top-K 的考古学（archaeology of top-K）**：**记录一周内每一条最终结果的家谱，然后数。** 每一次的发现都是——**多数时候，多数的 top 结果不是原始 chunk。** 那是**支持多表征架构的最强单一论据，而它只需要在你自己的流量上跑一周的日志**。然后**让它作为遥测一直跑下去，让家谱——而绝不是热情——决定哪些镜头留下**。

**摊销有一个分母（churn calculus）**：「一次辛苦，终身受用」假设**语料静止得足够久，久到能收得到利息**——而**一条每周翻新的监管数据流、或一个每小时翻新的工单队列，不是这样**。**churn 计算 = 每文档推导成本 × 翻新率，对上 质量提升 × 查询量**；**当 churn 赢了，就建更少、更便宜、更懒的派生物**（LazyGraphRAG 正是这笔交易的工业化）。

**当你确实要建时，失效会自然分层**：

- **本地失效**（按 document id 删除、重新推导）：**chunks、factoids、rewrites、QA pairs**
- **传递性过期**（写时标脏，**懒惰地、自底向上地、异步地**重建）：**summaries、树节点、community summaries**

> **分层新鲜度不是妥协，而是对「信息在不同高度上以不同速率衰减」这件事的正确读法。**
> 📎 正课 p.42 给了一个更好用的说法：***摘要就是物化视图（materialized views）***——底层表一变，视图必须失效；而数据库有现成机制，你的派生语料库没有，得自己建。

> 边注 · **Say 定律在检索里成立：供给创造自己的需求。** 因为实测分布是 80% 点查询而建了 factoid 索引，然后**眼看着主题查询的份额爬升**——因为用户发现这套系统现在**可以被托付更难的问题**了。**为你将会创造出来的分布做设计，并在路由器里为尚未建成的 sidecar 留出位置。**

### 3.6 幕间：长上下文幻象（The Long-Context Mirage）

**窗口装得下一百万 token，为什么还要检索？**

> **这个诱惑是真实的，必须用证据而不是教条来回答。**

1. **NoLiMa 的证据**：Needle-in-a-haystack 基准**看起来已解决**，是因为**针和问题共享词**。**去掉词面重叠——NoLiMa——十二个前沿模型里有十一个在 32K token 处丢掉一半准确率。** **Context rot 不是边角情况；当答案必须被推断而非被匹配时，它就是默认状况。**
2. **跑表（the meter）**：**每个问题一百万 token = 每个问题多少美元，每一个问题，永远**——那座算力冰山被拖到水面之上，**按推理价格付钱**。
3. **图书馆论证**：**你不会为了回答一个问题去读整座图书馆；你查目录。** 而 **Otlet 的馆员——他们本来可以读到任何答案——之所以建那些目录，恰恰是因为「读」不 scale。**

**诚实的综合结论**：

> **在蟑螂尺度上**（一万份文档、一种语域、少数几个候选），**长窗口是一个正当的器官**：把整份文档塞进去，让 reranker 挑。
> **在那之上，检索不是在和窗口竞争；检索是让窗口值得被填满的那个东西。**
> ***The window is for holding evidence, not for finding it.***

> 📎 正课 p.58 补了一条更精确的表述：**长上下文抬高的是「检索可以返回多少」的天花板，而不是「是否还需要检索」。** 它放宽的是**筛子及其之后**的约束，**一点也没动铲子**。

---


## 四、Act III · 法庭、问题侧与机房

> **组合建好了；现在是 Otlet 从未拥有的那一半。**

### 4.1 司法阶梯与按名次融合

**级联是一座法庭，便宜的法官缩小案卷，好让昂贵的法官负担得起「仔细」。**

**铲（the scoop）**：每条车道——**SPLADE、128 维 Matryoshka 车道、ColBERT**——各发出**自己的前几百个**；**这里召回是神圣的**，深度的选法是**让并集很少漏掉一颗弹珠**。

**然后是融合。** 车道的分数**不可通约**——BM25 分数和余弦**不共享任何标度**——**所以我们在名次上融合**，而诚实的基线是 **RRF（倒数名次融合）**：

$$
\mathrm{RRF}(d) = \sum_{r \in \text{lanes}} \frac{1}{k + \mathrm{rank}_r(d)}, \qquad k = 60
$$

**念出来**：**被任何一条车道排得高的文档都会上升；`k` 阻尼头部，使得某一条车道的第一名不能一家独大**；而 **k=60** 出自 **2009 年一篇三作者的 SIGIR 论文**，**至今仍是几乎每个引擎的默认值**。

**学习式融合**（调过的凸权重）**在你有 hold-out 可调时胜过 RRF**——这带来了难点：**融合权重与发射深度坐在一道你无法求导的台阶上**（名次是离散变化的）。**本课的答案是代理曲面法（surrogate-surface method）**：

> **在参数网格上采样 → 对每点实测的 nDCG 拟合一个光滑代理曲面 → 优化那个代理**（低维上的贝叶斯优化），**在封存集上做，并带配对 bootstrap 区间，好让 0.02 的差异不被误认成信号。**

> 边注 · **在标尺存在之前实行普选**：在你有 gold set 可调之前，**RRF k=60 + 各车道等权就是宪法。只在有证据时修宪。**

### 4.2 参考级联（可抄的起点，然后必须在你自己的标尺上调）

**正课 p.71 给出了带数字的完整版本**（参见第〇-B 节），讲义的叙述版本如下：

| 阶段 | 做什么 | 候选量 | 属于 |
|---|---|---|---|
| **发射** | SPLADE / Matryoshka-128d / ColBERT / 派生索引（factoid、QA、summary）各发前几百（**稀疏车道略深，因为它最便宜、且它的漏最丢人**） | 每车道**数百** | **the scoop** —— *召回是神圣的* |
| **融合** | **RRF，k=60** | → **数百** | |
| **去重** | **父级去重 + MMR** | → **数十** | **the sieve** —— *召回锁定后再花精度* |
| **复评** | **全维 rescore**（+ 赢得资格时的 ColBERT pass） | → **20–30** | |
| **终审** | **cross-encoder 读源文本**，返回**校准过的 top 10** 给生成器 | → **10** | **the verdict** —— *诱饵的任务早已结束* |

**p95 延迟保持在一两秒以内，因为每一级都在下一级开销之前先收窄。**

### 4.3 去重、诱饵与最高法院

**在任何法官开口之前——一个证人只准一个声音。**

派生语料库**保证**同一个源会**多次到达**：作为它的 chunk、它的 factoid、它的 QA 诱饵、它的 rewrite——而**一个被塞了同一段落五套戏服的 reranker，浪费了五个席位**。**所以在筛子之前先坍缩共享父级的候选**，然后**对剩下的用 MMR 求多样性**。

> 📎 正课 p.67 补了关键的一条：**余弦去重救不了这个**——**一个问题和它对应的段落本来就长得不像**（那正是 QA pair 有用的原因）。**必须按 `source_chunk_id`（身份）折叠，不能按相似度。** 而且**顺序不能反**：先跑 MMR，MMR 会把那几种化身当成「多样性」而主动保留它们。

**然后是那条绊倒最多团队的教条**：

> ### **The decoy's job ends at retrieval.**
> **cross-encoder 到场时，它必须拿 query 去审判「源文本」——绝不是那个合成问题，绝不是 rewrite，绝不是 summary。**
> ***A reranker grading the decoy is a court cross-examining the bait.***（一个给诱饵打分的 reranker，是一座在盘问自己下的饵的法庭。）

> 📎 正课 p.68 给了**机制**（而不只是比喻）：**那个 decoy 是「为了像问题」而被制造的，所以它当然像问题——这个分数不携带任何关于「这份文档能不能回答问题」的信息。对诱饵的判决在结构上无意义。**
> 并且给了**一个讲义没有的例外**：**一段为「主题查询」检索到的摘要，在那个高度上本身就是证据——按它自己重排。** 判据是：**「在这个查询的高度上就是证据」→ 按自己重排；「只是指向证据的替身」→ 解析回源。**
> 外加一条实用警告：***粒度需要配额或路由；一个「段落相关性」的法官会误判高度。***

**最高法院本身**——那台读得少、想得深的 cross-encoder——**已经便宜到**（rerank-2.5、Rerank 4、指令跟随、32K 窗口）**问题不再是「要不要设这个席位」，而是「递给它多深的案卷」**；而**它的判决必须在出口处被校准**，好让 **0.8 分在周二和在上线那天意思相同**，好让**一个弃权阈值可以被信任**。

### 4.4 问题侧：六种病理，六个动词

> **一半的架构站在 query 这一侧。一个 query 是「某人知识里的一个缺口」的描述，匆忙打下，并且以少数几种反复出现的方式到达时就已经坏了。**

**讲义给的六种**：

| 病理 | 动词 | 做法 |
|---|---|---|
| **Misspelled（拼错）** | **correct** | **便宜、确定性、最先做**；稀疏车道对一个换位字母毫不宽容 |
| **Underspecified（欠指定）** | **expand** | 「那份政策」→「2026 年准备金政策」；**伪相关反馈**与**会话自身的上下文**补上用户没说的 |
| **Overloaded（超载）** | **decompose** | 两个问题共用一个问号 → 拆开、分别检索、再合并（**multi-query fan-out**） |
| **Ambiguous（歧义）** | **对着语料消歧** | "Java" 在一份语料里是岛、在另一份里是语言；**是语料而不是词典说了算** |
| **Register-mismatched（语域错配）** | **rewrite** | 把朴素问题用语料的方言重述——**写时 rewrite 派生物的读时孪生兄弟** |
| **Multi-hop（多跳）** | **plan** | 答案需要一个中间答案的问题 → 拆成链、迭代检索——**agentic turn 的种子** |

> ⚠️ **正课 p.79 给的六种和讲义不完全一样**，新增了 **Context starvation → inject** 和 **Temporal ambiguity → resolve**，省掉了 rewrite 与 plan。**两套合起来是八种**，详见第〇-B 节 p.79。

**变换级联按成本顺序施加**（讲义边注）：**先便宜的确定性修复**（拼写、归一化、缩写展开）→ **再分类**（哪种病理、哪个高度、哪条路由）→ **再是 LLM 中介的改写** → **HyDE 最后**。**每一级都应该能短路掉其余各级——大多数 query 只需要第一级。**

**HyDE**：**捏造一个假想答案并 embed 它**——**一个文档形状的探针，去探一个文档形状的索引**。

> **HyDE 就是把生成 QA pairs 放到读时而不是写时来跑**：**一条原理（通过生成缺失的那一侧来消除语域错配），两个时机。** **最后才用它，用一个有能力的模型，并且知道：一个捏造的探针可以捏造出一整个邻域。**
> 📎 正课 p.81 的补充：**QA pair 是资本支出（离线，一次性），HyDE 是运营支出（在线，每次重付）——能用前者解决的就不要用后者。**

**派生侧的两条教条在这里以镜像返回**：

> **The canonised query**（拼写、扩展、消歧之后的规范化 query）**是每条车道收到的东西**，好让**车道们对同一个问题投票**；
> **The original query**（用户原话）**是 cross-encoder 审判时对照的东西**，好让**一次漂离了用户意图的变换无法通过法庭把自己洗白**。
> ***Transform for retrieval; judge against the truth.***

> 📎 正课 p.80 给了 canonized query 的**第三个用途**：**它，而不是原始字符串，才是语义缓存的键。**「WFH policy」和「remote work policy」必须在进缓存之前收敛。
> 同页还有一条容易漏的安全细节：**确定性修复在护栏之前，LLM 辅助改写在护栏之后——绝不在预筛之前放大对抗性内容。**

### 4.5 前门、路由与 agentic turn

- **语义缓存是前门**：一个 embedder `E` 和一个阈值 `τ`，决定这个问题**是否实际上已经被问过**——**serve、hint、或 miss，绝不 guess**。**它值得拥有自己的一天，而它下周就会拿到。**
- **路由器**把每个问题送到**对的目录**和**对的法庭**：**point 与 contextual 流量走高速公路；thematic 走 summary 车道；global 的少数派走图 sidecar；schema 问题走结构化存储**。
- **Agentic turn**（Search-R1 及其同类，**用强化学习端到端学出来的检索**）是**路由器最昂贵的一档——阶梯上的一级，不是异端**。
- **最安静的优化**：**有时正确的答案是根本不检索**——参数化答案已经够了、或者问题只是一句问候、或者缓存里已经有了。**一个反射式检索的系统，在为它用不上的证据付钱。**

> 📎 正课 p.83 的升级：**一个全局的权重向量，是跨所有高度的一个妥协。成熟的系统先分类，然后按查询类别给车道重新加权**——也就是说**代理曲面法要按 query class 各跑一次**。

### 4.6 机房（The Machine Room）

> **召回是用毫秒买来的，而汇率由「找到一个邻居」这件事的物理学设定。**

- **图索引（HNSW）**：拿内存换速度
- **磁盘驻留索引（DiskANN）**：拿延迟换规模
- **量化**（product、scalar、直到 1 bit）：拿精度换预算行——**而 scoop-and-rescore 模式把量化损失的东西找回来**

**三条让这间房保持诚实的戒律**：

1. **版本偏斜（Version skew）**：**一次查询绝不可以跨 embedder 版本。** 迁移用**双写**，**一次只从一个索引服务**，**绝不拿 v2 的 query 去比 v1 的向量**。
2. **投毒（Poisoning）**：**PoisonedRAG 表明，在数百万份的语料里放五份精心构造的文档，就能操纵 90% 的目标答案。** 所以**把每一份被摄取的文档当作不可信的代码**，**给检索到的证据打聚光灯（spotlight）**，并**在被污染的候选池上留意静默的检索坍缩**。
3. **访问控制（Access control）**：**索引时同步 ACL，查询时前置过滤（pre-filter），绝不后置过滤（never post-filter）**——**一个把十条结果里的八条删掉的 post-filtered top-K，已经静默地变成了一个 top-2，而召回天花板在无人察觉时塌了。**

> **成本账簿**（存储字节、每索引的边际美元）**是 CFO 读的那份，而组合里的每一个索引都必须向它记账。**

**服务中层法官是大多数延迟预算被赢下或输掉的地方**：

- **对几百个候选做的全维 rescore 是一次矩阵乘法，它属于和索引同一台机器**；
- **ColBERT pass 在赢得资格时，正是 MUVERA 的固定维编码与残差压缩兑现价值的地方**；
- **cross-encoder 的案卷深度是那个「用最多毫秒换最多质量」的单一旋钮**——**在标尺上调它，在仪表盘上盯它，并且绝不让一次 demo 的二十候选案卷悄悄变成生产环境的五十**。

**索引运维补完这间房**：**活的目录必须在 churn 时按出处键重新推导、按双写 playbook 在引擎间迁移，并在——不是「如果」而是「当」——某样东西丢失时，从语料和配方里重建。**

> **时钟预算（大致）**：**车道并行，各数十毫秒；融合与去重，个位数毫秒；全维 rescore，数十毫秒；cross-encoder，一百到几百毫秒**（取决于案卷深度与模型）——**对一块交易屏幕不可接受，对一条批处理管线则是免费的**。
> ***Latency is not a performance metric; it is a structural constraint that decides which judges may sit.***（延迟不是一个性能指标，它是一条决定「哪些法官有资格入席」的结构性约束。）

### 4.7 会看的目录（The Seeing Catalogue）

**Otlet 也收集图片，我们也必须。** 两条车道：

- **双塔车道（CLIP 及其后裔）看的是风格**——它把图像和文本嵌进同一空间，**但读不懂图里的一句话**；
- **caption 车道制造每一张图像的文本派生物**（**Otlet 的卡片，为像素而机械化**），**于是整套派生机器都适用**。

**然后是 OCR-free 的转向**：**ColPali 用后期交互直接检索页面图像，完全跳过解析器**；而**那项曾让这件事成为奢侈品的存储税，已经被拯救了 ColBERT 的同一套压缩废除了**。

> **展品加入同一份案卷：级联不在乎一个候选最初是一个段落还是一页图像。**

### 4.8 耦合标尺，与两栏账簿

> **这堂课里没有任何东西是在没有标尺的情况下可判定的——评估那两周就是为今天做的准备。**

- **gold set 是封存的、带版本的、对工程师隐藏的**；
- **关于某个组件的每一条声明都是那个集合上的一个配对 bootstrap 区间，绝不是一个点估计**；
- **公开排行榜是冒烟测试，不是仪器**——Evalcraft 的教训，用在我们自己身上；
- **标尺必须是活的**：**一个在上线时冻结的 gold set，测量的是你已经不再拥有的那批用户**，而 **Say 定律保证你的用户会变。**

**然后是 Pacioli 的纪律（威尼斯，1494）用在架构上——每个组件都要记两笔账**：

| 栏 | 内容 | 谁来写 |
|---|---|---|
| **第一栏：在场的成本（cost of presence）** | 构建步骤、需要的数据、延迟、维护、**那件从此可能在凌晨两点坏掉的东西** | **供应商会热切地替你逐项列出** |
| **第二栏：缺席的代价（price of absence）** | **没有它就退化的那类查询、登记那次退化的那个指标、用户真的会看见的那个失败** | **只能由测量来写**：一次消融、一场锦标赛、一条考古学轨迹 |

> **一个第一栏写满、第二栏空着的组件，不是基础设施。它是装饰。**
> 📎 正课 p.54 把它推进了一步：**成本不是组件的属性，是「组件 × 查询类别」这个配对的属性。** 正确的问法是「**这个组件，对这一类查询，值不值**」。

### 4.9 Playbook：规模决定架构，每个索引都要挣得自己的位置

**这份 playbook 的第一页是一个被软禁的老人写的。** **伽利略，1638**：把一根骨头在每个维度上放大，**强度按长度平方增长，而重量按长度立方增长**；**巨人在自己的股骨下垮掉**。**Haldane 的老鼠走开了；马摔成一摊。昆虫把骨骼穿在外面而繁荣；大象做不到。**

> **规模决定架构——不是品味，不是时尚，不是最新的那篇帖子。**

- **在蟑螂尺度**（一万份文档、一种语域）：**外骨骼**——调好的 BM25、一个慷慨的窗口、一台 cross-encoder——**不是妥协，它就是正确答案**。
- **规模上升到异质语域 + 监管级质量线**：**新的失效模式涌现**，在 **Anderson 精确的那个意义上：more is different**；而**内骨骼**——组合、派生语料库、法庭——**正是新物理学所要求的东西**。

**然后是那个告诉你「何时停止建造」的流程——升级阶梯（the escalation ladder）**：

> **朴素基线（BM25 + 一个 LLM）是神圣的；它是零假设，而你加的每一个组件都是一次「零假设不够用」的声明。**
> **在标尺之后建基线，绝不在之前；把可接受标准白纸黑字锁死；一次升级一个组件，每一级都测量；跑锦标赛；无情地消融。**

**各级（供参考）**：

| 级 | 内容 |
|---|---|
| **L1** | 基线（BM25 + LLM） |
| **L2** | dense 车道 |
| **L3** | 混合融合 + 一台 cross-encoder ——**质量通常在这里第一次跳跃** |
| **L4** | 后期交互（ColBERT） |
| **L5** | 完整级联 |
| **L6** | 派生 sidecar |
| **L7** | 检索前智能（问题侧） |
| **L8** | grounding 环路 |
| **L9** | 图 sidecar |
| **L10** | **被治理的 concept 层**——**只为被治理的核心赢得，且只在真的有主人会评审的地方** |

**这架阶梯是 Shapley 值的一个实用近似**——一个组件在**所有组装顺序上平均**的期望边际贡献：

$$
\varphi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(n - |S| - 1)!}{n!}\Big[v(S \cup \{i\}) - v(S)\Big]
$$

**唯一公平的功劳分配，也是那台把工程学和货物崇拜（cargo cult）分开的仪器。**

> **自底向上（阶梯）采样了一个顺序；自顶向下（消融）采样了另一个；两者合起来近似那本公平的账簿**，并**暴露出两种被点名的病理**：
> - **Kitchen Sink（洗碗池）**：每一项 arXiv 技术都被采纳，因为「它也许有用」；
> - **Sacred Cow（神牛）**：某个组件被留着，因为它很贵、或者有人力荐它。
>
> ***If removing it changes nothing, the cow is beef.***（如果拿掉它什么都没变，那头牛就是牛肉。）
> **Every index must earn its place through ablation.**

> 📝 **我的补注（不是讲义 / deck 的说法）**：神牛有一个**对偶**——**「烧过的手」：因为草率实现过一次、踩过坑，所以永不再碰。** 两者是同一个错误的两个方向：**用历史代替测量。**（deck 相关页在 **p.109 `CODA · THE DISCIPLINE OF ESCALATION`**，尚未截取。）

### 4.10 祝祷：全天一直在建的那句话

> **1940 年被摧毁的不是知识，是知识的表征**——目录、摘要、卡片本身——**而让那次损失不可逆的，是 Otlet 的推导管线是由馆员和四十年做成的。**
> **我们的可以重跑。今天我们建的每一个索引都是派生物，可以从两样东西重新生成：语料，以及这堂课写下来的配方。**
> **烧掉我们的 Mundaneum，我们就把它重新推导出来**——一座算力冰山、几天的管线时间、一套回归测试来证明这次重建是诚实的。
> ***The corpus is the only irreplaceable artifact. Guard it, project it many ways, and let the court decide.***

**全天的收束句**：

> **Scoop wide and sieve hard; manufacture what the examiner will ask; let cheap judges spend their pennies so the supreme court can afford its verdict; and let every index earn its place, or let it go. One corpus, many catalogues — and the discipline to know, by measurement, which of them to trust.**

**下周**：**语义缓存**——今天这栋房子的**前门**，也是「**在读时从诚实信号计算出来的信任**」这条纪律再次回归的地方。

---


## 五、故事 ↔ 教条对照表（讲义在收尾时由全场重建的地图）

> **这是在时间压力下重回这份材料最快的路。**
> ***The stories were not decoration on the mathematics; they were the mathematics before it had notation.***

| 故事 | 它教的那条教条 |
|---|---|
| **沙坑里的弹珠** | **召回天花板**：只有铲子决定什么被捞起 |
| **Mundaneum** | 一份语料，许多目录；**有组合而缺法庭** |
| **CT 扫描仪** | **断层扫描原理**：融合就是重建；拒绝全景敞视 |
| **同学的四十道题** | **用户即考官**；制造派生语料库 |
| **Berlin 那一段** | **embedding 稀释**，以及救回被静默丢弃答案的 factoid |
| **丢掉 "irrevocable" 的法律改写** | **检索派生物，从源生成** |
| **千元实习生发票** | **sidecar 教条**：望远镜不是给手表用的 |
| **百万 token 的竞标** | **长上下文幻象**：窗口装证据，它不负责找证据 |
| **没人能归一化的记分牌** | **按名次融合**；RRF，k=60 |
| **证人席上的诱饵** | **诱饵的任务在检索环节结束**；重排源文本 |
| **可疑地便宜的那 TB** | **机房的账簿**；版本偏斜与前置过滤的 ACL |
| **伽利略的巨人** | **规模决定架构**；外骨骼到内骨骼；每个索引挣得自己的位置 |
| **那张回来的卡片** | **被治理的 concept**，第七件派生物，最顶一级 |

> **而在这一切背后，是一位有着一千六百万张卡片的比利时律师——他有组合、缺法庭——而他的卡片今年夏天回来了，以带着出处写在 frontmatter 里的 typed markdown 的形式。**

**正课 deck 额外给的几个故事/意象**（见第〇-B 节）：

| 来源 | 意象 | 教条 |
|---|---|---|
| p.9 / p.10 | **Mein Herr 的一英里比一英里地图** / **Borges 帝国的地图** | **完美的地图就是没有地图**；不省略任何东西的地图会被所有人抛弃 |
| p.11 | **航海图 / 公路图 / 政治图 / 地质图** | **每一张之所以有用，正是因为它丢掉的东西** |
| p.21 | **溜进极冠的长颈鹿** | 更紧凑的向量 = **更粗的光圈**，只多不少 |
| p.43 | **西雅图与郊区**（p.81 HyDE） | **细节全错，语域对了** |
| p.50 | **穿了西装的 chunk** | 未经评审的 bundle **比 chunk 更糟，因为西装被读成权威** |
| p.53 | **用望远镜读手表** | 点查询穿过图 = 二十倍账单 |
| p.82 | **1 型 vs 2 型糖尿病的碰撞** | **绝不做没有阈值的 KNN** |
| p.86 | **算命先生的郊区** | 没有阈值的 KNN 永远有答案——最近的那个错误答案 |

---

## 六、阅读清单

### 必读（讲义指定顺序，每一篇都是今天架构的一堵承重墙）

1. **Cormack, Clarke & Büttcher — *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods*（SIGIR 2009）**
   三个作者，一页纸，k=60——**在你的 hold-out 集另有说法之前，这就是法庭的宪法**。读它是为了看清**这么一点点算术怎么把学习式融合压了十年，以及为什么**。
2. **Chen et al. — *Dense X Retrieval: What Retrieval Granularity Should We Use?*（2024）**
   **命题作为检索单位**——单篇原则的机械化，带着 FactoidWiki 的 2.57 亿张卡。**粒度论证的数字版；和 Berlin 实验并排读。**
3. **Yeh et al. — *Decoupled Contrastive Learning*（ECCV 2022）**
   **正例离开分母。** 短，且它解释了**为什么 house loss 是它现在的样子、为什么小 batch 不再是一种税**。
4. **Sarthi et al. — *RAPTOR*（ICLR 2024）+ Edge et al. — *From Local to Global*（2024）**
   **变焦镜头与望远镜。** 带着 **sidecar 教条**和 **LazyGraphRAG 的成本更正**，重读 Week 05 的 GraphRAG 论文。
5. **Modarressi et al. — *NoLiMa*（2025）**
   **长上下文幻象，被测量出来**：去掉词面重叠，前沿模型在 32K 处腰斩。**下次有人告诉你检索已经过时，这就是你需要的证据。**

### Oliver Twist 的选读清单（可选，各自加深一条线）

- **Kusupati et al. — *Matryoshka Representation Learning*（NeurIPS 2022）**：**维度作为运行时成本旋钮**——铲子的使能技巧，以及 **MRL–DCL 不变式为什么要紧**。
- **Khattab & Zaharia — *ColBERT*（SIGIR 2020）+ Dhulipala et al. — *MUVERA*（2024）**：**后期交互，以及那个把多向量检索归约成单向量 MIPS 的定理**——成本反对意见的诞生与倒下。
- **Anthropic — *Introducing Contextual Retrieval*（2024）**：**目录里收益最高、最不炫目的升级**：**每百万 token 一美元，换检索失败率的三倍改善**。
- **Zou et al. — *PoisonedRAG*（USENIX Security 2025）**：**数百万里的五份文档，90% 的操纵**——机房要上锁的理由。**和护栏那一周并排读。**
- **Rayward — *The Universe of Information: The Work of Paul Otlet*（1975）**：Otlet 的标准学术传记，也是**我们之所以知道这个故事的原因**。**给你心里那个人文主义者：那个用手工建成了我们架构的人。**

---

## 七、校准说明（讲义原话）与消化状态

> **这堂课很长，而它本来就该很长。**——讲义在 *A Calibration Note* 里点名了全天覆盖的东西（Mundaneum 与它精确的教训；论点、召回天花板、断层扫描原理；四种高度；从 BM25 到 ColBERT 的表征；带 DCL、课程表和 MRL–DCL 不变式的被训练仪器；考官与主模式；到第七件为止的派生物清单；长上下文幻象；法庭——按名次融合、去重、诱饵的任务、校准过的判决；问题侧；机房；会看的目录；以及从伽利略的巨人到 Shapley 账簿的 playbook），然后说：
>
> **「那超过了一天的量，也没期待你今晚就全部握住。握住论点和召回天花板。其余的，回到这里来取。」**

**今晚实际要握住的两句**（按讲义的要求）：

1. **A retrieval system is a portfolio of representations and a court of adjudication.**
2. **Only the scoop decides what is caught —— 召回天花板是下游任何东西都抬不高的。**

> ⭐ **结构观察**：正课的 **Prologue 恰好交付的就是这两件**——**p.7 = 论点，p.6 = 召回天花板**。**序章一结束，及格线就已经交付完毕；后面九个小时全部是可以事后再取的深度。**

### 贯穿全天的一条隐藏主线：几乎所有失效都是「静默」的

| 出处 | 静默失效 |
|---|---|
| 正课 p.27 | **赤道带静默填满 top-K**——14 个陌生人进了上下文 |
| 正课 p.34 / p.38 | **铲子静默腐烂**——仪表盘变绿，128 维召回塌了（**6.4 颗弹珠**） |
| 正课 p.43 | **装着答案的段落静默被丢弃**——0.64 差阈值 0.06 |
| 正课 p.45 / p.50 | **幻影簇 / 幻影概念带着 `verified` 静默晋升** |
| 正课 p.70 | **未校准的 0.92 静默放行幻觉**——级联最后、也最安静的失效 |
| 机房 | **post-filter 把 top-10 静默变成 top-2** |

**而正课 p.53 的成本爆炸是全天唯一「响亮」的失效。**

> **可带走的一般规律：成本类故障是响的，质量类故障是哑的——所以前者你会自动修好，后者只能靠纪律。**

### 这门课的另一条习惯：给每条结论标注认识论地位

- p.31：**「DCL 是小 batch 情形下本课的选择，不是普适定律」**
- p.23：**「当反对意见的全部内容是『太贵』时，每年重审」**
- p.58：**「这是混合派的共识，不是党派的共识」**
- p.82：**命中率 20–45%，标注为 `folklore`（江湖传说）——测你自己的**
- Week 09 OKF：**「agent 改变策展经济学这个赌注仍然敞开——目前还没有生产环境的事后复盘，我们如实说出这一点」**

**而面对宣称时，程序是一致的：等测量。**

| 宣称 | 证据 | 结果 |
|---|---|---|
| ColBERT「太贵」（p.23） | MUVERA / WARP / 压缩 | **改口**——反对意见倒下 |
| 长上下文「取代检索」（p.56） | **NoLiMa** | **不改口**——被证伪 |
| agentic「学会推理」（p.84） | **BRIGHT**（~18 → 66.9） | **改口**——被证实 |

### 明确待补

- [ ] **RetrievalCraft monograph 全文**（讲义自述为「完整解剖」；三个参考架构 small/mid/large 的**完整操作点**只在 monograph 里）
- [ ] 课后的 **book chapter**
- [ ] **正课 deck 的缺页**（见第〇-B 节末的补课清单）与 **p.85–125**
- [ ] **Lab**：级联的动手实现（发射深度 → RRF → 父级去重 + MMR → 全维 rescore → cross-encoder）

---

## 八、可迁移的工程动作（对照我们自己的仓库）

按讲义的纪律，这一周能立刻在本项目里落地的**不是新模型，而是几条可执行的测量动作**：

1. **top-K 考古学（成本最低、论据最强）**：给最终结果加**家谱日志**（`artifact_type` + `source_chunk_id` + `lane` + `score`），跑一周，数「多少 top 结果不是原始 chunk」。→ 和 `evals/` 现有 gold set 接口对齐。
   **⭐ 而且几乎免费**：只要实现了父级去重，这两个字段每次查询都已经在手里了，只差一条 log（正课 p.67）。
2. **消融门（ablation gate）**：把「每个索引必须通过消融赢得位置」写进 `decisions/`，作为往后新增任何检索组件的**准入条件**——同时给现有组件补第二栏（缺席的代价）。
   **⭐ 配套**：索引要**分 collection 存**，不要塞一个 collection 加 `type` 字段过滤——**关不掉就测不出**。
3. **MRL–DCL 不变式回归测试**：任何 embedder 更换之前，在封存集上跑 **recall@500 @ 128 维**（正课 p.34 的措辞是 *No exceptions*）——防「悄悄腐烂的铲子」。
4. **诱饵纪律检查**：审一遍现有 rerank 路径，确认 **cross-encoder 拿到的是源文本**而不是 rewrite/QA/summary；以及 **ACL 是否是前置过滤而非后置过滤**。
5. **canonised query vs original query 分流**：确认送进各车道的是规范化 query，送进 cross-encoder 的是**用户原话**；并确认**语义缓存的键用的是规范化 query**。
6. **两栏账簿**：给 `docs/` 里已有的每个检索组件补一张两栏表，第二栏空着的**当场标记为「装饰」**并排进消融队列。**并按 query class 分开记**（p.54）。
7. **拒绝理由分类**：`decisions/` 里每条否决记录带 `rejected_because: capability | cost`，**cost 类的自动进年度复审队列**（p.23）。

---

## 参考文献

Cormack, Clarke & Büttcher (2009). *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods*, SIGIR '09, pp. 758–759 · Chen et al. (2024). *Dense X Retrieval: What Retrieval Granularity Should We Use?*, arXiv:2312.06648 · Yeh et al. (2022). *Decoupled Contrastive Learning*, arXiv:2110.06848, ECCV 2022 · Sarthi et al. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*, ICLR 2024, arXiv:2401.18059 · Edge et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*, arXiv:2404.16130 · Modarressi et al. (2025). *NoLiMa: Long-Context Evaluation Beyond Literal Matching*, arXiv:2502.05167 · Kusupati et al. (2022). *Matryoshka Representation Learning*, NeurIPS 2022, arXiv:2205.13147 · Khattab & Zaharia (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT*, SIGIR '20, pp. 39–48 · Dhulipala et al. (2024). *MUVERA: Multi-Vector Retrieval via Fixed Dimensional Encodings*, arXiv:2405.19504 · Formal, Piwowarski & Clinchant (2021). *SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking*, SIGIR '21, pp. 2288–2292 · Anthropic (2024, Sept.). *Introducing Contextual Retrieval* · Gao et al. (2023). *Precise Zero-Shot Dense Retrieval without Relevance Labels*（HyDE）, ACL 2023, pp. 1762–1777 · Bruch, Gai & Ingber (2023). *An Analysis of Fusion Functions for Hybrid Retrieval*, arXiv:2210.11934, ACM TOIS · Hofstätter et al. (2020). *Improving Efficient Neural Ranking Models with Cross-Architecture Knowledge Distillation*（Margin-MSE）, arXiv:2010.02666 · Moreira et al. (2024). *NV-Retriever: Improving Text Embedding Models with Effective Hard-Negative Mining*, arXiv:2407.15831 · Gutiérrez et al. (2025). *From RAG to Memory: Non-Parametric Continual Learning for LLMs*（HippoRAG 2）, arXiv:2502.14802 · Jin et al. (2025). *Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning*, arXiv:2503.09516 · Zou et al. (2024). *PoisonedRAG: Knowledge Corruption Attacks to RAG*, arXiv:2402.07867, USENIX Security 2025 · Faysse et al. (2024). *ColPali: Efficient Document Retrieval with Vision Language Models*, arXiv:2407.01449 · McVeety & Hormati (2026, June). *How the Open Knowledge Format can improve data sharing*, Google Cloud Blog · Shapley (1953). *A Value for n-Person Games*, Contributions to the Theory of Games II · Rayward (1975). *The Universe of Information: The Work of Paul Otlet for Documentation and International Organisation*, FID/VINITI · Qamar, A. (2026). *Week 10 Lesson Plan — The Library of Many Catalogues*, SupportVectors · Qamar, A. (2026). *The Room as the Corpus*（Week 10 Prelude，20 页）· Qamar, A. (2026). *The Library of Many Catalogues*（Week 10 正课 deck，125 页）

