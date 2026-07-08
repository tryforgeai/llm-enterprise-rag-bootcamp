"""
Gradio UI — Compare CLIP, SigLIP2, and Text retrieval on PRML.pdf (first 85 pages).

Usage:
    python app.py
    python app.py --index-dir data/indices --share
"""

import argparse
import gc
from pathlib import Path

import gradio as gr
import numpy as np
import torch

from utils import load_faiss_index, load_meta, l2_normalize, INDICES_DIR

# ---------------------------------------------------------------------------
# Global state — indices loaded once at startup
# ---------------------------------------------------------------------------

_clip_index = None
_clip_meta = None
_siglip_index = None
_siglip_meta = None
_text_index = None
_text_meta = None
_index_dir = INDICES_DIR


def load_indices(index_dir: Path):
    global _clip_index, _clip_meta, _siglip_index, _siglip_meta
    global _text_index, _text_meta, _index_dir
    _index_dir = index_dir
    print("Loading FAISS indices...")
    _clip_index = load_faiss_index(index_dir / "clip.index")
    _clip_meta = load_meta(index_dir / "clip_meta.json")
    _siglip_index = load_faiss_index(index_dir / "siglip2.index")
    _siglip_meta = load_meta(index_dir / "siglip2_meta.json")
    _text_index = load_faiss_index(index_dir / "text.index")
    _text_meta = load_meta(index_dir / "text_meta.json")
    print(f"  CLIP   : {_clip_index.ntotal} vectors")
    print(f"  SigLIP2: {_siglip_index.ntotal} vectors")
    print(f"  Text   : {_text_index.ntotal} vectors")


# ---------------------------------------------------------------------------
# Encoders (lazy-load models, release after each call)
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


def encode_text(query: str, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    vec = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)
    return vec


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
# UI helpers
# ---------------------------------------------------------------------------

def load_page_image(page: int):
    from PIL import Image

    path = _index_dir.parent / "pages" / f"page_{page:04d}.png"
    if path.exists():
        return Image.open(path)
    return None


def results_to_html_table(clip_res: list, siglip_res: list, text_res: list) -> str:
    k = max(len(clip_res), len(siglip_res), len(text_res))
    clip_pages = {r["page"] for r in clip_res}
    siglip_pages = {r["page"] for r in siglip_res}
    text_pages = {r["page"] for r in text_res}
    all_three = clip_pages & siglip_pages & text_pages
    visual_both = clip_pages & siglip_pages

    td = "padding:6px 12px;border:1px solid #ccc;"
    td_all = td + "background:#d4edda;"    # green — all 3 agree
    td_vis = td + "background:#fff3cd;"   # yellow — both visual agree

    def fmt_visual_cell(r, pages_set):
        if r is None:
            return f'<td style="{td}">—</td>'
        if r["page"] in all_three:
            bg = td_all
        elif r["page"] in visual_both:
            bg = td_vis
        else:
            bg = td
        return f'<td style="{bg}">p.{r["page"]} &nbsp; <code>{r["score"]:.4f}</code></td>'

    def fmt_text_cell(r):
        if r is None:
            return f'<td style="{td}">—</td>'
        bg = td_all if r["page"] in all_three else td
        snippet = r.get("text", "")[:80].replace("\n", " ")
        return (
            f'<td style="{bg}">'
            f'p.{r["page"]} &nbsp; <code>{r["score"]:.4f}</code>'
            f'<br><small style="color:#555">{snippet}…</small>'
            f'</td>'
        )

    rows_html = []
    for i in range(k):
        c = clip_res[i] if i < len(clip_res) else None
        s = siglip_res[i] if i < len(siglip_res) else None
        t = text_res[i] if i < len(text_res) else None
        rows_html.append(
            f'<tr><td style="{td}"><b>{i + 1}</b></td>'
            f'{fmt_visual_cell(c, clip_pages)}'
            f'{fmt_visual_cell(s, siglip_pages)}'
            f'{fmt_text_cell(t)}</tr>'
        )

    legend = (
        '<p style="font-size:12px">'
        '<span style="background:#d4edda;padding:2px 6px">&#9632;</span> all 3 agree &nbsp;'
        '<span style="background:#fff3cd;padding:2px 6px">&#9632;</span> CLIP ∩ SigLIP2 &nbsp;'
        '</p>'
    )
    overlap_summary = (
        f'<p style="font-size:13px">'
        f'<b>All 3 agree:</b> {sorted(all_three) or "none"} &nbsp;|&nbsp; '
        f'CLIP ∩ SigLIP2: {sorted(visual_both - all_three) or "none"} &nbsp;|&nbsp; '
        f'Text only: {sorted(text_pages - clip_pages - siglip_pages) or "none"}'
        f'</p>'
    )

    return (
        '<table style="border-collapse:collapse;width:100%;font-size:14px;">'
        '<thead><tr>'
        f'<th style="{td}">Rank</th>'
        f'<th style="{td}color:#2d7a2d;">CLIP (page | score)</th>'
        f'<th style="{td}color:#8a6c00;">SigLIP2 (page | score)</th>'
        f'<th style="{td}color:#1a5276;">Text / MiniLM (page | score | snippet)</th>'
        "</tr></thead><tbody>"
        + "".join(rows_html)
        + "</tbody></table>"
        + legend
        + overlap_summary
    )


