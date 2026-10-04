---
type: Metric
title: NRR (Negative Rejection Rate)
description: 用语料回答不了的问题去测系统会不会诚实地拒答，而不是从参数记忆里编一个听起来合理的答案。
resource: course/week_08/week-08.zh.md
tags: [abstention, guardrail-adjacent, week-08, cognitive-humility]
sources:
  - id: week08-notes
    resource: course/week_08/week-08.zh.md
    author: agent-generated-notes
  - id: rgb-paper
    resource: "Chen et al. 2024, RGB (AAAI)"
    author: Chen et al.
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# NRR (Negative Rejection Rate)

## 定义

构造一批"语料里确实答不了"的查询集合，测系统在这些查询上诚实弃权（说"我不知道"或"资料里没有"）的比例。监管行业的部署门槛通常要求 NRR **> 70%**。[^week08-notes]

## Calabi–Yau 探针（课堂例子）

一家卖网络交换机的公司，RAG 系统却热情正确地讲起了超弦几何——这就是负拒绝失败：答案来自模型的参数记忆而非检索证据，本该被 Week 06 的响应门（response grounding gate）拦下。RGB 论文实测 ChatGPT 级模型的负拒绝率只有 **43–45%**——"从噪声里编造"仍是多数模型的默认行为。[^rgb-paper]

## 必须成对报告

单独报 NRR 容易被 game（模型可以对什么都不答来刷高这个数）。必须同时报告：

- 不可答问题上的拒绝率（NRR 本身）
- 可答问题上的**过度拒绝率**（over-refusal rate）——避免模型变成"什么都不敢答"

## 待人工核实的点

- [ ] 我们自己语料的"不可答查询集"目前是否已经构造好、覆盖了哪些主题，需要检查 evals 目录确认现状。

[^week08-notes]: 《第 08 周课堂笔记》，本课程笔记，2026-08-01。
[^rgb-paper]: Chen, J. et al. (2024). *Benchmarking Large Language Models in Retrieval-Augmented Generation (RGB)*. AAAI.
