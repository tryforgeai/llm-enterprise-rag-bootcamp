# Week 09 Slack draft (for review — not sent)

---

## Option A — English

**Week 09: When knowledge gets its papers — OKF and the governed corpus** 📇

One line: **the corpus was never a given — it has always been a choice.**

Weeks 07 and 08 measured retrieval and the generator. This week steps back and asks what the thing being retrieved is actually *made of*. The close reading is Google's young spec, the **Open Knowledge Format** — which, read strictly, is **not even software**: markdown files with YAML frontmatter, versioned in git, readable with `cat`. *"So slight an artifact, so loud a conversation: it touched an exposed nerve."*

**Three things worth your time:**

• **The inversion — move the intelligence from query time to authoring time.** Classical RAG bets meaning can be re-derived at query time: chunk, embed, gamble that cosine similarity reassembles the author's understanding on the fly. The economics are brutal when you write them down: *"the stack is cheap to produce and expensive to read — **a hundred times, by a hundred readers**. The card is expensive **once**."* And understanding at query time happens **without appeal** — nobody is present to check whether this particular similarity computation was reasonable.

• **Four questions a chunk cannot answer** — who says so? is it still true? has anyone checked? where did this number come from? The chunk answers: *uncredited; unknowable; silence; wherever the embedding landed.* The concept answers each with a field. Two design choices stand out: **signals, never scores** (no `credibility: 0.87` — *"the verdict embeds a judge, and judges do not travel"*), and **attested computation** for numbers — the model may fill typed parameter holes but **may never author or edit the computation**; deterministic code re-derives the expected binding and compares it to the receipt of what actually ran. *"The one link in the chain from which the LLM is banished by design."*

• **The phantom concept — worse than a bad chunk.** An agent mints a definition with clean frontmatter, three real sources, every footnote joined — and the definition is a plausible reconciliation of three superseded drafts, *a sentence no version of the policy ever contained*. A hallucinated chunk arrives **naked** and attracts suspicion; **the phantom arrives wearing the review gate's own seal**, and governance is *why* it will be believed. The moral is the week's sharpest: **a gate concentrates vigilance — it does not replace it.**

**The afternoon (Module 5 · Secure Retrieval)** added the axis similarity geometry is missing: **relevance does not imply authorization.** An employee asks about Project Phoenix; the best semantic match is the executive acquisition deck. *"The retriever did its job perfectly. That is precisely the problem."* Authorization must be a hard constraint **before** retrieval — not a term in the ranking score, not a line in the system prompt. Also: there are **six** leakage surfaces, not three — citation metadata, semantic cache and observability logs are the three teams forget entirely, and **even a refusal can leak** ("I found `Acquisition-of-Company-X.pdf` but you lack permission" just told an employee about the acquisition).

**Also worth knowing:** the ladder is a **scoping rule** — climb only for glossaries, metrics, policies and runbooks, where authority failure is fatal and an owner holds the pen; leave ten million emails to similarity. The currency is **sustained human attention**, and *"an unreviewed bundle is just **chunks wearing a suit**"* · git is already a governance machine (CODEOWNERS, branch protection, CI, releases, `revert`) — the spec's quietest masterstroke is **what it did not build** · the same substrate turned 90° becomes agent memory, and the four-tier cognitive map lands exactly: concept = semantic, `log.md` = episodic, playbook = procedural, index-walk = working.

Full bilingual write-up in the repo: `course/week_09/week-09-summary.md` / `week-09-summary-for-team.zh.md` (includes a post-class OKF-vs-Forge comparison)

---

## Option B — 中文

**Week 09：当知识拿到了自己的证件 —— OKF 与被治理的语料** 📇

一句话：**语料从来不是一个既定之物，它一直是一个选择。**

Week 07/08 量了检索和生成器，这周退后一步问：**被检索的东西，到底是用什么材料造的？** 精读的是 Google 那份年轻的规范 **Open Knowledge Format** —— 严格说它**甚至不是软件**：带 YAML frontmatter 的 markdown，用 git 做版本管理，`cat` 就能读。*"So slight an artifact, so loud a conversation: it touched an exposed nerve."*

**三件值得花时间的事：**

