# 第 03 周课堂笔记

日期：2026-06-20

状态：课前讲义、课堂讨论、视频补充、代码实验和 contextual chunking baseline 已记录；Week 03 eval artifact 已完成（`evals/week03-representation-tournament/`，2026-09-12）

来源：`course/week_03/week-3-summer-lesson-plan.pdf`

## 本周进度总览

Week 03 的主线是：

```text
chunking 不是普通预处理，
而是 RAG 对源文档做的第一次表示决策。
```

这周我已经从“知道 RAG 要切 chunk”，推进到能解释和实现下面这套判断：

```text
文档类型是什么？
用户会问什么？
哪些信息不能被切断？
用 text chunk、contextual chunk、late chunking、page-image retrieval，还是 hybrid？
如何用 eval 证明哪种表示方式更好？
```

### 已掌握的概念

| 概念 | 我现在应该能解释什么 |
| --- | --- |
| chunking as ontology | chunk 边界是在定义“什么算一个可独立检索的思想单元” |
| first projection | 文档进入 embedding 空间前的切分是有损且很难逆转的 |
| small chunk amnesia | 小 chunk 更纯，但可能丢掉指代、条件、定义、否定和安全范围 |
| centroid delusion | 大而杂的 chunk 会变成平均意义，对很多 query 都有点像但不真正回答问题 |
| query-chunk asymmetry | query 短而尖锐，chunk 长而弥散，二者匹配时可能产生偏差 |
| semantic / neural chunking | 把 chunking 当成边界检测任务，让模型判断哪里应该切 |
| contextual chunking | 切完后给每个 chunk 补一段可读上下文，减少 chunk 失忆 |
| late chunking | 先让 encoder 看长上下文，再按 chunk boundary pooling 出 chunk embedding |
| page-image retrieval | 不把 PDF 强行压成一维文本，而是保留页面、表格、公式和版面结构 |
| representation tournament | 不凭感觉选 pipeline，而是让多种表示方式在同一批 query/eval 上比赛 |

### 已完成的学习和实验

1. 阅读并总结 Week 03 lesson plan，形成 chunking failure mode 笔记。
2. 根据课堂截图补充了 endophora、scope failure、bridging inference、genre blindness、centroid delusion 等例子。
3. 看了 RAG-is-dead / context engineering 相关视频，明确“死掉”的是 naive top-k vector RAG，不是 retrieval 本身。
4. 写了 `course/week_03/punctuation_embedding_test.py`，用 BERT、MiniLM、fine-tuned embedding 跑标点敏感度实验。
5. 跑出课堂例子结果：BERT 和 MiniLM 都能看出熊猫句更接近无逗号句，但仍把词面高度重合的两句判得最像。
6. 写了 `pdf_to_textbook.py`，把 PRML PDF 转成 text/Markdown textbook baseline。
7. 写了两条 PRML QA path：
   - `path1_page_image_qa.py`：page image retrieval + vision answer
   - `path2_text_chunk_qa.py`：text chunk retrieval + text answer
8. 加了 `qa_compare_app.py`，用于比较 page-image path 和 text chunk path。
9. 检查了 PRML page images：749 页 PNG 连续完整，没有缺页。
10. 检查了课堂 `week-03-in-person-lab`：里面有 CLIP、SigLIP2、MiniLM 三路检索和 Gradio UI，但当前全局 Python 环境还缺运行依赖。
11. 处理了 capstone PDF，生成 regular chunks 和 contextual chunks：
    - `course/week_03/capstone_contextual_chunks/regular_chunks.jsonl`
    - `course/week_03/capstone_contextual_chunks/contextual_chunks.jsonl`
    - 共 266 个 chunk，contextual version 使用本地 deterministic context prefix，没有调用外部 API。

### 目前最重要的理解

本周最关键的变化是：我不再把 chunking 看成“调一个 chunk size”，而是把它看成一个完整的 representation design problem。

好的 RAG 不是简单做：

```text
PDF -> 512-token chunks -> embedding -> top-k
```

而是要先问：

```text
这个文档的意义住在哪里？
在句子里？
段落里？
章节里？
表格和图里？
页面布局里？
还是跨 chunk 的上下文关系里？
```

然后再选择：

```text
fixed / recursive / semantic / contextual / late / page-image / hybrid
```

### Representation tournament（已完成，2026-09-12）

