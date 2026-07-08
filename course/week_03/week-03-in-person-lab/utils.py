import json
import pathlib
import faiss
import numpy as np


DATA_DIR = pathlib.Path("data")
PAGES_DIR = DATA_DIR / "pages"
INDICES_DIR = DATA_DIR / "indices"


def ensure_dirs():
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    INDICES_DIR.mkdir(parents=True, exist_ok=True)


def save_faiss_index(index: faiss.Index, path: str):
    faiss.write_index(index, str(path))


def load_faiss_index(path: str) -> faiss.Index:
    return faiss.read_index(str(path))


def save_meta(meta: list, path: str):
    with open(path, "w") as f:
        json.dump(meta, f)


def load_meta(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype(np.float32))
    return index


def l2_normalize(vecs: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return vecs / norms