• **核心倒转 —— 把智能从查询时搬到创作时。** 经典 RAG 赌的是意义能在查询时被重新推导：切块、嵌入、赌 cosine 相似度能临场重组作者当年的理解。把账写下来就很残酷：*"碎片生产便宜、阅读昂贵 —— **一百个读者读一百次**。卡片只贵一次。"* 而且查询时的理解是**无处申诉（without appeal）**的 —— 没有人在场核对这次相似度计算是否合理。

• **一个 chunk 答不出的四个问题** —— 谁说的？还是不是真的？有人核实过吗？这个数字从哪来？chunk 的答案是：**无出处、不可知、沉默、embedding 落到哪就是哪**。两个设计决定特别值得拿走：**信号，绝不是分数**（没有 `credibility: 0.87` —— *"结论里嵌了一个判官，而判官不会旅行"*）；以及数字走**认证计算** —— 模型只能为声明过、有类型的参数供值，**绝不能撰写或编辑计算本身**，确定性代码重新推导预期绑定、与"实际跑了什么"的回执比对。*"这是整条链上唯一一处，LLM 被设计性地驱逐在外。"*

• **phantom concept —— 比坏 chunk 更危险。** 一个 agent 铸造出一份定义：frontmatter 干净、三条真实的 sources、逐条脚注都连着 —— 而这个定义是对三份**已被取代**的草稿一次似是而非的调和，**一句没有任何一个版本的政策真正包含过的句子**。幻觉出来的 chunk 是**裸奔着**到达的，会被环境性地怀疑；**phantom 戴着审阅门自己的印章到达**，而这套治理流程**正是它会被相信的原因**。本周最锋利的一句道德：**关卡是集中警惕的地方，不是替代警惕的地方。**

**下半场（Module 5 · 安全检索）** 补上了相似度几何缺的那个轴：**相关 ≠ 被授权。** 一个员工问 Project Phoenix，最佳语义匹配可能是一份高管级收购文档。*"检索器完美地完成了它的工作 —— 而这恰恰就是问题所在。"* 授权必须是检索**之前**的硬约束 —— 不是排序分数里的一项，也不是 system prompt 里的一句话。另外：泄漏面有**六个**不是三个 —— 引用元数据、语义缓存、可观测性日志是团队最常整个忘掉的三个，而且**连"拒绝"本身都可能泄漏**（"我找到了 `Acquisition-of-Company-X.pdf`，但你没有权限" —— 这句话刚刚告诉了一个普通员工公司正在收购谁）。

**顺带值得知道：** 梯子是一条**限定范围的规则** —— 只为术语表、指标、政策、runbook 攀爬（权威失败会致命、且有人握着笔的地方），一千万封邮件留给相似度。货币是**持续的人类注意力**，而*"一个未经审阅的 bundle，只是一堆**穿着西装的 chunk**"* · git 已经是一台治理机器（CODEOWNERS、分支保护、CI、releases、`revert`）—— 规范最安静的一记妙招是**它没有建什么** · 同一个基底转九十度就是 agent 记忆，四层认知地图精确落位：concept = 语义，`log.md` = 情景，playbook = 程序，索引遍历 = 工作记忆。

完整中英文总结在仓库：`course/week_09/week-09-summary.md` / `week-09-summary-for-team.zh.md`（含课后做的 OKF vs Forge 比对）

---

## Option C — Ultra-short (if the channel is busy)

**Week 09 · OKF and the governed corpus** — weeks 07/08 measured the answers; this week asks what the retrieved thing is *made of*. **Refuse the given**: manufacture the corpus into a shape worth retrieving from.

**Worth knowing:** the inversion — understanding paid **once at authoring time**, not re-gambled on every query, **without appeal** · **four questions a chunk cannot answer** (who says so / still true / anyone checked / where did this number come from — the chunk answers *uncredited, unknowable, silence, wherever the embedding landed*) · **signals, never scores** — *"the verdict embeds a judge, and judges do not travel"* · numbers go through **attested computation** — the model fills typed holes and **never** writes the computation; *"a phantom cannot forge a receipt"* · the **phantom concept** beats a bad chunk because it **arrives wearing the review gate's own seal** — *a gate concentrates vigilance, it does not replace it* · the ladder is a **scoping rule** (glossaries/metrics/policies only; *an unreviewed bundle is just chunks wearing a suit*) · afternoon: **relevance ≠ authorization**, authorization is a hard constraint **before** retrieval, and **six** leakage surfaces — **even a refusal leaks**.

Full notes (EN/中文): `course/week_09/week-09-summary.md`