Week 03 的 eval artifact 已经建好：`evals/week03-representation-tournament/`。

```text
PRML 749 页，27 个 query
-> fixed / semantic / contextual 三个文本臂（page-image 已搭好骨架，待接 CLIP）
-> 页级 gold（从 PRML running header 反推 65 个 section，可审计、非循环）
-> Recall@k / Hit@k / MRR / NDCG@k / NRR / units read + 错误类型
```

baseline 结论（BM25，k=5）：

| 臂 | Recall@5 | Hit@5 | NDCG@5 | units read |
| --- | ---: | ---: | ---: | ---: |
| semantic | 0.255 | 0.913 | 0.539 | 3.7 |
| contextual | 0.247 | 0.957 | 0.514 | 5.8 |
| fixed | 0.177 | 0.870 | 0.422 | 5.3 |

三个发现：

1. fixed chunking 在 k=3/5/10 上全部垫底，而且主要输在排序（NDCG 最低）而不是找不到 —— 和 centroid delusion 的预测一致。
2. contextual 在 scope_condition 和 figure_dependent 两族上是唯一打满的臂，正是"chunk 需要知道自己属于什么"的两种场景。
3. **最重要的一条，而且不是本来要测的**：关掉空格修复后跑 ablation，contextual 的优势完全消失（recall 0.166 vs fixed 0.165）。抽取质量决定了 chunking 策略能不能兑现。在 PDF 语料上选 chunking 方案之前，应该先量自己的 parser。

未解决：三个臂都在 W03-25（dropout，与 5.5 节 "Regularization in Neural Networks" 词面几乎全覆盖）上过度回答，NRR 停在 0.750。这和主 eval 的 EV-006 是同一个失败，说明问题出在 abstention gate 而不是语料。

## 一句话总结

本周围绕一个看似简单但很根本的问题展开：

```text
To chunk, or not to chunk?
```

也就是：RAG 是否应该默认把文档解析、切块、embedding、检索？课程的回答不是教条式的“必须 chunk”，而是要求把不同表示方式放进同一套评估里比赛。

核心思想：

```text
源文档
-> 选择表示方式
-> 选择是否切块
-> embedding 或视觉检索
-> retrieval eval
-> 用证据决定 pipeline
```

Chunking 不是无害的预处理。它是 RAG 流水线第一次决定“什么算一个思想单元”的地方，也是第一次不可逆的信息投影。

## 核心概念

### 1. Chunking 是本体论决策，不只是预处理

常见 RAG 教程默认：

```text
parse
-> chunk
-> embed
-> retrieve
```

但本周讲义要求先问：这个默认步骤是否适合当前语料？

把文档切成 chunk，实际上是在告诉系统：

```text
这一段文本就是一个可以独立检索、独立表示的思想单元
```

如果这个判断错了，后续的 embedding、reranking、prompt 和更强模型都只能在错误输入上修补。

### 2. 第一次投影是不可逆的

Embedding 是有损压缩。源文本进入 embedding 空间时，丰富的文本结构会被压缩成向量。

```text
源文本 X
-> chunk 边界
-> embedding 模型
-> latent representation Z
```

如果一个 chunk 里混入两个互不相关的思想，例如“牛跳过月亮”和“英伟达股票下跌”，一个固定维度向量只能把它们压成一个混合点。这个点既不真正代表牛，也不真正代表股票。

这就是本周的 mixing principle：

```text
一个 chunk 中混入多个正交思想
-> embedding 变成平均意义或混合意义
-> query 检索时对每个思想都只是“有点相关”
-> 结果变成噪声
```

### 3. 为什么仍然需要 chunk

课程不是反对 chunking，而是反对不加思考的默认 chunking。

我们仍然 chunk，主要有三个工程理由：

| 理由 | 解释 |
| --- | --- |
| 上下文窗口 | 不能把所有文档都塞进模型上下文 |
| 检索精度 | 整篇文档 embedding 太弥散，具体答案可能被平均掉 |
| 成本 | 长上下文 attention 成本高，而且容易出现 lost in the middle |

所以问题不是“chunking 好不好”，而是：

```text
当前任务应该切什么？
切多细？
用文本切还是视觉页面检索？
如何证明这个选择更好？
```

### 4. 512-token 默认值不是理论结论

很多系统默认 512 tokens 一个 chunk，但这只是方便的工程基线，不是语义边界。

