# Week 09 总结 —— 当知识拿到了自己的证件：Open Knowledge Format 与被治理的语料

**日期：** 2026-08-08 · **来源：** `course/week_09/summer-week-9-lesson-plan.pdf`（*When Knowledge Gets Its Papers — The Open Knowledge Format and the Governed Corpus*，Asif Qamar, SupportVectors）、*The Library in Your Head* 开场 deck（31 页）、下半场 Module 5 *Secure Retrieval / Enterprise Entitlement-RAG* 现场记录

---

## 一句话结论

整周可以压成一句话：

> **语料从来不是一个既定之物，它一直是一个选择 —— 把知识系统的智能从查询时搬到创作时。**

Week 07 量检索，Week 08 量生成器，**本周退后一步问：被检索的东西，到底是用什么材料造的？**

讲师给出的最锋利的一句浓缩：

> *"Our trained instinct: chunk, embed, retrieve top-k — **the corpus as a given**. The quiet radicalism today: **refuse the given**. Manufacture the corpus into a shape worth retrieving from."*
> （我们被训练出来的本能是：切块、嵌入、取 top-k —— **把语料当作既定输入**。今天这场安静的激进是：**拒绝这个既定**，把语料制造成一个值得被检索的形状。）

本周没有新数学。精读的是 Google 2026 年 6 月 12 日发布的年轻规范 **Open Knowledge Format（OKF）**。

全天结构：

```
PROLOGUE   The Press Release     （"RAG 死了吗" —— 一个错得有教学价值的问题）
ACT I      The Substrate         （bundle / concept / frontmatter，以及核心倒转）
ACT II     Trust                 （出处、三层信任、认证计算）
ACT III    The Channel           （文档 → 检索通道）
INTERLUDE  The Phantom           （幻觉出来的 concept —— 比坏 chunk 更危险）
ACT IV·CODA  The Other Bank      （经验 → 记忆；反方论证；交叉结构）
```

下半场另起一个模块：**Module 5 · Secure Retrieval**（企业权限 RAG），主题从"知识如何被建模和信任"切换到"检索本身如何被安全约束"。

---

## 开场：The Library in Your Head

延续 Week 08「七个你会亲手失败的实验」的手法，这次是**八次脑内散步**，每一次都先让你在自己身上确认一条直觉，再告诉你下午要给它起什么字段名。

> *"Close your eyes. You already know today's material — we only have to find where you keep it."*

| # | 思想实验 | 预埋的术语 |
|---|---|---|
| **I** | 翻开厚书之前，你早就用书名、简介、出处做过一轮判断 | **渐进式披露引擎 + 信任策略** → `index.md`、`verified` |
| **II** | 一部九百页的权威论著，书脊上写着 *Miscellany, Vol. XI*，封底空白 —— 你连**放慢脚步**都不会 | 元数据失职 → 诚实的 `type`/`title`/`description` 是被找到的先决条件 |
| **III** | 如果把整座图书馆拆成索引卡，一张卡一个事实、按层级归档、互相引用，你会怎么设计？ | 三问 → 一个 concept 装多少、卡片怎么互指、谁维护当前性 |
| **III+** | **揭晓：1895 年布鲁塞尔真的造过。** Otlet 和 La Fontaine 的 **Mundaneum** —— 一千二百万张索引卡，按 UDC 分类归档、交叉引用；寄信或拍电报提问，馆员走抽屉、把抄好的卡片寄回 | **一部用纸做的搜索引擎，比晶体管早五十年** |
| **IV** | 你上学做笔记卡片时，魔法从来不在"拥有"卡片，而在"**写**"卡片 | **理解发生在 authoring time，考试只是 retrieval** |
| **V** | 两种学习材料摆上桌：一堆打乱的散页（每页从句子中间开始又中间结束）vs 几张更大的、自足的索引卡 —— **你还没读一个字，那堆散页就已经让你抵触** | 散页 = **chunk**；卡片 = **concept** |
| **VI** | 活页夹上写着"**Currently**，RAG 课在上午" —— 你会犹豫。犹豫的靶心在哪？ | 三个缺失的时钟 → `stale_after`、`generated`、`verified` |
| **VII** | 一个排版精美、推导 plausible 的公式声称算出前一千个素数。**什么能一锤定音？** | 你会**跑一遍** → 认证计算 |
| **VIII** | "在 X 地立一根杆，春分正午没有影子" —— 你飞不过去、等不到三月。设计一个最便宜的判定性检验 | 剥掉表演，剩下一条可判定的不等式 |

### 三条值得单独记的

**Walk V 的经济账（整场 Prelude 唯一一次把论证升级成算账）：**

> *"The fragment outsources the assembly to **you, at reading time**. The card was **made whole at writing time** — someone paid the assembly cost once, so every reader afterward pays nothing. The stack is cheap to produce and expensive to read — **a hundred times, by a hundred readers**. The card is expensive **once**."*

这是"创作时智能 vs 查询时智能"第一次被讲成纯粹的经济学论证：不是"哪种更优雅"，而是**谁该为理解买单、买几次**。

> **阅读单元的选择，决定理解这件事发生在哪里 —— 要么在写的那一刻发生一次，要么在每一次阅读、永远地重复发生。**

还有一句很锋利的收尾：

> *"When you bite into a fragment, you risk finding **half a thought** — and half a thought can be worse than none."*
> 半个想法比没有想法更危险 —— "没有"会让你继续找，"半个"会让你误以为已经拿到完整答案。（这句精准预言了后面的 phantom concept。）

**Walk VI 的三个缺失时钟：**

> 你的犹豫活在**三处缺席**：currently —— **as of when?** · **Says who?** · **Has anyone confirmed it lately?**
> 一个没有日期的"currently"是一个**时间戳形状的洞**。日程变了，墨水不会褪色 —— **文本不会显性地变老。**
> *"The page might be perfectly right. Your unease is that **nothing on the page lets you tell**."*

这就是 OKF 存在的理由：**不是让每一句话都对，而是让每一份知识都携带足够的字段，使"我怎么知道它对不对"这个问题永远可以被问、被答。**

**Walk VII 的不对称（本周最该背下来的一条）：**

> *"Notice the **asymmetry** you just enacted: **sentences** you weigh; **computations** you re-run."*
> 句子你**权衡**（靠出处、作者、核实记录 —— 概率性的、社会性的信任）；计算你**重跑**（不做社会性判断，直接机械验证 —— 非黑即白）。
>
> **Claims earn trust from provenance. Numbers earn trust from re-execution. Two different kinds of trust, and they must never be conflated.**

---

## Prologue：实际发布的是什么

2026 年 6 月 12 日，两位 Google 工程师发博客宣布 OKF，一周内每个收件箱都在问同一个问题 —— **"RAG 死了吗？"**

> *"The question is wrong — but wrong in an **instructive** way."*

**祛魅陈述（全天最重要的一条）：**

> *"Not a vector-database killer. Read strictly, **not even software**. Knowledge laid down as **markdown files with YAML frontmatter**, versioned in git — readable by a human with `cat`, and by an agent with nothing at all."*
> *"So slight an artifact, so loud a conversation: it touched an **exposed nerve**."*

那根暴露在外的神经就是**碎片化上下文问题**：一个企业 agent 要诚实回答问题前必须知道 —— 哪张表是营收的权威来源、finance 说的"recognized"精确指什么、freshness 告警响起时走哪本 runbook、哪个 API 上季度被废弃了。

> *"None of it lives in one place — it is smeared across catalogs, **three generations of wikis**, docstrings, chat threads, and the heads of senior engineers."*

---

## Act I：The Substrate

### 承重命题

