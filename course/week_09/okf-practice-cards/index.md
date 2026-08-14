---
type: Index
title: RAG Bootcamp Practice Bundle — Week 06/07/08 Concepts
description: 十张练习用的 OKF concept 卡片，把 Week 06 的 guardrails 和 Week 07/08 的评估指标重新装订成带出处、带信任层级的知识对象。
---

# RAG Bootcamp Practice Bundle

这是一个练习性质的 knowledge bundle，把之前几周课上学到的评估指标和 guardrail 机制，按照 Week 09《The Open Knowledge Format》讲的规范重新写成 concept 卡片。

## Metrics（评估指标，来自 Week 07 / Week 08）

- [NDCG@5](metrics/ndcg-at-5.md) — 检索排序质量（Week 07）
- [Recall@5](metrics/recall-at-5.md) — 检索覆盖率（Week 07）
- [MRR](metrics/mrr.md) — 首个相关结果的排名（Week 07）
- [RAGAS Faithfulness](metrics/ragas-faithfulness.md) — 生成答案对检索上下文的忠实度（Week 08）
- [FActScore](metrics/factscore.md) — 声明级事实精度（Week 08）
- [ECE](metrics/ece.md) — 期望校准误差（Week 08）
- [NRR](metrics/nrr.md) — 负拒绝率（Week 08）

## Guardrails（来自 Week 06）

- [Response Grounding Gate](guardrails/response-grounding-gate.md) — 响应侧 grounding / 负拒绝闸门
- [PII Redaction Guardrail](guardrails/pii-redaction.md) — 个人信息脱敏
- [Indirect Prompt Injection Defense](guardrails/indirect-prompt-injection-defense.md) — 间接提示注入防御

## 注意

这十张卡目前都是**草稿**——`generated` 字段标注是我（agent）根据课堂笔记起草的，`verified` 字段是空的，也就是说信任层级目前都停在 **unverified**。按今天学的规矩，这正是应该的诚实状态：你需要自己核对每张卡的公式、阈值、来源是否准确，然后以 `human:rosso` 的身份把它们标记为 `human-reviewed`，卡片才真正"毕业"。