# ---------------------------------------------------------------------------
# Main search function (called by Gradio)
# ---------------------------------------------------------------------------

def search(query: str, k: int):
    if not query.strip():
        return "<p style='color:red'>Please enter a query.</p>", None, None, None

    if _clip_index is None:
        return "<p style='color:red'>Indices not loaded. Check the console for errors.</p>", None, None, None

    clip_qvec = encode_clip(query)
    siglip_qvec = encode_siglip2(query)
    text_qvec = encode_text(query)

    clip_res = retrieve(_clip_index, clip_qvec, _clip_meta, k)
    siglip_res = retrieve(_siglip_index, siglip_qvec, _siglip_meta, k)
    text_res = retrieve(_text_index, text_qvec, _text_meta, k)

    table_html = results_to_html_table(clip_res, siglip_res, text_res)

    clip_img = load_page_image(clip_res[0]["page"]) if clip_res else None
    siglip_img = load_page_image(siglip_res[0]["page"]) if siglip_res else None
    text_img = load_page_image(text_res[0]["page"]) if text_res else None

    return table_html, clip_img, siglip_img, text_img


# ---------------------------------------------------------------------------
# Build Gradio interface
# ---------------------------------------------------------------------------

def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown(
            "# CLIP vs SigLIP2 vs Text — Retrieval Comparison\n"
            "Query the first **85 pages** of *Pattern Recognition and Machine Learning* "
            "across three models and compare results side-by-side."
        )

        with gr.Row():
            query_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What is the EM algorithm?",
                scale=4,
            )
            k_slider = gr.Slider(minimum=1, maximum=10, value=5, step=1, label="Top-K", scale=1)

        search_btn = gr.Button("Search", variant="primary")

        results_html = gr.HTML(label="Results")

        with gr.Row():
            clip_image = gr.Image(label="CLIP — top result page", type="pil")
            siglip_image = gr.Image(label="SigLIP2 — top result page", type="pil")
            text_image = gr.Image(label="Text / MiniLM — top result page", type="pil")

        outputs = [results_html, clip_image, siglip_image, text_image]

        search_btn.click(fn=search, inputs=[query_box, k_slider], outputs=outputs)
        query_box.submit(fn=search, inputs=[query_box, k_slider], outputs=outputs)

        gr.Examples(
            examples=[
                ["What is the EM algorithm?", 5],
                ["Gaussian mixture model", 5],
                ["backpropagation neural network", 5],
                ["kernel methods support vector machine", 5],
                ["Bayesian inference posterior", 5],
            ],
            inputs=[query_box, k_slider],
        )

    return demo


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gradio UI: CLIP vs SigLIP2 vs Text retrieval")
    parser.add_argument("--index-dir", default=str(INDICES_DIR), help="Directory containing index files")
    parser.add_argument("--share", action="store_true", help="Create a public Gradio share link")
    parser.add_argument("--port", type=int, default=7860, help="Local port to serve on")
    args = parser.parse_args()

    index_dir = Path(args.index_dir)
    required = [
        "clip.index", "clip_meta.json",
        "siglip2.index", "siglip2_meta.json",
        "text.index", "text_meta.json",
    ]
    missing = [str(index_dir / f) for f in required if not (index_dir / f).exists()]
    if missing:
        print("ERROR: Missing index files. Run first:")
        print("  python team1_visual.py --pdf data/PRML.pdf")
        print("  python team2_text.py --pdf data/PRML.pdf")
        print("\nMissing:")
        for m in missing:
            print(f"  {m}")
        raise SystemExit(1)

    load_indices(index_dir)
    demo = build_ui()
    demo.launch(
        server_port=args.port,
        share=args.share,
        app_kwargs={"title": "CLIP vs SigLIP2 vs Text — PRML Retrieval"},
    )
