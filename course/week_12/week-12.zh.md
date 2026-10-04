# 第 12 周课堂笔记：语义缓存现场课（The Stones in the River）

日期：2026-08-29（周六）

状态：**讲义 72 页已全部精读归档**（分七篇，见下表）。本文保留课堂现场的自己想通的例子。

## 全篇索引：五件仪器 ↔ 五种失败（讲义 p.66）

| 仪器 | 抓住的失败 | 幕 | 笔记 |
| --- | --- | --- | --- |
| **cap bound** 极冠界 | 偶然命中（**根本不存在**，命中都是有因的） | ACT I | [`act1-geometry.zh.md`](act1-geometry.zh.md) |
| **error contract δ** 误差合同 | **自信的错答案** | ACT II | [`act2-decision.zh.md`](act2-decision.zh.md) · [`sigmoid-decision.zh.md`](sigmoid-decision.zh.md) |
| **evidence gauntlet** 证据夹道 | **陈旧服务** | ACT III | [`act3-machine.zh.md`](act3-machine.zh.md) |
| **scoped key** 范围键 | **租户泄露** | Interlude | [`interlude-adversary.zh.md`](interlude-adversary.zh.md) |
| **break-even $H^*$** | **烧钱坑** | ACT IV | [`act4-economics.zh.md`](act4-economics.zh.md) |

> ***几何让这个赌注成为可能；策略让它诚实；范围让它安全；算术决定到底要不要下注。***

其余：[`prologue.zh.md`](prologue.zh.md)（序幕 p.4–7）· [`act5-wild-and-close.zh.md`](act5-wild-and-close.zh.md)（市场、模式语言、**周一早上的清单**）· [`rag-request-flow.zh.md`](rag-request-flow.zh.md) · [`kv-cache-and-prefix-caching.zh.md`](kv-cache-and-prefix-caching.zh.md)

## 周一早上，按顺序（讲义 p.70）

1. **打开 prefix caching** —— 免费、无风险、约 60% 的收益
2. **跑可行性闸门** —— 抽样查询里十分之一能在 0.85 匹配上，**否则不要建**
3. **手术刀只切密集、已划范围的切片**
4. **签下误差合同 δ**
5. **每周给样本打分**

> ***prefix caching 是默认项。语义缓存是一把手术刀 —— 而决定它往哪儿切的是那张表格，不是热情。***

---

来源：

- 现场讲义：*The Stones in the River — Semantic Caching for Enterprise RAG*（SupportVectors，Enterprise RAG · Advanced Course），讲师 Asif Qamar
- 课前预习与专著精读见 [`../week_11/week-11.zh.md`](../week_11/week-11.zh.md)

> **和 Week 11 的关系**：Week 11（8/22）已经把这份讲义 + 配套专著 *CacheCraft* 做过课前预习和课后精读，但当时记的是"读出来的东西"。本周是**同一份讲义的现场讲授**，所以这份笔记只记三样：讲师现场的口头补充、我自己想通的例子、以及和预习理解不一致的地方。概念的完整梳理不重复抄，直接引 Week 11。

---

## 讲义精读入口

> **→ [`prologue.zh.md`](prologue.zh.md)：序幕 p.4–7 逐页精读**
>
> 赌注（THE WAGER）/ 血统（THE LINEAGE）/ 解剖（THE ANATOMY，Front Door 模式）/ 划界（THE FIELD GUIDE，四象限）+ ACT II 前瞻（vCache 的 δ 合同与四级阶梯）。含 PDF 原页截图。

> **→ [`act1-geometry.zh.md`](act1-geometry.zh.md)：ACT I 几何 p.12–22 逐页精读**
>
> 极冠与测度集中 / 每次命中都是有因之事 / 各向异性 / 大都市效应 / 温度即玻尔兹曼因子 / 准正交容量 / hubs 与 CSLS / Goldilocks 带。含 PDF 原页截图。

> **→ [`act2-decision.zh.md`](act2-decision.zh.md)：ACT II 决策 p.21–31 逐页精读**
>
> $d'$ 决定该不该建 / 四级阶梯 / vCache 的 δ 合同 / 验证通道三出口 / 调速器不是闸门 / VoS 经济学 / Quiz 2「一个都不选」。

> **→ [`interlude-adversary.zh.md`](interlude-adversary.zh.md)：INTERLUDE 对手 p.41–46 逐页精读**
>
> 定理被武器化 / 熊皮衣：位置可以被购买 / **能工作的每个性质都是攻击面** / 防御要付两次钱 / **结构胜过警惕，因为警惕会宕机**。

> **→ [`rag-request-flow.zh.md`](rag-request-flow.zh.md)：RAG 请求全流程（地基参考）**
>
> 检索到底返回什么、怎么拼成 prompt、发给 LLM 之后怎么回写 provenance —— 三层缓存分别短路这条链的哪一段。

序幕四页的骨架：**定性 → 溯源 → 解剖 → 划界**。

