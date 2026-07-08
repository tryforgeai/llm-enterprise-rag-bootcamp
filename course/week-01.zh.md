# 第 01 周课堂笔记

[English Version](week-01.md)

## 课程概要

课程把企业级 RAG 介绍为一条完整的端到端流水线，而不是一组彼此孤立的技术：

```text
原始文档
-> 摄取
-> 检索
-> 增强
-> 可扩展架构
-> 安全与可信
-> 评估
-> 可衡量、可信的答案
```

这条流水线也在非结构化文档与结构化数据之间建立了一座桥梁。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/01-course-journey.png]]

## 核心概念

### 课程旅程：十四种工具，一条流水线

1. **基础**
   - 入门
   - 机器如何学习

2. **摄取**
   - 分块（Chunking）
   - 课件将分块称为“第一次不可逆切割”

3. **检索**
   - 检索流水线
   - 查询转换

4. **增强**
   - 衍生制品
   - RAPTOR
   - GraphRAG

5. **架构与速度**
   - 规模决定架构
   - 语义缓存

6. **安全与可信**
   - 请求护栏
   - 回应溯源

7. **证明与前沿**
   - 评估与指标
   - Text-to-SQL

### 初步理解

- RAG 的质量由整条流水线决定，不只由模型或向量数据库决定。
- 分块之所以被称为不可逆，是因为后续检索只能使用摄取时保留下来的结构。
- 可信回答既需要请求阶段的控制，也需要基于证据的回应。
- 评估是流水线的一部分，不是最后可有可无的检查。

### 什么是 RAG？

RAG 是 **Retrieval-Augmented Generation，检索增强生成**。

课程把它比喻为：在语言模型回答问题时，给它一本可以翻阅的书。系统不只依赖冻结在模型参数里的知识，而是在回答时从指定文档中检索相关材料，并把这些材料作为生成上下文。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/02-what-is-rag.png]]

最小流程：

```text
用户问题
-> 检索相关文档片段
-> 将问题和片段交给语言模型
-> 生成基于这些片段的答案
```

关键区别：

```text
模型训练
= 改变模型参数中存储的内容

RAG
= 在回答时提供外部证据
```

RAG 不会自动保证正确。系统仍可能检索错误片段、遗漏关键证据，或者生成检索上下文无法支持的主张。

### 为什么 RAG 不会消失

课程观点：

> 上下文窗口不是文件柜，而是一张书桌。你仍然需要图书馆。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/03-rag-will-not-die.png]]

解释：

- 上下文窗口是临时工作空间。
- 文档或知识系统是更大的图书馆。
- 即使上下文窗口很大，也不会自动选择最相关、最新、获授权且可信的证据。
- RAG 是图书馆与模型书桌之间的搜索、筛选和证据传递层。

```text
知识图书馆
-> 检索相关证据
-> 将选定证据放进上下文窗口
-> 推理并回答
```

课程的第一个可运行系统将是“语义搜索到回答”的闭环，也会解释什么情况下 RAG 在经济性上比微调更合适。

RAG 与微调的初步区别：

| 需求 | RAG | 微调 |
|---|---|---|
| 经常变化的事实 | 非常适合 | 反复更新成本高 |
| 来源归因 | 较容易保留 | 知识来源较不透明 |
| 私有文档访问 | 回答时按需检索 | 训练可能带来隐私与删除问题 |
| 改变行为或风格 | 能力有限 | 通常更适合 |
| 快速更新知识 | 重新建立索引 | 重新训练或继续训练 |

### 机器如何学习：Embedding 复习

这一模块从第一性原理理解 embedding 如何训练，以及“把意义变成几何”是什么意思。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/04-how-the-machine-learns.png]]

工作心智模型：

```text
文本或其他输入
-> embedding 模型
-> 数值向量
-> 高维空间中的位置
```

“把意义变成几何”是指：模型学习一个空间，让向量关系能够作为语义关系的信号：

- 相关项目通常应该更接近
- 不相关项目通常应该更远
- 方向和邻域可能编码有用模式

Embedding 不是意义本身，而是由模型和训练目标优化出来的数值表示。它的几何结构可能保留一些关系，同时丢失或扭曲另一些关系。

后续需要继续记录：

- 什么训练目标塑造了 embedding 空间？
- 什么构成正样本对和负样本对？
- 使用哪一种相似度或距离度量？
- 几何接近在什么情况下不等于人类理解的语义接近？
- 训练数据如何影响检索质量？

### 所有下游能力都依赖 Embedding 空间

Embedding 空间是多个下游技术的基础：

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/05-embedding-space-foundation.png]]

| 技术 | 对 embedding 几何的依赖 |
|---|---|
| 检索 | 相关查询与文档必须在选定的相似度下足够接近 |
| 重排序 | 候选排序依赖相关性信号是否被正确表示 |
| 语义缓存 | 相似请求必须足够接近，才可以安全复用结果 |
| 聚类 | 有意义的分组需要有效的邻域和边界 |

课程原则：

> 如果我们误读了几何结构，后面的技术就会变成猜测。

实践含义：不要仅仅因为某个 embedding 模型或阈值流行就采用它。需要测试邻域、误报、漏报以及具体领域中的表现。

