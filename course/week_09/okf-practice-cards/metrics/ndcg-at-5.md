---
type: Metric
title: NDCG@5
description: 归一化折损累积增益，衡量检索返回的前 5 个结果里，相关文档是否排在靠前位置的排序质量指标。
resource: course/week_07/summer-week-7-lesson-plan.pdf
tags: [retrieval, ranking, week-07, six-metric-ladder]
sources:
  - id: week07-lesson
    resource: course/week_07/summer-week-7-lesson-plan.pdf
    author: Asif Qamar
  - id: week08-notes
    resource: course/week_08/week-08.zh.md
    author: agent-generated-notes
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# NDCG@5

## 定义

NDCG(Normalized Discounted Cumulative Gain)在检索返回的前 5 个结果里，给排名靠前的相关文档更高权重、靠后的相关文档权重按对数衰减，再除以理想排序下能拿到的最大增益做归一化，得到一个 0–1 之间的分数。[^week07-lesson]

## 为什么不能只看 Recall

Recall@5 只问"相关文档有没有进前 5"，不管它排在第 1 位还是第 5 位；NDCG@5 在乎**顺序**——同样是命中，排第 1 和排第 5 对下游生成器（尤其是只截取前几条拼进 prompt 的系统）而言价值完全不同。这也是六指标阶梯里，从 precision/recall 往上爬到 NDCG 这一级的原因。[^week08-notes]

## 使用场景

- 精调 reranker 时的核心优化目标之一。
- 和 Context precision（RAGAS）联动读：NDCG 低但生成端 FActScore 高，通常说明"生成器能扛，是 reranker 在饿它"——参见 Week 08 的 Evaluation Map 压力测试读图规则。[^week08-notes]

## 待人工核实的点

- [ ] 具体的对数衰减公式（$\text{DCG}_k=\sum_{i=1}^k \frac{rel_i}{\log_2(i+1)}$）和理想排序基线（IDCG）在本课件里的确切呈现方式，需要对照 Week 07 讲义原文核实。

[^week07-lesson]: 《Summer Week 7 Lesson Plan》，SupportVectors，2026。
[^week08-notes]: 《第 08 周课堂笔记》，本课程笔记，2026-08-01。
