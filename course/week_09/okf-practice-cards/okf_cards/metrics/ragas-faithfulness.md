---
type: Metric
title: RAGAS Faithfulness
description: 把生成的答案拆成一条条声明，逐条对检索上下文做蕴含核验，报告有多大比例的声明被证据支持。
resource: course/week-08.zh.md
tags: [generation, ragas, week-08, faithfulness]
sources:
  - id: week08-notes
    resource: course/week-08.zh.md
    author: agent-generated-notes
  - id: ragas-paper
    resource: "Es et al. 2023, RAGAS"
    author: Es et al.
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# RAGAS Faithfulness

## 定义

把生成器的答案拆解成一条条可独立核验的声明（claim），逐条与检索到的上下文做蕴含核验（entailment check），报告被上下文支持的声明占比。后端可以用 LLM（灵活但存在自我增强偏见的循环风险）或经典 NLI 模型（更便宜、更保守）。[^week08-notes]

## 只是地板，不是天花板

Faithfulness 高只说明答案对**检索到的上下文**忠实，不说明：

- 答案是否真的回答了问题（这是 Answer relevancy 的职责——Quiz 7 "流畅的敷衍"：问退款答运费，每句都被文档完美支持，Faithfulness 仍高，Answer relevancy 崩）
- 检索到的上下文本身是否完整、是否遗漏了更好的证据（这是 Context recall 的职责）
- 声明的粒度是否被蒙混（一句含 3 个可独立证伪的声明，可能整体被判定为"支持"）

## 使用场景

作为生成端评估的**地板指标**——先用它做第一轮回归门禁，再叠加 FActScore（原子声明粒度更细）、RAGChecker（双向蕴含 + 检索/生成双诊断）做更细的诊断。

## 待人工核实的点

- [ ] 我们自己的两道"门"（Week 06 的 request guardrail + response grounding）在 RAGAS 默认分解粒度下，实测 Faithfulness 分数具体是多少，需要跑一次评估集才能填上这个数字。

[^week08-notes]: 《第 08 周课堂笔记》，本课程笔记，2026-08-01。
[^ragas-paper]: Es, S. et al. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*.
