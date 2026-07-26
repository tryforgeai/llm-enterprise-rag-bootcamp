"""
Week 07 eval artifact — reranker + retrieval-metric demo.

目的：亲手走通一条完整的评估闭环
    金数据集(graded 0-4) -> 第一阶段检索 -> 第二阶段 reranker -> 算 Recall@5 / nDCG@5 / MRR
并回答三个课堂问题：
    1. rerank 怎么就改变了结果？          -> 见 stage-1 vs stage-2 的排序与 nDCG 对比
    2. 已经有 rerank 但排序还是错，怎么改？ -> 见 "弱 reranker vs 强 reranker" 对比
    3. recall 低 vs 排序错，分别该修哪里？  -> 见 diagnose() 的判定

设计成 **纯 Python、零依赖、永远能跑**：
    - 第一阶段检索 = 字符 bigram 余弦（bag-of-bigrams cosine），朴素、会被高频字干扰
    - 第二阶段 reranker：
        * "弱 reranker"  = 同样的 bigram 余弦（等于没重排，用于演示"有 rerank 但没用"）
        * "强 reranker"  = bigram BM25（带 idf，压低"年/假"这类高频字的干扰）—— 更接近 cross-encoder 的效果
    - 如果本机装了 sentence-transformers，可切换成真实神经模型（见文件末尾说明）

这不是要证明 BM25 比余弦好，而是用两个"不同强度的打分器"演示：
    reranker 换一个更强的相关性信号，就能把被埋的正确答案顶上来 -> nDCG 上升。
"""

from __future__ import annotations
import math
from collections import Counter

# --------------------------------------------------------------------------
# 1) 金数据集：一个 query，8 篇文档，每篇由 "SME" 打了 0-4 的分级相关性分数
#    （0=无关 … 4=完美）。注意 doc-G "年会" 是个干扰项：和 query 共享 "年" 字，
#    朴素字面打分器容易把它错排到前面。
# --------------------------------------------------------------------------
QUERY = "入职半年能休年假吗"

DOCS = {
    "doc-A": "年假政策 员工入职满六个月后可以开始休年假 每年十天",   # rel 4 完美
    "doc-B": "试用期规定 试用期为六个月 试用期内不可以申请年假",     # rel 3 高度相关
    "doc-C": "请假流程 休假申请需要在系统提交并经过主管批准",       # rel 2 部分相关
    "doc-D": "病假政策 病假与年假分别计算 不互相抵扣",             # rel 1 勉强相关
    "doc-E": "着装规范 办公室着装应当整洁得体",                   # rel 0
    "doc-F": "报销制度 差旅费用凭发票在月底报销",                 # rel 0
    "doc-G": "年会通知 公司年终年会将在十二月举行",               # rel 0 干扰项(含"年")
    "doc-H": "食堂菜单 本周午餐提供三种套餐",                     # rel 0
}

# SME 标注的分级相关性（gold）——只用于"打分"，检索/reranker 都不许偷看它
GOLD = {"doc-A": 4, "doc-B": 3, "doc-C": 2, "doc-D": 1,
        "doc-E": 0, "doc-F": 0, "doc-G": 0, "doc-H": 0}


# --------------------------------------------------------------------------
# 2) 评估指标（纯函数，无依赖）
# --------------------------------------------------------------------------
def recall_at_k(ranking, gold, k):
    """找回的相关文档 / 全部相关文档。相关 = gold 分 >= 1。"""
    all_relevant = [d for d, r in gold.items() if r >= 1]
    hit = [d for d in ranking[:k] if gold.get(d, 0) >= 1]
    return len(hit) / len(all_relevant) if all_relevant else 0.0


def dcg_at_k(ranking, gold, k):
    """DCG = sum (2^rel - 1) / log2(rank+1)。"""
    total = 0.0
    for i, doc in enumerate(ranking[:k]):
        rel = gold.get(doc, 0)
        total += (2 ** rel - 1) / math.log2(i + 2)  # i 从 0 起，rank=i+1，log2(rank+1)=log2(i+2)
    return total


def ndcg_at_k(ranking, gold, k):
    """nDCG = DCG / IDCG（理想排序的 DCG）。"""
    ideal = sorted(gold, key=lambda d: gold[d], reverse=True)
    idcg = dcg_at_k(ideal, gold, k)
    return dcg_at_k(ranking, gold, k) / idcg if idcg > 0 else 0.0


def mrr(ranking, gold):
    """第一个相关结果排名的倒数。"""
    for i, doc in enumerate(ranking):
        if gold.get(doc, 0) >= 1:
            return 1.0 / (i + 1)
    return 0.0


# --------------------------------------------------------------------------
# 3) 打分器（都不许读 GOLD）
# --------------------------------------------------------------------------
def ngrams(text, n):
    t = text.replace(" ", "")
    if n == 1:
        return list(t)
    return [t[i:i + n] for i in range(len(t) - n + 1)]


def cosine_scorer(query, docs):
    """第一阶段检索（弱信号）：单字(unigram)词袋余弦。
    只看单个汉字重叠，极易被'年/假/休/员/工'这类高频字骗到——
    正确答案 doc-A 会被'年会''请假流程'等干扰项挤下去。"""
    q = Counter(ngrams(query, 1))
    out = {}
    for did, text in docs.items():
        d = Counter(ngrams(text, 1))
        dot = sum(q[g] * d[g] for g in q)
        nq = math.sqrt(sum(v * v for v in q.values()))
        nd = math.sqrt(sum(v * v for v in d.values()))
        out[did] = dot / (nq * nd) if nq and nd else 0.0
    return out