一个页面大约 300 到 400 tokens，512 tokens 约等于一页左右。但一页不一定包含一个完整思想：

- 新闻报道可能一页包含多个主题。
- 学术文章可能一个论点跨很多页。
- 法律、医学、财务文档中的条件、定义、例外可能远离引用位置。

因此 512-token chunk 应该被当作 baseline，而不是被当作合理答案。

## Chunking 会破坏什么

### 1. Endophora：文本内部引用断裂

Endophora 指文本引用文本内部其他部分，包括：

- anaphora：向前引用，例如 `it` 指前一句的主语
- cataphora：向后引用，例如先说 `he`，后面才给出 John

如果引用和被引用对象被切到不同 chunk，chunk 可能语法通顺但语义悬空。

RAG 失败形态：

```text
检索到含有代词、缩写、"as shown above" 的 chunk
-> 但缺少被引用对象
-> 模型用猜测补全
-> 回答看起来流畅但证据不完整
```

### 2. Discourse structure：论证关系被切断

文档不是句子的简单列表。句子之间有因果、让步、对比、证据、限定、反驳等关系。

如果只检索到一个强烈主张，而没有检索到后面的让步或限定，答案可能反转原文结论。

特别危险的场景：

- 科学论文中的 `however`
- 法律合同中的条件句
- 医学研究中的适用人群
- 风险声明中的例外和限定

工程判断：

```text
一个可检索 chunk 不一定要完整复现全文，
但至少应该保留 claim、condition、qualifier、evidence 之间的关键关系。
```

### 3. Negation trap 与 scope failure

否定、条件、反事实和不确定性修饰都有作用范围。

如果 chunking 把作用范围切断：

- `no significant evidence` 可能丢掉 `in patients under 65`
- `if debt-to-income ratio exceeds 43%` 可能丢掉条件
- `may play a role` 可能被后续句子误读成确定事实

这类错误很危险，因为系统不一定会暴露出明显错误信号。它会生成一个看似可靠、实际过度确定的答案。

### 4. Lexical cohesion 与 definition-use chain

一个文档会通过反复出现的相关词形成语义场。法律文档、API 文档、医学标准尤其依赖定义链。

示例：

```text
第 2.1 节定义 "Covered Losses"
第 7.4 节多次使用 "Covered Losses"
```

如果定义和使用被分开检索，模型看到的只是普通英文词，而不是合同中的精确定义。

这解释了一个常见现象：

```text
chunk 越小不一定越好。
小 chunk 更纯，但可能失去词汇伙伴和定义上下文。
```

### 5. Bridging inference 与 genre blindness

有些关系没有显式连接词，需要读者凭背景框架补全。

例如：

```text
John walked into the room. The chandelier was magnificent.
```

读者知道吊灯在房间里，但文本没有直接说。chunking 可能把这种隐含场景切掉。

Genre blindness 是更大的问题：不同文体的信息密度不同。

| 文体 | Chunking 风险 |
| --- | --- |
| 法律合同 | 每个词和条件都可能有约束力 |
| 小说 | 大量氛围铺垫可能服务于一个关键反转 |
| 科学论文 | abstract、methods、results 互相预设 |
| 财务 PDF | 表格、图、注释、版面位置携带意义 |

同一个 512-token 策略不应该无差别用于所有文体。

### 6. Embedding space 的病理：centroid delusion

一个 chunk embedding 往往像内容的平均意义。内容越杂，向量越可能落在“谁都像一点，但谁都不是”的位置。

风险：

```text
大而杂的 chunk
-> embedding 靠近语义空间中心
-> 对很多 query 都有中等相似度
-> 经常出现在 top-k
-> 但很少真正回答问题
```

这会制造“热门但无用”的检索结果。解决办法通常不是过滤，而是重新设计切分和表示方式。

## 两条路线：更好地 chunk，还是不 chunk

### 路线一：更好地 chunk

#### Fixed-size chunking

固定长度切块简单、稳定、便宜，但它只考虑 token 数，不理解句子、段落、论点和文档结构。

适合作为 baseline，不适合作为默认结论。

#### Recursive chunking

递归切块优先在段落、句子、词边界切，比固定长度好，但仍然主要围绕 size，不一定围绕 meaning。

#### Semantic chunking

语义切块检测相邻句子或段落之间的语义变化，在 topic shift 处切开。

