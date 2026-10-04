# RAG 一次请求的全流程：检索返回什么、怎么发给 LLM

Week 12（2026-08-29）课堂追问整理。这是本周所有缓存内容的**地基参考**——三层缓存分别短路这条链的不同段落。

> **一句话**：**所谓 RAG，本质就是「自动化的复制粘贴」。**所有工程复杂度都在"粘贴什么进去"这一步。

---

## 全景图

```text
用户问题
  │
  ├─→ ① 精确哈希层 ────────────────────────────→ 命中即返回   ⏱ 微秒  💰 免费
  │        ↓ miss
  ├─→ ② embed → HNSW → decide(γ, τ, p*) ────→ 命中即返回   ⏱ 几十ms 💰 便宜
  │        ↓ miss
  └─→ ③ 完整流水线
         │
         ├─ 检索 top-20
         ├─ 权限过滤（ACL）
         ├─ rerank → top-5
         ├─ 去重 / 截断 / 排序
         ├─ 拼成 prompt        ← 稳定部分在前（prefix caching 生效点）
         ├─ 调 LLM             ← prefill + decode（KV cache 生效点）
         ├─ 抽引用、渲染来源
         └─ **回写缓存**（answer + provenance + versions）
```

① ② 就是讲义 p.6 的 **Front Door 模式**三道门，见 [`prologue.zh.md`](prologue.zh.md)。

---

## 一、检索返回的是什么

**不是答案，是一个「候选片段列表」。**每个元素：

```json
[
  {
    "chunk_id": "doc_hr_042#c3",
    "text": "员工报销需在费用发生后 30 天内提交。提交入口为 Concur 系统，需上传发票原件扫描件。单笔超过 5000 元需部门总监审批...",
    "score": 0.87,
    "metadata": {
      "source_doc": "员工报销管理办法_v4.2.pdf",
      "doc_version": "4.2",
      "page": 3,
      "section": "3.1 提交流程",
      "updated_at": "2026-06-15",
      "acl": ["all_employees"]
    }
  },
  {
    "chunk_id": "doc_fin_011#c7",
    "text": "财务部每周三、周五处理报销单。审批通过后 T+3 个工作日到账...",
    "score": 0.81,
    "metadata": { "source_doc": "财务处理时效说明.docx", "doc_version": "2.0", "...": "..." }
  }
]
```

三个必须有的部分：

| 部分 | 干什么用 |
| --- | --- |
| **text** | **唯一会进 prompt 的东西** |
| **score** | 排序、过滤、决定要不要放弃 |
| **metadata** | 引用、权限过滤、**失效**（= 讲义说的 provenance + versions） |

> ⚠️ **关键点**：**向量到这一步就用完了，被丢掉了。**
>
> LLM 从头到尾**看不到任何向量**——它只会看到纯文本。向量只是"找到这些文本"的工具。

---

## 二、检索到发送之间的七步

原始检索结果不能直接扔给 LLM：

```python
hits = vector_search(query_embedding, top_k=20)     # ① 粗召回，要多
hits = filter_by_acl(hits, user)                    # ② 权限过滤（Week 09 那套）
hits = rerank(query, hits)[:5]                      # ③ 精排，交叉编码器重新打分
hits = dedupe(hits)                                 # ④ 去重（同文档邻近 chunk）
hits = drop_below(hits, min_score=0.5)              # ⑤ 太差的宁可不给
hits = fit_to_budget(hits, max_tokens=4000)         # ⑥ 截断到预算内
hits = reorder(hits)                                # ⑦ 排序（见下）
```

**第 ⑦ 步值得单说**：LLM 对长上下文有 **"lost in the middle"** 现象——**开头和结尾记得牢，中间容易忽略**。所以常见做法是把最相关的放**首尾**，次要的埋中间。

---

## 三、怎么拼成 prompt

**就是字符串拼接，没有魔法。**

```python
context_block = "\n\n".join(
    f"[{i+1}] 来源：{h['metadata']['source_doc']} "
    f"(v{h['metadata']['doc_version']}, 更新于 {h['metadata']['updated_at']})\n"
    f"{h['text']}"
    for i, h in enumerate(hits)
)
```

拼出来的完整 prompt：