### Chunking：第一次切割

分块将文档切成可以被 embedding、索引、检索并传给模型的单元。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/06-chunking-first-cut.png]]

这是流水线中最重要的决策之一，因为它定义了检索系统能够看到的信息单元：

```text
原始文档
-> 选择边界
-> 创建 chunks
-> embedding 并建立索引
```

主要权衡：

- chunk 太小，可能丢失上下文和关系
- chunk 太大，可能混合多个主题，降低检索精度并浪费上下文
- 边界不好，可能把主张与解释、限定条件、表格、标题或来源拆开
- overlap 可以保留连续性，但增加存储、重复检索和 token 成本

### 为什么第一次投影被称为不可逆

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/07-chunking-irreversible.png]]

课程原则：

> 如果索引中的 chunks 没有保留某些信息，任何 reranker、prompt 或更强模型都无法恢复它。

更准确的工程理解：

- 下游组件无法恢复当前索引中缺失的上下文。
- 如果保留了原始文档，可以重新处理并重新分块。
- 因此必须保留原始来源、分块配置、解析器版本和 provenance，以便重建摄取过程。

分块决定当前检索索引的上限。更好的 reranker 可以重新排列已有 chunks，却无法找回摄取时被破坏或遗漏的关系。

### 检索流水线

课程把检索描述成多阶段引擎，而不是一次向量搜索：

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/08-retrieval-pipeline.png]]

```text
查询
-> 稀疏检索：BM25 / SPLADE
-> 稠密检索：embedding 相似度
-> 融合候选集
-> 级联重排序
-> 最终证据
```

两条互补通道：

- **稀疏检索**保留姓名、ID、罕见术语和关键词等精确词法信号。
- **稠密检索**可以在查询和文档用词不同时发现语义相似性。

融合阶段追求较高召回率，之后由级联 reranker 对逐步缩小的候选集使用更仔细、通常也更昂贵的模型。

工作原则：

```text
早期阶段：快速、广泛
后期阶段：较慢、精确
```

### 单一 Retriever 永远不够

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/09-one-retriever-not-enough.png]]

关键词检索与语义检索的失败方式不同：

- 稀疏检索可能遗漏改写和概念匹配
- 稠密检索可能遗漏精确标识符、罕见术语、否定关系或严格词法约束

生产架构会组合两条通道，并且只有在预期质量收益值得时，才升级到昂贵评分。

这是召回率与精度之间的设计：

```text
多个 retriever
-> 多样化候选池
-> 融合与去重
-> 逐级增强评分
-> 小型最终证据集
```

### 成本感知的升级阶梯

课程比喻：

> 从地区法院到最高法院。便宜的 retriever 处理大多数案件，cross-encoder 只审理最困难的案件。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/10-retrieval-escalation-ladder.png]]

可能的四阶段模式：

```text
1. 稀疏与稠密检索：便宜、并行、高召回
2. 候选融合与去重
3. 轻量重排序或过滤
4. cross-encoder 重排序：昂贵、小型候选集
```

Cross-encoder 会把查询和候选一起评估，相关性判断通常比独立 embedding 后比较更强，但延迟和计算成本也更高。

升级策略应考虑：

- 查询难度或歧义
- 不同 retriever 是否意见不一致
- 候选之间的置信度差距
- 安全或业务重要性
- 延迟与成本预算

### Query Transformation：翻译器

查询转换是一条分阶段流水线，把用户混乱或含糊的问题改写为 retriever 能回答的一个或多个查询。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/11-query-transformation.png]]

```text
用户原始问题
-> 理解意图和上下文
-> 澄清、规范化、拆解或扩展
-> 生成检索查询
-> 执行检索
```

可能的操作：

- 消解代词或对话中的指代
- 规范缩写、名称和术语
- 把用户语言转换为领域词汇
- 把多部分问题拆成多个子查询
- 生成多个查询变体
- 加入时间、产品、来源或司法辖区等约束

重要区别：

- **查询转换**改变搜索请求，以改善证据检索。
- **回应生成**在证据取回之后回答用户。

转换必须保留用户意图。一个流畅但改变了问题含义的改写，可能检索到看似可信却无关的证据。

建议 trace 字段：

```text
original_query
interpreted_intent
transformed_queries
transformation_reason
retrieval_results_per_query
```

Retriever 只能看到翻译层允许通过的问题版本，因此查询转换是检索控制点，不是无害的预处理。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/12-query-transformation-six-stage.png]]

课程将构建六阶段查询流水线：

1. **纠错**
   - 修复拼写、畸形文本和明显输入噪声。
2. **注入上下文**
   - 加入相关对话或应用上下文。
3. **扩展术语**
   - 展开缩写，并把用户语言映射到领域术语。
4. **改写**
   - 生成更适合检索的清晰查询。
5. **多跳拆解**
   - 拆分需要多个事实或推理步骤的问题。
6. **HyDE**
   - 生成一个假设答案或文档，对其做 embedding，再检索与该假设表示相似的真实文档。

每个阶段都可能改善检索，也可能引入意图漂移。Trace 应保存每个已执行阶段的输入和输出。

### Derivative Artifacts：棱镜

