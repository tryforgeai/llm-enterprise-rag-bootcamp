#!/usr/bin/env python3
"""Week 03 punctuation-sensitive embedding and collection analysis.

This script has two related jobs:

1. Test whether embedders distinguish punctuation / syntax:

1. "Eats, shoots, and leaves."
2. "Eats shoots and leaves."
3. "A panda eats bamboo shoots and leaves."

Expected human judgment:

    cos(2, 3) should be higher than cos(1, 3)

because sentence 2 and sentence 3 are about eating shoots/leaves, while
sentence 1 is a comma-controlled action list.

2. Inspect the exported Week 1 projector collections:

    vectors.tsv / metadata.tsv

Those exported vectors can show anisotropy/isotropy and same-subject gaps, but
they cannot embed new sentences. New sentence tests still need the classroom API
or a local SentenceTransformer checkpoint.

The collection-analysis flow mirrors the classroom cosine notebook:

    cosine = direction -> same-subject grid -> anchor same/different gap
    -> three-model comparison -> one-number summary

The BERT and MiniLM embedders use the SupportVectors classroom embedding API.
The fine-tuned model is optional and requires a local SentenceTransformer
checkpoint path. If you accidentally pass the exported projector vectors
directory, the script will detect it and explain why that directory cannot
embed new sentences.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib import request
from urllib.error import HTTPError, URLError


os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(os.environ.get("TMPDIR", "/tmp")) / "matplotlib"),
)

SCRIPT_DIR = Path(__file__).resolve().parent
COURSE_DIR = SCRIPT_DIR.parent
DEFAULT_OUTPUT = COURSE_DIR / "rag_2026_week2_uslab" / "embedded_model" / "output"
DEFAULT_FIG_DIR = SCRIPT_DIR / "figures"
DEFAULT_EMBED_BASE_URL = "http://10.0.10.51:8000"
DEFAULT_FINE_TUNED_MODEL_PATH = os.environ.get("SUBJECT_FINETUNED_MODEL_PATH", "")

TEXTS = [
    "Eats, shoots, and leaves.",
    "Eats shoots and leaves.",
    "A panda eats bamboo shoots and leaves.",
]

CLUSTER_MODELS = {
    "BERT (anisotropic, 768d)": "google-bert/bert-base-uncased",
    "MiniLM (isotropic, 384d)": "sentence-transformers/all-MiniLM-L6-v2",
}

COLLECTION_PATHS = {
    "BERT (anisotropic, 768d)": (
        "subjects",
        "SV_LLM_RAG_Week_1_Anisotropic_Subject",
    ),
    "MiniLM (isotropic, 384d)": (
        "subjects",
        "SV_LLM_RAG_Week_1_Isotropic_Subject",
    ),
    "Fine-tuned (384d)": (
        "subjects_finetuned",
        "SV_LLM_RAG_Week_1_Subject_Fine_Tuned",
    ),
}

COLORS = {
    "BERT (anisotropic, 768d)": "#d62728",
    "MiniLM (isotropic, 384d)": "#1f77b4",
    "Fine-tuned (384d)": "#2ca02c",
}

DEFAULT_ANCHOR_MODEL = "MiniLM (isotropic, 384d)"


@dataclass(frozen=True)
class ModelResult:
    name: str
    cos_12: float
    cos_13: float
    cos_23: float

    @property
    def expected_pair_wins(self) -> bool:
        return self.cos_23 > self.cos_13 and self.cos_23 > self.cos_12

    @property
    def panda_relation_detected(self) -> bool:
        return self.cos_23 > self.cos_13

    @property
    def punctuation_trap_avoided(self) -> bool:
        return self.cos_23 > self.cos_12


def import_numpy():
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError(
            "numpy is required for collection analysis. "
            "Run from the course virtualenv or install numpy."
        ) from exc
    return np


def load_collection(folder: Path):
    """Load one projector export folder as (vectors, labels)."""
    np = import_numpy()
    vectors_path = folder / "vectors.tsv"
    metadata_path = folder / "metadata.tsv"

    vectors = np.loadtxt(vectors_path, delimiter="\t", dtype=np.float32)
    labels = []
    with metadata_path.open(encoding="utf-8") as fh:
        fh.readline()
        for line in fh:
            labels.append(line.rstrip("\n").split("\t")[-1])

    labels = np.asarray(labels)
    if len(labels) != vectors.shape[0]:
        raise RuntimeError(
            f"metadata/vector length mismatch in {folder}: "
            f"{len(labels)} labels vs {vectors.shape[0]} vectors"
        )

    return vectors, labels


def expected_dim_from_name(name: str) -> int | None:
    if "(768d)" in name:
        return 768
    if "(384d)" in name:
        return 384
    return None


def load_all_collections(output: Path):
    """Load all known Week 1 collections from an output directory."""
    data = {}
    for name, (subdir, leaf) in COLLECTION_PATHS.items():
        folder = output / subdir / leaf
        vectors_path = folder / "vectors.tsv"
        metadata_path = folder / "metadata.tsv"
        if not vectors_path.exists() or not metadata_path.exists():
            print(f"!! Missing collection export: {folder}")
            continue

        vectors, labels = load_collection(folder)
        data[name] = (vectors, labels)
        subjects = ", ".join(sorted(set(labels)))
        print(
            f"{name:26s} -> {vectors.shape[0]:5d} vectors, "
            f"dim {vectors.shape[1]:3d}, subjects: {subjects}"
        )
        expected_dim = expected_dim_from_name(name)
        if expected_dim is not None and vectors.shape[1] != expected_dim:
            print(
                f"   !! label says {expected_dim}d, but vectors.tsv is "
                f"{vectors.shape[1]}d; check how this export was created."
            )

    return data


def normalize_rows(matrix):
    """Normalize each row so dot product equals cosine similarity."""
    np = import_numpy()
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def cosine_np(left, right) -> float:
    """Cosine similarity for NumPy vectors."""
    np = import_numpy()
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0
    return float(np.dot(left, right) / denominator)


def print_toy_cosine_demo() -> None:
    """Print the small direction-not-length cosine demo from the lesson notes."""
    np = import_numpy()
    same_direction = np.array([2.0, 2.0])
    also_northeast = np.array([5.0, 5.0])
    perpendicular = np.array([-3.0, 3.0])
    opposite = np.array([-1.0, -1.0])

    print("\n=== cosine intuition: direction, not length ===")
    print(
        "same direction, different length : "
        f"{cosine_np(same_direction, also_northeast):+.3f}"
    )
    print(f"perpendicular                    : {cosine_np(same_direction, perpendicular):+.3f}")
    print(f"opposite                         : {cosine_np(same_direction, opposite):+.3f}")


def sample_pair_cosines(vectors, n_pairs: int, rng):
    """Sample random pairwise cosine similarities."""
    np = import_numpy()
    unit = normalize_rows(vectors.astype(np.float64))
    n = unit.shape[0]
    i = rng.integers(0, n, size=n_pairs)
    j = rng.integers(0, n, size=n_pairs)
    keep = i != j
    i, j = i[keep], j[keep]
    return np.einsum("ij,ij->i", unit[i], unit[j])


def sample_intra_inter(vectors, labels, n_pairs: int, rng):
    """Split sampled cosine similarities into same-label and different-label."""
    np = import_numpy()
    unit = normalize_rows(vectors.astype(np.float64))
    n = unit.shape[0]
    i = rng.integers(0, n, size=n_pairs * 2)
    j = rng.integers(0, n, size=n_pairs * 2)
    keep = i != j
    i, j = i[keep], j[keep]
    cosines = np.einsum("ij,ij->i", unit[i], unit[j])
    same = labels[i] == labels[j]
    return cosines[same], cosines[~same]


def within_subject_cosines(vectors, labels, subject: str, n_pairs: int, rng):
    """Sample cosines for random distinct pairs from one subject."""
    np = import_numpy()
    unit = normalize_rows(vectors.astype(np.float64))
    idx = np.where(labels == subject)[0]
    if len(idx) < 2:
        return np.asarray([], dtype=np.float64)

    i = rng.choice(idx, size=n_pairs)
    j = rng.choice(idx, size=n_pairs)
    keep = i != j
    i, j = i[keep], j[keep]
    return np.einsum("ij,ij->i", unit[i], unit[j])


def print_collection_summary(data, n_pairs: int, seed: int) -> None:
    """Print one-line cosine distribution summaries for each collection."""
    np = import_numpy()
    rng = np.random.default_rng(seed)
    header = (
        f"{'model':28s} {'mean':>7s} {'std':>7s} "
        f"{'intra':>7s} {'inter':>7s} {'gap':>7s}"
    )
    print()
    print(header)
    print("-" * len(header))
    for name, (vectors, labels) in data.items():
        cosines = sample_pair_cosines(vectors, n_pairs, rng)
        intra, inter = sample_intra_inter(vectors, labels, n_pairs, rng)
        print(
            f"{name:28s} {cosines.mean():7.3f} {cosines.std():7.3f} "
            f"{intra.mean():7.3f} {inter.mean():7.3f} "
            f"{intra.mean() - inter.mean():7.3f}"
        )


def plot_same_subject_grid(data, n_pairs: int, rng, out_path: Path) -> None:
    """Grid of same-subject histograms: rows=models, columns=subjects."""
    np = import_numpy()
    import matplotlib.pyplot as plt

    first_labels = next(iter(data.values()))[1]
    subjects = sorted(set(first_labels))
    nrows = max(len(data), 1)
    ncols = max(len(subjects), 1)
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(5 * ncols, 3.4 * nrows),
        sharex=True,
        sharey=True,
        squeeze=False,
    )

    for row, (name, (vectors, labels)) in enumerate(data.items()):
        for col, subject in enumerate(subjects):
            ax = axes[row][col]
            cosines = within_subject_cosines(vectors, labels, subject, n_pairs, rng)
            if len(cosines) == 0:
                ax.text(0.5, 0.5, "no pairs", ha="center", va="center")
                continue
            ax.hist(
                cosines,
                bins=40,
                range=(-1, 1),
                density=True,
                alpha=0.7,
                color=COLORS.get(name),
            )
            ax.axvline(0.0, color="black", lw=0.8, ls="--")
            ax.axvline(cosines.mean(), color="black", lw=1.5)
            ax.text(
                0.03,
                0.93,
                f"mean={cosines.mean():.2f}",
                transform=ax.transAxes,
                fontsize=9,
                va="top",
            )
            if row == 0:
                ax.set_title(subject, fontsize=12)
            if col == 0:
                ax.set_ylabel(f"{name}\n\ndensity", fontsize=9)

    for col in range(ncols):
        axes[-1][col].set_xlabel("cosine similarity")
    fig.suptitle("Same-subject pairs -- rows = models, columns = subjects", fontsize=13)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    print(f"Saved {out_path}")


def plot_anchor_same_vs_different(
    data,
    anchor_model: str,
    n_pairs: int,
    rng,
    out_path: Path,
) -> None:
    """Single-model same-vs-different plot that makes the gap easy to see."""
    import matplotlib.pyplot as plt

    if anchor_model not in data:
        print(f"!! Anchor model not available for plot: {anchor_model}")
        return

    vectors, labels = data[anchor_model]
    intra, inter = sample_intra_inter(vectors, labels, n_pairs, rng)
    gap = intra.mean() - inter.mean()

    plt.figure(figsize=(9, 5))
    plt.hist(
        inter,
        bins=50,
        range=(-1, 1),
        density=True,
        alpha=0.55,
        color="#999999",
        label=f"different subject   mean={inter.mean():.2f}",
    )
    plt.hist(
        intra,
        bins=50,
        range=(-1, 1),
        density=True,
        alpha=0.6,
        color=COLORS.get(anchor_model),
        label=f"same subject        mean={intra.mean():.2f}",
    )
    plt.axvline(0.0, color="black", lw=0.8, ls="--")
    plt.title(f"{anchor_model}: same vs different subject   (gap = {gap:.2f})")
    plt.xlabel("cosine similarity")
    plt.ylabel("density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    print(f"Saved {out_path}")


def plot_collections(data, n_pairs: int, seed: int, fig_dir: Path, show: bool) -> None:
    """Save the same cosine histograms as the classroom analysis script."""
    np = import_numpy()
    try:
        import matplotlib
    except ImportError as exc:
        raise RuntimeError(
            "matplotlib is required for --plot-collections. "
            "Run from the course virtualenv or install matplotlib."
        ) from exc

    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(seed)
    fig_dir.mkdir(parents=True, exist_ok=True)

    plot_same_subject_grid(
        data,
        n_pairs,
        rng,
        fig_dir / "cosine_same_subject_grid.png",
    )
    plot_anchor_same_vs_different(
        data,
        DEFAULT_ANCHOR_MODEL,
        n_pairs,
        rng,
        fig_dir / "cosine_minilm_same_vs_different.png",
    )

    overall_path = fig_dir / "cosine_overall.png"
    plt.figure(figsize=(9, 5))
    for name, (vectors, _labels) in data.items():
        cosines = sample_pair_cosines(vectors, n_pairs, rng)
        plt.hist(
            cosines,
            bins=60,
            range=(-1, 1),
            density=True,
            alpha=0.5,
            color=COLORS.get(name),
            label=f"{name}   mean={cosines.mean():.3f}",
        )
    plt.axvline(0.0, color="black", lw=0.8, ls="--")
    plt.xlabel("cosine similarity (random pairs)")
    plt.ylabel("density")
    plt.title("Pairwise cosine similarity by model")
    plt.legend()
    plt.tight_layout()
    plt.savefig(overall_path, dpi=120)
    print(f"Saved {overall_path}")

    intra_inter_path = fig_dir / "cosine_intra_inter.png"
    ncols = max(len(data), 1)
    fig, axes = plt.subplots(1, ncols, figsize=(5 * ncols, 4), sharex=True, sharey=True)
    axes = np.atleast_1d(axes)
    for ax, (name, (vectors, labels)) in zip(axes, data.items(), strict=True):
        intra, inter = sample_intra_inter(vectors, labels, n_pairs, rng)
        ax.hist(
            inter,
            bins=50,
            range=(-1, 1),
            density=True,
            alpha=0.55,
            color="#999999",
            label=f"different  mu={inter.mean():.2f}",
        )
        ax.hist(
            intra,
            bins=50,
            range=(-1, 1),
            density=True,
            alpha=0.6,
            color=COLORS.get(name),
            label=f"same      mu={intra.mean():.2f}",
        )
        ax.axvline(0.0, color="black", lw=0.8, ls="--")
        ax.set_title(name, fontsize=10)
        ax.set_xlabel("cosine similarity")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("density")
    fig.suptitle("Same-subject vs different-subject cosine similarity")
    plt.tight_layout()
    plt.savefig(intra_inter_path, dpi=120)
    print(f"Saved {intra_inter_path}")

    if show:
        plt.show()


def run_collection_analysis(args: argparse.Namespace) -> None:
    if args.explain_cosine:
        print_toy_cosine_demo()

    if not args.inspect_collections and not args.plot_collections:
        return

    output = args.output.expanduser().resolve()
    print(f"\n=== exported collection analysis ===")
    print(f"output: {output}\n")

    data = load_all_collections(output)
    if not data:
        print("No usable collections found.")
        return

    if args.inspect_collections:
        print_collection_summary(data, args.n_pairs, args.seed)
    if args.plot_collections:
        plot_collections(data, args.n_pairs, args.seed, args.fig_dir, args.show)


def l2_norm(vector: Iterable[float]) -> float:
    return math.sqrt(sum(value * value for value in vector))


def normalize(vector: list[float]) -> list[float]:
    norm = l2_norm(vector)
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    left_unit = normalize(left)
    right_unit = normalize(right)
    return sum(a * b for a, b in zip(left_unit, right_unit, strict=True))


def embed_with_cluster_api(
    texts: list[str],
    model_name: str,
    base_url: str,
    api_token: str | None = None,
    timeout_seconds: int = 120,
) -> list[list[float]]:
    """Embed text with the SupportVectors classroom API."""
    url = f"{base_url.rstrip('/')}/embed-text/v1/embeddings"
    payload = json.dumps({"model": model_name, "input": texts}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    req = request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Embedding API HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach embedding API at {url}: {exc}") from exc

    parsed = json.loads(body)
    return [item["embedding"] for item in parsed["data"]]


def embed_with_fine_tuned_model(
    texts: list[str],
    model_path: str,
    batch_size: int = 16,
) -> list[list[float]]:
    """Embed text with a local fine-tuned SentenceTransformer checkpoint."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "sentence-transformers is not installed in this Python environment. "
            "Run this from the course virtualenv or install sentence-transformers."
        ) from exc

    path = Path(model_path).expanduser()
    if not path.is_dir():
        raise RuntimeError(f"Fine-tuned model path does not exist: {path}")

    model = SentenceTransformer(str(path))
    vectors = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return [vector.tolist() for vector in vectors]


