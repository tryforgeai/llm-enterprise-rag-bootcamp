# Week 03 总结 — Chunking 是一次表示决策

**日期：** 2026-06-20 · **来源：** `course/week_03/week-3-summer-lesson-plan.pdf`、课堂 lab、Week 03 实验代码

---

## 一句话结论

Chunking 不是预处理。它是我们对语料做的第一个、并且实际上不可逆的决定：**什么算一个可以独立检索的思想单元**。后面所有环节（embedding、reranking、prompt、换更大的模型）都只能在这个错误的第一次投影上打补丁。

对我们的实际意义：不要再把 chunk size 当成一个调参旋钮，而是跑 **representation tournament** —— 把 fixed / semantic / contextual / late chunking / page-image 几种方案放在同一批 query 上，用检索指标决胜负。

---

## 核心概念

| 概念 | 实际含义 |
| --- | --- |
| **Chunking as ontology** | chunk 边界等于声明"这一段就是一个可检索的思想单元"。切错了，再好的 reranker 也救不回来。 |
| **第一次投影不可逆** | 文本 → 边界 → embedding，结构被压进固定维向量。边界切掉的东西无法恢复。 |
| **Mixing principle** | 两个正交思想塞进一个 chunk，向量平均后谁都不代表。对所有 query 都"有点相关"。 |
| **Small-chunk amnesia** | 小 chunk 更纯，但容易丢掉指代对象、适用条件、定义、否定和安全范围。 |
| **Centroid delusion** | 大而杂的 chunk 会飘向语义空间中心——对很多 query 中等相似，却不真正回答任何一个。经常进 top-k，但在答案里没用。 |
| **Query–chunk asymmetry** | query 短而尖锐，chunk 长而弥散。匹配时会偏向"内部一致"的 chunk，而不是真正能回答问题的 chunk。 |
| **Contextual chunking** | 在**文本空间**修复上下文：先切小，再补最小必要上下文。可读、可审计，但每个 chunk 要一次 LLM 调用。 |
| **Late chunking** | 在**隐空间**修复上下文：先让 encoder 读完整文档，再按边界 pooling 成 chunk 向量。优雅、便宜，但解释性弱。 |
| **Page-image retrieval** | 不把二维页面压成一维文本。ColPali / ColVision 保留每页多个 patch 向量，用 ColBERT 式 MaxSim 匹配 query token。 |

### Chunking 到底破坏了什么

五种失败模式，值得在 code review 和事故复盘里直接点名：

1. **Endophora（指代断裂）** —— 代词和被指代对象被切到不同 chunk。chunk 读起来通顺，但指代对象没了，模型靠猜来补。
2. **Discourse structure（论证关系断裂）** —— 只检索到主张，没检索到后面的 `however`、让步或限定，答案可能和原文结论相反。论文、合同、临床结果、风险声明里风险最高。
3. **Negation / scope failure（否定与作用域）** —— `no significant evidence` 丢掉 `in patients under 65`；`if debt-to-income exceeds 43%` 丢掉条件。**这一类最危险**：没有任何错误信号，只有一个自信的、过度泛化的答案。
4. **Definition–use chain（定义链断裂）** —— §2.1 定义 "Covered Losses"，§7.4 反复使用。切开之后模型看到的只是普通英文词，不是合同里的精确定义。这也是"chunk 越小越好"不成立的原因。
5. **Bridging inference 与 genre blindness** —— 隐含的场景关系被切掉；同一套 512-token 策略被无差别套用到合同、论文、小说和财报 PDF 上，而这些文体承载意义的方式完全不同。

**关于 512-token 默认值：** 它只是一个方便的工程基线，大约一页（约 300–400 tokens/页），不是语义边界。把它当对照组，别当结论。

---

## 本周跑的实验

### 1. 标点敏感度实验 — `course/week_03/punctuation_embedding_test.py`

测试 embedding 模型看到的是标点控制的句法结构，还是只有词面重合。三个句子：