衍生制品是从原始材料生成、面向搜索的精炼视图，可以与原文一起建立索引，也可以在特定场景替代原文索引。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/13-derivative-artifacts.png]]

课程示例：

- 原子事实
- 搜索友好的改写
- 问答对
- 摘要

```text
源文档
-> 生成多个可检索视图
-> 每个制品链接回来源
-> 索引原文和/或衍生视图
```

可能带来的帮助：

- 用户问题可能更像生成的问答对，而不像原始散文
- 摘要支持更高层级检索
- 原子事实暴露单独主张
- 搜索友好改写可以跨越难懂表达

可信要求：衍生制品是生成式解释，不是一级证据。每个制品都应保存来源、类型、生成器及版本，并能回到原始文本。

### 为什么多种表示有帮助

用户会用很多不同形式提出语义相关的问题。文档的单一表示通常只能很好地匹配其中一部分。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/14-derivative-artifacts-many-shapes.png]]

对于同一段来源，索引可以包含：

```text
原始片段
+ 简短摘要
+ 原子事实
+ 可能的用户问题
+ 搜索友好改写
```

这些表示创建了多个返回同一来源的语义入口，当用户表达更接近生成问题或摘要而不是原文时，可以提高召回。

成本和风险：

- 索引变大，摄取成本增加
- 同一来源可能出现重复候选
- 生成内容可能出错或丢失限定条件
- 误导性的制品可能提高相似度，却降低事实可靠性

必要控制：

- 同一来源的所有表示共享 source ID
- 按来源去重或聚合候选
- 最终 grounding 前重新评分原始片段
- 对比召回增益与索引大小、延迟和误报率

### RAPTOR：可调节的检索分辨率

RAPTOR 是 **Recursive Abstractive Processing for Tree-Organized Retrieval**。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/15-raptor-adjustable-focal-length.png]]

平面索引只存储大致同一细节层级的 chunks。RAPTOR 递归聚类相关 chunks 并生成摘要，形成包含多个抽象层级的树。

```text
详细源 chunks
-> embedding 并聚类相关 chunks
-> 为每个 cluster 生成摘要
-> 对摘要继续 embedding 和聚类
-> 重复形成更高层摘要
-> 从适合的树层级检索
```

这棵树像可调焦镜头：

- 窄而具体的问题 -> 取回叶子 chunks
- 章节级问题 -> 取回中间摘要
- 宽泛主题问题 -> 取回高层摘要
- 复杂问题 -> 组合多个层级的证据

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/16-raptor-zoom-lens.png]]

讲师的检索尺度比喻：

| 技术 | 镜头 | 更适合 |
|---|---|---|
| Factoids / 衍生制品 | 显微镜 | 独立事实、实体、数值和精确细节 |
| RAPTOR | 变焦镜头 | 在原始细节与层次摘要之间移动 |
| GraphRAG | 望远镜 | 跨语料关系、社区、模式与主题 |

这些技术是互补关系，不是直接替代。选择取决于问题需要的分辨率和结构。

```text
“使用了哪个精确阈值？”
-> 详细 chunk

“这份文档的整体安全策略是什么？”
-> 高层摘要 + 支持性 chunks
```

风险和成本：

- 摘要可能遗漏限定条件或引入错误
- 构建树增加摄取成本
- 源文档变化后可能需要更新树
- 高层摘要仍必须链接回支持它的源 chunks
- 并非所有语料都值得增加这种复杂度

### GraphRAG：理解整个语料库

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/17-graphrag-telescope.png]]

GraphRAG 把非结构化文本转换成知识图谱，并利用图结构支持检索：

```text
文档
-> 抽取实体、关系和主张
-> 构建知识图谱
-> 发现相关社区
-> 为社区生成摘要
-> 回答局部或全局问题
```

基础向量检索寻找与查询相似的 chunks；GraphRAG 则可以围绕相互连接的实体和社区组织证据。

适用问题：

- 局部：“组织 X 与项目 Y 有哪些关系？”
- 多跳：“人物 A 如何间接连接到政策 B？”
- 全局：“整个语料库中有哪些主要主题和群体？”
- 综合理解：“哪些社区意见不同？什么证据解释了分歧？”

讲师把它称为望远镜，因为它帮助系统看到分布在很多文档中的结构和主题，而不是只检查一个匹配片段。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/18-graphrag-whole-corpus-structure.png]]

RAPTOR 与 GraphRAG 的选择：

| 需求 | 优先考虑 |
|---|---|
| 以不同抽象层级检索同一材料 | RAPTOR |
| 总结章节或整篇长文档 | RAPTOR |
| 跟踪实体之间的关系 | GraphRAG |
| 发现社区、网络或全局主题 | GraphRAG |
| 同时需要层次和关系 | 评估后有选择地组合 |

决定性问题是缺失的信号属于**分辨率**还是**结构**：

```text
分辨率问题 -> RAPTOR
关系 / 语料结构问题 -> GraphRAG
```

#### 与 SAGE 的关系