> 技能（skills）、记忆（memories）、检索到的知识（retrieved knowledge），说到底都是同一件事 —— **在正确的时刻，把策展过的文本放进 context 里** —— 都站在同一个基质上：**小的、有类型的、互相链接的文档，像源代码一样被拥有和治理。**

**推论（全天结构的地图）：**

> 把这套格式对准组织的**文档** → 一个**检索通道**（被治理、被策展、可回答）。
> 把它对准 agent 的**经验** → 一个**记忆库**（可携带、可审阅、可共享）。
> **一个格式，两个方向的流动。** —— Coda 会把这个环合上。

### 谱系与追认

| 时间 | 祖先 | 解决的问题 |
|---|---|---|
| 2024 | `llms.txt` | 内容是**为谁写**的（第一次主流承认内容应该为机器读者创作） |
| 2025 | `AGENTS.md` | 知识**跟不跟着工件走** |
| 2025–26 | `SKILL.md` | **程序怎么打包**（frontmatter + markdown，按需加载） |
| 2025–26 | memory-as-files | **agent 自己的过去存在哪** |
| 2026 | **OKF v0.1/v0.2** | 这个模式，被**追认（ratified）** |

> *"Every element already existed in folk practice. What did not: a public, vendor-neutral document precise enough that producer and consumer **interoperate without a meeting**."*
> *"The cleverness of OKF lies in **how little it dared to standardize**."*

注意措辞是 **vendor-blessed**（厂商背书）而不是 invented（发明）。**它的聪明之处不在于标准化了多少，而在于它敢标准化的东西有多少 —— 故意标准化得很少。**

### 全天最深的一个想法：核心倒转

> *"Classical RAG bets meaning can be **re-derived at query time**: chunk, embed, gamble that cosine similarity reassembles the author's understanding on the fly. OKF moves the intelligence to **authoring time**: the unit of retrieval becomes a **curated knowledge object**."*
> *"Understanding happens **once, at curation, under review** — not on every query, in the dark, **without appeal**."*

**"without appeal"（无处申诉）** 是容易被略过、但很重的一个维度：经典 RAG 的查询时重新推导，不仅是每次重赌一把，而且押错了**没有申诉渠道** —— 没有人在场核对这次相似度计算是否合理。创作时理解多出来的是一层**社会性**：审阅是有人在场、有记录、可被质疑、可被驳回的过程。

### 为什么是现在，而不是 1996

> *"Wikis rot: curation is expensive and humans will not sustain it. What changed in 2025–26: **a worker who does not get bored** — the agent that drafts, cross-references, and opens the PR."*
> *"Elegant symmetry: **embeddings made raw retrieval cheap; agents made curated knowledge affordable.** The wager is open — hold it open all day."*

「创作时策展」这个想法不新（Mundaneum 一百三十年前就是这个思路，wiki 时代也喊过同样的口号）。变的不是格式，是**谁来做这份枯燥、重复、永不停止的策展工作**。

> **Quiz 1：** "我们公司 2009、2015、2021 launch 过三次 wiki，全都两年内腐烂了。OKF 不就是第四个 wiki 吗？"
> **答：** 变的那个经济变量是**策展劳动的边际成本** —— 从"人类注意力"换成了"计算成本"。但批判性的答案还该指出：**生产端变便宜了，审阅端依然是人类瓶颈** —— 单靠"agent 不会腻"只是把失败模式从"没人写"换成了"没人审"。

### 解剖：bundle / concept / frontmatter / body

- 一个 **knowledge bundle** 就是一棵 markdown 文件的目录树，别无其他。git 是推荐的皮肤（提供历史、归属、diff）。
- 每层保留两个文件名：`index.md`（目录清单，供渐进式披露）、`log.md`（按时间顺序的变更史）。
- 其余每个 `.md` 都是一个 **concept**：一个知识单元、一个文件。

**路径即身份：**

> *"A concept's ID **is its file path**, minus `.md`. No UUID. No registry. No content hash. **The filesystem is the namespace.**"*
> *"The Unix instinct applied to knowledge: universal tooling (`grep`, `diff`, `mv`) — at the price of **rename fragility**."*

**两半订在一起：**

```yaml
---
type: BigQuery Table   # 整份规范里唯一必填的字段
title: Customer Orders
description: One row per completed order.
resource: https://console.cloud.google...
tags: [sales, orders, revenue]
generated: { by: reference_agent/gemini, at: 2026-05-28T14:30:00Z }
---
# Schema
| Column   | Type   | Description      |
|----------|--------|------------------|
| order_id | STRING | Unique order id. |
```

> **Frontmatter** = 机器的那一半（你要查询和过滤的那几个字段）。**Body** = 读者的那一半（人和模型实际读的东西）。

唯一必填字段是 **`type`** —— 一个短的、由生产者自创的字符串（`Metric`、`Playbook`、`BigQuery Table`），消费者用它路由，**遇到未知值必须容忍**。

### 链接：藏在树里的图

> *"Concepts link with **ordinary markdown links**; the **kind** of relationship lives in the **prose around the link**. Edges are **untyped** — and the semantic-web tradition winces. The spec's answer: the reader is now a language model, and **language models read sentences**."*
> *"The most revealing choice in the spec: **prose now carries the semantics that formality used to carry**."*

**红链不是错误，是邀请：**

> *"A link whose target does not exist is **not malformed** — it may simply represent not-yet-written knowledge. **The corpus is allowed to want things.**"*
> 一个红链是**地图上可见的边缘**，是下一个贡献者知道该去挖的地方。

### 布局里的经济学

`index.md` 看似小事却是承重的 —— 一份比大部头便宜的目录读物。agent 读根索引只花几百 token，下钻，**只打开问题需要的两三个 concept**。

> *"**Value-of-information**, built into the directory layout — the same economics that govern skill loading and memory recall."*
> `log.md` 是同一个想法**指向时间**：`index.md` 是空间维度的渐进式披露，`log.md` 是时间维度的。

合规门槛几乎贴地：一个 bundle 只要**每个 concept 都有可解析、非空的 `type`** 就算合规。严格性只活在一个地方 —— **消费者必须容忍什么**。

> **这是一份让生产变容易、让拒绝变难的规范：先采纳，靠增量积累严谨 —— 正是 JSON、markdown、HTTP 走过的路。过度规定的标准才是没人采用就死掉的那种。**

---

## Act II：Trust —— 出处、核实、认证

> **v0.1 描述的是一个文件系统，v0.2 描述的是一个社会。**

公告后几周内规范就长出了第二套器官。修订速度说明了作者从真实使用里最先学到的东西：**语料一旦由 agent 撰写，问题就从"这份文件说了什么"变成"我为什么该相信它"。**

### 无分数的出处

```yaml
sources:
  - id: rev-policy
    resource: https://wiki.acme/finance/rr
    title: Revenue recognition policy
    author: team:finance-fpa
    last_modified: 2026-04-02
  - id: exec-rev-dash
    resource: dashboards/exec-revenue
    title: Executive revenue dashboard
    usage_count: 5000
usage_window: { from: 2026-06-01, to: 2026-06-30 }
```

每条 source = **一个 resource + 一个稳定 id + 三个可选信誉信号**（`author`、某窗口内的 `usage_count`、`last_modified`）。注意三个信号里**没有一个是分数**，全是可以被独立核实的原始事实。

**设计上的拒绝：**

> *"No `credibility: 0.87`. A stored score is **subjective, unportable, stale on arrival**. Trust is **inferred at read time**, by each consumer, against its own policy."*
> *"The **personal equation**, applied to metadata: publish the raw readings, never the verdict — **the verdict embeds a judge, and judges do not travel**."*

