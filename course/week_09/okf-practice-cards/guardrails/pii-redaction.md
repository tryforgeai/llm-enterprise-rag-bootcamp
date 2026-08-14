---
type: Guardrail
title: PII Redaction Guardrail
description: 在检索结果进入 prompt 之前或答案返回给用户之前，识别并脱敏个人身份信息（姓名、电话、邮箱、身份证号等）。
resource: course/week_06/pii_redaction_demo.py
tags: [guardrail, week-06, privacy, pii]
sources:
  - id: week06-demo
    resource: course/week_06/pii_redaction_demo.py
    author: Asif Qamar
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# PII Redaction Guardrail

## 作用

在语料被检索到、或答案被生成之后，识别文本里的个人可识别信息（PII：姓名、电话号码、邮箱地址、身份证/护照号等），按策略脱敏（替换成占位符、部分掩码，或直接拒绝返回该片段）。

## 为什么必须是独立的一道门，而不是靠 prompt 提示模型"注意保护隐私"

提示词层面的约束不可靠——模型仍然可能在生成阶段把检索到的 PII 原样复述出来。可靠的做法是用确定性的规则或专用的 NER/PII 检测模型，在文本进入 prompt 之前或离开系统之前做机械过滤，而不是依赖生成模型"自觉"。

## 和企业语料治理的关系

如果上游语料本身就没有做好访问控制分级（哪些字段谁能看），PII redaction guardrail 只能是最后一道补救；更根本的做法是在 OKF 的 concept 层面就标注哪些字段含敏感信息，从源头限制它进入可被检索的索引。

## 待人工核实的点

- [ ] `pii_redaction_demo.py` 具体用的检测方法（正则、NER 模型，还是两者结合）以及支持哪些 PII 类型，需要打开脚本核实。
- [ ] 这道门在 Avaloka 项目里目前是否已经接入，接入到管线的哪个位置。
