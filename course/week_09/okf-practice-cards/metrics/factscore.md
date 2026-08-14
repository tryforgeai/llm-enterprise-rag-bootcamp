---
type: Metric
title: FActScore
description: 把答案拆成不可再分的原子事实，逐条核实真伪，报告事实精度——比 RAGAS Faithfulness 粒度更细。
resource: course/week-08.zh.md
tags: [generation, hallucination, week-08, claim-level]
sources:
  - id: week08-notes
    resource: course/week-08.zh.md
    author: agent-generated-notes
  - id: factscore-paper
    resource: "Min et al. 2023, FActScore (EMNLP)"
    author: Min et al.
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# FActScore

## 定义

把答案分解成一条条不可再分的原子事实（atomic fact），逐条独立核验其真伪，报告被支持的原子事实占比。原始论文测出 2023 年 ChatGPT 生成的人物传记只有 **58%** 事实精度，这个数字被课上称为"唤醒钟"。[^factscore-paper]

## 三年后的进展（Week 08 讲义 p.97 引用）

到 2026 年，事实精度被"检索 + 弃权"推动、而非单靠模型规模：

- 带浏览的推理模型（GPT-5 system card 数据）：约 99% 声明精度
- GPT-4o 级非推理模型：62–71%
- 无检索的尾部知识：依旧残酷，SimpleQA Verified 最好也只有 72.1%，多数前沿模型在 29–55%

## 和 RAGAS Faithfulness 的分工

RAGAS Faithfulness 检查的是"句子层面是否被上下文支持"，容易被一句含多个可证伪声明的句子蒙混；FActScore 把粒度打到**原子事实**级别，能抓住 RAGAS 会漏掉的部分对错混杂的句子。[^week08-notes]

## 待人工核实的点

- [ ] 我们自己的评估集里，用什么工具/流程做"原子事实分解"（是否是 LLM 分解，还是有更便宜的规则式方法），需要在实现里补上。

[^week08-notes]: 《第 08 周课堂笔记》，本课程笔记，2026-08-01。
[^factscore-paper]: Min, S. et al. (2023). *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation*. EMNLP.