（这正是 Week 08 开场那个"人差方程"的回归：原始读数可以在观测者之间共享；校正后的结论里已经嵌入了某一个观测者的个人方程，换个人用误差就对不上。）

**逐条归因用了一个优雅的装置：markdown 脚注，标签就是 source id。** 句子里带 `[^rev-policy]`，frontmatter 里带匹配的 source —— **是 keyed 而非 positional**，因为 agent 会不断重写这些文档，而位置索引在列表重排的那一刻就悄悄张冠李戴。

### Writer、Confirmer 与三层信任

信任家族把我们这个领域习惯混为一谈的问题分开：**谁写了这个，谁核实了它。**

- `generated` 记录作者。
- `verified` 记录零条或多条确认事件，每条带一个 actor 和一个时间戳。actor 遵循三段式惯例：`producer/version` 给 agent、`human:id` 给人、`process:id` 给自动化。

**三个层级完全从 `verified` 列表推导：**

| 层级 | 条件 |
|---|---|
| **unverified** | 完全没有 `verified` 键 —— 可见地是草稿或机器猜测，永不被误认 |
| **machine-confirmed** | 只有非人类的 verifier（夜间流程重新核对过，没有人签字） |
| **human-reviewed** | 有至少一个 `human:` actor 在场 —— **整个惯例里最有分量的 token** |

**三个特性（"a small machine"）：**

1. **推导而非声明（derived, not declared）** —— 没有可以伪造或腐烂的层级字段。
2. **独立标注时间** —— "内容在最后一次核实**之后**又被重新生成"这个危险状态是**机械可见的**（`changed since review`：只需比较两个时间戳）。
3. **缺席有意义但从不排除** —— 语料可以持有草稿和直觉，只是清楚标注。

> *"In the classical corpus, the hallucinated wiki page and the audited finance policy arrive **wearing the same clothes**."*

> **Quiz 3：** 一个 concept 8/5 由 `pipeline_agent/v3` 生成，8/7 由 `process:eval-nightly` 核实（没有别人）。8/8 agent 重写了 body，无人重新核实。推导 8/7 和 8/8 之后的层级。
> **答：** 8/7 = **machine-confirmed**（只有 `process:` actor）；8/8 之后 = **降级回 unverified** —— 内容修改时间晚于唯一那次核实，那次核实已经不再覆盖当前内容。**配对的日期暴露的不是内容错没错，而是核实本身有没有跟上内容。**

### 生命周期

> *"Knowledge ages like **milk**, not wine."*
> `status:` `draft` → `stable` → `deprecated`（deprecated 的 concept 被保留，供链接和历史）
> `stale_after:` 一个**绝对日期**，**stamped at write time, when the shelf life is best known** —— 在最了解时效性的那一刻，由作者提前把保质期写死。
> *"Retire a concept the way a library moves a book to the **annex** — not the way a database **drops a row**."*

### 认证计算：规范最原创的一招

**企业语料里最危险的不是断言而是数字** —— 而 agent 面对数字的诱惑不是抄错它，而是**有创意地重新算它**：一段似是而非的 SQL，恰好错在财务团队的识别政策明令禁止的地方。

```yaml
type: Attested Computation
runtime: bigquery           # 锁定执行环境
parameters:                 # 声明的是语义，不是取值
  - { name: fiscal_year, type: integer, required: true }
computation: computations/revenue.sql   # 独立存放，模型看不到也改不了
executor:
  resource: references/skills/run-bq.md
  receipt: [job_id, executed_sql, result]
attester:
  resource: references/attesters/rev.py
  # deterministic code — no LLM, by rule
```

**认证原则（the sharpest line in the spec）：**

> *"The model may supply **values for declared parameters**. It may **never** author or edit the computation."*
> *"The attester re-derives the expected binding and compares it to the receipt of what **actually ran** — a rewritten query **mechanically fails**."*
> *"'Did the sanctioned thing run' becomes a **string comparison** — the one link in the chain from which the LLM is **banished by design**."*

**谱系：这是从可信计算（trusted computing）移植来的 remote attestation** —— measure → compare → gate 这套三段式，原本用来验证远程机器上跑的二进制没被篡改，这里被原样搬到 SQL 上，**LLM 扮演的是那个 untrusted host**。

> *"The model, creative and unreliable, fills **typed holes**; deterministic code **checks the paperwork**."*

**两条轴必须分开（Definition-trust vs Run-trust）：**

| | `verified` | attestation |
|---|---|---|
| 确认的是 | **定义**依然匹配政策 | **单次运行**以受批准方式产出了这个值 |
| 粒度 | doc-level | per-call |
| 节奏 | 慢（人工核实） | 运行时（跟着执行走） |
| 存储 | 记在 bundle 里 | **从不存储** |

> *"A **stale definition can attest cleanly**; a **fresh definition still needs attestation on every run**. Conflating the axes **is how dashboards lie**."*

### 收束：一个 chunk 答不出的四个问题

| 问题 | chunk 的答案 | concept 的答案 |
|---|---|---|
| **Who says so?** | uncredited（无出处） | `generated.by`、`verified[].by`、脚注连接 |
| **Is it still true?** | unknowable（不可知 —— 文本不会显性变老） | `stale_after`、`status`、source 的 `last_modified` |
| **Has anyone checked?** | **silence**（沉默） | 一个带日期签字的推导层级 |
| **Where did this number come from?** | **wherever the embedding landed** | 一次受批准的计算，经过认证 |

> *"These are the questions **every enterprise answer must survive**."*

（**这不意味着 chunk 过时** —— 对大规模无结构语料的逐字召回依然是它的主场。）

> **Quiz 4（陷阱题）：** 一个同事想在查询时读 OKF 存的那个 trust score，它在哪个字段？(a) `credibility` (b) `trust_score` (c) `usage_count` (d) `verified.score`
> **答：没有一个选项是对的** —— 题目前提本身是假的。排名**从来不在 bundle 里被计算或存储**，而是在查询时、由每个消费者依自己的策略，从 `sources` 里那几个原始信号现算出来的。这道题真正在提醒设计者：**"想要一个分数"是一个非常自然、非常常见的错误冲动，格式必须对它免疫。**

---

## Act III：The Channel —— 文档 → 检索通道

> *"a derivative artifact with **a human gate built into its format**"*

### 给尸体命名：权威失败

> *"Similarity retrieval has no notion of **authority**, **currency**, or **correction**. Three definitions of **recognized revenue** across five years: top-*k* returns the most **similar**, never the most **authoritative**. And when an error is found — **no unit to correct**."*
> *"Retrieval dies here not by missing text, but by **returning text no one currently stands behind**."*

**野外的尸体 —— Cosine similarity 0.91：**

- 一份来自**已被取代的政策**的合规回答
- 一份来自**重组前**旧 deck 的指标
- 一份点名**已下线服务**的入职文档

统统以 0.91 的相似度被检索出来。

> **Invisible to every metric of the last two weeks** —— 过去两周学的 MRR、nDCG、Recall、RAGAS faithfulness 全都看不见这个问题：这段文本**确实相关**，只是**不再为真，或不再被认可**。**我们的几何对这两者都没有轴。**

### Week 1 的辩论被重新打开

> Week 1 问：to chunk or not to chunk？**这条轴现在多了第三个点。**
> **Chunk raw text** —— 意义在查询时被重新推导。
> **VLM over the page** —— 视觉页面被保持完整。
> **Author into OKF** —— 单元**在被检索之前就已经被做成完整的**。
>
> *"One axis underneath: **where does understanding happen?** A chunk boundary **bites the apple and finds half a worm**; a concept is **born whole** — and an LLM integrity pass in CI can verify that wholeness."*

