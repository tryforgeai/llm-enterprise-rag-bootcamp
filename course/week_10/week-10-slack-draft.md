# Week 10 Slack draft (for review — not sent)

---

## Option A — English

**Week 10: The Library of Many Catalogues — retrieval architecture, end to end** 🗂️

One line: **a retrieval system is not a search over documents. It is a portfolio of representations and a court of adjudication.**

This is the week the load-bearing wall gets its engineering — eleven in the morning to half past eight at night, the whole retrieval side of the house. It starts in Brussels in 1895, with a lawyer who catalogued the world by hand and built, a century early, exactly the architecture we are now mechanizing.

**Three things worth your time:**

• **The recall ceiling — write it on the inside of your eyelids.** A child loses her marbles in a sandbox and recovers them with a bucket and a sieve: scoop wide, tolerate sand, the sieve cleans up later. **But if the scoop misses a marble, no sieve can recover it.** Whatever recall you have at stage one is a ceiling **nothing downstream can raise** — not a reranker, not a better prompt, not a bigger model. Hence: **tune the scoop for recall, the sieve for precision.** Paired with it, the tomographic principle: a CT scanner never photographs the tumor, it takes hundreds of individually blind projections and reconstructs. **Fusion is the reconstruction; a single index claims total sight, and the portfolio refuses that claim.**

• **The user is the examiner — so manufacture documents that match your queries.** The corpus was written with no examiner in mind (textbooks for pedagogy, contracts for opposing counsel); the register mismatch is permanent. The orthodox fix transforms the query; the deeper move runs the other way — take the corpus offline and recast every chunk into shapes a question can seize. One rule governs all of it: **retrieve the derivative, generate from the source.** And the number worth memorising — **the Berlin experiment**: the paragraph *containing the answer* scores **0.64** against the query; the extracted factoid scores **0.81–0.90**. At a production threshold of 0.7–0.8, **the paragraph holding the answer is silently dropped.**

• **The court: fuse in ranks, and the decoy's job ends at retrieval.** A BM25 score and a cosine share no scale, so fusion happens over ranks — **RRF at k=60**, a one-page SIGIR paper from 2009 that is still the default in essentially every engine, and the constitution until your hold-out set says otherwise. Then the doctrine that trips more teams than any other: when the cross-encoder arrives it must judge **the source text** — never the synthetic question, never the rewrite, never the summary. **A reranker grading the decoy is a court cross-examining the bait.** (Also: collapse candidates sharing a parent *before* the sieve, or five costumes of one passage waste five seats.)

**Also worth knowing:** **long context is not a substitute** — NoLiMa removes the lexical overlap and **11 of 12 frontier models lose half their accuracy by 32K**; the window holds evidence, it does not find it · **pre-filter ACLs, never post-filter** — a post-filtered top-K that drops eight of ten has silently become a top-two · **a query must never span embedder versions** (dual-write, serve from one index at a time) · **every index must earn its place through ablation** — vendors happily itemize the cost of presence, but only measurement writes the price of absence, and **a component with an empty second column is decoration, not infrastructure** · **scale decides architecture, not fashion** (Galileo: strength grows as length², weight as length³ — the giant collapses under his own femur) · and the week-long experiment anyone can run: **log the genealogy of every top result for a week** — the finding, every time, is that **most top results are not raw chunks.**

Full bilingual write-up in the repo: `course/week_10/week-10-summary.md` / `week-10-summary-for-team.zh.md`

> Housekeeping: this one was a backfill. The lesson plan had been sitting loose in `course/` with a ` (1)` on the filename, so Week 10 was recorded as "missing" and its topic guessed wrong in the Week 11 notes.

---

## Option B — 中文

**Week 10：多目录的图书馆 —— 检索架构，从头到尾** 🗂️

一句话：**一个检索系统不是对文档的搜索。它是一个表征的投资组合，外加一个裁决的法庭。**

这是承重墙拿到它的工程学的一周 —— 从上午十一点到晚上八点半，整个检索侧的房子。开场在 1895 年的布鲁塞尔：一位用手给世界编目的律师，提前一个世纪建成了我们现在正在机械化的那套架构。

**三件值得花时间的事：**

