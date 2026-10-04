# Week 08 — 人差方程 / The Personal Equation（2026-08-01）

主题：*The Personal Equation — Seven small experiments you are going to fail* + *The Measure of All Things*（五幕完整版）（SupportVectors，讲师 Asif Qamar）

> **一句话**：先测量测量者本身（measure the measurer first）—— 而最深的那个指标，是**「它知道自己不知道吗」**。

Week 07 量检索，本周量**生成器本身**，再量**上线之后的世界**。

## 目录

| 文件 | 内容 |
| --- | --- |
| [`week-08.zh.md`](week-08.zh.md) | 课堂笔记 |
| [`week-08-summary-for-team.zh.md`](week-08-summary-for-team.zh.md) | 团队总结（中文） |
| [`week-08-summary.md`](week-08-summary.md) | 团队总结（英文） |
| [`week-08-slack-draft.md`](week-08-slack-draft.md) | Slack 草稿（英 / 中 / 超短三版） |
| `uploads/` | 讲义 PDF（待放入，见下） |

## 原始材料

- [ ] `uploads/the-personal-equation.pdf` — 开场实验课，29 页（**待放入**）
- [ ] `uploads/the-measure-of-all-things.pdf` — 正课讲义完整版，169 页，**五幕版**（相较 Week 07 的四幕版新增 Act V「The Observatory」）（**待放入**）

## 全天结构

```
开场      The Personal Equation   （七个你会亲手失败的小实验）
Act III   The Generator           （RAGAS 地板 → FActScore / RAGChecker → ALCE）
Act IV    The Frontier            （judge 2.0、RGB 四能力、认知谦逊、多跳、进化题库、agentic）
Act V     The Observatory         （离线闸门 + 在线驱动 + 漂移 + 棘轮）—— 全新
Coda      The Evaluation Map      （把每个低分接回「该修哪个组件」）
```

## 关键教条（速查）

- **人差方程** —— 每台仪器都有稳定可测的偏差；**减掉它，别开除它**（而 judge 偏差是**非平稳**的，校正项带保质期）
- **correct ≠ grounded** —— 事实正确但无据的答案仍是 grounding 失败
- **Cohen's κ，不是原始一致率** —— 75% 一致率可能 κ 只有 0.375；**κ < 0.6 拒用**
- **评委陪审团胜过单个大模型** —— 3 个异构小 judge κ 0.763 > 单个 GPT-4 的 0.627，成本约 1/7
- **小验证器优先** —— MiniCheck 约 1/400 成本达 GPT-4 精度
- **弃权是旋钮不是开关** —— 风险–覆盖曲线找工作点；监管行业 NRR 门槛 > 70%
- **pass^k 不是 pass@k** —— 单次 70% 在连续三个客户上只剩 29%
- **Goodhart** —— Kelvin 测量，Cameron 警告，Goodhart 解释警告如何成真

## 相关

- 前置：[`../week_07/`](../week_07/)（量检索：标尺 + 六指标阶梯）—— 本周是它的生成器半场
- 后续：[`../week_09/week-09.zh.md`](../week_09/week-09.zh.md)（OKF 受治理语料）