### 转换：文档 → bundle，穿过一道门

```
documents → extraction agent → pull request → governed bundle → retrieval channel
```

> Agent 提议**带类型、带出处**的 concept；产物落在一个 **pull request** 里，由**领域所有者**审阅。**只有被合并的 bundle 才对外服务。**
>
> *"The PR is **not plumbing** — it is an **epistemic event**: synthesized text is either promoted to governed knowledge, or refused. **Corrections return as diffs, not re-ingestions.**"*

### 三条特性

1. **修复很便宜** —— 一个错误事实是一次**单行 diff**，不是一次季度重摄取。
2. **它启用了导航** —— agent 像图书管理员走书架一样走索引和链接，与 embedding 并行。
3. **审阅门是结构性原生的** —— **merge 本身就是升级事件**，记在 `verified` 里，机械地抬高层级。
   > *"Recall the phantom cluster: synthesis needs a coherence gate, and **we had to bolt one on**. Here the gate is **the format's native workflow**."*

### 梯子规则是一条限定范围的规则

> 攀爬这一级，代价花在**真正要紧的货币**上：**持续的人类注意力**。抽取对 agent 来说便宜，**审阅对 owner 来说贵**。
>
> 只为**术语表、指标、政策、runbook、API 合约**这几千个 concept 攀爬 —— 那些**权威失败会真正致命、且有一个人握着笔（an owner holds the pen）**的地方。
>
> *"Leave the long tail — slide archives, ten million emails — to the **similarity machinery that handles bulk with grace**."*

### 诚实的账（借方栏，没有缓冲垫）

| 借方 | 内容 |
|---|---|
| **Curation recurs** | 一个被**橡皮图章**通过的 bundle，会腐烂成它本来要取代的那个未被审计的语料，**还多了一层不该有的权威光环 —— 情况更糟** |
| `stale_after` | **是一个闹钟，不是一支维护队伍** |
| 覆盖面 | 结构性不完整 —— **策展者只回答他们预料到的问题** |
| 抽取本身 | **会产生幻觉**（见下一节） |

**对着这份借方，唯一一条贷方：**

> *"The only artifact that **gets better with age under use** — corrections accumulate as diffs. **The metal self-anneals.**"*
> （退火：金属在受控加热下消除内部应力、变得更坚韧。语料在持续使用和持续修正下，会把使用中暴露的应力点一点点修掉 —— **用得越久、错得越少**，前提是人类注意力没有断供。）

> **Quiz 5：** VP 下令："把所有公司知识 —— 一千万封邮件、每一份 deck、wiki、政策手册 —— 全部转成 OKF，Q4 之前完成。"
> **答：政策手册、术语表、指标定义：爬**（definitional, audited, owner-reviewed）。**一千万封邮件、幻灯归档：留在下面**（**bulk without owners**）。决定性的货币是**持续的人类注意力** —— 一级台阶只在有 owner 愿意审阅的地方才配被攀爬，因为**一个未经审阅的 bundle，只是一堆穿着西装的 chunk（chunks wearing a suit）**。

---

## Interlude：The Phantom —— 幻觉出来的 concept

### 解剖

> 一个 agent 铸造出 `recognized-revenue.md`：类型化的 frontmatter、描述清脆、**三条真实的 sources**、逐条脚注都连着。而这个定义**微妙地错了** —— 是对三份**已被取代**的草稿一次似是而非的调和；**一句没有任何一个版本的政策真正包含过的句子。**
>
> *"Interpolating fluently between things that were each individually true — **exactly the way language models synthesize**."*

注意这划清了 phantom 和"过时信息"的界限：**过时信息曾经为真、只是现在不再为真；phantom 从一开始就从未在任何一个真实文档里出现过。**

### 为什么它比一个坏 chunk 更危险

> **信任机制是一台推广信任的机器。** 一个熬过审阅的 phantom 会被合并、盖上 human-reviewed 章、**被过滤进各层级本该保护的每一条高风险路径**。一个幻觉出来的 chunk 是**裸奔着（naked）**到达的，会被环境性地怀疑。
>
> *"The phantom arrives wearing **the review gate's own seal** — a faithfulness failure laundered by the governance process, and **governance is why it will be believed**."*

**越是治理完善、审阅严格的系统，一旦 phantom 混进去，被相信的程度就越高** —— 这不是治理机制的漏洞，是它**正常运作**的必然副产品。

### 四道防线，一个都不能少

1. **审阅的是忠实度，不是形式** —— 逐条脚注核对声明与出处。*"YAML hygiene is a **rubber stamp**."*
2. **忠实度核查本身要被工具化** —— 对 (句子, 被引用片段) 做**蕴含核验（entailment pass）**，跑在 CI 里，像测试挡住代码合并一样挡住 merge。*"**Tests for knowledge PRs.**"*
3. **数字不给任何散文空间** —— 任何量化声明都必须落在一次认证计算里。*"**A phantom cannot forge a receipt.**"*（四条里唯一一条**不依赖语言判断**、纯靠计算证据的防线。）
4. **未核实的必须在每一个消费者界面里看起来未核实** —— *"or the tiers mean nothing."*（前三道是摄取时的一次性把关，第四道是**每一次消费**都要重新兑现的承诺。）

### 最锋利的一句道德

> *"**A gate concentrates vigilance — it does not replace it.** The format gives the reviewer everything — small diffs, typed claims, joined sources, expiry dates. What it cannot give is **attention**."*
> *"Every governance technique today is the same wager: that attention, **made cheap and pointed precisely**, will be paid. The phantom is **what collects when it is not**."*

---

## Act IV：The Other Bank —— 经验 → 记忆

### 把基底转九十度

> Act III 把格式对准**文档**，得到检索通道。把它对准 agent 的**经验** —— 得到**记忆库**。
> *"Read the spec beside the memory literature and it reads like **that literature's missing appendix**."*
> *"File-based agent memory — standardized by a vendor that may **never have thought of it as memory at all**."*

### 认知地图，重新安家

| 记忆类型 | 性质 | bundle 器官 |
|---|---|---|
| **语义记忆** | 事实、无时态 | **concept 文件** —— *learning faded to a timestamp* |
| **情景记忆** | 带时间戳的事件 | **`log.md`** —— 每个目录讲述自己的历史 |
| **程序记忆** | how-to、被编译过的 | **playbook** —— 一个 `SKILL.md`，**精确到一个字段名的程度** |
| **工作记忆** | 注意力里的热集合 | **索引遍历** —— 渐进式披露即分页 |

**一个惊叹的瞬间 —— 三条谱系，一个划分：**

> Google 当初着手描述的是**数据目录（data catalogs）** —— 而一个由 agent 维护的语料所带来的信任问题，把他们**一个字段一个字段地**，逐渐推到了认知科学**五十年前**就已经画出的那张地图上；agent 民间实践**重新发现**的，是同一张地图。
>
> *"When **three independent lineages** arrive at the same partition, **the partition is probably real**."*

（这是一次经典的**收敛性论证**：自上而下的理论、自下而上的工程试错、外部约束驱动的设计，三条不同方法论、不同动机的路径收敛到同一个四分法 —— 这个四分法更可能反映某种客观存在的结构，而不是任何一方的主观建构。）

### 标准买到了什么：三份红利

| 红利 | 内容 |
|---|---|
| **可移植性** | 框架中立；**积累下来的知识不再是人质（hostage）** |
| **可审阅性** | 记忆写入是 diff；未经审阅的记忆**看得出来是二等公民** —— **一个对抗记忆投毒（memory poisoning）的控制面** |
| **共享记忆** | **一个 bundle 服务一整支舰队** |