```
1. Eats, shoots, and leaves.
2. Eats shoots and leaves.
3. A panda eats bamboo shoots and leaves.
```

| 模型 | cos(1,2) | cos(1,3) | cos(2,3) |
| --- | ---: | ---: | ---: |
| BERT（anisotropic） | 0.9041 | 0.7610 | 0.7908 |
| MiniLM（isotropic） | 0.9231 | 0.4605 | 0.5065 |

拆成两个问题看：

- `cos(2,3) > cos(1,3)` —— 模型知不知道熊猫句更接近无逗号句？**两个模型都通过。**
- `cos(2,3) > cos(1,2)` —— 句法结构能不能压过词面重合？**两个模型都没通过。**

BERT 三组分数普遍偏高，也印证了 Week 02 讲的 anisotropy / cone 效应。这个结果不是"embedding 完全失效"，而是一个更细的失败：**模型能看到 topic 和词汇关系，但看不够标点控制的句法。** 对法律、医学、监管和 Avaloka 安全规则来说，`not / unless / except / however / if / only when / , / ;` 都可能翻转结论，而 embedding 未必察觉。

### 2. PRML 视觉检索 vs 文本检索 — `course/week_03/week-03-in-person-lab/`

在 Bishop 的 PRML 上跑两条 pipeline，用 `compare.py` 对比：

| | Team 1（视觉） | Team 2（文本） |
| --- | --- | --- |
| 输入 | 页面渲染成 PNG @150 DPI | 解析文本，512 字符 chunk / 50 overlap |
| 模型 | CLIP + SigLIP2 | sentence-transformers（MiniLM） |
| 能看到 | 文字、图、表、版面、公式 | 只有纯文本 |
| 索引 | FAISS `IndexFlatIP` + L2 归一化（等价 cosine） | 同上 |

跨模态检索意味着文本 query 可以直接打图像索引，**不需要 OCR 环节**。overlap 分析暴露出的不对称：**公式密集页和纯图页解析出的文本 chunk 几乎是空的，在文本索引里基本不出现。** 像 "Gaussian mixture model diagram"、"hidden Markov model trellis" 这类 query，文本 pipeline 实际上是瞎的。

另外还写了 `path1_page_image_qa.py`（page-image 检索 + vision 回答）、`path2_text_chunk_qa.py`（文本 chunk 检索 + 文本回答）、`qa_compare_app.py`（并排对比）、`pdf_to_textbook.py`（PRML → Markdown textbook baseline）。页面渲染已验证连续完整，没有缺页。

### 3. Contextual chunking baseline — `course/week_03/capstone_contextual_chunks/`

Capstone PDF（213 页，203 页非空，约 335K 字符）→ 266 个 chunk，1800 字符 / 250 overlap，输出两个版本：

- `regular_chunks.jsonl` —— 普通 chunk
- `contextual_chunks.jsonl` —— 每个 chunk 带一段 context 前缀：文档标题、页码范围、所属 section、本地关键词

context 前缀是**本地确定性生成的，没有调用任何外部 API**。这给了我们一个低成本的 contextual chunking 参赛方案，不用为每个 chunk 付 LLM 调用费。

> 备注：`contextual_chunk_pdf.py` 默认读 `data/rag-capstone-projects.pdf`，该文件刻意未提交；换源用 `--pdf`。离线单测：`uv sync --frozen && uv run pytest`（用假 model client，不需要 API key）。

---

## "RAG is dead" 到底死的是什么

Chroma 和 Turbopuffer 那两个视频都不是说 retrieval 过时了。真正失败的是：

```
固定 chunk → 向量 top-k → 全塞进 prompt → 祈祷
```

没有失败的是：retrieval、evidence、context engineering、agentic search、grounding、eval。

正确方向是 agentic retrieval —— agent 自己判断需要什么，混用 vector / full-text / regex / metadata filter，多轮搜索改写 query，裁掉噪声，把干净的证据交给 reasoning model。