论文 [SAGE: A Framework of Precise Retrieval for RAG](https://arxiv.org/abs/2503.01713) 主要提升传统 chunk + vector 检索流水线的精度。

项目长期笔记：[SAGE 论文笔记](../resources/papers/2503.01713-sage.md)

```text
语义分块
-> 向量检索与 reranking
-> 在相关性分数明显下降处动态截断
-> LLM 反馈判断上下文应该增加还是减少
```

SAGE 与 GraphRAG 解决不同问题：

| 框架 | 主要问题 |
|---|---|
| SAGE | 检索语义完整的 chunks，减少上下文遗漏和噪声 |
| GraphRAG | 对实体、关系、社区和全局结构进行推理 |

两者可能互补。SAGE 式语义切分可以改善图谱抽取前的文本单元，其自适应选择和反馈思想也可能改善部分局部检索路径；GraphRAG 仍负责图构建和社区级推理。

证据边界：SAGE 论文引用了 GraphRAG，但没有提供两者的直接对比实验。论文报告的比较包括 RAPTOR，不包括 GraphRAG。因此组合两者只是架构推断，需要独立评估。

GraphRAG 的风险和成本：

- 实体和关系抽取可能不完整或错误
- 图构建和社区摘要成本较高
- 文档变化需要维护图结构
- 生成关系和社区报告需要追溯到源文本
- 如果问题主要是简单事实查询，GraphRAG 没有必要

### 规模决定架构

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/19-scale-decides-architecture.png]]

架构应由已证明的问题形态和规模决定。每个额外组件都必须用可衡量的改善证明其成本合理。

```text
从最小完整系统开始
-> 在 traces 和 evals 中观察失败
-> 分类失败
-> 添加专门处理该失败的组件
-> 验证该组件是否真正改善结果
```

示例升级逻辑：

| 观察到的失败 | 候选措施 |
|---|---|
| 检索不到相关事实 | 改善分块、embedding 或混合检索 |
| 上下文过多或过少 | 自适应选择或 SAGE 式反馈 |
| 问题需要不同摘要层级 | RAPTOR |
| 问题需要关系或全局结构 | GraphRAG |
| 证据很好但行为仍系统性错误 | 先考虑 prompt、工具、策略逻辑，再考虑微调 |

该原则防止团队因为技术流行而选择架构。复杂度必须通过具体领域 eval 证明自己。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/20-architecture-inundation.png]]

讲师将其关联到伽利略的平方立方定律：在某一规模有效的设计，换到另一规模可能失败，因为成本与约束不会以同一速度增长。

实践规则不是一开始就为最大规模设计，而是先建立简单、可测量的 baseline，再根据证据升级。

添加组件前要求：

1. traces 或 evals 中存在已观察到的失败
2. 明确该组件要改善的指标
3. 估计延迟、token、维护与隐私成本
4. 与当前 baseline 比较
5. 如果没有出现预期改善，定义移除标准

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/21-shapley-style-component-test.png]]

讲师提出 Shapley-style 组件价值测试。工程上可理解为消融实验和边际贡献纪律：

```text
测量 baseline
-> 增加一个组件
-> 用相同 eval 集重跑
-> 移除或禁用组件
-> 比较质量和成本差异
-> 只有边际价值值得边际成本时才保留
```

建议的组件评分表：

| 指标 | Baseline | 加入组件后 | 差值 |
|---|---|---|---|
| 检索 recall / precision | | | |
| grounded answer quality | | | |
| 安全失败 | | | |
| p50 / p95 latency | | | |
| 输入与输出 tokens | | | |
| 基础设施成本 | | | |
| 维护和调试负担 | | | |

当组件相互作用时，应在可行范围内测试不同顺序或组合。某个组件单独价值不大，但与另一个组件组合时可能有意义。早期产品通常不需要精确计算 Shapley value。

### Semantic Cache

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/22-semantic-cache.png]]

语义缓存会在新查询与历史查询意义足够相似时复用工作，即使用词不同。

```text
新查询
-> 创建 embedding
-> 搜索已缓存查询的 embeddings
-> 验证相似度和缓存范围
-> 命中：复用检索结果或回答
-> 未命中：运行完整流水线并保存符合条件的结果
```

两种缓存层级：

| 缓存层级 | 复用内容 | 主要权衡 |
|---|---|---|
| 检索缓存 | 证据 ID 或排序结果 | 更安全，但证据可能过时 |
| 回应缓存 | 最终生成答案 | 更快更便宜，但更容易复用不合适或过时的答案 |

正确性不能只依赖 embedding 阈值，还可能需要：

- tenant 或用户范围
- 知识索引版本
- prompt 和模型版本
- 安全策略版本
- locale 和回应模式
- 权限与 memory scope
- TTL 和失效规则

Avaloka 边界：不能跨用户语义复用个性化回答。涉及私有记忆、情绪状态、危机风险、健康背景或变化中用户情况的回答，应绕过共享回应缓存。需要缓存时，应先从公共、稳定知识的检索缓存开始。

讲师提出成熟工作负载可能约有 90% 查询由缓存服务。应把它视为需要测量的工作负载假设，而不是普遍常数。

如果命中率确实如此高，架构会发生根本变化：

```text
语义缓存 = 主要服务路径
完整检索和生成 = 填充缓存 / fallback 路径
```

影响：

