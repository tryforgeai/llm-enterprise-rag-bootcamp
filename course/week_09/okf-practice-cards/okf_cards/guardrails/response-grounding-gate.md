---
type: Guardrail
title: Response Grounding Gate
description: 在答案返回用户之前拦截的一道门，检查每条声明是否真的能在检索到的证据里找到支撑，防止模型用参数记忆"补全"答案。
resource: course/week_06/guardrailed_rag_pipeline_demo.py
tags: [guardrail, week-06, grounding, negative-rejection]
sources:
  - id: week06-demo
    resource: course/week_06/guardrailed_rag_pipeline_demo.py
    author: Asif Qamar
  - id: week08-notes
    resource: course/week-08.zh.md
    author: agent-generated-notes
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# Response Grounding Gate

## 作用

在答案生成后、返回给用户前，检查答案里的每条声明是否能在本次检索到的上下文里找到支撑证据。找不到支撑的声明要么被剔除，要么被标注为"资料未提及、以下是常识性背景"。这道门直接对应 Week 08 NRR 指标要衡量的能力。[^week08-notes]

## 和 Request Guardrail 的分工

Request guardrail 在**输入侧**拦截（比如判断问题是否在服务范围内）；Response grounding gate 在**输出侧**拦截（判断已经生成的答案是否有据）。两道门缺一不可——请求侧过滤不了模型在生成阶段临时"想起"的参数记忆内容。

## 失败时的样子（课堂例子）

一家卖网络交换机的公司，RAG 系统被问到无关问题时，热情正确地讲起了超弦几何——这正是这道门本该拦下、却没拦住的案例（Calabi–Yau 探针）。

## 待人工核实的点

- [ ] `guardrailed_rag_pipeline_demo.py` 里这道门具体的实现方式（是声明级蕴含核验，还是更粗粒度的关键词匹配），需要打开脚本核实。

[^week08-notes]: 《第 08 周课堂笔记》，本课程笔记，2026-08-01。