def is_sentence_transformer_checkpoint(path: Path) -> bool:
    """Return True when a directory looks like a SentenceTransformer model."""
    return (
        path.is_dir()
        and (path / "modules.json").exists()
        and (
            (path / "config_sentence_transformers.json").exists()
            or any(path.glob("*_Pooling"))
            or any(path.glob("*_Transformer"))
        )
    )


def find_exported_vectors_dir(path: Path) -> Path | None:
    """Find a projector export dir containing vectors.tsv and metadata.tsv."""
    if (path / "vectors.tsv").exists() and (path / "metadata.tsv").exists():
        return path

    if path.is_dir():
        for child in sorted(path.iterdir()):
            if child.is_dir() and (child / "vectors.tsv").exists() and (
                child / "metadata.tsv"
            ).exists():
                return child

    return None


def resolve_fine_tuned_model_path(raw_path: str) -> str:
    """Return a loadable checkpoint path, or an empty string with a warning."""
    if not raw_path:
        return ""

    path = Path(raw_path).expanduser()

    if is_sentence_transformer_checkpoint(path):
        return str(path)

    exported_dir = find_exported_vectors_dir(path)
    if exported_dir is not None:
        print()
        print("Skipping fine-tuned model.")
        print(f"  Provided path: {path}")
        print(f"  Detected exported vectors: {exported_dir}")
        print("  This contains metadata.tsv/vectors.tsv for old texts, not a model.")
        print("  To embed new sentences, provide the checkpoint directory instead.")
        print("  A checkpoint usually contains modules.json and 0_Transformer/.")
        return ""

    if not path.exists():
        print()
        print("Skipping fine-tuned model.")
        print(f"  Path does not exist: {path}")
        return ""

    print()
    print("Skipping fine-tuned model.")
    print(f"  Path is not a recognized SentenceTransformer checkpoint: {path}")
    print("  Expected files include modules.json and config_sentence_transformers.json.")
    return ""