- 平均延迟和推理成本显著降低
- 模型能力集中处理新问题或变化问题
- 缓存质量决定多数用户体验
- 错误语义命中会反复传播同一错误答案
- 知识、prompt、模型或策略更新后，旧缓存可能继续存在
- 失效、版本控制、可观察性和预热成为核心架构
- 命中与未命中流量必须分别评估和监控

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/23-semantic-cache-playing-with-fire.png]]

课程实现目标包括：

1. 领域微调的 embedding 模型
2. 根据 precision 与 recall 调整的相似度阈值
3. 针对五种语义缓存失败模式的保护

这里的微调针对判断查询等价性的 embedder，不一定针对回答模型。

阈值存在非对称权衡：

```text
降低阈值
-> 命中率和节省增加
-> 错误语义匹配增加

提高阈值
-> 错误匹配减少
-> 未命中和完整流水线成本增加
```

敏感应用应根据错误命中的代价优化阈值，而不是只追求命中率。课件尚未给出五类失败模式的确切定义，应等待讲师定义，不自行编造。

需要评估：

- cache hit rate
- false-hit rate
- 语义匹配的 answer-equivalence rate
- 延迟与 token 节省
- stale-answer rate
- 跨用户或权限泄漏
- 绕过安全策略的情况
- 命中与未命中质量

### 请求护栏

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/24-request-guardrails.png]]

请求护栏是模型之前的门卫。课程目标是构建一条十六道 gate 的输入流水线，在请求到达模型推理前进行检查。

护栏目标是 **Helpful、Harmless、Honest（有帮助、无伤害、诚实）**：

| 原则 | 操作含义 |
|---|---|
| Helpful | 回应用户的合理意图并提供有用下一步 |
| Harmless | 避免可预防伤害、不安全行为、隐私侵犯和有害升级 |
| Honest | 用证据支持事实主张，说明不确定性和限制，不伪造信心 |

三者需要平衡：有帮助不能凌驾于安全，无伤害不应依赖欺骗，诚实也包括承认不知道。

```text
进入的请求
-> 有顺序的护栏检查
-> 阻止、净化、约束、路由或批准
-> 只有批准后的请求才能进入检索与模型
```

生成前护栏的价值：

- 提前拒绝禁止或危险请求
- 防止 prompt injection 到达工具或私有检索
- 执行身份、权限、tenant 和 memory 边界
- 分类风险并为高风险请求使用不同路由
- 避免不必要的模型与检索成本
- 保存哪一道 gate 作出决策的 trace

隐私敏感系统中，部分 gate 必须在检索用户记忆之前执行。事后拒绝不能撤销已经发生的不必要私有数据访问。

课件尚未展示确切的十六道 gates，应记录讲师实际顺序，而不是自行替代。

建议 trace 字段：

- request ID 和 policy version
- gate 名称与顺序
- pass、block、transform 或 route 结果
- reason code 和 confidence
- gate 使用的脱敏证据
- 最终 route，以及是否执行了检索和模型

### 回应溯源

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/25-response-grounding.png]]

流畅且自信的回答仍可能没有证据支持。生成器不应成为自己回答是否 grounded 的唯一裁判。

```text
生成答案
-> 抽取事实主张
-> 将每个主张映射到检索证据
-> 验证蕴含关系、来源和新鲜度
-> 通过、修改、再次检索、加限定或拒绝
-> 只发布 grounded 回应
```

Grounding 检查应区分：

- 直接有证据支持的主张
- 合理但需要明确标记的推断
- 无支持主张
- 被证据反驳的主张
- 需要更新或更权威证据的主张

验证器需要与生成过程有实质分离，例如独立证据检查、不同 prompt 或模型、确定性规则、引用或外部 evaluator。仅使用另一个 LLM 并不保证独立。

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/26-assertion-evidence-graph.png]]

课程实现目标：

- 三层验证层次
- assertion-evidence graph
- 在最高层使用 LLM-as-judge

Assertion-evidence graph 把回应表示为可审计结构：

```text
assertion node
-> supported_by -> 来源片段
-> derived_from -> 获允许的记忆或制品
-> contradicted_by -> 冲突证据
-> verification_status -> supported / inferred / unsupported / contradicted
```

每个事实主张必须指向证据，否则不允许离开系统。这样可以按句子或主张修改，而不是把整份回答当成一个整体接受或拒绝。

回应溯源主要执行 HHH 中的 **Honest**；请求护栏和安全路由支持 **Harmless**；系统仍要保持 **Helpful**，在不能满足原请求时提供合适替代方案或下一步。

验证层次应把昂贵、概率性的判断留给简单检查无法解决的情况。课件尚未给出三层的确切定义，应等待讲师规范。

建议指标：

- claim-level support rate
- citation correctness 与 completeness
- contradiction rate
- unsupported-claim rate
- appropriate abstention rate
- 因 grounding 触发的重试和升级率

### 评估与指标

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/27-evaluation-and-metrics.png]]

RAG 系统需要分别衡量检索与生成答案。好的答案分数无法诊断检索失败，好的检索分数也不能保证回答 grounded。

检索指标：

| 指标 | 重点 |
|---|---|
| MRR | 第一个相关结果出现得有多早 |
| MAP | 对包含相关结果的排序位置计算 precision，再跨查询平均 |
| NDCG | 允许多级相关性，并对高排名结果给予更高权重 |

