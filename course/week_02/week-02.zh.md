# 第 02 周课堂笔记

日期：2026-06-13

状态：课堂进行中

来源：课堂讲义照片 `IMG_0498.jpg`、`IMG_0499.jpg`、`IMG_0500.jpg`、`IMG_0501.jpg`

## 一句话总结

本周从概率论和 Transformer 内部机制出发，解释机器如何把离散语言变成连续向量、如何用 Attention 生成上下文语义，以及为什么这些向量最终能够支持文本和图片检索。

```text
概率分数
-> softmax 概率分布
-> 负对数似然训练
-> attention 上下文混合
-> 每个 token 的上下文向量
-> pooling 得到 chunk embedding
-> 对比学习改善向量空间
-> 在共享语义空间中检索文本与图片
```

## 核心概念

### 1. Softmax：把任意分数变成概率分布

对分数 \(z_i\)，softmax 为：

\[
p_i = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}
\]

- 指数函数让所有结果为正，并放大分数差异。
- 分母执行归一化，使全部概率之和为 1。
- softmax 不只是选出最大项，而是在多个候选之间分配一单位的概率质量。

温度 \(T\) 控制分布的锐利程度：

- \(T \to 0\)：分布趋近 argmax，接近硬选择。
- \(T \to \infty\)：分布趋近均匀，选择变得平缓。
- 较低温度更确定，较高温度保留更多候选。

实际计算时通常使用数值稳定版本：

\[
\operatorname{softmax}(z)_i
=
\frac{\exp(z_i-\max_j z_j)}
{\sum_k \exp(z_k-\max_j z_j)}
\]

减去最大值不会改变最终概率，但能降低指数溢出的风险。

### 2. Surprise 与负对数似然

一个结果的“惊讶度”定义为：

\[
I(x) = -\log p(x)
\]

- 高概率事件的惊讶度低。
- 当 \(p=1\) 时，惊讶度为 0。
- 低概率事件产生较大的训练惩罚。

序列的 likelihood 是多个 token 概率的乘积。取对数后，乘积变成求和：

\[
-\log \prod_t p(x_t \mid x_{<t})
=
-\sum_t \log p(x_t \mid x_{<t})
\]

这就是 negative log-likelihood。对数让训练目标具有可加性，也避免大量小概率相乘造成浮点下溢。

### 3. Entropy、Cross-Entropy 与 Perplexity

Entropy 衡量一个概率分布本身的不确定性：

\[
H(p)=-\sum_i p_i\log p_i
\]

Cross-entropy 衡量真实分布 \(p\) 与模型分布 \(q\) 之间的预测代价：

\[
H(p,q)=-\sum_i p_i\log q_i
\]

如果标签是 one-hot，cross-entropy 就等于正确类别的 negative log-likelihood。

Perplexity 是平均不确定性的指数形式。对数以 2 为底时：

\[
\operatorname{PPL}=2^H
\]

如果使用自然对数，则对应 \(\operatorname{PPL}=e^H\)。数值越低，表示模型平均需要在越少的有效候选之间犹豫，但低 perplexity 不自动代表事实正确、安全或适合检索。

Softmax 与 cross-entropy 组合后，对 logit 的梯度有一个简洁形式：

\[
\frac{\partial \mathcal{L}}{\partial z}=p-y
\]

直觉上，训练会把预测概率 \(p\) 推向真实标签 \(y\)。

### 4. Maximum Likelihood Estimation

对一组观测，likelihood 是模型赋予所有正确结果概率的乘积：

\[
L=\prod_{k=1}^{N}p_k
\]

最大化 likelihood 等价于最大化 log-likelihood：

\[
\log L=\sum_k\log p_k
\]

也等价于最小化 negative log-likelihood。它们不是三个不同目标，而是同一训练原则的三种写法。

### 5. Attention：可微分的近似字典查询

Attention 可以理解为一种“软检索”：

```text
Query：我正在寻找什么？
Key：每个位置可以用什么特征与我匹配？
Value：匹配后应该取回什么信息？
```

Scaled dot-product attention：

\[
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]

- \(QK^\top\)：query 与 key 的接近程度。
- \(1/\sqrt{d_k}\)：控制高维点积的尺度，防止 softmax 过早饱和。
- softmax：把接近程度变成总和为 1 的注意力权重。
- 乘以 \(V\)：按权重混合并取回上下文意义。