```text
┌─ system ────────────────────────────────────────────┐
│ 你是企业知识助手。仅依据下方提供的资料回答。          │
│ 每个论断必须用 [编号] 标注来源。                      │
│ 资料中找不到答案时，明确说"资料中没有相关信息"，       │
│ 不要依据常识推测。                                    │
└─────────────────────────────────────────────────────┘
┌─ user ──────────────────────────────────────────────┐
│ <资料>                                               │
│ [1] 来源：员工报销管理办法_v4.2.pdf (v4.2, 2026-06-15)│
│ 员工报销需在费用发生后 30 天内提交。提交入口为 Concur │
│ 系统，需上传发票原件扫描件。单笔超过 5000 元需...     │
│                                                      │
│ [2] 来源：财务处理时效说明.docx (v2.0, 2026-03-01)   │
│ 财务部每周三、周五处理报销单。审批通过后 T+3 个...    │
│ </资料>                                              │
│                                                      │
│ 问题：报销流程是什么？                                │
└─────────────────────────────────────────────────────┘
```

四个设计要点：

- **`[1] [2]` 编号** → 让模型能引用，输出里带编号后**能映射回原文档**
- **来源和版本写进文本** → 模型可以说"根据 v4.2 的规定"
- **`<资料>` 标签包起来** → 边界清晰，也是**抵御间接注入**的一层（Week 06 的两道门）
- **system 里明确"找不到就说找不到"** → 抑制幻觉

> 📌 **和 prefix caching 的接口就在这里**：system prompt + few-shot + 工具定义是**每次都一样**的，必须排在最前面；检索结果和用户问题**每次都变**，必须排在最后。顺序搞反 = 命中率清零。见 [`kv-cache-and-prefix-caching.zh.md`](kv-cache-and-prefix-caching.zh.md)。

---

## 四、发给 LLM

一次普通的 API 调用：

```python
response = client.messages.create(
    model="claude-sonnet-5",
    system=SYSTEM_PROMPT,              # 固定不变 → 可被 prefix cache 命中
    messages=[
        {"role": "user",
         "content": f"<资料>\n{context_block}\n</资料>\n\n问题：{query}"}
    ],
    max_tokens=1024,
)
answer = response.content[0].text
```

**LLM 收到的就是一大段纯文本**，它不知道这些文字是"检索来的"——对它来说和用户手打进去的没有区别。

---

## 五、回来之后

### 抽引用

```python
# 模型输出："报销需在 30 天内提交 [1]，审批后 T+3 到账 [2]。"
citations = extract_citations(answer)                     # → [1, 2]
sources = [hits[i-1]["metadata"] for i in citations]
# 前端渲染成可点击的来源链接
```

### 回写缓存（Front Door 的 write-back）

```python
cache.write(
    key          = canonical_key(query),
    embedding    = query_embedding,
    answer       = answer,
    provenance   = [h["chunk_id"] for h in hits],          # ← 用了哪些 chunk
    doc_versions = {h["metadata"]["source_doc"]:
                    h["metadata"]["doc_version"] for h in hits},   # ← 各自什么版本
    acl          = intersect_acl(hits),                    # ← 权限取交集
)
```

**这就是讲义 p.6 `payload: KV store — responses, provenance, versions` 那一行的实际内容。**

存下 provenance 和 version，才能在 `员工报销管理办法.pdf` 升到 v4.3 时**精确作废这一条**，而不是全清或干等 TTL。

`acl` 取**交集**是因为：这条答案综合了多个 chunk，能看它的人必须是**每个 chunk 都有权限**的人。

---

## 六、三层缓存分别短路哪一段

| 缓存 | 从哪里短路 | 省掉什么 |
| --- | --- | --- |
| **精确哈希层** | ① 直接返回 | **全部**，连 embedding 都不用调 |
| **语义缓存** | ② 直接返回 | 检索 + rerank + 生成 |
| **Query→Docs 缓存** | 跳过检索，直接拿第三步的 `hits` | 向量检索 + rerank |
| **Embedding 缓存** | 跳过 `embed(query)` | 一次 embedding API 调用 |
| **prefix caching** | 跳过 prompt 前半段的 prefill | ~72% 的 prefill |
| **KV cache** | 生成过程内部 | 自回归的重复计算（O(n²)→O(n)） |

**风险沿这张表从上到下递减**：最上面两个可能答错，下面四个不会。

---

## 留存句

- **RAG 本质是自动化的复制粘贴。**复杂度全在"粘贴什么"。
- **向量在拼 prompt 前就被丢掉了**——LLM 只见文本，不见向量。
- **provenance + version 是失效机制的地基**，不存就只能靠 TTL 瞎猜。
- **acl 取交集**：能看这条答案的人 = 每个来源 chunk 都有权限的人。
- **prompt 按稳定度排序**，否则 prefix caching 直接失效。

## 待办

- [ ] 检查 Avaloka 现有的 prompt 拼装顺序（稳定的在前吗）
- [ ] 现有系统有没有存 provenance / doc_version？没有的话失效只能靠 TTL
- [ ] 命中回写时的 acl 是取交集还是取并集？取并集是安全事故