回答与 RAG 流水线指标：

| 指标 / 框架 | 重点 |
|---|---|
| RAGAS | 自动评估上下文相关性、faithfulness、答案相关性等维度 |
| FActScore | 把文本拆成原子事实，衡量其中有多少得到可靠来源支持 |

评估应沿流水线展开：

```text
检索
-> 排序指标
-> 上下文质量
-> 主张 grounding 与事实性
-> 回答有用性
-> 安全和运营指标
```

Agent-first 系统还应衡量：

- 是否选择正确下一步行动
- 记忆访问是否遵守 scope 与 permission
- 回应是否 Helpful、Harmless、Honest
- 系统是否在适当时提问、放弃回答、拒绝或升级
- 延迟、token 成本、缓存行为与重试率

在检查单项失败信号之前，不要把所有维度压缩为一个总分。

### Text-to-SQL：结构化数据桥梁

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/28-text-to-sql.png]]

Text-to-SQL 将证据访问从非结构化文档扩展到结构化数据库：

```text
自然语言问题
-> 识别意图和允许的数据范围
-> 检索相关 schema 和业务定义
-> 生成 SQL
-> 验证权限、语法和 query plan
-> 在受约束的只读环境中执行
-> 基于返回行生成回答
```

它与 RAG 相关，因为系统必须先检索 schema、表关系、指标定义和示例查询，才能生成有用 SQL。

必要控制：

- 默认使用只读数据库凭据
- table、column、row 和 tenant 权限
- 尽可能使用 allowlist 操作和查询模板
- 参数化与注入防护
- 查询复杂度、超时和结果大小限制
- 执行前进行 SQL 解析或 dry-run
- 保存问题、SQL、结果与答案之间的审计日志
- 任何具有写能力的操作都必须明确确认

Text-to-SQL 评估应包含执行正确性、结果正确性、权限合规、效率，以及最终自然语言回答是否忠实表达返回数据。

### 课程最终目标

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/29-course-outcome.png]]

课程提出的三个月结果是形成检索架构判断力：

```text
知道应该构建什么
+ 知道规模需要多少架构
+ 知道如何证明它有效
```

对本项目而言，就是以 Avaloka 已有能力为 baseline，加入可观察性，评估真实失败，并且只在证据支持时升级架构。

## 代码与实验笔记

来源记录：

- [2026-06-06 共享课程记录](sources/2026-06-06-shared-chat-record.md)

### 使用 SentenceTransformers 进行文本语义搜索

共享记录中的教学项目是 SupportVectors 的 `rag_to_riches`，用于快速学习基础 RAG 检索路径。

实验先对语料做 embedding：

```python
embeddings = embedder.encode(sentences, convert_to_tensor=True)
```

然后对查询做 embedding 并执行语义搜索：

```python
query_text = "a friendship with animals"
query = embedder.encode(query_text, convert_to_tensor=True)

from sentence_transformers import util

search_results = util.semantic_search(
    query_embeddings=query,
    corpus_embeddings=embeddings,
    top_k=3,
)
```

概念流程：

```text
查询文本
-> 查询 embedding
-> 与语料 embeddings 比较
-> 按向量相似度排序
-> 返回 top-k corpus IDs 和分数
-> 查找原始来源文本
```

`corpus_id` 标识 `sentences` 中的原始项目。相关性分数表示查询与语料项目在该 embedding 模型相似度函数下有多接近。

关键区别：

```text
关键词搜索 -> 匹配词法形式
语义搜索 -> 匹配学习得到的表示相似性
```

语义相似性是概率性的。高分不代表结果一定正确、获允许、最新或可以安全使用。

### 使用 CLIP 进行图片搜索

后续实验使用以下模型为图片建立 embedding 索引：

```python
model = SentenceTransformer("clip-ViT-B-32")
```

CLIP 把文本和图片放进可比较的 embedding 空间：

```text
图片 -> 图片 embeddings
文本查询 -> 文本 embedding
-> 跨模态比较
-> 检索语义相关图片
```

图片索引在概念上是：

```text
图片文件名 + 图片 embedding
```

课程示例可以复用预计算图片 embeddings，因为图片 embedding 的成本高于加载已有向量。这属于 embedding 计算缓存，不是语义回答缓存。

### 实验证据边界

共享对话中还有关于 hallucination、机密和不可见信息、历史索引、向量语言、embedding 变体以及 Jabber 文本示例的图片课件或 notebook 截图。来源笔记已记录标题，但精确内容仍需从原始录像或 notebook 恢复。

## 解锁的 Agent 能力

Agent 可以把知识访问当作一条可测量的流水线：

```text
摄取 -> 检索 -> 增强 -> 决策 -> 护栏 -> 溯源 -> 评估
```

这让 Agent 获得的不只是检索，而是查询转换、证据选择、安全边界和质量测量能力。

Embedding 让 Agent 可以进行语义查找：即使查询与来源用词不同，也能找到相关项目。但这种能力是概率性的，必须使用领域样本评估。

因为检索、reranking、缓存和聚类都依赖 embedding 空间，所以 embedding 评估是基础级 Agent eval，不只是底层实现细节。

