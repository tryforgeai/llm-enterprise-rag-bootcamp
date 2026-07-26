"""
Week 07 · Precision-Recall 曲线 / AUC-PR 手算 demo

对应 Act II · Metric 5 "The Precision-Recall curve"。
演示：同样 Recall=1.0(相关的都找到了)的两个系统，
     AUC-PR 却能凭"相关文档排得靠不靠前"分出高下。

PR 曲线怎么建：
    沿排序从上往下扫，每命中一个相关文档就记一个点：
        precision = 到此为止命中的相关数 / 已看的文档数
        recall    = 到此为止命中的相关数 / 全部相关数
AUC-PR ≈ Average Precision(AP) = 在每个相关文档命中处的 precision 的平均。

跑法： python3 pr_curve_demo.py   (纯 Python，零依赖)
"""

# 排序里 1=相关文档(✓)，0=无关文档(✗)。两个系统对同一 query，各返回 top-10。
CAREFUL = [1, 1, 1, 0, 1, 0, 0, 1, 0, 0]   # 细心的孩子：相关的多数排前面
CLUMSY  = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1]   # 笨拙的孩子：相关的都排后面
TOTAL_RELEVANT = 5                          # 语料里该 query 共有 5 篇相关文档


def pr_points(ranking, total_relevant):
    """扫一遍排序，在每个相关文档命中处记 (recall, precision, rank)。"""
    hits = 0
    pts = []
    for rank, rel in enumerate(ranking, start=1):
        if rel == 1:
            hits += 1
            precision = hits / rank
            recall = hits / total_relevant
            pts.append((rank, recall, precision))
    return pts


def average_precision(ranking, total_relevant):
    """AP = 每个相关命中处 precision 的平均（对 recall 曲线的面积近似）。"""
    pts = pr_points(ranking, total_relevant)
    if not pts:
        return 0.0
    return sum(p for _, _, p in pts) / total_relevant


def recall_at_k(ranking, total_relevant, k):
    return sum(ranking[:k]) / total_relevant


def show(name, ranking, total_relevant):
    seq = " ".join("✓" if r else "✗" for r in ranking)
    print(f"\n【{name}】排序: {seq}")
    print(f"    {'命中#':>5} {'rank':>5} {'recall':>8} {'precision':>10}")
    for i, (rank, rec, prec) in enumerate(pr_points(ranking, total_relevant), 1):
        bar = "█" * round(prec * 20)
        print(f"    {i:>5} {rank:>5} {rec:>8.2f} {prec:>10.2f}  {bar}")
    ap = average_precision(ranking, total_relevant)
    print(f"    Recall@10 = {recall_at_k(ranking, total_relevant, 10):.2f}   "
          f"AUC-PR(≈AP) = {ap:.3f}")


def main():
    print("=" * 62)
    print(f"共有 {TOTAL_RELEVANT} 篇相关文档；两个系统各返回 top-10。")
    print("PR 曲线：每命中一个相关文档记一个点(recall↑ 时 precision 怎么变)")
    print("=" * 62)

    show("细心的孩子 (careful)", CAREFUL, TOTAL_RELEVANT)
    show("笨拙的孩子 (clumsy)", CLUMSY, TOTAL_RELEVANT)

    ap_c = average_precision(CAREFUL, TOTAL_RELEVANT)
    ap_k = average_precision(CLUMSY, TOTAL_RELEVANT)
    print("\n" + "-" * 62)
    print("结论：")
    print(f"  · 两者 Recall@10 都是 1.00（5 篇相关的都找到了）——分不出高下")
    print(f"  · 但 AUC-PR：细心 {ap_c:.2f}  vs  笨拙 {ap_k:.2f} —— 一眼分出好坏")
    print("  · 差别只在'相关文档排得靠不靠前'：细心的一路保持高 precision，")
    print("    笨拙的一开始就跌到谷底(0.33)爬不起来。")
    print("  · 这正是 ROC 做不到的(会被类别失衡骗成都满分)，而 PR 曲线能。")
    print("-" * 62)


if __name__ == "__main__":
    main()
