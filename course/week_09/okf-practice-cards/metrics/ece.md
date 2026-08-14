---
type: Metric
title: ECE (Expected Calibration Error)
description: 分桶比较模型陈述的置信度与实际准确率之间的加权差异——衡量模型是否"该有把握的时候有把握，该犹豫的时候犹豫"。
resource: course/week-08.zh.md
tags: [calibration, week-08, cognitive-humility]
sources:
  - id: week08-notes
    resource: course/week-08.zh.md
    author: agent-generated-notes
  - id: guo-calibration
    resource: "Guo et al. 2017, On Calibration of Modern Neural Networks (ICML)"
    author: Guo et al.
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# ECE (Expected Calibration Error)

## 定义

把模型给出的置信度分成若干区间（bin），在每个区间里比较"模型自称的置信度"和"实际观测到的准确率"，取加权差异。完美校准是 0；现代 LLM 常见范围是 0.05–0.15，且**模型越大、指令微调越多，往往越差**（置信度被推高但准确率没跟上）。[^week08-notes]

## 课堂手算例（两 bin）

高置信度 bin 出现过度自信约 15 分（陈述置信度比实际准确率高 15 个百分点），且该 bin 因样本占比大而主导了整体误差——这正是典型的现代 LLM 签名，也是最危险的区域，因为用户最愿意听信高置信度的答案。

## 修复方法

- 温度缩放（temperature scaling）——最便宜、最常用
- Platt scaling
- Isotonic regression

## 和风险-覆盖曲线的关系

ECE 校准得好，是风险-覆盖曲线呈现"凸形"（弃权一小部分就能大幅降低错误率）的前提——校准差的模型，弃权信号本身就不可靠，风险-覆盖曲线会退化成一条直线甚至凹形。

## 待人工核实的点

- [ ] 具体的分桶数量（bin 数）和加权方式（按样本数加权还是等权）在课堂讲义里的确切定义，需要对照 Guo et al. 原论文核实。

[^week08-notes]: 《第 08 周课堂笔记》，本课程笔记，2026-08-01。
[^guo-calibration]: Guo, C. et al. (2017). *On Calibration of Modern Neural Networks*. ICML.