多模态 embedding 把查找扩展到不同数据类型。当文本与图片共享学习得到的向量空间时，Agent 可以用文本检索图片，但相似度搜索后仍必须执行权限、敏感性、provenance 和 grounding 规则。

Chunking 决定 Agent 能否检索到某项证据。混合检索通过组合精确匹配和语义信号改善召回，reranking 则改善最终进入推理步骤的证据质量。

成本感知检索阶梯让 Agent 只为不确定或高风险案例使用昂贵判断，而不是对每个查询支付最高成本。

查询转换是人类语言与检索系统语言之间的翻译层。当歧义无法安全解决时，Agent 应要求澄清，而不是默默创造用户意图。

衍生制品为同一来源提供多个检索入口，可以提高召回；但最终回答应基于原始或已验证来源，而不是把生成摘要或问答对当作无条件真相。

RAPTOR 让 Agent 可以进行多分辨率检索，根据问题选择精确细节或高层综合。

## 所需证据、记忆、工具与评估

- **证据**：源文档、chunks、检索片段和 grounding 引用
- **记忆**：尚未定义；记忆必须遵循独立的 scope 与隐私规则
- **工具**：embedding 模型、摄取流水线、retriever、query transformer、cache、guardrails 和 evaluator
- **评估**：embedding 邻域质量、检索质量、grounding、安全、延迟和端到端答案质量

## 问题清单

- 为什么 chunking 被称为第一次不可逆切割？
- 七个流水线阶段中的十四种工具分别是什么？
- 系统达到什么规模时需要改变架构？
- 如何把请求护栏与回应溯源分开评估？
- 为什么 Text-to-SQL 与评估和前沿主题放在一起？
- 当检索找不到可靠证据时，RAG 系统应如何行动？
- 如何衡量生成答案是否真正基于检索片段？
- 语料规模或上下文长度达到什么程度时，检索比发送全部文档更经济？
- 哪些问题应该使用 RAG、微调或两者结合？
- 课堂 embedding 模型的具体训练目标是什么？
- 为什么向量之间的距离或角度可以表示语义相似度？
- 把意义压缩到固定大小向量时会丢失什么？
- 信任检索前，应该如何检查 embedding 邻域？
- 检索、缓存和聚类是否应使用同一 embedding 模型和阈值？
- 如何发现 embedding 空间在专业领域中表现不佳？
- 讲师比较的三种 embedding 变体是什么？分别适合什么任务？
- `rag_to_riches` 文本实验使用哪个 embedding 模型和相似度函数？
- 该 notebook 中 `util.semantic_search` 是否自动归一化向量或选择 cosine similarity？
- 当文本与图片只松散相关时，如何评估多模态检索？
- 图片被 embedding 和索引后，哪些 metadata 与隐私规则必须保留？
- 课程将使用哪一种 chunking baseline？
- 如何评估 chunk size 和 overlap，而不是凭感觉设置？
- 如何融合 sparse 与 dense 结果？
- 每个阶段使用什么 reranker？延迟与成本是多少？
- 什么指标决定 retrieval funnel 是否改善质量？
- 系统如何判断查询困难到需要 cross-encoder？
- 每个阶段前后保留多少候选？
- 如何联合评估延迟、成本、recall 与 precision？
- 哪些查询转换是确定性的，哪些使用 LLM？
- 如何评估转换后的查询是否保留用户意图？
- 何时应该澄清，而不是自动改写？
- 是否应把每个转换查询及其结果保存到 trace？
- 六个转换阶段中的哪些阶段可以跳过检索？
- 当 HyDE 的假设答案包含错误假设时，如何评估？
- 衍生制品与原始 chunks 是否进入同一索引？
- 如何防止生成的 factoids 和摘要成为错误证据？
- 每个来源生成多少种表示时，召回收益才不会被重复伤害抵消？
- Reranking 应评分衍生制品、原始来源还是两者？
- RAPTOR 如何选择要检索的抽象层级？
- 课程使用树遍历，还是搜索所有树节点？
- 如何发现摘要错误并追溯到源 chunks？
- 什么 eval 能证明 RAPTOR 优于简单 chunk + reranker？

## Avaloka 应用

Avaloka 不应把记忆检索简化成一次向量搜索。未来知识路径应作为完整流水线设计：

```text
获批准的来源或记忆
-> 隐私感知摄取
-> 检索与查询转换
-> 加入 care 与 safety 上下文
-> 有边界的下一步决策
-> 请求与回应护栏
-> grounded 回应
-> trace 与 eval
```

最直接的教训是：Avaloka 的安全、检索和评估层必须一起设计。

RAG 可以为 Avaloka 提供一本获批准的“开放书籍”，包含产品知识、照护原则、安全规则和经过筛选的用户安全记忆。但模型不能把每个检索项都当作向用户暴露它的许可；检索权限与回应披露权限是两次不同决策。

文本语义搜索实验是 Avaloka 检索路径的最小原型：

```text
获批准的文档或记忆
-> embeddings
-> query embedding
-> top-k 检索
-> 查找原始证据
```

Avaloka 必须在教学骨架上增加：

```text
语义搜索
-> 权限和 memory-scope filter
-> sensitivity filter
-> reranker
-> grounding check
-> HHH guardian
-> trace 与 eval
```

