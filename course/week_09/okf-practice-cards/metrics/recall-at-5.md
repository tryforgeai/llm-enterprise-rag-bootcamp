---
type: Metric
title: Recall@5
description: 检索返回的前 5 个结果里，覆盖了全部相关文档中多大比例——衡量"该找到的东西有没有被找到"。
resource: course/week_07/summer-week-7-lesson-plan.pdf
tags: [retrieval, coverage, week-07, six-metric-ladder]
sources:
  - id: week07-lesson
    resource: course/week_07/summer-week-7-lesson-plan.pdf
    author: Asif Qamar
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# Recall@5

## 定义

在所有和某个查询相关的文档（ground-truth 相关集合）中，有多少比例出现在检索系统返回的前 5 个结果里。[^week07-lesson]

## 和 Recall@k 家族的关系

k 值的选择要匹配下游用途：如果生成器只截取前 3 个 chunk 拼进 prompt，测 Recall@10 就没有直接的操作意义——应该测 Recall@k，k 等于实际会喂给生成器的检索条数。

## 为什么它是六指标阶梯的地基

Recall 低是最需要优先修的问题——它意味着**证据从一开始就没进入候选池**，下游无论 reranker 多强、生成器多忠实，都无法补救没有检索到的信息。参见 Week 08 Evaluation Map："Context recall 低 → 修 chunking/检索，下游无法补救没到的证据。"

## 待人工核实的点

- [ ] Avaloka 项目里实际使用的 k 值（截取给生成器的 chunk 数）是多少，需要和检索管线配置对齐后再确定卡片里默认引用的 k。

[^week07-lesson]: 《Summer Week 7 Lesson Plan》，SupportVectors，2026。