优点：

- 更接近真实话题边界
- 比固定 chunk 更少切断思想

限制：

- 只能改善切在哪里
- 不能恢复被切断的引用和长距离关系

#### Hierarchical chunking

层级切块同时保留粗粒度 parent 和细粒度 child。

```text
section parent
-> paragraph child
-> atomic child
```

优点是同时拥有局部精度和上层上下文。风险是：检索到 child 后替换成 parent，可能把大量无关句子塞进生成上下文，导致答案被 parent 中的旁支内容带偏。

#### Contextual chunking

Contextual chunking 在文本空间修复上下文：先切小块，再让模型阅读全文，为每个小块补上最小必要上下文。

```text
原始 chunk:
It has a population of 3.6 million.

补上下文后:
Berlin is the most populous city of Germany. It has a population of 3.6 million.
```

优点是可读、可审计。缺点是每个 chunk 可能需要额外 LLM 调用，成本更高。

#### Late chunking

Late chunking 在 latent space 修复上下文：先让 encoder 读完整文档，让每个 token 的表示吸收全局上下文，然后再按边界 pooling 成 chunk vector。

```text
whole document
-> contextual token representations
-> cut / pool selected token spans
-> chunk embeddings with global context
```

优点是优雅、效率高，尤其适合解决代词和跨句引用问题。限制是解释性弱于 contextual chunking。

### 实用 pipeline

本周建议的思路可以写成：

```text
尊重文档 markup / headings
-> semantic hierarchical chunking
-> budget 允许时做 contextual chunking
-> late chunking before embedding
-> 保存 section、position、parentage、source metadata
-> 用 eval 选择 winner
```

这不是固定配方，而是候选方案集合。每个新语料都应该跑 representation tournament。

### 路线二：不 chunk，直接做 page-image retrieval

课程的第二条路线是质疑 parse-and-chunk 本身。

有些文档不只是文字序列，而是二维页面：

- 表格
- 图表
- 公式
- 版面位置
- 缩进
- 脚注
- 图注
- 图与正文的空间关系

把页面 parse 成一维文本会丢掉这些视觉和空间语法。

Vision-language retrieval 的做法是：

```text
PDF page
-> render as image
-> split into visual patches
-> encode patches with VLM
-> text query 与 page patches 做 late interaction
-> retrieve page or page region
```

ColPali / ColVision 这类方法不是把整页压成一个向量，而是保留多个 patch vectors，再用类似 ColBERT 的 MaxSim 方式匹配 query token 和页面区域。

适合 page-image retrieval 的语料：

- 财务报告
- 科学论文 PDF
- 扫描件
- 包含表格、图、公式、图注的教材
- 版面结构本身携带意义的文档

不适合完全替代文本检索的场景：

- 需要字符级精确匹配
- 需要长距离跨页推理
- 需要低成本大规模索引
- 文档主要是纯文本 prose

因此最稳妥的设计通常不是二选一，而是：

```text
text parse-and-chunk
vs page-image retrieval
vs hybrid index
```

用同一批查询、同一套指标做比赛。

## Representation Tournament

本周最重要的工程方法是 representation tournament。

不是先争论哪种方法“理论上更好”，而是为自己的语料设计比赛：

```text
语料样本
-> held-out queries
-> gold evidence / acceptable answers
-> competing representations
-> retrieval metrics
-> latency / cost / safety checks
-> winner or hybrid strategy
```

候选表示可以包括：

- fixed-size chunks
- recursive chunks
- semantic chunks
- hierarchical chunks
- contextual chunks
- late chunking
- page-image retrieval
- hybrid text + vision retrieval

评估指标：

| 指标 | 用途 |
| --- | --- |
| Recall@k | 相关证据是否进入候选集 |
| MRR | 第一个正确证据出现得多早 |
| NDCG@k | 排序是否把高价值证据放前面 |
| hard-negative error | 是否把相似但错误的证据排高 |
| answer grounding | 最终回答是否被取回证据支持 |
| latency / cost | 是否可用于真实系统 |
| safety / privacy | 是否取回不该使用的内容 |

## 与前两周的关系