未来的多模态路径中，图片和截图可能包含私有或敏感证据。图片相似度绝不能绕过授权、provenance、retention 和回应披露规则。

书桌与图书馆比喻同样适用于 Avaloka：

- context window：当前放在桌面上的少量证据
- 知识库和获批准的记忆库：图书馆
- retrieval policy：决定哪些材料可以拿到桌面的图书管理员
- response guardrail：决定哪些内容可以对用户说的规则

## 后续任务

- 记录讲师对 chunking 为什么不可逆的解释。
- 随课程推进，把十四种工具映射到七个课程阶段。
- 评估模块讲解后补充具体指标。
- 构建基础模块展示的 semantic-search-to-answer loop。
- 记录讲师对 RAG 与微调的成本比较。
- 选择生产 embedding 模型前，创建一个小型 Avaloka embedding 邻域测试。
- 复现 `rag_to_riches` 文本语义搜索实验，保存环境、模型名、语料、查询和排序输出。
- 从 notebook 或录像恢复讲师的三种 embedding 类别。
- 创建包含相关、模糊和敏感图片案例的小型 CLIP text-to-image eval。
- 保存 Avaloka 原始来源和摄取 metadata，以便重新 chunk。
- 在同一组 Avaloka eval 问题上比较 sparse-only、dense-only 和 hybrid retrieval。
- 将安全敏感或低置信度检索升级到更强 reranker。
- 在 Avaloka retrieval traces 中加入原始查询和转换查询字段。
- 保持每个衍生制品与获批准来源的链接，绝不把它作为原始用户记忆暴露。
- 评估问题式制品能否改善检索且不增加 unsupported claims。
- 在简单检索处理不了宽泛问题且 traces 证明存在多分辨率需求之前，延后 RAPTOR。

## 下午基础：Transformer 内部机制与 LARQL 准备

来源记录：

- [2026-06-06 下午 Transformer 与 LARQL 记录](sources/2026-06-06-afternoon-transformer-larql-record.md)

### Hugging Face 访问经验

下午配置工作区分了三个不同问题：

```text
CLI 身份认证
!= TLS 证书信任
!= gated model 仓库授权
```

- `hf auth login` 使用 Hugging Face token 对本地 CLI 认证。
- `CERTIFICATE_VERIFY_FAILED` 来自本地 Python 证书链和企业代理证书，不代表 token 无效。
- 即使登录成功，也不自动获得 `google/gemma-3-4b-it` 权限；账户需要单独接受或获得 gated Gemma 仓库访问权。

常用命令：

```bash
hf auth login
hf auth whoami
hf download google/gemma-3-4b-it
```

不要在本项目中保存 access token。

### Transformer Block 心智模型

The Illustrated Transformer 提供了可视化基础：

- Query：当前 token 在寻找什么
- Key：每个可用 token 提供什么匹配信号
- Value：从匹配 token 中取回的信息
- causal mask：防止当前生成 token 看到未来位置
- multi-head attention：并行学习多种关系视角
- residual stream：在层之间携带并积累贡献
- MLP/FFN：转换每个 token 位置并写入学习到的 features

简化数据流：

```text
token representation
-> causal multi-head self-attention
-> 将 attention contribution 加入 residual stream
-> MLP / FFN feature transformation
-> 将 FFN contribution 加入 residual stream
-> 下一个 Transformer block
```

核心公式：

```text
A = softmax(QK^T / sqrt(d_k))
Z = AV
x' = x + Attention(x)
x'' = x' + MLP(x')
```

第一层近似理解：

```text
attention -> 在 token 位置之间交换信息
MLP / FFN -> 转换并写入 features
residual stream -> 保存持续演化的共享状态
```

### 为什么这对 LARQL 重要

LARQL 研究的是模型内部 features 与输出行为之间的路径：

```text
attention contribution
+ FFN contribution
-> residual-stream trajectory
-> output-token ranking
```

只读命令提供不同视角：

- `DESCRIBE`：推断出的 feature associations
- `WALK`：在 feature neighborhoods 中移动
- `TRACE`：答案轨迹和各层贡献
- `INFER`：实际 next-token behavior

由此产生一个重要的证伪问题：

> 浏览命令报告的内部关联，是否与模型在推理、改写、否定和歧义上下文中的真实行为一致？

内部 trace 可以解释或诊断模型行为，但不能证明事实是最新的、具有来源 provenance，或允许向用户披露。

### 解锁的 Agent 能力

Agent 可以获得第二类 trace：

```text
外部 trace
-> 检索证据、决策、安全检查、答案

内部研究 trace
-> 层轨迹、attention/FFN contribution、token preference
```

对 Avaloka 而言，内部 tracing 未来可能帮助调查不安全关联或过度自信语言。生产行为仍应以外部 grounding、Care Card permissions 和 HHH review 为权威。

### 后续行动

- 完成一个受支持小模型的 Hugging Face 访问批准。
- 深入实施 LARQL 前先阅读 The Illustrated Transformer。
- 在 T009 中继续保持只读边界。
- 用公共或合成案例比较 `DESCRIBE`、`WALK`、`TRACE` 和 `INFER`。
- 绝不把 Hugging Face tokens 或私有 Avaloka memory 写入课程文件或模型 patches。