def score_model(name: str, vectors: list[list[float]]) -> ModelResult:
    if len(vectors) != 3:
        raise ValueError(f"Expected exactly 3 vectors, got {len(vectors)}")
    return ModelResult(
        name=name,
        cos_12=cosine(vectors[0], vectors[1]),
        cos_13=cosine(vectors[0], vectors[2]),
        cos_23=cosine(vectors[1], vectors[2]),
    )


def print_result(result: ModelResult) -> None:
    verdict = "PASS" if result.expected_pair_wins else "CHECK"
    print(f"\n{result.name}")
    print("-" * len(result.name))
    print(f"cos(1,2) = {result.cos_12:.4f}")
    print(f"cos(1,3) = {result.cos_13:.4f}")
    print(f"cos(2,3) = {result.cos_23:.4f}")
    print(
        "panda relation cos(2,3) > cos(1,3): "
        f"{'YES' if result.panda_relation_detected else 'NO'}"
    )
    print(
        "punctuation trap avoided cos(2,3) > cos(1,2): "
        f"{'YES' if result.punctuation_trap_avoided else 'NO'}"
    )
    print(f"expected pair 2-3 highest overall: {verdict}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Projector export root containing subjects/ and subjects_finetuned/. "
        f"Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--inspect-collections",
        action="store_true",
        help="Load exported vectors.tsv/metadata.tsv and print cosine summaries.",
    )
    parser.add_argument(
        "--explain-cosine",
        action="store_true",
        help="Print a tiny toy-vector demo: cosine measures direction, not length.",
    )
    parser.add_argument(
        "--plot-collections",
        action="store_true",
        help="Save cosine histogram PNGs for the exported collections.",
    )
    parser.add_argument(
        "--only-collections",
        action="store_true",
        help="Run only local collection analysis; skip the three-sentence embed test.",
    )
    parser.add_argument(
        "--n-pairs",
        type=int,
        default=20_000,
        help="Random pair count for collection cosine analysis.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--fig-dir",
        type=Path,
        default=DEFAULT_FIG_DIR,
        help=f"Directory for --plot-collections PNG output. Default: {DEFAULT_FIG_DIR}",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show matplotlib windows when plotting collections.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("EMBED_BASE_URL", DEFAULT_EMBED_BASE_URL),
        help="SupportVectors embed API base URL.",
    )
    parser.add_argument(
        "--api-token",
        default=os.environ.get("EMBED_API_TOKEN"),
        help="Optional bearer token for the embed API. Defaults to EMBED_API_TOKEN.",
    )
    parser.add_argument(
        "--fine-tuned-model-path",
        default=DEFAULT_FINE_TUNED_MODEL_PATH,
        help="Optional local SentenceTransformer checkpoint path.",
    )
    parser.add_argument(
        "--skip-cluster",
        action="store_true",
        help="Skip BERT/MiniLM API calls and only run local fine-tuned model if provided.",
    )
    parser.add_argument(
        "--include-comma-variant",
        action="store_true",
        help="Also print the classroom screenshot's possible 'Eats shoots, and leaves.' variant.",
    )
    return parser.parse_args()


