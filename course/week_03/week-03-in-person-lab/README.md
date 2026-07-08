# Visual vs. Text Chunking — PRML Lab

Compares two retrieval strategies on Bishop's *Pattern Recognition and Machine Learning*:

| | Team 1 (Visual) | Team 2 (Text) |
|---|---|---|
| Input | Page rendered as PNG | Parsed text |
| Model | CLIP + SigLIP2 | sentence-transformers |
| What it sees | Text, figures, tables, layout, equations | Plain text only |

The key insight: traditional parse-and-chunk pipelines destroy semantic content encoded in figures, equations, and layout. Treating a page as an image preserves everything.

---

## Prerequisites

- Python 3.10+
- ~2 GB disk for model weights (~950 MB CLIP+SigLIP2, ~90 MB MiniLM)
- ~500 MB disk for page images (738 pages at 150 DPI)
- **Poppler** (required by `pdf2image`):

```bash
brew install poppler          # macOS
sudo apt install poppler-utils  # Linux
```

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Run the Pipelines

### Team 1 — Visual (CLIP + SigLIP2)

```bash
python team1_visual.py --pdf data/PRML.pdf
```

First run downloads ~950 MB of model weights. Expect ~20–40 minutes on CPU for 738 pages.

Options:
- `--dpi 200` — higher resolution images (slower, more detail)
- `--batch-size 8` — reduce if you hit memory limits
- `--force-rebuild` — recompute even if indices exist

Outputs:
- `data/pages/page_NNNN.png` — one PNG per page
- `data/indices/clip.index` + `clip_meta.json`
- `data/indices/siglip2.index` + `siglip2_meta.json`

### Team 2 — Text (sentence-transformers)

```bash
python team2_text.py --pdf data/PRML.pdf
```

First run downloads ~90 MB. Expect ~5–10 minutes on CPU.

Options:
- `--chunk-size 512` — characters per chunk (default 512)
- `--overlap 50` — overlap between chunks (default 50)
- `--force-rebuild` — recompute

Outputs:
- `data/indices/text.index` + `text_meta.json`

---

## Compare Retrieval

```bash
python compare.py "What is the expectation-maximization algorithm?"
python compare.py --k 10 "kernel methods and support vector machines"
python compare.py --show-images "Gaussian mixture model diagram"
python compare.py --output-json results.json "principal component analysis"
```

If you omit the query it prompts interactively.

### Sample output

```
Query: "What is the expectation-maximization algorithm?"

╭───────┬────────────────────┬────────────────────┬───────────────────────────────────────────╮
│ Rank  │ CLIP               │ SigLIP2            │ Text                                      │
│       │ (page | score)     │ (page | score)     │ (page | score | snippet)                  │
├───────┼────────────────────┼────────────────────┼───────────────────────────────────────────┤
│  1    │ p. 439  0.312      │ p. 441  0.341      │ p. 438  0.821  "The EM algorithm is a...  │
│  2    │ p. 441  0.287      │ p. 439  0.318      │ p. 439  0.807  "...at each E-step we..."  │
╰───────┴────────────────────┴────────────────────┴───────────────────────────────────────────╯

Page overlap analysis:
  CLIP ∩ SigLIP2 : [439, 441]
  CLIP ∩ Text    : [439]
  SigLIP2 ∩ Text : [438, 439]
  All three      : [439]
```

---

## Interesting Test Queries

| Query | Why it's interesting |
|---|---|
| `"expectation maximization algorithm"` | Ch. 9 — diagram-heavy; visual should rank figure pages highly |
| `"backpropagation neural network"` | Ch. 5 — equation-heavy pages; text chunks may be sparse |
| `"principal component analysis"` | Ch. 12 — PCA figure vs. mathematical derivation |
| `"Gaussian mixture model diagram"` | Page with the GMM scatter plot — visual retrieves it, text may miss it |
| `"hidden Markov model trellis"` | Ch. 13 — trellis diagram is image-only content |

---

## Architecture Notes

**Cross-modal retrieval (Team 1):** CLIP and SigLIP2 embed text and images into a *shared* vector space. Querying with a text string against the image-based FAISS index is cross-modal retrieval — the text query finds visually relevant pages directly, no OCR needed.

**Text pipeline limitation:** Pages that are mostly equations or figures yield very short (often empty) text chunks and barely appear in the text index. The overlap analysis in `compare.py` surfaces this asymmetry.

**FAISS index type:** `IndexFlatIP` (inner product) with L2-normalised vectors equals cosine similarity search. Flat exhaustive search is fast enough at this scale (~738 pages, ~3000 text chunks).

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `PDFInfoNotInstalledError` | `brew install poppler` |
| `KeyError: Siglip2Model` | Upgrade: `pip install transformers>=4.44` |
| Out of memory during Team 1 | Reduce `--batch-size` to 4 or 8; models are loaded sequentially |
| Slow on CPU | Normal — CLIP takes ~3s/page, SigLIP2 ~5s/page at batch_size=1 |
| HuggingFace download timeout | Set `HF_ENDPOINT=https://huggingface.co` or use a VPN |