| 主题 | 第 01 周 | 第 02 周 | 第 03 周 |
| --- | --- | --- | --- |
| RAG | 端到端流水线 | embedding 和 attention 为什么能工作 | 第一次切分如何决定检索上限 |
| Embedding | 意义变成几何 | 训练、anisotropy、contrastive learning | chunk composition 如何扭曲几何 |
| Retrieval | sparse + dense + rerank | cosine / attention / multimodal space | 不同表示方式的检索比赛 |
| Chunking | 第一次不可逆切割 | token 到 chunk embedding | 系统讲清 chunking 破坏什么以及替代路线 |
| Multimodal | CLIP 搜图 | 共享语义空间 | page-image retrieval 用视觉保留版面结构 |

一句话连接：

```text
第 01 周讲 RAG 流水线。
第 02 周讲向量空间为什么能用。
第 03 周讲进入向量空间之前，源文档被怎样切坏或保留下来。
```

## 解锁的 Agent 能力

Agent 可以更准确地诊断 RAG 检索失败是不是源于表示选择，而不是盲目调 prompt 或 reranker。

具体能力：

- 识别 chunking 是否切断代词、定义、条件、否定、论证关系或版面关系。
- 判断小 chunk 是提升精度，还是制造上下文失忆。
- 判断大 chunk 是保留上下文，还是制造 centroid delusion。
- 为不同语料设计 representation tournament。
- 在文本 chunking、late chunking、contextual chunking、page-image retrieval 和 hybrid retrieval 之间做证据驱动选择。
- 在 trace 中记录 chunk 策略、source metadata、parent/child 关系、context restoration 和 retrieval winner。

## Avaloka 应用

Avaloka 的 Care Card 和智慧材料检索不应该直接套用默认 chunking。

需要先区分材料类型：

| 材料 | 可能策略 |
| --- | --- |
| Care Card | 小而完整的原子记忆，保留 permission、lifecycle、risk scope |
| Wisdom principle | 语义 chunk + 上下文补充，避免断章取义 |
| Baifa / mind-state notes | 保留定义-use chain 和反例 |
| 评估失败记录 | 按 failure mode 和 decision point 切分 |
| 讲义、PDF、表格或扫描内容 | 考虑 page-image retrieval 或 hybrid index |

对 Avaloka 最重要的风险是：chunking 可能把安全边界和温柔语气从事实片段中切掉。

例如：

```text
care preference
-> 如果脱离 risk condition 或 permission scope
-> 可能被 agent 用在不该用的情境
```

因此 Avaloka retrieval 的 chunk schema 至少要保留：

- source id
- memory type
- permission scope
- risk scope
- lifecycle status
- created / updated time
- related user intent
- parent context
- safety qualifiers
- exact quoted evidence when needed

## 今日课堂与视频补充

### 1. 小 chunk 为什么更纯但容易失忆

小 chunk 更纯，是因为它通常只包含一个局部主题，embedding 不容易被其他主题污染。

但小 chunk 容易失忆，是因为它可能把这句话成立所需的上下文切掉：

```text
原文:
When user is stable and not in acute distress, user likes gentle reminders.

坏 chunk:
User likes gentle reminders.
```

第二个 chunk 看起来很清楚，但它忘了最重要的条件：`not in acute distress`。对 Avaloka 来说，这类失忆会把一个安全、温柔的偏好变成危险的泛化规则。

好的小 chunk 应该是：

```text
小而完整
= 事实 + 指代对象 + 适用条件 + 禁用条件 + 权限范围 + 来源
```

### 2. Endophora、论证关系和 scope failure

课堂截图里的第一组失败是 broken reference。例子：

```text
The cow jumped over the moon.
It was rather pleased with itself.
```

如果第二句单独成为 chunk，`It` 的指代对象就丢失了。这就是 endophora 被切断。

第二组失败是 discourse relation 被切断。文档不是独立句子的列表，而是 claim、evidence、condition、concession、evaluation 的组合。只取一个看似相关的句子，可能会和全文结论相反。

医学例子：

```text
The drug reduced tumor volume by 40%.
However, the placebo group also improved.
Adjusted for baseline, the net effect was not clinically significant.
```

只检索第一句会让模型以为药物效果强；完整关系其实说明它没有达到临床显著。

第三组失败是 negation / scope trap。否定、条件、年龄范围、疾病条件和不确定性修饰都有作用范围。

```text
65 岁以下：没有显著证据显示风险升高
65-80 岁且有高血压：数据提示风险升高
```

如果只检索其中一句，系统要么过度报警，要么漏掉风险。真正的意思在两个条件之间的关系里。