它不是只能找到一个完全匹配的 key，而是把注意力分配给多个相近位置，再读取混合后的 value。因此同一个词，例如 `bank`，可以根据周围 token 获得“银行”或“河岸”的不同上下文表示。

讲义还给出了自回归序列概率：

\[
p(y_1,\ldots,y_T)=\prod_{t=1}^{T}p(y_t\mid y_{<t},x)
\]

模型不是一次预测整句话，而是在已有输入和先前 token 的条件下逐步预测下一个 token。

### 6. 为什么除以 \(\sqrt{d_k}\)

如果 query 和 key 的各维方差约为 1，未缩放点积的方差会随维度增长：

\[
\operatorname{Var}\left(\sum_{i=1}^{d}q_i k_i\right)\approx d
\]

维度越高，点积越容易变得很大，使 softmax 过度尖锐、梯度变弱。除以 \(\sqrt{d_k}\) 后，分数尺度更稳定。

### 7. Tokenization：从文字到可计算单元

模型不能直接处理原始文字。Tokenizer 先把文本切成 token，并把每个 token 映射到整数 ID：

```text
原始文本
-> token / subword 序列
-> token IDs
-> 初始 embeddings
-> Transformer 上下文化
```

Token 不一定等于一个完整单词。它可能是词、子词、标点或字符片段。Tokenization 会影响序列长度、成本、跨语言表现，以及专有名词和罕见词的表示质量。

#### 藏语为什么是有价值的 RAG 测试语言

藏语并不是天然比其他语言“更适合 RAG”，但它很适合作为多语言 RAG 的压力测试：

- 词边界和分词需要专门处理；错误切分会直接影响 chunking、embedding 和召回。
- 相比英语，训练语料和标注资源较少，通用 multilingual 模型未必已经学到稳定的藏语语义空间。
- 藏文文献可能来自扫描件，因此 OCR 误差会继续传入 chunking 和 retrieval。
- 用户问题、知识库和最终回答可能跨藏语、中文与英文，需要测试跨语言 embedding 是否真正对齐。
- 专有名词可能有多种转写或拼写形式，精确匹配和自动评估都需要 normalization。

因此，藏语可以帮助检验整个链路：

```text
藏文或扫描文档
-> OCR 与 Unicode normalization
-> Tibetan-aware tokenization
-> chunking
-> multilingual embedding
-> 单语或跨语言 retrieval
-> 藏语生成
-> 人工与自动评估
```

至少应分别测量藏语查询检索藏语文档、中文或英文查询检索藏语文档，以及藏语查询检索中文或英文文档。不能只凭英文 benchmark 判断模型是否适用。

### 8. 为什么机器需要连续的“机器语言”

词典中的词是离散符号，但梯度下降需要能够进行微小、连续的参数移动。因此，意义必须被表示在一个平滑的连续空间中。

```text
离散 token
-> 连续向量
-> 可计算距离与方向
-> 可用梯度逐步调整
```

Embedding 的意义不在单个坐标，而在向量之间的相对位置、方向和邻域结构。

### 9. 从 token 表示到 chunk embedding

Transformer 的 attention 会为每个 token 生成一个上下文化向量。检索系统通常需要每个 chunk 只有一个可以建立索引的向量，因此需要 pooling：

```text
chunk 中的 token
-> 每个 token 的上下文向量
-> mean pooling 或其他 pooling
-> 一个 chunk embedding
```

Pooling 是压缩步骤。它让索引和比较变得可行，但也可能丢失词序、局部关系、否定和少数重要 token 的信息。

### 10. Masked Language Modelling

Masked language modelling 可以理解为“猜缺失词”：

```text
带有 [MASK] 的句子
-> 根据左右上下文预测缺失 token
-> 用正确 token 的负对数似然评分
```

如果模型能够持续准确地完成任务，它必须学习词义如何随上下文变化。这也是上下文化 embedding 的重要来源。

### 11. Anisotropy 与对比学习

如果训练只有“吸引力”，许多 embedding 可能挤在一个狭窄方向或圆锥中。这叫 anisotropy，会降低 cosine similarity 区分相关与不相关样本的能力。

对比学习同时加入：

- 正样本之间的吸引力
- 负样本之间的排斥力

可以通过比较两类 cosine similarity 分布评估改善：

- within-class：相关样本之间
- between-class：不相关样本之间

