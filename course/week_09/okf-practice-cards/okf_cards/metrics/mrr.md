---
type: Metric
title: MRR (Mean Reciprocal Rank)
description: 第一个相关结果出现在检索列表第几位——只关心"最快多久能找到一个能用的答案"。
resource: course/week_07/summer-week-7-lesson-plan.pdf
tags: [retrieval, ranking, week-07, six-metric-ladder]
sources:
  - id: week07-lesson
    resource: course/week_07/summer-week-7-lesson-plan.pdf
    author: Asif Qamar
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# MRR (Mean Reciprocal Rank)

## 定义

对每个查询，找到第一个相关结果所在的排名位置 $rank$，取倒数 $1/rank$；MRR 是这个倒数在所有查询上的平均值。排名越靠前分数越高，命中第 1 位得 1 分，第 2 位得 0.5 分，以此类推。[^week07-lesson]

## 和 NDCG@5 的分工

MRR 只关心"第一个相关结果多快出现"，适合那种"只要有一个正确答案就够"的场景（比如 FAQ 检索）；NDCG@5 关心整个 top-5 列表的排序质量，适合需要多条证据支撑一个综合答案的 RAG 场景。两者经常一起报，因为它们回答的是不同的问题。

## 使用场景

- 快速诊断"检索系统是不是完全找不到东西"——MRR 接近 0 说明连一个相关结果都很难排进前几位，是比 NDCG 更敏感的早期报警信号。

## 待人工核实的点

- [ ] 讲义里 MRR 是否有专门的现场例题或战争故事（Week 07 逐页记录里目前没有覆盖到，需要补课或找同学要笔记核对）。

[^week07-lesson]: 《Summer Week 7 Lesson Plan》，SupportVectors，2026。