> *"The oncall agent's hard-won diagnosis, merged as a playbook, is recalled by an agent that **never lived the incident** — organizational memory, **non-metaphorically**."*

### 四个动词：write, recall, compact, forget

- **WRITE** —— 一次 commit；对任何要紧的事，一个 PR。**什么配得上被记住 = 能熬过审阅的东西。**
- **RECALL** —— **按信任加权**：偏好 human-reviewed，给过期的打折，对数字要求认证。
- **COMPACT & FORGET** —— 用改写做整合，**git 就是撤销键**；`deprecated` = **附录，不是碎纸机**。

### 最安静的一记妙招：git 作为治理机器

> **规范最安静的一记妙招是它没有建什么** —— 没有角色系统、没有 ACL、没有审批工作流，因为 git 托管本来就有，**还被两个十年的代码审查磨练过**。

| git 机制 | 治理职能 |
|---|---|
| `CODEOWNERS` | 域所有权（`/finance/` 目录让 finance 团队成为强制审阅人） |
| 分支保护 | 没过审阅，就上不了服务分支 —— **让信任层级变得有意义** |
| CI | frontmatter 校验、链接完整性、**蕴含核验** |
| releases | 一个**有版本号**的语料（"三月给出那个合规答案的 agent，服务它的是 bundle v3.2"是可审计的） |
| `revert` | **一条命令撤销投毒** —— 不是一次翻矢量索引的考古挖掘 |

> *"'Knowledge curation becomes a normal software-engineering activity' — **not a metaphor: a reuse claim**, and the reused asset is **the social technology of code review**."*

### 维护循环：机器巡逻，人类裁决

> 每晚：扫描过期的 concept、重新核查 sources、起草刷新用的 diff、**给依然成立的重新盖章（re-stamp what holds）**、为需要人判断的地方开 PR。
> Staleness 变成一个**队列**；队列变成一个**仪表盘**；仪表盘 —— **freshness debt** —— **像测试覆盖率一样按周画趋势**。
>
> *"Every step reads **standard fields**, so patrol tooling is **generic** — written once, pointed at any bundle. That is what 'agents change the economics' **cashes out to**."*

### 诚实地说说接缝（记忆映射哪里会断）

- **按时效加权的召回** —— OKF 给的是**阶跃函数**，不是**衰减曲线**。*"Timestamps travel; **half-lives do not**"* —— 这条曲线要消费者自己写。
- **双重时间性（bitemporality）** —— "Q1 为真、Q3 才学到"这种情况在规范里**没有第一等公民的位置**。*"Two clocks; **the spec ticks one**."*

> *"A student who can **diagnose a spec's memory model** has learned the real lesson."*

> **Quiz 6：** 四十个 agent，每个都有一份私有的 `MEMORY.md`；on-call agent 那个周二深夜熬出来的诊断，随会话一起死掉了。迁移到一个共享的、PR 把关的 bundle。
> **答：** 原始条目 = **情景记忆**（`log.md`）；折叠进 playbook = **程序记忆**（git 保存着**尚未压缩的过去**）。买到的红利是**共享记忆** —— **整支舰队继承了一个 agent 的那个周二**；代价是**每一道关卡都要收的那笔钱**：merge 时的审阅注意力，否则这个 bundle 会腐烂成一堆**穿着西装的 chunk**。

---

## Coda：The Case Against

一堂无法为自己主题给出反方论证的课还没想完。

### 最刺痛的一条：对人类作者的降级

> 那些**分析师** —— 他们习惯了用**丰富、零培训门槛**的工具来承载"知识作者"这个身份 —— "奇怪的文本格式加 git"，把他们的**写作体验**，换成了机器的**阅读体验**。
>
> 反驳意见（让 agent 来做中介，人在渲染视图里审阅）**恰恰承认了核心问题**。
>
> *"If mediation tooling does not materialize, **the knowledgeable will not write** — and the bundles become **a cage for machine summaries**."*

**这条风险的荒诞之处：** 一套本来是为了对抗 phantom concept（agent 幻觉出来的知识）而设计的治理格式，如果人类作者被写作门槛劝退，**最终反而会只剩下 agent 生成的内容** —— 它最想防范的失败模式，换了一个入口重新发生。

### 天花板，与幽灵

> **天花板** —— 空间性的、视觉性的、真正关系性的东西，会溢出这套格式；用散文写出来的、带类型的边，对**确定性消费者**来说是不可读的。
>
> **幽灵** —— RDF、OWL、Dublin Core：三十年前语义网那场既视感。
>
> *"But **the ratio inverted**: RDF asked **authors** to carry the burden of formalization, and authors refused. OKF asks **almost nothing of authors** — now it is the **consumers** that read prose. That is why this time may be different."*

**三十年前失败的不是这个目标本身，而是那一次实现选错了负担该压在谁身上。这一次，负担压对了地方。**

### 不小的小字条款（四笔未偿的账单）

1. **没有钉死的 markdown 方言** —— 脚注拼接在不同消费者那里可能解析得不一样。
2. **路径即身份** —— **改名会静默打断入站链接。**
3. **未经认证的行动者** —— **`generated.by` 只是一句断言；没有任何东西去核验它。**
4. **扁平的人类层级** —— **实习生和首席精算师，签名的效力一模一样。**

> *"Each **hardens an existing joint** rather than adding an **organ** — the mark of a minimal spec that drew its boundary in roughly the right place."*

### 冷静的预测

| 正方 | 反方 |
|---|---|
| 免费试用 | **作者门槛的缺口（authoring gap）** |
| 退出（defection）的代价被刻意设计得很低 | **没有公开发表过任何大规模落地的结算案例** |
| "卖铲子"式的配套工具按计划到位 | **单一供应商在托管这份规范** |
| **没有被明确提出的对手** | v0.1 → v0.2 只用了**八周** —— 这既是速度，**也是不稳定** |

> *"The pattern is likely inevitable under any banner. **Formats are ratified by their second vendor, not their first.**"*

这给出了一个可以在未来验证的判据：**如果看到别的团队、别的公司在没有被要求的情况下也开始采用这套模式，那才是真正落地的信号。**

### 收尾的图形：交叉结构（chiasmus）

> **文档** → OKF → **一个检索通道**：知识**从记录流向使用的那一刻**。
> **经验** → OKF → **记忆**：知识**从使用的那一刻流向记录**。
>
> *"RAG and memory are **two directions of one flow across one substrate** — reading the past, and writing it — **the same discipline, met from opposite banks**."*

一个具体的例子说明这个交叉交在哪：一份"如何排查某类故障"的知识，可以从两个相反方向进入**同一个** bundle —— **文档方向**：工程师把排障手册写成文档，审阅后变成一个 concept 供未来检索（知识从记录流向使用）；**记忆方向**：一个 agent 真的处理了一次这样的故障，这次经验被折叠、审阅、写回同一个格式（知识从使用流向记录）。两条路径起点不同、方向相反，**用的却是完全同一套机制**。

### 承诺已兑现

**THE WHAT：** 一个被治理的语料 —— 小的、带类型的、互相链接的 markdown concept；**唯一必填字段**；信任放在 frontmatter 里；**层级在读取时推导**；数字要有认证背书；一切都在 git 里，背后是一道**人类关卡**。

> *"Knowledge with **papers to carry**: **typed, sourced, dated, and signed**."*
> （这四个词分别对应 Act I 的 `type`、Act II 的 `sources`/`verified.by`、`stale_after`/时间戳、Act III 的 review gate 签字 —— 是这门课名字的最终解释。）

**THE HOW：** 只对被治理的核心爬梯子 · 审阅的是**忠实度**不是形式 · **数字不配文字** · **机器巡逻，人类裁决** · 也要**衡量这个知识库本身**：**覆盖率、新鲜度欠账（freshness debt）、层级构成比例（tier mix）**。

