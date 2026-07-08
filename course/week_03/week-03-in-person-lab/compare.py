"""
Comparison script — query CLIP and SigLIP2 indices side-by-side.

Usage:
    python compare.py "What is the EM algorithm?"
    python compare.py --k 10 "kernel methods"
    python compare.py --show-images "Gaussian mixture model diagram"
    python compare.py --output-json results.json "backpropagation"
"""

import argparse
import json
import sys
import gc
from pathlib import Path

import numpy as np
import torch

from utils import load_faiss_index, load_meta, l2_normalize, INDICES_DIR


# ---------------------------------------------------------------------------
# Query encoders
# ---------------------------------------------------------------------------

def encode_clip(query: str) -> np.ndarray:
    from transformers import CLIPModel, CLIPTokenizerFast

    model_name = "openai/clip-vit-base-patch32"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained(model_name).to(device)
    tokenizer = CLIPTokenizerFast.from_pretrained(model_name)
    model.eval()
    inputs = tokenizer([query], return_tensors="pt", padding=True, truncation=True, max_length=77).to(device)
    with torch.no_grad():
        out = model.get_text_features(**inputs)
    # transformers 5.x returns BaseModelOutputWithPooling; earlier versions return a tensor
    feats = out.pooler_output if hasattr(out, "pooler_output") else out
    vec = feats.cpu().numpy()
    del model
    gc.collect()
    return l2_normalize(vec)


def encode_siglip2(query: str) -> np.ndarray:
    from transformers import AutoModel, AutoTokenizer

    model_name = "google/siglip2-base-patch16-224"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModel.from_pretrained(model_name).to(device)
    # AutoProcessor fails on SigLIP2 because it tries to load SiglipTokenizer, but
    # this checkpoint ships a GemmaTokenizer. AutoTokenizer resolves it correctly.
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model.eval()
    inputs = tokenizer([query], return_tensors="pt", padding="max_length", truncation=True, max_length=64).to(device)
    with torch.no_grad():
        text_inputs = {k: v for k, v in inputs.items() if k in ("input_ids", "attention_mask")}
        out = model.text_model(**text_inputs)
        feats = out.pooler_output if hasattr(out, "pooler_output") else out.last_hidden_state[:, 0]
    vec = feats.cpu().numpy()
    del model
    gc.collect()
    return l2_normalize(vec)


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve(index, query_vec: np.ndarray, meta: list, k: int) -> list:
    scores, ids = index.search(query_vec.reshape(1, -1).astype(np.float32), k)
    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], ids[0])):
        if idx < 0:
            continue
        results.append({"rank": rank + 1, "score": float(score), **meta[idx]})
    return results


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display_results(query, clip_res, siglip_res, show_images=False):
    try:
        from rich.console import Console
        console = Console()
        _rich_display(console, query, clip_res, siglip_res)
    except ImportError:
        _plain_display(query, clip_res, siglip_res)

    # Overlap analysis
    clip_pages = {r["page"] for r in clip_res}
    siglip_pages = {r["page"] for r in siglip_res}
    print("\nPage overlap analysis:")
    print(f"  CLIP ∩ SigLIP2 : {sorted(clip_pages & siglip_pages)}")
    print(f"  CLIP only      : {sorted(clip_pages - siglip_pages)}")
    print(f"  SigLIP2 only   : {sorted(siglip_pages - clip_pages)}")

    if show_images:
        from PIL import Image
        shown = set()
        for res in clip_res[:3] + siglip_res[:3]:
            path = res.get("image_path")
            if path and path not in shown:
                try:
                    Image.open(path).show()
                    shown.add(path)
                except Exception as e:
                    print(f"  Could not open {path}: {e}")


def _rich_display(console, query, clip_res, siglip_res):
    from rich.table import Table
    from rich import box

    console.print(f"\n[bold cyan]Query:[/bold cyan] {query}\n")

    k = max(len(clip_res), len(siglip_res))
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("Rank", justify="center", width=5)
    table.add_column("CLIP\n(page | score)", style="green", width=30)
    table.add_column("SigLIP2\n(page | score)", style="yellow", width=30)

    for i in range(k):
        def visual_cell(results):
            if i >= len(results):
                return ""
            r = results[i]
            return f"p.{r['page']:>4}  {r['score']:.3f}"

        table.add_row(str(i + 1), visual_cell(clip_res), visual_cell(siglip_res))

    console.print(table)


def _plain_display(query, clip_res, siglip_res):
    print(f"\nQuery: {query}\n")
    print("─" * 50)
    k = max(len(clip_res), len(siglip_res))
    for i in range(k):
        c = clip_res[i] if i < len(clip_res) else {}
        s = siglip_res[i] if i < len(siglip_res) else {}
        print(f"\nRank {i+1}")
        if c:
            print(f"  CLIP    : p.{c['page']}  score={c['score']:.3f}")
        if s:
            print(f"  SigLIP2 : p.{s['page']}  score={s['score']:.3f}")
    print("─" * 50)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Compare CLIP and SigLIP2 retrieval side-by-side")
    parser.add_argument("query", nargs="?", help="Search query (prompted if omitted)")
    parser.add_argument("--k", type=int, default=5, help="Top-K results per index")
    parser.add_argument("--show-images", action="store_true", help="Open top page images in viewer")
    parser.add_argument("--output-json", metavar="FILE", help="Dump results to JSON file")
    parser.add_argument("--index-dir", default=str(INDICES_DIR), help="Directory containing index files")
    args = parser.parse_args()

    index_dir = Path(args.index_dir)

    required = {
        "CLIP": ("clip.index", "clip_meta.json"),
        "SigLIP2": ("siglip2.index", "siglip2_meta.json"),
    }
    missing = []
    for name, (idx_file, meta_file) in required.items():
        if not (index_dir / idx_file).exists():
            missing.append(f"  {name}: {index_dir / idx_file}")
    if missing:
        print("ERROR: Missing indices. Run the pipeline scripts first:")
        print("  python team1_visual.py --pdf data/PRML.pdf")
        print("\nMissing files:")
        print("\n".join(missing))
        sys.exit(1)

    query = args.query or input("Enter your question: ").strip()
    if not query:
        print("No query provided.")
        sys.exit(1)

    print("Loading indices...")
    clip_index = load_faiss_index(index_dir / "clip.index")
    clip_meta = load_meta(index_dir / "clip_meta.json")
    siglip_index = load_faiss_index(index_dir / "siglip2.index")
    siglip_meta = load_meta(index_dir / "siglip2_meta.json")

    print("Encoding query with CLIP text encoder...")
    clip_qvec = encode_clip(query)
    print("Encoding query with SigLIP2 text encoder...")
    siglip_qvec = encode_siglip2(query)

    clip_res = retrieve(clip_index, clip_qvec, clip_meta, args.k)
    siglip_res = retrieve(siglip_index, siglip_qvec, siglip_meta, args.k)

    display_results(query, clip_res, siglip_res, show_images=args.show_images)

    if args.output_json:
        out = {"query": query, "clip": clip_res, "siglip2": siglip_res}
        with open(args.output_json, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nResults saved to {args.output_json}")


if __name__ == "__main__":
    main()