def bm25_scorer(query, docs, k1=1.5, b=0.75):
    """强 reranker：字符 bigram 上的 BM25，带 idf——用二元词组('年假''入职''休年')
    捕捉短语级匹配，并用 idf 压低到处都出现的高频片段，从而不被单字干扰项骗到。
    更接近 cross-encoder '看 query 与文档整体语义相关性'的效果。"""
    N = len(docs)
    doc_bg = {d: ngrams(t, 2) for d, t in docs.items()}
    avgdl = sum(len(bg) for bg in doc_bg.values()) / N
    # df: 每个 bigram 出现在多少篇文档里
    df = Counter()
    for bg in doc_bg.values():
        for g in set(bg):
            df[g] += 1
    q_bg = set(ngrams(query, 2))
    out = {}
    for d, bg in doc_bg.items():
        tf = Counter(bg)
        dl = len(bg)
        score = 0.0
        for g in q_bg:
            if g not in tf:
                continue
            idf = math.log(1 + (N - df[g] + 0.5) / (df[g] + 0.5))
            denom = tf[g] + k1 * (1 - b + b * dl / avgdl)
            score += idf * (tf[g] * (k1 + 1)) / denom
        out[d] = score
    return out


def rank_by(scores):
    return sorted(scores, key=lambda d: scores[d], reverse=True)


# --------------------------------------------------------------------------
# 4) 诊断：把指标翻译成"该修哪里"（对应 Week 07 讲义 Act II 的 nDCG↔Recall 诊断对）
# --------------------------------------------------------------------------
def diagnose(ranking, gold, k=5):
    r = recall_at_k(ranking, gold, k)
    n = ndcg_at_k(ranking, gold, k)
    if r >= 0.8 and n < 0.85:
        return f"Recall@{k}={r:.2f} 高 / nDCG@{k}={n:.2f} 低 → 文档找到了但排序烂 → 修 reranker"
    if r < 0.8 and n < 0.85:
        return f"Recall@{k}={r:.2f} 低 / nDCG@{k}={n:.2f} 低 → 根本没找全 → 修检索(embedding/chunking/hybrid)"
    return f"Recall@{k}={r:.2f} / nDCG@{k}={n:.2f} → 都不错，进 Act III 评生成侧"


def report(name, ranking, gold, k=5):
    print(f"\n【{name}】top-{k} 排序: " +
          " > ".join(f"{d}(rel{gold[d]})" for d in ranking[:k]))
    print(f"    Recall@{k}={recall_at_k(ranking, gold, k):.3f}  "
          f"nDCG@{k}={ndcg_at_k(ranking, gold, k):.3f}  "
          f"MRR={mrr(ranking, gold):.3f}")
    print(f"    诊断: {diagnose(ranking, gold, k)}")


# --------------------------------------------------------------------------
# 5) 走一遍完整闭环
# --------------------------------------------------------------------------
def main():
    K = 5
    print("=" * 78)
    print(f"Query: {QUERY}")
    print(f"金数据集(gold 相关度): {GOLD}")
    print(f"理想排序: {rank_by(GOLD)}")
    print("=" * 78)

    # 第一阶段：向量检索（bigram 余弦），捞全部候选并排序
    stage1_scores = cosine_scorer(QUERY, DOCS)
    stage1_rank = rank_by(stage1_scores)
    report("阶段①：检索(bigram余弦)，无 reranker", stage1_rank, GOLD, K)

    # 场景 A：装了一个"弱 reranker"——用和检索一样的信号，等于白重排
    weak_rank = rank_by(cosine_scorer(QUERY, {d: DOCS[d] for d in stage1_rank[:6]}))
    report("阶段②：弱 reranker(同款余弦信号) —— '有 rerank 但排序还是错'", weak_rank, GOLD, K)

    # 场景 B：换一个"强 reranker"——BM25(带 idf)，只对第一阶段 top-6 候选重排
    top6 = stage1_rank[:6]
    strong_scores = bm25_scorer(QUERY, {d: DOCS[d] for d in top6})
    strong_rank = rank_by(strong_scores)
    report("阶段②：强 reranker(BM25 带 idf)", strong_rank, GOLD, K)

    print("\n" + "-" * 78)
    print("结论：")
    print("  · rerank 怎么改变结果 —— 它不改检索捞回哪些文档(Recall 可不变)，")
    print("    只重新给候选打分排序，把被埋的正确答案(doc-A)顶上来 -> nDCG 上升。")
    print("  · 已有 rerank 但排序还是错 —— 说明 reranker 的相关性信号不够强")
    print("    (弱 reranker 和检索用同一种信号，等于没重排)。修法：换更强的")
    print("    reranker(如 cross-encoder / BM25 带 idf)、调候选数 N、或换适配语言的模型。")
    print("  · Recall 低 vs 排序错 —— 看 diagnose()：Recall 高+nDCG 低=修 reranker；")
    print("    两个都低=修检索。")
    print("-" * 78)


if __name__ == "__main__":
    main()

# ==========================================================================
# 想换成【真实神经模型】？装 sentence-transformers 后替换两处打分器：
#
#   from sentence_transformers import SentenceTransformer, CrossEncoder, util
#   bi = SentenceTransformer("BAAI/bge-small-zh-v1.5")          # 第一阶段
#   ce = CrossEncoder("BAAI/bge-reranker-v2-m3")                # 第二阶段 reranker
#
#   # 检索：用 bi 编码 query 和文档，算 cosine
#   # 重排：ce.predict([(QUERY, DOCS[d]) for d in top_n])
#
# 指标函数(recall/ndcg/mrr)、金数据集、诊断逻辑完全不变——
# 只把"打分器"从字面算法换成模型即可。这正是本周的核心：
# 尺子(金数据集+指标)不变，被测系统(检索/reranker)可以随意替换和对比。
# ==========================================================================