理想情况下，两种分布应有清晰间隔，而不是大量重叠。

讲义列出了两种重要的对比学习目标。

Triplet loss：

\[
\mathcal{L}_{\text{triplet}}
=
\max\left(0,\lVert a-p\rVert^2-\lVert a-n\rVert^2+m\right)
\]

- \(a\)：anchor
- \(p\)：positive
- \(n\)：negative
- \(m\)：希望正负样本至少保持的 margin

InfoNCE：

\[
\mathcal{L}_{\text{InfoNCE}}
=
-\log
\frac{\exp(\operatorname{sim}(a,p)/T)}
{\sum_j\exp(\operatorname{sim}(a,x_j)/T)}
\]

它把“从一组候选中识别正确正样本”写成 softmax 分类问题。温度控制模型对相似度差异的敏感程度，因此 softmax、temperature 和 contrastive learning 在这里重新连接起来。

常用 cosine similarity：

\[
\cos\theta
=
\frac{\langle u,v\rangle}{\lVert u\rVert\lVert v\rVert}
\]

它比较方向而不是向量长度，但其有效性仍依赖 embedding 空间是否经过适当训练和校准。

### 11a. 周六下半段实验：用 cosine histogram 评价 embedding 空间

下午的 notebook 实验把 Week 02 的 embedding 理论变成了一个可测量的问题：

```text
同一批文本
-> 用不同 embedding 模型编码
-> 计算文本 pair 的 cosine similarity
-> 画 histogram
-> 用 mean / std / intra / inter / gap 总结空间质量
```

这节的核心不是“哪个图好看”，而是学习如何判断一个 embedding model 是否适合 semantic search、RAG retrieval、clustering、classification 或 subject-based retrieval。

#### 实验比较的三个模型

| 模型 | 空间特征 | 课堂观察 |
| --- | --- | --- |
| Raw BERT | anisotropic | 向量挤在狭窄方向里，很多随机文本也显得很像 |
| MiniLM / Sentence-BERT | 更接近 isotropic | 随机文本的相似度更接近 0，适合句向量检索 |
| Fine-tuned subject encoder | task-shaped | 同 subject 拉近，不同 subject 推远 |

Raw BERT 很强，但它原始输出的 token 或 sentence 表示不一定适合直接做 semantic retrieval。原因是它的向量空间可能 anisotropic：许多无关文本的 cosine similarity 也偏高，导致“什么都像什么”。

MiniLM / Sentence-BERT 这类 sentence embedding 模型经过面向句子相似度的训练，随机文本不会被强行挤到一起，所以通常比 raw BERT 更适合 RAG 的第一版 dense retrieval。

Fine-tuned encoder 则进一步学习当前任务结构。如果训练目标是按 subject 区分文本，那么理想结果就是：

```text
same subject -> cosine 高
different subject -> cosine 低
```

#### 指标定义

| 指标 | 定义 | 怎么读 |
| --- | --- | --- |
| `mean` | 随机文本 pair 的平均 cosine similarity | 太高说明模型容易把无关文本也看成相似 |
| `std` | cosine similarity 分布的标准差 | 越大通常表示模型把相似和不相似 pair 拉开了 |
| `intra` | 同类文本之间的平均相似度 | same subject similarity，越高越好 |
| `inter` | 不同类文本之间的平均相似度 | different subject similarity，越低越好 |
| `gap` | `intra - inter` | 最重要的分离度指标，越大越能区分类别 |

课堂中记录的结果：

| 模型 | mean | std | intra | inter | gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| BERT | 0.722 | 0.120 | 0.786 | 0.679 | 0.107 |
| MiniLM | 0.169 | 0.151 | 0.278 | 0.100 | 0.179 |
| Fine-tuned | 0.202 | 0.541 | 0.859 | -0.213 | 1.072 |

读法：

- BERT 的 `mean` 很高、`std` 小、`gap` 小：整体相似度挤在高位，同类和异类差距不明显。
- MiniLM 的 `mean` 更接近 0，`gap` 比 BERT 大：空间更健康，随机文本不再全部很像。
- Fine-tuned 的 `intra` 高、`inter` 低、`gap` 最大：同类被拉近，异类被推远，说明 fine-tuning 成功学到了 subject 结构。

一句话结论：

```text
Fine-tuned encoder 的 same/different gap 最大，
所以它最适合当前 subject-based retrieval task。
```