- **p.4** 缓存是一场赌注；语义缓存把 Karlton 那两件难事**都占了**——因为判断"是不是同一个问题"**就是命名问题**
- **p.5** 1996 定理 → 2023 赌注 → 2024 贬值 → 2025 精算 → 2026 对手。**GPTCache 死于价格变动，不是死于对手**（prefix caching 把 G 里最好拿的 90% 免费拿走 → $p^*$ 逼近 1）
- **p.6** Front Door 模式：精确哈希 → 语义层 → 完整流水线，**每次生成都回写**。语义层给的是 *evidence, not proof*
- **p.7** 两轴四象限：语义缓存孤零零在「复用答案 × 近似匹配」的右上角，**家族里唯一会出错的成员**。三条边界：不是 prefix caching、不是检索（只找不答）、不是记忆（**关于你，不是关于问题**）
- **p.25–26 前瞻**：*A threshold is a hope. A contract is a measurable promise.* —— **δ 可移植，τ 从来不是**

---

## 〇、开场：标题的隐喻

> "No one steps in the same river twice — but some questions are stones. A cache is the wager that Heraclitus was only mostly right."

赫拉克利特说人不能两次踏进同一条河。缓存押的是反面：**企业里的问题很多是河里的石头**——反复出现、答案稳定、水流过去它还在原地。

这个隐喻里有整节课的三个张力：

| 隐喻元素 | 对应的工程问题 |
| --- | --- |
| 河（不断变的水） | 底层语料在变 → 失效（invalidation）与 TTL |
| 石头（重复出现的问题） | 命中率的来源；哪些 query 值得缓存 |
| "mostly right"（只是大体上对） | 阈值不可能完美 → false hit 是必然的成本，不是 bug |

留存句：**缓存不是省钱技巧，是一个关于"过去会重演"的赌注。**

---

## 一、语义缓存 vs. 精确缓存

普通缓存按**字符串精确匹配**，查询变一个字就 miss。语义缓存按**意思匹配**：把查询转成向量，在缓存里做向量检索，相似度超过阈值就直接返回旧答案，跳过检索 + 生成。

### 例子 1：为什么必须是"语义"

```text
Q1: "What's our PTO policy?"
Q2: "How many vacation days do I get?"
Q3: "年假有几天？"
```

字符串完全不同，意图相同。

- 精确缓存：3 次全 miss，每次走完整 RAG（约 2s、约 $0.01）
- 语义缓存：只算 1 次，后两次约 50ms、约 $0.0001

企业内部 query 分布是**长尾 + 极粗的头部**——头部那几十个问题（报销怎么走、假期几天、VPN 怎么连）就是石头。命中率的绝大部分来自它们。

---

## 二、阈值：这场赌注的定价

阈值是语义缓存唯一真正难的旋钮。调高 → 命中率崩塌，缓存形同虚设；调低 → 开始返回**似是而非的错答案**。

### 例子 2：高相似度 ≠ 同一个问题

```text
Q1: "What was our 2024 revenue?"
Q2: "What was our 2025 revenue?"
cosine similarity ≈ 0.97
```

两句话意思几乎一样，答案完全不同。阈值设 0.95 就会把 2024 的数字返回给问 2025 的人——**语义缓存最典型的事故形态**。

同类陷阱（都属于"小 token 差异、大语义差异"）：

- **否定**："Is X covered by insurance?" vs "Is X **not** covered?"
- **主体互换**："A 向 B 汇报吗？" vs "B 向 A 汇报吗？"
- **量词/时间限定**："上季度" vs "本季度"、"净利" vs "毛利"

> 共同结构：embedding 模型对**实体和时间的替换**不敏感，但答案对它们极度敏感。所以阈值不能拍脑袋定，要用真实 query log 标注一个集合，画出 hit rate 与 false hit rate 的权衡曲线再选点。
>
> 补救方向（待课上确认讲师给的做法）：命中后加一道轻量校验——抽取实体/日期做精确比对，或用小模型判"这两个问题是否等价"。相当于把语义匹配当**召回**，再加一层**精排**。

### ⭐ 现场白板：硬阈值只是特例

讲师在这里推翻了"硬阈值"这个说法本身——完整推演另开一篇：

> **→ [`sigmoid-decision.zh.md`](sigmoid-decision.zh.md)：从相似度到决策（σ / γ / τ / p / p\*）**
>
> 本周最核心的一块，含白板原图、余弦逐步算术、Platt scaling 拟合、四个 query 的完整数值推演。

要点速记：

$$p(\text{hit}) = \sigma\big(\gamma(s-\tau)\big), \qquad \text{命中当且仅当 } p > p^* = \frac{C}{G+C}$$

```text
   s        →     x = s − τ     →    p = σ(γx)    →    p > p*
相似度            相对边界位置          命中概率           决策
(几何 ACT I)        (定位)          (决策 ACT II)   (经济学 ACT IV)
```

- **硬阈值不是另一种方法，它是 sigmoid 在 γ = ∞ 时的特例**——一个假装自己百分之百确定的特例
- **τ** = 边界在哪（校准出来的）；**γ** = 边界多硬（模型能力）；**p\*** = 我怕不怕犯错（业务成本）
- γ、τ 管左半边，p\* 管右半边，**两边彻底解耦**：换模型只重拟合 γ、τ，换业务只重算 p\*
- 没有 γ，公式数值上根本不能用：相似度差只有 ±0.05，而 sigmoid 的工作区是 ±4，**差了 100 倍**
- γ 拟合得小 → 不是阈值定错了，是 embedding 分不开——**该换模型，不是调阈值**