def run_case(texts: list[str], args: argparse.Namespace, title: str) -> None:
    print(f"\n=== {title} ===")
    for index, text in enumerate(texts, start=1):
        print(f"{index}. {text}")

    if not args.skip_cluster:
        for name, model_name in CLUSTER_MODELS.items():
            vectors = embed_with_cluster_api(
                texts=texts,
                model_name=model_name,
                base_url=args.base_url,
                api_token=args.api_token,
            )
            print_result(score_model(name, vectors))

    if args.fine_tuned_model_path:
        vectors = embed_with_fine_tuned_model(
            texts=texts,
            model_path=args.fine_tuned_model_path,
        )
        print_result(score_model("Fine-tuned (384d)", vectors))


def main() -> None:
    args = parse_args()
    run_collection_analysis(args)

    if args.only_collections:
        return

    args.fine_tuned_model_path = resolve_fine_tuned_model_path(
        args.fine_tuned_model_path
    )
    run_case(TEXTS, args, "standard punctuation test")

    if args.include_comma_variant:
        comma_variant = [
            "Eats, shoots, and leaves.",
            "Eats shoots, and leaves.",
            "A panda eats bamboo shoots and leaves.",
        ]
        run_case(comma_variant, args, "possible screenshot comma variant")


if __name__ == "__main__":
    main()
