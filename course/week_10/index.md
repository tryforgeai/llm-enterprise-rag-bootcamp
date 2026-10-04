# Week 10 — 多目录的图书馆 / The Library of Many Catalogues（2026-08-15）

主题：*Enterprise RAG: The Library of Many Catalogues — Retrieval Architecture, from the Representation to the Verdict*（SupportVectors，讲师 Asif Qamar）

> **一句话**：*A retrieval system is not a search over documents. It is a **portfolio of representations** and a **court of adjudication**.*
> 一个检索系统不是「在文档上做搜索」，而是**一组表征的投资组合**加上**一座裁决的法庭**。

全天从上午十一点到晚上八点半 —— 整个检索侧的房子。

## 目录

| 文件 | 内容 |
| --- | --- |
| [`week-10.zh.md`](week-10.zh.md) | 课堂笔记：Prelude 逐页 + 正课 deck p.3–p.87 逐页 + 讲义精读（3,900+ 行） |
| [`week-10-summary-for-team.zh.md`](week-10-summary-for-team.zh.md) | 团队总结（中文） |
| [`week-10-summary.md`](week-10-summary.md) | 团队总结（英文） |
| [`week-10-slack-draft.md`](week-10-slack-draft.md) | Slack 草稿（英 / 中 / 超短三版） |
| `uploads/` | Prelude（20 页）与正课 deck（125 页）的 PDF |

## 原始材料

- [x] [`summer-week-10-lesson-plan.pdf`](summer-week-10-lesson-plan.pdf) — 课堂讲义 refresher，29 页，首稿 2026-08-15
- [x] [`uploads/the-room-as-the-corpus.pdf`](uploads/the-room-as-the-corpus.pdf) — 开场 Prelude 幻灯，20 页
- [x] [`uploads/the-library-of-many-catalogues.pdf`](uploads/the-library-of-many-catalogues.pdf) — 正课 deck，125 页
- [ ] RetrievalCraft monograph（同名）—— 讲义自述其来源：**讲义是 refresher 和第一返回点，monograph 是完整解剖，book chapter 课后跟进**（**待补**）
- 实物教具：实验一发到手的航海图 `OTLETIA — Approaches to Otlet Harbour`（SupportVectors 自制，页脚标 *Week 10 prelude · Experiment I*）

## 全天结构

```
Prelude   The Room as the Corpus  （连续第三周的「先动手/先失败，再命名」开场）
Act I     The Library             （Mundaneum、召回天花板、断层扫描原理、四个高度、
                                    表征清单 BM25→SPLADE→稠密→Matryoshka→ColBERT、DCL 与 MRL–DCL 不变式）
Act II    The Second Corpus       （派生工件七件套，以及长上下文的海市蜃楼）
Act III   The Court               （排序层融合 RRF k=60、去重与诱饵、问题侧六病理、
                                    机房、会看图的目录、两栏账本、伽利略与 Shapley 剧本）
```

## 关键教条（速查）

- **召回天花板** —— 只有铲斗决定什么被捞到；下游任何东西都抬不高它
- **断层扫描原理** —— 融合就是重建；单一索引宣称全视，投资组合拒绝这个宣称
- **用户就是考官** —— 制造匹配你的查询的文档，而不是等查询来匹配文档
- **主模式** —— 检索派生物，从源生成（retrieve the derivative, generate from the source）
- **柏林实验** —— 段落 0.64 vs factoid 0.81–0.90；在 0.7–0.8 阈值上答案被静默丢掉
- **在排序层面融合** —— RRF, k=60，尺子出现之前的宪法
- **诱饵的工作在检索处结束** —— cross-encoder 只判源文本
- **每个索引通过消融赢得位置** —— 第二栏（缺席的代价）空着的组件是装饰

## 相关

- 前置：[`../week_09/week-09.zh.md`](../week_09/week-09.zh.md)（OKF 受治理语料 + Secure Retrieval）—— 第七件工件「受治理 concept」就是上周的客人回来入座
- 后续：[`../week_11/`](../week_11/)（语义缓存 —— **本周建的这座房子的前门**）

> **补档说明**：这份讲义曾长期散落在 `course/` 根目录、文件名带着 ` (1)` 后缀，因此 Week 10 一度被记成"无任何记录"（见 `../week_11/week-11.zh.md` 第一节），其主题也被推断错（MemoryCraft / SkillCraft / Secure Retrieval 续集均不成立）。2026-10-03 归档并补齐。