### 3. Bridging inference 和 genre blindness

Bridging inference 是文本没有明说、但读者会靠场景推出来的关系。

```text
John walked into the room.
The chandelier was magnificent.
```

人类知道吊灯在房间里，因为 `room` 激活了空间场景。chunking 把两句切开后，第二句会丢掉这个场景。

Genre blindness 是把所有文体都当成同一种文本来切：

| 文体 | 为什么不能乱切 |
| --- | --- |
| 法律合同 | 定义、条件、例外可能隔很远 |
| 科学论文 | abstract、methods、results 互相预设 |
| 小说 | 反讽、铺垫和转折可能跨页成立 |
| 财报 / PDF | 表格、脚注、版面位置携带意义 |

所以 chunking strategy 必须由语料类型和查询任务决定。

### 4. Centroid delusion、query-chunk asymmetry 和标点问题

大而杂的 chunk 会变成平均意义：

```text
A: pricing
B: supply chain
C: customer support

chunk vector = average(A, B, C)
```

这个向量对很多 query 都有一点像，但不真正回答任何一个问题。这就是 centroid delusion，也可以理解成 centroid diffusion。

课堂边注还强调 query-chunk asymmetry：

```text
query: 短、尖锐、目标明确
chunk: 长、弥散、混合多个线索
```

短 query 匹配长 chunk 的平均点时，系统可能偏向内部一致的 chunk，而不是真正能回答问题的 chunk。

标点和小词也可能决定意思：

```text
Eats, shoots, and leaves.
Eats shoots and leaves.
A panda eats bamboo shoots and leaves.
```

人类知道第二句更接近熊猫吃竹笋和叶子；但一些 embedding 模型可能只看到词重合，忽略逗号造成的结构差异。

课堂脚本 `course/week_03/punctuation_embedding_test.py` 的实际结果：

| 模型 | cos(1,2) | cos(1,3) | cos(2,3) | 解释 |
| --- | ---: | ---: | ---: | --- |
| BERT anisotropic | 0.9041 | 0.7610 | 0.7908 | 三组都偏高，说明向量空间有 cone / anisotropy；它看出 2 比 1 更接近熊猫句，但 1 和 2 的词重合仍然最高 |
| MiniLM isotropic | 0.9231 | 0.4605 | 0.5065 | 能把熊猫句和逗号句拉远很多，但仍然把 1 和 2 判得最像，说明标点结构没有压过词面重合 |

这不是“模型完全失败”，而是一个更细的失败：

```text
模型能看到 topic / lexical relation
但没有充分看到 punctuation-controlled syntax
```

所以这个测试要拆成两个问题：

1. `cos(2,3) > cos(1,3)`：模型是否知道熊猫句更接近“吃 shoots/leaves”的无逗号句？
2. `cos(2,3) > cos(1,2)`：模型是否真的避开了标点陷阱，让语法结构压过词面重合？

这次 BERT 和 MiniLM 都通过第一个问题，但都没有通过第二个问题。

对法律、医学、监管和 Avaloka 安全规则来说，下面这些词和符号都可能改变结论：

```text
not
unless
except
however
if
only when
,
;
```

### 5. RAG is dead 的真正含义

今天看的 Jeff Huber / Chroma 和 Kuba Rogut / Turbopuffer 视频都不是说 retrieval 死了，而是说旧式 naive RAG 失败了。

失败的是：

```text
fixed chunk
-> vector search top-k
-> stuff everything into prompt
-> hope the LLM answers correctly
```

没有失败的是：

```text
retrieval
evidence
context engineering
agentic search
grounding
eval
```

更准确的方向是 agentic retrieval / context engineering：

```text
agent 判断自己需要什么
-> 使用 vector / full-text / regex / glob / metadata filters
-> 多轮搜索和改写 query
-> 裁剪噪声上下文
-> 把正确证据交给 reasoning model
```

其中一个很有用的说法是：

```text
Embeddings are cached compute.
```

Embedding 不是魔法，而是把未来会反复使用的语料预先理解、压缩并索引。是否值得做 embedding，取决于语料是否会被高频重复查询。

### 6. 当前 ChatGPT/Codex 是否在用 RAG

当前这个 Codex 对话不是自动对整个 Obsidian vault 做传统 RAG。

它更像：