> *"A gate concentrates vigilance, but it never replaces it. **Budget the attention, or the phantom collects.**"*

---

## 下半场：Module 5 · Secure Retrieval（企业权限 RAG）

> *"Building a secure retriever is **engineering**; **proving it stays secure** is the **discipline**."*

方法论骨架：**define the problem → do the mathematics → build it → then prove it**。本次只讲到 Section 1–2。

### 1.1 传统 RAG 的隐藏假设

```
d* = arg max sim(q, d)   over all d in D
```

> *"This formulation assumes **every document in D is available to the user**."*

这条大家早就在用的公式里藏着一个从没被显式写出来过的假设：**相似度函数 `sim(q, d)` 完全不关心 `d` 是谁能看 —— 它的定义域里根本没有"谁在问"这个变量。**

### 1.2 相关 ≠ 被授权

> 一位员工问："公司对 **Project Phoenix** 项目有什么计划？" —— 最佳语义匹配结果，可能是一份**高管级收购文档**。
>
> *"**The retriever did its job perfectly. That is precisely the problem.** A retriever that performs perfectly on a mixed corpus is **an efficient leak**."*

**检索器越强、语义理解越准，在一个没有权限约束的混合语料库上就泄漏得越精准、越高效。**

> 这其实是"相似度几何缺一个轴"这个母题的**第四次出现**：Act III 说它缺 **authority / currency / correction** 三个轴，这里补上第四个 —— **authorization**。四个轴的病理是同一种：相似度只回答"这段内容和问题像不像"，从不回答"该不该被眼前这个人看到、该不该被信、是不是还作数"。

### 1.3 修正后的公式

```
D_u = { d ∈ D : Authorized(u, d) = 1 }     # user u 的已授权子语料库
d*  = arg max sim(q, d)   over d ∈ D_u      # 检索被限制在这个子语料库内
```

> *"**One subscript changes everything.** D became D_u — and **D_u is not a static property of the corpus**; it is recomputed **per user, per request, from live entitlements**."*

注意形式上的修改有多小：参数从 `q` 变成 `(q, u)`，加一个 `subject to`。但 **`D` 本身的定义域变了** —— 未授权文档根本不会进入被排序的候选集，这和"在排序分数里加一个权限项"是两种完全不同层级的修复。

> *"Note what the constraint is **not**: it is **not a term added to the ranking score**, and it is **not an instruction in the system prompt**."*
>
> 如果只是一个加权项，一份高度相关但未授权的文档理论上可以靠"相关性够高"把授权劣势抵消回来；如果只是一句系统提示，它就活在自然语言层面，可以被 prompt injection 绕过或谈判掉。

### 1.4 安全原则：Prevention vs Suppression

| | **PREVENTION（预防）** | **SUPPRESSION（压制）** |
|---|---|---|
| 做法 | 未授权片段**永远不会进入上下文窗口** | 机密片段进了上下文，**要求模型拒绝回答** |
| 性质 | **确定性的基础设施** | 这个秘密现在身处一个**随机系统**内部 |
| 风险 | 没有什么可以泄漏、需要压制、需要信任模型去做 | **只差一次 prompt injection** |
| 一句话 | 一个**控制（control）** | 只是一个**请求（request）** |

> *"A refusal generated **after** the LLM has already received confidential information is **not equivalent to preventing exposure**."*

即便这一次模型确实成功拒绝了，Suppression 模式依然是失败的 —— **暴露发生在更早的一步**：机密内容已经离开了它该被物理隔离的边界，进入了一个不受确定性规则支配的处理环节。

（**这和 Act II 的认证原则是完全同一个设计模式**：把一个必须无条件成立、不容协商的约束，从"说给模型听、指望它遵守"的层面，挪到"模型根本没有机会违反"的层面。）

### 1.5 六个泄漏面

> **检索只是机密信息可能泄漏的六个地方里的第一个。**

1. **未授权检索** —— 片段进入候选集
2. **未授权 LLM 上下文** —— 片段跨进了 prompt
3. **生成答案泄漏** —— 事实出现在回答里
4. ⚠️ **引用/元数据泄漏** —— 标题、文件名或 URL 被暴露
5. ⚠️ **缓存泄漏** —— 一个用户的特权答案被提供给了另一个用户
6. ⚠️ **日志/追踪/可观测性泄漏** —— 秘密落进了你的 SIEM

> **被高亮的这三个，正是团队最常整个忘掉的。**

三条高亮项的讽刺之处：

- **第 4 条** —— 为了增强可信度和可追溯性而做的**引用溯源**机制（正是 grounding 的好实践），如果本身不做权限检查，一个 `Project-Phoenix-Board-Deck.pptx` 这样的**文件名**就已经泄漏了"存在这样一份文档"。
- **第 5 条** —— 语义缓存如果缓存键不绑定授权身份，一个有权限用户的答案会被直接喂给另一个只是问了语义相近问题的无权限用户。**这是一条绕开所有 Prevention 机制的旁路。**
- **第 6 条** —— 为了"证明系统安全、方便审计"而建的**可观测性系统**，如果不加权限控制地记录完整 prompt/上下文，反而成了机密信息的又一个副本。**可审计性和数据最小化在这里正面冲突。**

### 最微妙的泄漏面：一次拒绝，可能比一个答案泄漏得更多

> *"我找到了 `Acquisition-of-Company-X.pdf`，但你没有权限访问它。"*
>
> **非常礼貌。拒绝得也完全正确。而它刚刚告诉了一个普通员工：公司正在收购 Company X。**

**两种不同的拒绝：**

- **content denial（内容拒绝）** —— "你不能看这份文档**里面的内容**"
- **resource-discovery denial（资源发现拒绝）** —— "你甚至**不能知道这份文档存在**"

> *"Your tests must distinguish the two. A system that denies content while **confirming the document exists** is still leaking."*

这其实是传统安全工程里很成熟的模式被原样迁移过来：登录表单"密码错误"和"用户不存在"必须给出同一句提示（否则构成用户名枚举）；HTTP 用 404 而不是 403 来隐藏一个未授权用户不该知道其存在的资源。

> ⚠️ **注意这里和上半场 OKF 的价值观正面冲突：** OKF 反复讲"容忍红链是一种美德"、"absence means, never excludes" —— 鼓励对语料的存在状态保持透明。而这一页对最高敏感级别的内容要求的恰恰相反：**连"存在"这件事本身都不能承认。** 两套哲学服务不同目标：OKF 优化**认知透明度**，这里优化**信息遏制**。**密级越高的内容，需要的恰恰是相反方向的设计。**

### 2.1 三个必须分开的关注点

| | 回答的问题 | 组件 |
|---|---|---|
| **Authentication 认证** | **你是谁？** | 身份提供方 · token · session · 租户上下文 |
| **Authorization 授权** | **你被允许访问什么？** | ACL · 角色 · 属性 · 关系 · 策略引擎 |
| **Retrieval 检索** | **在被授权的信息里，哪些最相关？** | embedding · 词法 · 混合 · 重排序 |

> *"They can be implemented in one platform. But they must still be **reasoned about — and audited — as three layers**."*

三者是一条**严格的依赖链**，正好对应 1.3 的公式：认证解出 `u`；授权算出 `Authorized(u,d)`；检索在缩小后的 `D_u` 里做 `arg max sim`。

**为什么必须分层：** 如果三者被融合成一次不透明的判断（比如全部交给一个 LLM 一次性决定"这个人能不能看这个答案"），出问题时根本**无法定位**是认证搞错了身份、授权判错了策略、还是检索召回了不该召回的。

