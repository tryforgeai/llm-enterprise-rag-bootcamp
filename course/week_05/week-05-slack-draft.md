# Week 05 Slack draft (for review — not sent)

---

## Option A — English

**Week 05: GraphRAG — when the library becomes a city** 📍

One line: **the structure is real, the harvest is expensive, and the art is knowing which queries deserve it.**

Extract entities + relationships from a corpus and the documents dissolve into a network — which then has hubs, communities, and small-world structure that *no single passage contains*. Every GraphRAG variant harvests that emergent structure. Every variant pays for it.

**Three things worth your time:**

• **GraphRAG only pays rent on one query type** — global sensemaking ("what are the main regulatory themes across these 500 earnings calls?"). Point queries, small corpora, and real-time lanes are anti-patterns. Routing a point query through community summaries is using a telescope to read your wristwatch.

• **The invoice is real.** One public-domain book through Microsoft GraphRAG ≈ **$1,000**. Every successor system (Lazy, Light, Hippo, MemGraph) is an answer to that bill. MemGraphRAG's alternative — personalized PageRank over a 3-layer graph — retrieves in **0.061s** with zero LLM calls at query time.

• **"Preserve, then decide."** The week's best idea, and it generalizes well past GraphRAG. MemGraphRAG drops schemas below a frequency threshold — but on technical corpora the rare cross-domain gem and the copyright notice have the *same* frequency. You can't retrieve what was never admitted to the graph. **Demote, don't delete.**

**Our position:** deferring GraphRAG, on purpose. Our corpus is a bathtub (187 records) and our failing eval is a point query. What we *are* taking: the **local-vs-global router** (useful with zero graph work) and **hub suppression** for the EV-001 retrieval failure.

Full bilingual write-up in the repo: `course/week_05/week-05-summary-for-team.md` / `.zh.md`

---

## Option B — 中文

**Week 05：GraphRAG —— 当图书馆变成城市** 📍

一句话：**结构是真的，收割是贵的，工程的艺术在于判断哪些 query 值这笔账单。**

把语料里的实体和关系抽出来，文档就溶解成一张网 —— 于是有了 hub、社区、小世界结构，而这些**不存在于任何单个 passage 里**。每种 GraphRAG 都在收割这个涌现结构，也都要为它付钱。

**三件值得花时间的事：**

• **GraphRAG 只在一类 query 上交得起房租** —— 全局意义建构（「这 500 场财报会里主要的监管主题是什么？」）。点查询、小语料、实时通道都是 anti-pattern。把点查询路由进社区总结，等于用望远镜看手表。

• **账单是真的。** 一本公共领域的书跑一遍 Microsoft GraphRAG ≈ **$1,000**。后来的每个系统（Lazy / Light / Hippo / MemGraph）都是对这张账单的回答。MemGraphRAG 的替代方案 —— 三层图上的 personalized PageRank —— **0.061 秒**完成检索，query 时零 LLM 调用。

• **「先保存，再决定」。** 这周最好的想法，适用范围远超 GraphRAG。MemGraphRAG 会丢掉低于频率阈值的 schema —— 但在技术语料上，罕见的跨域宝石和版权声明**频率一样**。你无法检索一个从未被允许进图的东西。**降级，别删除。**

**我们的立场：** 有意推迟 GraphRAG。我们的语料是个浴缸（187 条记录），失败的那个 eval 是点查询。我们要拿走的是：**局部/全局路由器**（零图工作就有用）和 **hub suppression**（针对 EV-001 的检索失败）。

完整中英文总结在仓库：`course/week_05/week-05-summary-for-team.md` / `.zh.md`

---

## Option C — Ultra-short (if the channel is busy)

**Week 05 · GraphRAG** — corpus → network; hubs and communities emerge that no passage contains.

**Worth knowing:** it pays rent *only* on global sensemaking queries · one book through MS GraphRAG ≈ **$1,000** · MemGraphRAG does it in **0.061s** with PPR and no query-time LLM calls · best idea of the week = **"preserve, then decide"** (demote sub-threshold facts, don't delete — you can't retrieve what never entered the graph).

**Us:** deferring GraphRAG on purpose (our corpus is a bathtub). Taking the **local-vs-global router** and **hub suppression** for EV-001.

Full notes (EN/中文): `course/week_05/week-05-summary-for-team.md`