---

## 三、企业场景：缓存必须带权限

### 例子 3：一次绕过 ACL 的泄漏

用户 A（HR）问"张三的薪资是多少"，答案进了缓存。
用户 B（实习生）问同样的问题 → 如果缓存全局共享，**直接命中并返回，完全绕过了权限检查**。

这是 Week 09 Secure Retrieval 那条"权限流水线必须和内容流水线同步"的直接延续：**缓存是第三条流水线，而且它最容易被忘掉。**

可行做法：

- 缓存 key 带上租户 / 权限维度：`hash(tenant_id + acl_group) + query_embedding`
- 或者保守方案：只对**公开语料**的问答启用 Query→Answer 缓存，受控语料只缓存到 embedding 层
- 权限变更时必须能定向失效对应分区

---

## 四、缓存可以放在哪一层

| 层 | 缓存内容 | 省什么 | 风险 |
| --- | --- | --- | --- |
| Query → Answer | 完整回答 | 检索 + 生成，省得最多 | 最高：过期/错答案直接出口 |
| Query → Docs | 检索到的 chunk | 省向量检索 + rerank | 低，生成仍会重做 |
| Text → Embedding | 向量 | 省 embedding API 调用 | 几乎为零 |
| Prompt prefix | KV cache | 省 prefill | 无 |

> 上线顺序建议：从下往上。Embedding 缓存和 prefix 缓存几乎无风险，先拿走这部分收益；Query→Docs 次之；Query→Answer 放在有了 false hit 监控之后再开。

最底两层单独展开一篇：

> **→ [`kv-cache-and-prefix-caching.zh.md`](kv-cache-and-prefix-caching.zh.md)：KV Cache 与 Prefix Caching**
>
> 含因果注意力为什么让 K/V 可复用、显存占用逐步算术（Llama-3-70B 每 token 320KB）、prompt 稳定度排序原则、跨请求共享的计时侧信道。

要点速记：

- **KV cache 不是优化，是可行性前提** —— 把 $O(n^2)$ 降到 $O(n)$，5000+500 的请求差约 480 倍计算量
- **显存是真瓶颈**：70B 模型单请求 8K 上下文吃 2.6GB，32 并发就 84GB；GQA/MQA/MLA 都是为压它而生
- **prefix caching 和语义缓存完全相反**：精确逐 token 匹配、零风险、框架自动；不需要 γ/τ/p\*，**没有决策，只有省钱**
- **prompt 按稳定度从高到低排列** —— 把时间戳放开头 = 亲手把命中率清零
- **单请求内零风险，跨请求共享才有侧信道** —— 光靠首字延迟就能推断"有没有人问过某个问题" ⚠️ 疑似 INTERLUDE 伏笔

---

## 五、失效（invalidation）

> ⚠️ **课后修正（讲义 p.35）**：我课上先写的是「TTL 为主」的方案，**这属于旧范式**。讲义的处方是 **evidence gauntlet（证据夹道）—— 在命中时刻实地核对证据，TTL 降级为兜底**。
>
> ***"TTLs guess; the world doesn't consult them."***（TTL 在猜；世界不会来问它。）
>
> 四道串行闸：**相似度 → 证据重叠 → chunk 版本一致性 → 词面支持**。全过才放行。
> 外加 **Version Pin**：`embedder_version` + `index_version` 写进条目 schema，不匹配 = 无条件 miss。
>
> 完整内容见 [`act3-machine.zh.md`](act3-machine.zh.md)。

下面是我课上先写的版本，保留作为对照（**为什么不够**：时间和正确性之间没有可靠关系——文档可能三个月不变，也可能十分钟前刚改）：

- **TTL 分级**：静态政策类 7 天，产品/库存数据 1 小时，实时数据不缓存
- **文档指纹**：缓存条目记录当时用到的 doc version / hash，源文档更新时批量失效
- **不缓存清单**：query 含"现在 / 今天 / 最新 / 当前"等时效词的直接 bypass

---

## 六、指标

必须成对上报：

- **hit rate**（收益侧）
- **false hit rate**（成本侧，最重要）
- p50 / p95 延迟下降
- 每千次查询成本下降
- 缓存条目年龄分布（发现"僵尸条目"）

> 只报 hit rate 不报 false hit rate 的语义缓存 demo，等于只报收入不报亏损。

---

## 七、待补（课程进行中）

- [ ] 讲师现场给的阈值调优方法 / 具体数值区间
- [ ] 命中后是否有二次校验层，用什么做
- [ ] 对抗视角：缓存投毒（把错误答案喂进缓存）与 timing side channel
- [ ] 本周 Lab 内容
- [ ] 本周 eval case → 写入 `evals/`
- [ ] Avaloka 映射：agent memory 的语义缓存怎么落
- [ ] Week 10（8/15）记录缺口是否已补