### 2.2 四种权限模型

| 模型 | 核心理念 | 适用场景 | 要小心的坑 |
|---|---|---|---|
| **ACL** | **资源自己说明谁能看** | 源系统的事实来源；逐文档的例外 | 清单规模、**漂移** |
| **RBAC** | **职位暗示了权限范围** | 粗粒度门禁；入职-转岗-离职的卫生维护 | **角色爆炸** |
| **ABAC** | **属性现算出权限** | 密级、数据驻留、租户、设备安全态势 | **元数据质量** |
| **ReBAC** | **一条路径就能授予权限** | 项目、文件夹、层级、委托 | **图遍历代价** |

**ACL** —— `{"document_id": "DOC-731", "allow_users": ["u123"], "allow_groups": ["finance", "executives"]}`。
> **这正是 SharePoint、Google Drive、Confluence 实际存储权限的方式**，所以摄取在这里是一次**复制**，而不是一次**翻译**。不管你下游更偏好哪种模型，**摄取层最先碰到的永远是它。**

**RBAC** —— 权限是**职位**的属性，不是人的属性。优点：入职/转岗/离职这些正常流程的**副作用**就能顺带更新权限。缺点：`Engineer` 区分不出"在 Project Falcon 项目上的工程师"，于是出现 `Engineer-Falcon-EMEA-Contractor` 这类**组合角色爆炸**（随维度数量近似指数级增长）。
> *"The interesting boundaries are **project, region and classification**, not job title."*

**ABAC** —— 权限从用户和文档双方的属性**现算**出来：
```
user.department == document.department
  AND user.region IN document.allowed_regions
  AND user.clearance >= document.classification
```
优点：**改一个属性就能一次性改变所有相关的访问权限**。缺点：完全取决于元数据质量 —— 如果 `document.classification` 没设置或设错，**ABAC 会静默失败，而且除非专门设计成"默认拒绝"，否则默认会是"失败开放（fail open）"**。

**ReBAC** —— 权限是**图上的一条路径**：`Alice --member_of--> Engineering --works_on--> Project Falcon --contains--> roadmap.pdf`。
> Alice 能读它，**不是因为某份清单点了她的名字，也不是因为她的职位头衔，而是因为存在一条从她到这份文档的路径。**
> 缺点：查询时做图遍历是一个**分布式系统问题**（专用引擎：OpenFGA、SpiceDB，都受 Google Zanzibar 论文启发）。
> *"Reach for ReBAC when your authorization question keeps turning into **'who is connected to what'**."*

> **四种模型不是竞争对手 —— 生产系统会把它们叠在一起用。** 典型栈：**RBAC 做粗粒度门禁，ABAC 处理密级和数据驻留，ReBAC 或源系统 ACL 处理具体细节 —— 最后统一归一化成一个描述符。**

### 2.3 归一化安全描述符

> **源系统对权限的表达方式各不相同。你的摄取层必须让它们达成一致。**

```json
{
  "document_id":    "DOC-731",
  "tenant":         "acme",
  "classification": "confidential",
  "allow_users":    ["u123"],
  "allow_groups":   ["finance", "executives"],
  "deny_users":     [],
  "regions":        ["US"],
  "projects":       ["phoenix"]
}
```

**"一种形状，适配所有来源。"** SharePoint、Drive、Confluence、Git、ServiceNow 各自用不同方言表达权限 —— **索引不可能同时按五种方言做过滤。**

逐字段来源：`allow_*` 来自 ACL · `classification`/`regions` 来自 ABAC · **`projects` 是把 ReBAC 的关系边压平（flattened）后的结果**（不是查询时现场做图遍历，而是提前算好摊平成静态字段，用刷新延迟换查询速度）· `tenant` 是硬隔离边界 · `deny` 是显式否定项。

**三条设计规则：**

1. **缺失字段一律按拒绝处理，绝不默认允许**（直接修补 ABAC 的 fail-open 隐患）
2. **拒绝优先于允许**（一个人可能因属于 `finance` 被放行，同时因利益冲突审查被单独列进 `deny_users`）
3. **这份描述符要带版本号，以便日后能重放某次判定的过程**

> 第 3 条和上半场 OKF 的"写入与核实要独立标注时间戳"（`changed since review`）是**同一条设计原则**：任何被治理的状态都不能只保留"当前值"，必须留下**带版本的历史快照** —— 万一日后发现泄漏，唯一能回答"当时的授权判断到底是怎样的"的方式，就是把描述符倒回到那次查询发生时的版本。

### 2.4 切片时的权限传播

> **内容能毫不费力地在切片过程中存活下来。权限做不到 —— 除非你专门让它做到。**

切片算法天然操作的是**文本流**，内容是它的直接产物；但权限挂在**文档对象**上，不是文本的一部分，切片逻辑对它一无所知。

> *"A common implementation error is **preserving document content while losing or incorrectly transforming source permissions**."*

**一条可以直接写成单元测试的红队检验标准：**

> *"If a chunk is retrieved **on its own**, can the system still say **who is allowed to see it**?"*

（单独从向量库里拽出任意一个 chunk，不做任何回查父文档的操作，看它自己携带的元数据是否足够回答授权问题。**元数据必须自带在对象身上，不能靠外部指针间接引用** —— 这和 OKF"出处/信任信息写在自己的 frontmatter 里，而不是另存一份索引"是同一条架构直觉的第二次独立出现。）

### 2.5 两条必须保持同步的流水线

| | 流水线 | 评语 |
|---|---|---|
| **CONTENT** | `documents → parse → chunk → embed → index` | **广为人知。每个 RAG 团队都搭过一条。** |
| **ENTITLEMENT** | `ACLs / groups / relationships → normalize → synchronize → policy state` | **很少被同等用心地搭建过。而它变化的频率比内容高得多。** |

> **这两条流水线之间的一致性，就是安全属性本身。**
>
> 一份 **10:01** 建好索引的文档，如果它的权限在 **10:05** 发生了变化，那么 **10:06** 的一次查询，**就是一次正在等待发生的泄漏。**

**一个值得警觉的注意力错配：** 文档一旦写完，内容大部分时间是**静止**的；而权限在**持续变动**（入职、离职、转岗、重新定级）。**恰恰是那条变化最快、最需要认真对待同步问题的流水线，实际投入的工程精力最少。**

这也解释了为什么权限撤销必须靠**事件驱动失效**立刻生效，而不能靠 TTL 慢慢过期。

---

## 一条贯穿全天的暗线

"**任何被治理的状态，都必须能回答'这是什么时候的快照'，而不是被当作一个永远最新的既定事实**"这条架构直觉，今天在三个完全不同的场景里**独立出现了三次**：

1. OKF 的 `generated` vs `verified` 时间戳（`changed since review` 机制）
2. `D_u` 必须逐请求现算，不能是语料的静态属性
3. 内容索引时间戳 vs 权限变更时间戳（10:01 / 10:05 / 10:06）

**三处场景（知识信任、检索范围、访问授权）完全不同，却反复独立推导出同一条原则。**

---

## 可以直接拿走的几条