更一般的结论是：

```text
不是所有 embedding 都适合 RAG。
RAG 之前必须先检查 embedding 空间是否有区分度。
```

#### 这节学到的定义

- **Embedding**：把文本变成高维向量，使语义可以用距离和方向计算。
- **Cosine similarity**：衡量两个向量方向是否相近，接近 1 表示相似，接近 0 表示弱相关，接近 -1 表示方向相反。
- **Anisotropic**：向量空间不均匀，很多向量挤在同一方向，导致无关文本也有较高相似度。
- **Isotropic**：向量分布更均匀，随机 pair 的 cosine similarity 更接近 0。
- **Fine-tuning for embeddings**：通过正负样本训练，把任务相关样本拉近，把任务无关样本推远。
- **Cosine histogram**：不是只看一个 top-k 结果，而是看整个空间的相似度分布，判断检索模型是否可用。

### 12. KL Divergence

\[
D_{\mathrm{KL}}(p\Vert q)
=
\sum_i p_i\log\frac{p_i}{q_i}
=
H(p,q)-H(p)
\]

KL divergence 衡量使用 \(q\) 近似 \(p\) 时增加的信息代价。它不对称，因此通常不能当作普通几何距离。

### 13. 检索是语义空间中的运动

搜索可以理解为在弯曲的高维语义空间中，从 query 的位置移动到邻近证据。距离函数和 embedding 模型共同决定哪些方向被视为“语义接近”。

CLIP 把文本和图片训练到同一个共享空间：

```text
文本 query -> 文本向量
图片 -> 图片向量
-> 在共享空间比较
-> 用一句话检索相关图片
```

共享空间只解决语义匹配，不自动解决真实性、权限、隐私、来源或安全问题。

### 14. Attention 与现代 Hopfield Memory

讲义末页把 Attention 与现代 Hopfield network 联系起来。两者都可以看成 associative memory：

```text
当前状态或 query
-> 与已存模式计算相似度
-> softmax 分配权重
-> 加权取回 value
-> 得到更新后的状态
```

一种概念化更新形式是：

\[
q_{\text{new}}=V\operatorname{softmax}(\beta A^\top q)
\]

其中 \(\beta\) 类似 inverse temperature。这个视角说明 Attention 不只是矩阵技巧，也可以理解为在能量景观中向相关记忆模式更新。

## 与第 01 周的关系

是有重复，但教学层次不同：

| 主题 | 第 01 周 | 第 02 周 |
| --- | --- | --- |
| Embedding | 直觉、语义搜索和下游用途 | 连续流形、上下文化表示与空间质量 |
| Attention | Q/K/V、Transformer block 心智模型 | scaled dot-product、softmax 权重和缩放原因 |
| Tokenization | 只作为模型输入背景出现 | 明确连接原始文字、token IDs 与 embeddings |
| 多语言压力测试 | 未展开 | 用藏语检验分词、OCR、跨语言 embedding 与生成 |
| CLIP | 实际进行文本搜图片 | 用对比学习和共享空间解释为什么可行 |
| Cosine similarity | 用于语义检索 | 明确公式并讨论 anisotropy 带来的失真 |
| Chunk embedding | 直接使用 SentenceTransformers | 解释 token 向量如何经 pooling 变成索引向量 |
| 训练目标 | 基本没有展开 | MLE、NLL、cross-entropy、perplexity、triplet 和 InfoNCE |
| 检索质量 | 关注 top-k 与安全过滤 | 追问 embedding 空间本身是否有区分度 |

可以把两周理解为：

```text
第 01 周：RAG 系统有哪些部件，如何使用？
第 02 周：这些部件为什么在数学上能够工作，又会在哪里失效？
```

真正重复的部分是 Q/K/V、Attention 公式、CLIP 和语义空间；本周新增的重点是 tokenization、概率论、训练损失、数值稳定性、缩放因子、pooling、anisotropy、对比学习和 Hopfield memory 视角。

## 本周知识之间的连接

```text
softmax
-> 把匹配分数变成概率权重

negative log-likelihood
-> 为正确答案提供可优化的训练损失

attention
-> 用 softmax 对上下文进行软检索和混合

masked language modelling
-> 训练模型学习上下文意义

pooling
-> 把 token 级意义压缩为可索引的 chunk embedding

contrastive learning
-> 让检索空间更有区分度

CLIP
-> 把同一原理扩展到文本和图片
```

