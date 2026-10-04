# Week 07 Slack draft (for review — not sent)

---

## Option A — English

**Week 07: Evaluation — we stop building and start measuring** 📏

One line: **you cannot improve what you cannot measure — and the yardstick is yours to build, not someone else's.**

Six weeks of building the library, the map and the gates, and one question was never asked rigorously: *does any of it work?* The whole day hangs on `argmax_θ E_{q∼𝒬}[μ(q,θ)]` — tune every knob θ to maximise metric μ over **your own** query distribution 𝒬.

**Three things worth your time:**

• **The minimal diagnostic pair — the most useful page of the week.** nDCG low + Recall high → the docs are found but badly ordered → **fix the reranker**. Both low → they aren't found at all → **fix retrieval** (chunking, embedder, hybrid). Both high → move on to generation. Live example: Recall@50 = 0.91 healthy, NDCG@10 dropped 0.71 → 0.55 overnight, teammate proposes re-chunking the corpus. He's wrong, and the pair just saved a week of surgery on a healthy organ.

• **No gold dataset, no metrics.** Every retrieval metric *presupposes* a ruler someone signed their name to. The affordable recipe: SMEs (not engineers) author queries from real intent → a simple engine pulls top 100–200 → cherry-pick 25–30 and grade them **0–4** → freeze and version. *"No human can scan a corpus. Anyone can scan two hundred candidates."* Size: min 200, shoot for 1,000 — and that number isn't folklore, power analysis says N≈500–1,000 to detect a 1-point nDCG gain at 80% power.

• **Statistical significance ≠ practical significance.** A 1.2-point gain on 200 queries may be nothing. Run a paired bootstrap. Enterprise rule of thumb: **nDCG delta of 0.02–0.05** is worth engineering effort; below that you're chasing noise. And Goodhart is waiting — optimise faithfulness alone and the model learns to over-hedge ("it is possible that…"), technically faithful and useless.

**Also worth knowing:** nDCG has *two* gain conventions (linear vs `2^rel − 1`) — numbers don't compare across them · ROC is useless for RAG (an empty-set retriever scores beautifully; class imbalance is the assassin of ROC) · on the generation side, answer-level faithfulness lets one wrong claim ride along free, so go claim-level (FActScore; ChatGPT bios score 58%) · citation accuracy runs 40–75%, i.e. **one in three citations wrong or missing**.

Full bilingual write-up in the repo: `course/week_07/week-07-summary.md` / `week-07-summary-for-team.zh.md` · three runnable demos in `course/week_07/`

---

## Option B — 中文

**Week 07：评估 —— 停止建造，开始测量** 📏

一句话：**你无法改进你无法测量的东西 —— 而尺子得你自己造，不是借别人的。**

六周建了图书馆、地图和闸门，但有个问题从没被严肃问过：*这些到底管不管用？* 全天挂在一个公式上 `argmax_θ E_{q∼𝒬}[μ(q,θ)]` —— 调遍所有旋钮 θ，让指标 μ 在**你自己的**查询分布 𝒬 上最大。

**三件值得花时间的事：**

• **最小诊断对 —— 本周最实用的一页。** nDCG 低 + Recall 高 → 文档找到了但排序烂 → **修 reranker**；两者都低 → 根本没找到 → **修检索**（chunking、embedder、hybrid）；都高 → 去评生成侧。现场例子：Recall@50 = 0.91 健康，NDCG@10 一夜从 0.71 掉到 0.55，同事提议重新 chunk 整个语料。他错了 —— 这个诊断对刚省下一周对着健康语料动的手术。

• **没有金数据集就没有指标。** 每一个检索指标都**预设**了那把"有人签名负责"的尺子。可负担的做法：SME（不是工程师）从真实意图出题 → 简单引擎捞 top 100–200 → 精挑 25–30 条打 **0–4 分** → 冻结、版本化。*"没人扫得完整个语料库，但谁都扫得完两百个候选。"* 规模：最少 200、目标 1000 —— 这不是拍脑袋，功效分析说要在 80% 功效下检测出 1 分 nDCG 提升需要 N≈500–1000。

• **统计显著 ≠ 实用显著。** 200 个 query 上涨 1.2 分可能什么都不是，先跑配对 bootstrap。企业经验阈值：**nDCG 提升 0.02–0.05** 才值得投工程，低于此是在追噪声。Goodhart 在后面等着 —— 只优化 faithfulness，模型就学会过度对冲（"有可能……"），技术上忠实但没用。

**顺带值得知道：** nDCG 有**两套**增益约定（线性 vs `2^rel − 1`），跨约定的数字不可比 · ROC 在 RAG 上没用（返回空集也能刷满分，类别失衡是 ROC 的刺客）· 生成侧要到**声明级**，答案级的 faithfulness 会让一个错声明搭便车混过（FActScore：ChatGPT 生成的传记只有 58%）· 引用准确率 40–75%，**约每三条引用就有一条错或缺**。

完整中英文总结在仓库：`course/week_07/week-07-summary.md` / `week-07-summary-for-team.zh.md` · 三个可运行 demo 在 `course/week_07/`

---

## Option C — Ultra-short (if the channel is busy)

**Week 07 · Evaluation** — six weeks of building, zero weeks of measuring. The fix: `argmax_θ E[μ(q,θ)]` over **your own** query distribution.

**Worth knowing:** the **minimal diagnostic pair** — nDCG low + Recall high = fix the reranker, both low = fix retrieval (saves a week of re-chunking a healthy corpus) · no gold dataset, no metrics (SME-authored queries, top 100–200 pool, cherry-pick 25–30, grade 0–4, min 200 / shoot for 1,000) · **statistical ≠ practical significance** — paired bootstrap, and only a **0.02–0.05 nDCG delta** is worth shipping · ROC is useless for RAG, use AUC-PR · generation side goes **claim-level** (FActScore 58%, citation accuracy 40–75%).

Full notes (EN/中文): `course/week_07/week-07-summary.md`
