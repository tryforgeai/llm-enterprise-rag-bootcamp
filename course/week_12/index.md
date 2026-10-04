# Week 12 — 语义缓存现场课 / The Stones in the River（2026-08-29）

主题：*The Stones in the River — Semantic Caching for Enterprise RAG*（SupportVectors，Enterprise RAG · Advanced Course，讲师 Asif Qamar）

Week 11 是同一份讲义的**课前预习 + 专著精读**；本周是**现场讲授实录**。

## 目录

| 文件 | 内容 |
| --- | --- |
| ⭐⭐ [`summary.zh.md`](summary.zh.md) | **课后总结 —— 先读这个**：五幕骨架 / 三个理解修正 / 四道闸门 / 周一清单 / Avaloka 映射 |
| [`week-12.zh.md`](week-12.zh.md) | 课堂现场笔记：口头补充、自己的例子、与预习理解不一致处 |
| ⭐ [`sigmoid-decision.zh.md`](sigmoid-decision.zh.md) | **本周核心**：从相似度到决策的完整链条 σ / γ / τ / p / p\*，含白板原图与逐步算术 |
| ⭐ [`prologue.zh.md`](prologue.zh.md) | **讲义 p.4–7 逐页精读**：赌注 / 血统 / 解剖（Front Door）/ 划界（象限图）+ ACT II 前瞻（vCache 与四级阶梯） |
| ⭐ [`act1-geometry.zh.md`](act1-geometry.zh.md) | **讲义 p.12–22 逐页精读**：极冠 / 每次命中都有因 / 各向异性 / 大都市效应 / 玻尔兹曼 / 准正交容量 / hubs |
| ⭐ [`act2-decision.zh.md`](act2-decision.zh.md) | **讲义 p.21–31 逐页精读**：$d'$ 该不该建 / 四级阶梯 / δ 合同 / 验证通道 / 调速器 / VoS 经济学 / Quiz 2 |
| [`act3-machine.zh.md`](act3-machine.zh.md) | **讲义 p.32–40 逐页精读**：专用匹配器 / 近失矿脉 / **证据夹道** / 版本钉死 / agent 计划缓存 |
| ⭐ [`interlude-adversary.zh.md`](interlude-adversary.zh.md) | **讲义 p.41–46 逐页精读**：定理被武器化 / 熊皮衣 / 邻近即碰撞 / 防御的代价 / 邻居租户测验 |
| ⭐ [`act4-economics.zh.md`](act4-economics.zh.md) | **讲义 p.47–56 逐页精读**：供应商杀局 / 幸存的三样 / $H^*$ / Build·Do not build / 洗白 / 落位图 |
| [`act5-wild-and-close.zh.md`](act5-wild-and-close.zh.md) | **讲义 p.57–72 逐页精读**：市场即证据 / 阈值之塔 / **十个模式 + 四个反模式** / **周一早上的清单** |
| [`rag-request-flow.zh.md`](rag-request-flow.zh.md) | 地基参考：RAG 一次请求全流程——检索返回什么、怎么拼 prompt、三层缓存分别短路哪一段 |
| [`kv-cache-and-prefix-caching.zh.md`](kv-cache-and-prefix-caching.zh.md) | 缓存的最底三层：KV cache、prefix caching、KV-cache reuse，含显存算术与计时侧信道 |
| [`uploads/whiteboard-01-sigmoid-gamma.png`](uploads/whiteboard-01-sigmoid-gamma.png) | 白板：sigmoid 与三条不同 γ 的曲线 |
| [`uploads/whiteboard-02-sigmoid-x-tau.png`](uploads/whiteboard-02-sigmoid-x-tau.png) | 白板：补上 p(·) 与 x = (s − τ) |
| [`uploads/the-stones-in-the-river.pdf`](uploads/the-stones-in-the-river.pdf) | 现场讲义，72 页 |
| [`uploads/slide-01-title.png`](uploads/slide-01-title.png) | p.1 标题页（Heraclitus 引言） |
| [`uploads/slide-02-map-of-the-day.png`](uploads/slide-02-map-of-the-day.png) | p.2 课程地图（七幕折线） |

> 配套专著 *CacheCraft*（91 页）归档在 [`../week_11/uploads/cachecraft-shareable.pdf`](../week_11/uploads/cachecraft-shareable.pdf)。

## 讲义结构（第 2 页 "Today's learning journey"）

| 节点 | 英文 | 中文 |
| --- | --- | --- |
| PROLOGUE | The Bet | 序幕：那场赌注 |
| ACT I | The Geometry | 第一幕：几何 |
| ACT II | The Decision | 第二幕：决策 |
| ACT III | The Machine | 第三幕：机器 |
| INTERLUDE | The Adversary | 插曲：对手 |
| ACT IV | The Economics | 第四幕：经济学 |
| ACT V | The Wild | 第五幕：野外 |

> 一句话骨架：缓存是一场"过去会重演"的赌注（Prologue）；**几何**让它成为可能（I），**决策论**让它诚实（II），**对手**让它危险（Interlude），**算术**决定该不该下注（IV）。

## 相关

- 课前预习与专著精读：[`../week_11/week-11.zh.md`](../week_11/week-11.zh.md)
- Week 11 目录：[`../week_11/index.md`](../week_11/index.md)
- 前置：[`../week_09/week-09.zh.md`](../week_09/week-09.zh.md)（OKF + Secure Retrieval）
