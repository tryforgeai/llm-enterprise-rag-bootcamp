# Week 08 Slack draft (for review — not sent)

---

## Option A — English

**Week 08: The Personal Equation — measure the measurer first** 🔭

One line: **your judge has a bias too — and the deepest metric is "does it know what it doesn't know?"**

Week 07 measured retrieval. This week measures the **generator**, and then the world **after launch**. The opening is the best part: seven small experiments you fail with your own hands, each one pointing at a metric you learn that afternoon. (Greenwich, 1796: Maskelyne fires his assistant for recording transit times "slow." Bessel, 1823: it wasn't negligence — every observer has a stable, measurable bias. **Subtract it, don't fire it.**)

**Three things worth your time:**

• **correct ≠ grounded — the hardest rule of the week.** Give the room an Australia passage mentioning only Sydney and Melbourne, ask for the capital, and half of them write *Canberra* — which never appears in the text. The trap is that **Canberra is actually right**, so nothing in a "was the answer correct?" check ever fires. An answer can be entirely correct and still be a grounding failure. The full-marks response: *"The passage doesn't say — though it's commonly known to be Canberra."* Measured by **negative rejection rate**, where ChatGPT-class systems score **43–45%** and regulated deployment needs **>70%**.

• **Your judge needs a judge — and κ, not raw agreement.** A judge agreeing with humans 75% of the time can have **κ = 0.375** (60 points of that was luck). A lazy judge that always says "grounded" gets 70% agreement and **κ = 0**. Rule: **reject any judge below κ 0.6**, use a different model family than the generator, average both orderings (position bias swings scores **40–60 points**), never trust one judge. Best result of the day: **three small heterogeneous judges voting reach κ 0.763 vs a single GPT-4's 0.627, at 1/7 the cost.** Diversity beats scale — which is just "average several observers to cancel the personal equation."

• **pass@k vs pass^k — one log file, two opposite conclusions.** At 70% per run, `pass@3 = 97%` (the optimist's number) and `pass^3 = 34%` (three consecutive customers all served). GPT-4o on τ-retail drops from ~61% at k=1 to **~25%**. **"70% success" doesn't mean 70% done — it means three customers in ten are comprehensively broken.** Harnesses with a verifier live on the first curve; customer-facing agents live on the second. Related: a 5-step chain at 90% per step is a **59%** process.

**Also worth knowing:** **Act V "The Observatory" is new** — evaluation doesn't end at launch (offline gates the merge, online scores live traffic by implicit signals — *a rewrite is a downvote, a copy-paste is an upvote*, and every production failure ratchets into a permanent test case) · RAG tasks drift **25–75%** over months; the cheap probe is a **domain classifier** on frozen vs live query embeddings, where **AUC ≈ 0.5 means sleep well** · small verifiers first — **MiniCheck hits GPT-4 accuracy at ~1/400 the cost** · FActScore on ChatGPT bios was 58% in 2023; with retrieval + abstention 2026 reasoning models reach ~99%, **but tail knowledge without retrieval is still 29–55%** · **~70% of RAG systems still have no systematic evaluation.**

Full bilingual write-up in the repo: `course/week_08/week-08-summary.md` / `week-08-summary-for-team.zh.md`

---

## Option B — 中文

**Week 08：人差方程 —— 先测量测量者** 🔭

一句话：**你的评委也有偏差 —— 而最深的那个指标，是「它知道自己不知道吗」。**

Week 07 量的是检索，这周量**生成器本身**，再量**上线之后的世界**。开场设计最妙：七个你会亲手失败的小实验，每个失败对应下午学的一个指标。（1796 年格林威治，Maskelyne 因助理记录星体过中天「总是慢」把他开除；1823 年 Bessel 发现这不是失职 —— **每个观测者都有稳定可测的偏差。减掉它，别开除它。**）

**三件值得花时间的事：**

• **correct ≠ grounded —— 本周最硬的一条。** 给一段只提悉尼、墨尔本的澳洲短文，问首都是哪，半屋子写 **Canberra** —— 文中根本没出现。陷阱在于 **Canberra 现实里是对的**，所以任何「看答案对不对」的检查都不会报警。**一个答案可以完全正确，同时仍是 grounding 失败。** 满分答案：*「资料没说 —— 不过众所周知是 Canberra。」* 用**负拒绝率**测，ChatGPT 级只有 **43–45%**，监管行业部署门槛 **>70%**。

• **评委也需要被评 —— 要看 κ，不是原始一致率。** 一个与人工一致 75% 的评委，κ 可能只有 **0.375**（其中 60 分是碰运气）；一个永远说「有据」的偷懒评委能拿 70% 一致率、**κ = 0**。规矩：**κ < 0.6 拒用**、judge 用与 generator 不同的模型家族、两个顺序都跑取平均（位置偏见能让分数摆动 **40–60 分**）、绝不信单一评委。当日最好的结果：**3 个异构小 judge 投票 κ 0.763，完胜单个 GPT-4 的 0.627，成本约 1/7。** 多样性胜过规模 —— 这正是「对多个观测者取平均抵消人差方程」。

• **pass@k vs pass^k —— 同一批日志，两个相反结论。** 单次 70%：`pass@3 = 97%`（乐观数）、`pass^3 = 34%`（连续三个客户全成）。GPT-4o 在 τ-retail 从 ~61%@k=1 掉到 **~25%**。**「70% 成功」不是完成 70%，是十个客户里三个彻底坏掉。** 有 verifier 可重试的 harness 活在第一条曲线，面向客户的 agent 活在第二条。顺带：每步 90% 的 5 步链，整体只有 **59%**。

**顺带值得知道：** **Act V「The Observatory」是全新一幕** —— 评估不在上线处结束（离线卡合并、在线用隐式信号打分：*改写 = 反对票、复制进邮件 = 赞成票*，每次生产失败棘轮成永久用例）· RAG 任务数月漂移 **25–75%**，最便宜的探针是对「冻结 vs 实时」query embedding 训个 **domain classifier**，**AUC ≈ 0.5 就睡得香** · 小验证器优先 —— **MiniCheck 约 1/400 成本达 GPT-4 精度** · FActScore 在 2023 年 ChatGPT 传记只有 58%，靠检索+弃权推到 2026 推理模型 ~99%，**但无检索的尾部知识仍只有 29–55%** · **约 70% 的 RAG 至今没有系统化评估。**

完整中英文总结在仓库：`course/week_08/week-08-summary.md` / `week-08-summary-for-team.zh.md`

---

## Option C — Ultra-short (if the channel is busy)

**Week 08 · Evaluating the generator** — Week 07 measured retrieval; this week measures the chef, and the world after launch. Opens with seven experiments you fail yourself (Greenwich 1796: every observer has a measurable bias — **subtract it, don't fire it**).

**Worth knowing:** **correct ≠ grounded** — a factually right but unsupported answer is a grounding failure and no "was it right?" check catches it (negative rejection: ChatGPT-class **43–45%**, regulated bar **>70%**) · judge your judge with **Cohen's κ, not raw agreement** — 75% agreement can be κ 0.375; **κ < 0.6 = reject**; three small judges voting beat one GPT-4 (**0.763 vs 0.627**, 1/7 the cost) · **pass@k vs pass^k** — 70% per run is 97% optimistic and **34%** across three consecutive customers · new **Act V "The Observatory"**: offline gates the merge, online scores live traffic, drift probe = domain classifier with **AUC ≈ 0.5 = sleep well** · **MiniCheck: GPT-4 accuracy at ~1/400 cost.**

Full notes (EN/中文): `course/week_08/week-08-summary.md`