• **召回天花板 —— 把它写在眼皮内侧。** 一个小孩把弹珠丢在沙坑里，用铲斗和筛子找回来：铲得宽、容忍沙子，筛子稍后清理。**但如果铲斗漏掉了一颗弹珠，没有任何筛子能把它找回来。** 第一阶段的召回率是一个**下游任何东西都抬不高**的天花板 —— 不是 reranker，不是更好的 prompt，不是更大的模型。所以：**铲斗为召回调，筛子为精度调。** 与之配套的是断层扫描原理：CT 扫描仪从不拍摄肿瘤，它拍几百张单独看都是盲的投影然后重建。**融合就是那次重建；单一索引宣称拥有全视，而投资组合拒绝这个宣称。**

• **用户就是考官 —— 所以去制造匹配你的查询的文档。** 语料写成时心里根本没有考官（教科书为教学而写，合同为对方律师而写），语域错配是永久的。正统做法是变形查询；更深的一步朝反方向走 —— 把语料拿到离线，把每个 chunk 重铸成一个问题能一把抓住的形状。一条规则统治这一切：**检索派生物，从源生成。** 而最值得背下来的那个数字是**柏林实验**：**装着答案的那个段落**对查询打 **0.64**，抽取出来的 factoid 打 **0.81–0.90**。在 0.7–0.8 的生产阈值上，**那个装着答案的段落被静默地丢掉了。**

• **法庭：在排序层面融合，而诱饵的工作在检索处结束。** BM25 分数和 cosine 不共享标度，所以融合发生在排序上 —— **RRF、k=60**，一篇 2009 年一页纸的 SIGIR 论文，至今仍是几乎每个引擎的默认值，也是在你的 hold-out 集说话之前的宪法。然后是那条比任何其他条都绊倒更多团队的教条：cross-encoder 到场时必须判**源文本** —— 绝不是合成问题、绝不是重写、绝不是摘要。**一个给诱饵打分的 reranker，是一个在盘问诱饵的法庭。**（另：**在筛子之前**先折叠掉共享同一个父的候选，否则同一段文字的五套戏服会浪费五个席位。）

**顺带值得知道：** **长上下文不是替代品** —— NoLiMa 拿掉词汇重叠，**12 个前沿模型里 11 个在 32K 处损失一半准确率**；窗口是盛放证据的，不是寻找证据的 · **ACL 要预过滤，绝不后过滤** —— 后过滤掉十个里的八个，top-K 已经静默变成了 top-2 · **一个查询绝不能跨 embedder 版本**（双写迁移，一次只从一个索引服务）· **每个索引都必须通过消融赢得位置** —— 供应商乐意为你列出"存在的成本"，但**只有测量能写出"缺席的代价"**，而**第二栏空着的组件是装饰，不是基础设施** · **规模决定架构，不是时尚**（伽利略：强度按长度²增长，重量按长度³增长 —— 巨人在自己的股骨下崩塌）· 以及任何人都能跑的那个一周实验：**把每个 top 结果的家谱记录一周** —— 每一次的发现都是：**大多数 top 结果不是原始 chunk。**

完整中英文总结在仓库：`course/week_10/week-10-summary.md` / `week-10-summary-for-team.zh.md`

> 一点说明：这周是补档的。讲义一直散落在 `course/` 根目录、文件名带着 ` (1)`，所以 Week 10 之前被记成"缺失"，Week 11 笔记里对它主题的推断也猜错了。

---

## Option C — Ultra-short (if the channel is busy)

**Week 10 · Retrieval architecture** — **a retrieval system is not a search over documents; it is a portfolio of representations plus a court of adjudication.** Begins in Brussels, 1895: Otlet had the portfolio and lacked the court; half the day is the half he never built.

**Worth knowing:** **the recall ceiling** — if the scoop misses a marble no sieve recovers it, so tune the scoop for recall and the sieve for precision · **the tomographic principle** — fusion is the reconstruction; a single index claims total sight and the portfolio refuses it · **the user is the examiner** → manufacture documents matching your queries, and always **retrieve the derivative, generate from the source** · **the Berlin number**: paragraph-with-the-answer **0.64** vs extracted factoid **0.81–0.90** — at a 0.7–0.8 threshold the right answer is **silently dropped** · **fuse in ranks (RRF, k=60)**, and **the decoy's job ends at retrieval** — the cross-encoder judges the *source text* · **NoLiMa**: 11 of 12 frontier models lose half their accuracy by 32K — the window holds evidence, it does not find it · **pre-filter ACLs, never post-filter** · **every index earns its place through ablation** — an empty "price of absence" column means decoration, not infrastructure.

Full notes (EN/中文): `course/week_10/week-10-summary.md`
