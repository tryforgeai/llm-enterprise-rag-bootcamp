"""
Week 07 · nDCG 手算 demo —— 把四层拆开，每一步都打印中间值。

nDCG = Normalized Discounted Cumulative Gain（归一化折扣累积增益）
是 Act II 六指标的"顶峰"：唯一同时做到
    · 看相关程度（分级 0-4，不是二元）
    · 看排序位置（越靠前越值钱）
的检索指标。

四层（从里到外）：
    1) Gain（增益）        G_i = 2^rel - 1          —— 相关程度值多少分，指数放大高相关
    2) Cumulative（累积）  CG  = ΣG_i               —— 前 k 个加总
    3) Discounted（折扣）  DCG = Σ G_i/log2(rank+1)  —— 越靠后越打折
    4) Normalized（归一）  nDCG = DCG / IDCG         —— 除以理想排序，压到 0~1

跑法： python3 ndcg_demo.py     （纯 Python，零依赖）
"""

import math

# 每篇文档由 SME 打的分级相关性（gold）。0=无关 … 4=完美
GOLD = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0, "F": 0, "G": 0}


def gain(rel):
    """第1层 Gain：指数增益 2^rel - 1。"""
    return 2 ** rel - 1


def dcg_at_k(ranking, gold, k, show=False):
    """第2+3层：累积 + 折扣。可选打印每一行的贡献。"""
    total = 0.0
    if show:
        print(f"    {'rank':>4} {'doc':>4} {'rel':>4} {'gain=2^rel-1':>13} "
              f"{'discount=log2(r+1)':>18} {'贡献':>10}")
    for i, doc in enumerate(ranking[:k]):
        rel = gold.get(doc, 0)
        g = gain(rel)
        disc = math.log2(i + 2)          # rank=i+1, 折扣=log2(rank+1)=log2(i+2)
        contrib = g / disc
        total += contrib
        if show:
            print(f"    {i+1:>4} {doc:>4} {rel:>4} {g:>13} "
                  f"{disc:>18.3f} {contrib:>10.3f}")
    return total


def ndcg_at_k(ranking, gold, k, show=False):
    """第4层：归一化。DCG / IDCG。"""
    ideal = sorted(gold, key=lambda d: gold[d], reverse=True)  # 理想排序=按相关度降序
    if show:
        print(f"  [DCG] 你的排序 {ranking[:k]}：")
    dcg = dcg_at_k(ranking, gold, k, show)
    if show:
        print(f"  -> DCG@{k}  = {dcg:.3f}")
        print(f"  [IDCG] 理想排序 {ideal[:k]}：")
    idcg = dcg_at_k(ideal, gold, k, show)
    if show:
        print(f"  -> IDCG@{k} = {idcg:.3f}")
    n = dcg / idcg if idcg else 0.0
    if show:
        print(f"  => nDCG@{k} = DCG/IDCG = {dcg:.3f}/{idcg:.3f} = {n:.3f}")
    return n


def main():
    K = 5
    print("=" * 70)
    print(f"金数据集(gold 相关度): {GOLD}")
    print(f"理想排序(按相关度降序): {sorted(GOLD, key=lambda d: GOLD[d], reverse=True)}")
    print("=" * 70)

    # 详细走一个排序：完美答案 A 被干扰项 G 挤到后面
    print("\n### 详细拆解一个排序：A > G > D > C > B ###\n")
    ranking = ["A", "G", "D", "C", "B"]
    ndcg_at_k(ranking, GOLD, K, show=True)

    # 直觉对比：几种不同排序的 nDCG@5
    print("\n" + "=" * 70)
    print("直觉对比：同一批文档，不同排序的 nDCG@5")
    print("=" * 70)
    cases = {
        "理想排序      A>B>C>D>E": ["A", "B", "C", "D", "E"],
        "本 demo 排序  A>G>D>C>B": ["A", "G", "D", "C", "B"],
        "把好的排后面  E>F>G>D>C": ["E", "F", "G", "D", "C"],
        "完全颠倒      G>F>E>D>C": ["G", "F", "E", "D", "C"],
        "只错第1名     G>A>B>C>D": ["G", "A", "B", "C", "D"],
    }
    for name, r in cases.items():
        n = ndcg_at_k(r, GOLD, K)
        bar = "█" * round(n * 30)
        print(f"  {name}   nDCG@5={n:.3f}  {bar}")

    print("\n" + "-" * 70)
    print("怎么读这些数字：")
    print("  · nDCG=1.0 -> 你的排序就是理想排序（好东西全在最前）")
    print("  · nDCG 越低 -> 高相关的文档被排得越靠后 / 被无关的挤下去")
    print("  · '只错第1名'(把无关G放第1)就掉到 ~0.69，说明第1名的权重极大")
    print("    (折扣 log2(2)=1 最轻，第1个位置贡献最重)")
    print("  · 指数增益让 rel=4 的 A 值 15 分、rel=1 的 D 只值 1 分，")
    print("    所以'把 A 排后面'的惩罚远重于'把 D 排后面'")
    print("-" * 70)


if __name__ == "__main__":
    main()