## 讲义阅读路线

### 必读

- Vaswani et al., *Attention Is All You Need*
- Devlin et al., *BERT: Pre-training of Deep Bidirectional Transformers*
- Reimers and Gurevych, *Sentence-BERT*
- Radford et al., *Learning Transferable Visual Models From Natural Language Supervision*
- Ethayarajh, *How Contextual Are Contextualized Word Representations?*

### 延伸阅读

- Shannon, *A Mathematical Theory of Communication*
- Jaynes, *Information Theory and Statistical Mechanics*
- Ramsauer et al., *Hopfield Networks Is All You Need*
- Cover and Thomas, *Elements of Information Theory*
- Su et al., *Whitening Sentence Representations*

这组阅读的逻辑是：

```text
信息论
-> Transformer / BERT
-> Sentence-BERT 与句向量
-> CLIP 跨模态空间
-> anisotropy、whitening 与向量空间修复
```

## 解锁的 Agent 能力

Agent 可以更准确地理解和诊断语义检索系统：

- 判断问题出在分数、softmax 温度、embedding、pooling，还是相似度阈值。
- 理解 attention 是模型内部的软检索，但它不等于对外部知识库的 RAG 检索。
- 通过正负样本分布检查 embedding 是否真正具有区分度。
- 在文本和图片之间进行跨模态检索。
- 对检索置信度保持校准，不把向量接近误认为事实正确或授权许可。

## Avaloka 应用

这周内容直接支持 Avaloka Memory Reader 的后续评测。

```text
用户问题或状态
-> query embedding
-> 与 Care Card embeddings 比较
-> softmax、top-k 或阈值选择候选
-> 权限、敏感性、时效和安全过滤
-> rerank
-> 生成有边界的回应
```

需要特别验证：

- mean pooling 是否丢失否定、风险词或细微照护偏好。
- 相似 Care Cards 是否挤成一团，导致无关记忆也有较高 cosine similarity。
- 温度或阈值是否让检索过于自信或过于平均。
- 正样本与 hard negatives 的 cosine 分布是否有足够间隔。
- 多模态内容是否保留 provenance、权限和隐私 metadata。
- 如果未来给 Avaloka 加 embedding retrieval，不能只看“能搜到例子”，还要画 same-memory-intent 与 different-memory-intent 的 cosine histogram。
- 在 Care Card 检索里，`gap = intra - inter` 可以成为模型是否值得上线到下一层 eval 的门槛之一。

## 所需证据、工具与评估

- **证据**：课堂公式、实验输出、token 和 chunk embeddings、正负样本标签。
- **工具**：Transformer、SentenceTransformers、CLIP、向量可视化和 cosine histogram。
- **Trace**：原始分数、温度、softmax 权重、top-k、pooling 方法、模型版本、embedding 模型名、相似度阈值和过滤原因。
- **Eval**：Recall@k、MRR、NDCG、hard-negative error、within/between-class separation、intra/inter/gap、敏感内容误检率和延迟。

## 今日应能回答的问题

1. Softmax 的指数、分母、温度和数值稳定变体分别做什么？
2. 为什么 surprise 使用 \(-\log p\)？
3. NLL、cross-entropy 和 maximum likelihood 之间是什么关系？
4. Perplexity 表达什么，又不能证明什么？
5. Attention 的 \(Q\)、\(K\)、\(V\) 分别是什么？
6. 为什么 attention 分数要除以 \(\sqrt{d_k}\)？
7. 为什么同一个词在不同句子中会得到不同向量？
8. 如何从 token embeddings 得到一个 chunk embedding？
9. Anisotropy 为什么会伤害 cosine retrieval？
10. Triplet loss 与 InfoNCE 如何组织正负样本？
11. KL divergence 与 cross-entropy 有什么关系？
12. CLIP 为什么能让一句话检索一张图片？

## 后续课堂捕获

- 补充讲师使用的 softmax 和 temperature 数值示例。
- 保存 attention 中 `bank` 多义词的完整计算过程。
- 记录 mean pooling 与其他 pooling 方法的实验比较。
- 保存 anisotropy、isotropy、fine-tuned 三类 cosine histogram 和数字 summary table。
- 把课堂实验转化为 Avaloka Memory Reader 的 hard-negative eval。