一个好用的说法：**embeddings are cached compute（embedding 是预先缓存的算力）。** 只有当语料会被反复高频查询时，预先理解并索引它才划算。

---

## 建议的默认 pipeline

这不是配方，是一组参赛候选：

```
尊重文档 markup / headings
→ semantic hierarchical chunking
→ budget 允许时做 contextual chunking
→ embedding 前做 late chunking
→ 保存 section、position、parentage、source metadata
→ 用 eval 选 winner
```

每个新语料都应该跑自己的 tournament：

```
语料样本 → held-out queries → gold evidence
→ 竞争的表示方式
→ 检索指标 + latency/cost + safety 检查
→ winner 或 hybrid
```

**指标：** Recall@k、MRR、NDCG@k、hard-negative rate、scope-inversion error、definition-orphan error、visual-table retrieval accuracy、answer grounding、latency/cost、safety/privacy 泄漏。

**什么时候值得上 page-image retrieval：** 财报、科学论文 PDF、扫描件、含表格/图/公式的教材，以及任何版面本身携带意义的文档。**什么时候不值得：** 需要字符级精确匹配、需要长距离跨页推理、需要低成本大规模索引、语料主要是纯 prose。多数情况下答案是 hybrid index，而且该由证据决定，不该靠争论决定。

---

## 对 Avaloka 的影响

默认 chunking 对 Care Card 和智慧材料是不安全的。不同材料类型需要不同策略：

| 材料 | 可能策略 |
| --- | --- |
| Care Card | 小而**完整**的原子记忆 —— 保留 permission、lifecycle、risk scope |
| Wisdom principle | 语义 chunk + 上下文补充，避免断章取义 |
| Baifa / mind-state notes | 保留 definition–use chain 和反例 |
| Eval 失败记录 | 按 failure mode 和 decision point 切分 |
| 讲义 PDF、表格、扫描件 | 考虑 page-image retrieval 或 hybrid index |

**最大的风险：** chunking 可能把安全边界和温柔语气从事实片段上剥掉。

```
原文:     When user is stable and not in acute distress, user likes gentle reminders.
坏 chunk: User likes gentle reminders.
```

第二个看起来很干净，而且很危险 —— 它丢掉了 `not in acute distress`。我们的工作定义：

```
小而完整 = 事实 + 指代对象 + 适用条件
         + 禁用条件 + 权限范围 + 来源
```

Avaloka retrieval 的最低 chunk schema：source id、memory type、permission scope、risk scope、lifecycle status、created/updated time、related user intent、parent context、safety qualifiers，必要时还有 exact quoted evidence。

---

## 留给团队的开放问题

1. 对以纯文本为主、含少量表格的企业文档，hybrid text + page-image 的**最低可行实验**该怎么设计？
2. 对有权限和安全范围的记忆系统，chunk metadata 应该参与 embedding、filtering、reranking，还是只参与最终过滤？
3. Late chunking 的最大上下文长度限制在长文档上怎么处理？是否要先按章节做局部 late chunking？
4. 如果 contextual chunking 用 LLM 补上下文，怎么评估它没有引入原文没有的解释？
5. Tournament 的 gold evidence 应该标注在 chunk、page 还是 source span 层级？

---

## 后续行动

- [ ] **补上 Week 03 的 eval artifact**（目前仍然缺失）：同一批 query 跑 fixed / semantic / contextual / page-image 检索，比较 Recall@k、answer grounding 和错误类型。
- [ ] 给 Avaloka Memory Reader V0 benchmark 加上 chunking / representation 维度。
- [ ] 在 capstone 计划里明确语料类型、用户问题、检索挑战、候选表示方式和成功指标。
- [ ] 修复课堂 lab 的 Python 依赖缺失问题（CLIP / SigLIP2 / MiniLM 三路 + Gradio UI）。

---

## 在整体进度中的位置

```
Week 01 —— 端到端的 RAG 流水线
Week 02 —— 向量空间为什么能用
Week 03 —— 源文档在进入这个空间之前，是怎样被切坏或保留下来的
```