1. **拒绝把语料当既定输入。** 检索单元可以是被策展的知识对象，而不是任意 token 窗口 —— 理解在**创作时**付一次账，而不是每次查询重赌一把。
2. **一个 chunk 答不出四个问题** —— 谁说的、还是不是真的、有人核实过吗、这个数字从哪来。这是**每一个企业级答案都必须扛住的**。
3. **信号，绝不是分数。** 发布可独立核实的原始读数（`author`/`usage_count`/`last_modified`），信任在**读取时**由每个消费者自己推断。**结论里嵌了判断，而判断不会旅行。**
4. **信任层级要推导，不要声明** —— 没有可伪造或腐烂的层级字段；`generated` 晚于 `verified` 就机械降级。
5. **数字走认证计算。** 模型只能为声明过、有类型的参数供值，**绝不能撰写或编辑计算本身**。"受批准的东西是否真的跑了"降级成一次**字符串比较**。
6. **梯子是一条限定范围的规则** —— 只为术语表、指标、政策、runbook 这几千个 concept 攀爬；长尾留给相似度检索。货币是**持续的人类注意力**，而**一个未经审阅的 bundle 只是一堆穿着西装的 chunk**。
7. **phantom concept 比坏 chunk 更危险** —— 它戴着审阅门自己的印章到达。四道防线一个都不能少，其中唯一不依赖语言判断的是：**phantom 伪造不出一张回执**。
8. **git 已经是一台治理机器** —— CODEOWNERS、分支保护、CI、releases、`revert`。不要再造角色系统和审批工作流。
9. **授权是检索前的硬约束，不是排序分数里的一项，也不是 system prompt 里的一句话。** 已经进入上下文的机密，即使这次没被说出来，也已经构成暴露。
10. **泄漏面有六个，不是三个。** 引用元数据、语义缓存、可观测性日志是最常被整个忘掉的三个。**连"拒绝"本身都可能泄漏。**
11. **两条流水线的一致性就是安全属性本身** —— 权限变化比内容快得多，却通常投入最少。

---

## 一句话定位

Week 07 学会了量检索，Week 08 学会了量生成器，**本周学到知识本身也可以被做成可评判的 —— 有类型、有出处、有日期、有签字。**

核心是一次倒转：把智能从查询时搬到创作时。信任分三层且**从证据推导而非声明**；数字的信任来自**认证计算**而非语言模型的复述；最危险的失败不是裸奔的幻觉 chunk，而是**戴着审阅印章通过的 phantom concept**；同一个基底、两个方向的流动 —— 文档变成检索通道，经验变成记忆 —— **是同一门手艺从两岸相遇**。

而下半场补上了相似度几何缺的第四个轴：**相关 ≠ 被授权**，一个在混合语料上表现完美的检索器，就是**一条高效的泄漏通道**。

---

## 附：OKF vs 我司 Forge（Standards Library）—— 课后自做的比对

> 以下不是课堂内容，是对照 Google Cloud 官方公告博客和 `rr-standards/plugins/forge` 自己读出来的，**建议找团队里熟悉 Forge 设计初衷的人再核实一遍。**

**一句话结论：OKF 是一份格式规范，Forge 是一套软件工程流程框架。** 两者名字都在做"给知识建结构"这件事，但服务的不是同一个问题。

| 维度 | OKF | Forge |
|---|---|---|
| **范围** | 不预设领域，任何知识都能装 | 五种写死的工件类型，服务"工程师在写代码"这一个场景 |
| **Typing** | `type` 是 frontmatter 唯一必填字段，几乎完全由作者决定 | 类型由**文件名和路径模式机械推导**；每种类型有硬性行数上限和必需章节 |
| **治理** | 推导式信任层级 + 认证计算 | `.policy.md` 的 severity 表（blocking/advisory/informational）+ 黄金测试样例 |
| **版本化** | 博客未谈 concept 级版本号 | 每个 standard/policy/guide 挂 **semver**，`Implements: standard@version` 显式声明耦合 |
| **导航** | `index.md` 渐进式披露 —— **pull 模型** | AGENTS.md 强制 + `CLAUDE.md` 注入 + pre-tool-use hook —— **push 模型** |
| **组织轴** | 围绕 **concept**（任意知识实体）—— 贴语义记忆 | 围绕 **SDLC**（effort / deployable / product）—— 更接近程序性/情景性记忆 |

**哲学上是反过来的：OKF 让消费者（agent）多啃散文，换作者的自由；Forge 让作者多守结构，换机器可校验性。**

**一个值得注意的点：** Forge 的 `COVERAGE.md`（complete/draft/stub/absent/major-stale 五态的语料覆盖度仪表盘）**基本就是课上讲的 freshness debt 仪表盘的一个真实存在的实现** —— 只不过它监控的是"工程标准文档"而不是通用知识 bundle。

**Forge 相对 OKF 具体缺什么：**

1. **没有机器可读的 frontmatter** —— 类型靠路径规则推导，标准库没法被 Forge 生态之外的 consumer 直接消费。
2. **没有内容忠实度这一层信任** —— severity 表核查的是"代码合不合规"，不是"这条标准文本本身有没有被谁核实过"。标准文档自己反而没有 sources/verified 这类出处字段。
3. **没有认证计算** —— 标准里写的具体数字或阈值，没有机制独立核验它现在还对不对。
4. **是平台耦合，不是可移植格式** —— 依赖 Claude Code 的 hook、`CLAUDE.md` 注入、本地插件缓存路径查找；OKF 刻意设计成 producer/consumer 相互独立。
5. **没有 concept 粒度的变更史** —— `log.md` 那种"这个知识单元自己的历史"在 Forge 里没有对应物，只有 effort 级别的 `.state.json`。

**最直接的一个改造点：** 给 `standards/` 里每个文件补一层 YAML frontmatter（`type`、`sources`、`verified`），把 TAXONOMY.md 的路径推导规则改写成 frontmatter 声明式。这样标准库理论上就能**同时**被"人类 / Claude Code hook"和"任何遵守 OKF 的通用 consumer"两套系统消费 —— 正好呼应 OKF 反复强调的 **producer/consumer independence** 这条设计原则。

**补记：官方参考实现 `GoogleCloudPlatform/knowledge-catalog`** —— OKF 有一个真实开源、有人维护的参考实现，提供两个 CLI：`enrich`（从 BigQuery 等元数据源**自动生成** OKF bundle）和 `visualize`（把 bundle 转成交互式关系图 HTML），自带三份可浏览的样例 bundle。
> 值得多想一层：**全天课堂讲的 OKF 都假设是人在写 markdown concept，但官方参考实现的第一个用例却是 agent 自动生成** —— 这和"agents change the economics"是同一件事的另一个印证：**curation 的边际成本被 agent 拉低之后，"谁来写 concept"这个问题的默认答案，可能已经悄悄从"人"变成了"agent 生成、人审阅"。**

---

## 必读与选读

**必读（刻意精简的追赶周）：**

- **The OKF Specification, v0.2** —— 规范本身，从头到尾，约一千行 markdown。重点看 conformance 条款和信任家族。**精读一份年轻标准的能力本身就是本周要教的专业技能。**
- **McVeety & Hormati, *How the Open Knowledge Format can improve data sharing*** —— 官方公告博客；读它取框架（供应商自己坦率承认的碎片化上下文问题）和它点名的 LLM-wiki 谱系。
- **Edge et al., *From Local to Global: A Graph RAG Approach*** (arXiv:2404.16130) —— 与本周对照：社区摘要是一个**被诱导出（induced）**的图工件；OKF bundle 是一个**被撰写并审阅（authored）**的工件。**知道该在什么时候用哪种工具，是手艺的标志。**
- **Sumers et al., *Cognitive Architectures for Language Agents*（CoALA）** (arXiv:2309.02427) —— 四层记忆分类法最干净的表述。

**选读：** `llms.txt` 提案（2024）· Packer et al., *MemGPT* (arXiv:2310.08560) —— 渐进式披露背后的 RAM-与-磁盘类比 · SLSA 框架文档 —— 让"远程认证移植到 SQL 上"这句话变具体 · OKF 公告后的评论串（2026 年 6–7 月）—— practice 在自己的话里陈述最强反方论证。