```text
LLM
+ 当前对话上下文
+ agentic tool retrieval
+ 文件系统搜索 / PDF extraction / web lookup
```

也就是说，项目文件不会自动全部 embedding 后 top-k 注入。我需要判断需要什么，然后显式读取文件、PDF 或网页。这更接近 agentic retrieval，而不是固定内置 RAG。

### 7. Loop Engineer 和本项目的关系

AI Jason 的 Loop Engineer 视频讲的是另一层：不是“如何检索上下文”，而是“如何让 agent 反复工作并留下可继续的状态”。

基本循环：

```text
trigger
-> agent wakes up
-> reads shared memory / project context
-> investigates
-> does work
-> runs verification
-> logs result
-> next run continues from the log
```

本项目已经有这个雏形：

```text
tasks/
docs/
course/
traces/
evals/
docs/decisions/decision-log.md
```

后续可以把它发展成几个 loop：

| Loop | 作用 |
| --- | --- |
| weekly-course-loop | 每周课后读取讲义、课堂截图、视频，更新 week note 和任务 |
| avaloka-eval-loop | 定期跑 Avaloka eval，记录失败模式和 follow-up |
| memory-quality-loop | 检查 Care Card 的 permission、risk scope、staleness |
| rag-research-loop | 把新论文/视频转成 Avaloka 设计约束和 eval 问题 |

Loop Engineer 解决的是工作节奏和持续记忆；RAG / context engineering 解决的是每次工作时 agent 应该看到什么上下文。

## 所需证据、工具与评估

- **证据**：源文档、chunk 边界、上下文窗口、parent-child 关系、视觉页面、gold evidence。
- **工具**：semantic chunker、contextual chunking prompt、late chunking encoder、视觉文档 retriever、vector DB、reranker。
- **Trace**：chunking strategy、chunk size、boundary reason、context restoration、metadata、retrieved evidence、missed evidence、representation variant。
- **Eval**：Recall@k、MRR、NDCG@k、hard-negative rate、scope inversion error、definition orphan error、visual-table retrieval accuracy、answer grounding。

## 今日应能回答的问题

1. 为什么 chunking 不是普通预处理，而是本体论决策？
2. 为什么第一次 embedding 投影是不可逆的？
3. 为什么把多个正交思想放进一个 chunk 会制造噪声？
4. 既然 chunking 有损，为什么仍然需要 chunk？
5. 512-token 默认值的问题是什么？
6. Endophora、discourse relation、negation scope、definition-use chain 分别如何被 chunking 破坏？
7. 为什么 chunk 越小不一定越好？
8. 什么是 centroid delusion？
9. fixed、recursive、semantic、hierarchical chunking 各自解决什么、不能解决什么？
10. contextual chunking 和 late chunking 的差别是什么？
11. 什么文档适合 page-image retrieval？
12. 如何为 capstone 设计 representation tournament？

## 课堂问题

- 对纯文本为主但包含少量表格的企业文档，hybrid text + page-image retrieval 的最低可行实验应该怎么设计？
- 对需要权限和安全范围的记忆系统，chunk metadata 应该参与 embedding、filtering、reranking，还是只参与最终过滤？
- Late chunking 对长文档的最大上下文长度限制如何处理？是否需要先按章节做局部 late chunking？
- 如果 contextual chunking 用 LLM 补上下文，如何评估它没有引入原文没有的解释？
- Representation tournament 的 gold evidence 应该人工标注到 chunk、page、还是 source span？

## 后续行动

- ~~为 Week 03 创建一个 eval case：比较 fixed chunk、semantic chunk、contextual chunk 或 page-image retrieval 的证据召回。~~ 已完成，见 `evals/week03-representation-tournament/`。
- 接上 page-image 臂：在 Mac 上装好 lab 依赖后，给 `run_tournament.py` 加一个 CLIP/SigLIP2 encoder 类（接口只有 `build()` 和 `score()` 两个方法，下游全部已经和 unit 类型无关）。
- 修 abstention gate：term coverage 挡不住 W03-25 这类词面全覆盖但不可回答的 query，需要 answer-type 或 entailment 检查。
- 为 Avaloka Memory Reader V0 benchmark 增加 chunking/representation 维度。
- 在 capstone 计划里明确语料类型、用户问题、检索挑战、候选表示和成功指标。
- 课堂后补充本周实际代码、实验或 instructor 反馈。
