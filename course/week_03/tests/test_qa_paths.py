from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


path1 = load_module("path1_page_image_qa", "path1_page_image_qa.py")
path2 = load_module("path2_text_chunk_qa", "path2_text_chunk_qa.py")
ui = load_module("qa_compare_app", "qa_compare_app.py")


def test_path1_defaults_to_colqwen3_model_id():
    assert path1.DEFAULT_MODEL_ID == "TomoroAI/tomoro-colqwen3-embed-4b"


def test_path1_parser_exposes_colqwen3_backend():
    args = path1.parse_args(
        [
            "What is PRML?",
            "--retrieval-backend",
            "colqwen3",
            "--retrieval-model",
            path1.DEFAULT_MODEL_ID,
        ]
    )

    assert args.retrieval_backend == "colqwen3"
    assert args.retrieval_model == path1.DEFAULT_MODEL_ID


def test_ui_builds_path_commands_with_question_and_outputs():
    path1_command = ui.build_path1_command(
        question="What is PRML?",
        pdf=Path("course/week_03/PRML.pdf"),
        pages_dir=Path("course/week_03/data/pages"),
        output=Path("course/week_03/runs/path1.json"),
        top_k=3,
        max_pages=10,
        retrieval_backend="colqwen3",
        retrieval_model=path1.DEFAULT_MODEL_ID,
        vision_model="gpt-4.1-mini",
    )
    path2_command = ui.build_path2_command(
        question="What is PRML?",
        pdf=Path("course/week_03/PRML.pdf"),
        textbook=Path("course/week_03/textbook/PRML.textbook.md"),
        output=Path("course/week_03/runs/path2.json"),
        top_k=5,
        chunk_words=350,
        overlap_words=60,
        embedding_model="text-embedding-3-small",
        answer_model="gpt-4.1-mini",
    )

    assert "path1_page_image_qa.py" in path1_command
    assert "--retrieval-backend colqwen3" in path1_command
    assert "TomoroAI/tomoro-colqwen3-embed-4b" in path1_command
    assert "path2_text_chunk_qa.py" in path2_command
    assert "--textbook course/week_03/textbook/PRML.textbook.md" in path2_command


def test_chunk_words_uses_overlap_and_word_offsets():
    chunks = path2.chunk_words(
        "one two three four five six seven",
        source="book.md",
        chunk_words=3,
        overlap_words=1,
    )

    assert [chunk.text for chunk in chunks] == [
        "one two three",
        "three four five",
        "five six seven",
    ]
    assert [(chunk.start_word, chunk.end_word) for chunk in chunks] == [
        (0, 3),
        (2, 5),
        (4, 7),
    ]


def test_retrieve_chunks_ranks_by_cosine_with_fake_embeddings(monkeypatch):
    chunks = [
        path2.Chunk(0, "alpha topic", "book.md", 0, 2),
        path2.Chunk(1, "beta topic", "book.md", 2, 4),
        path2.Chunk(2, "gamma topic", "book.md", 4, 6),
    ]

    def fake_embed_texts(_client, texts, model, batch_size):
        del model, batch_size
        mapping = {
            "alpha topic": [1.0, 0.0],
            "beta topic": [0.0, 1.0],
            "gamma topic": [0.7, 0.7],
            "find beta": [0.0, 1.0],
        }
        return np.asarray([mapping[text] for text in texts], dtype=np.float32)

    monkeypatch.setattr(path2, "embed_texts", fake_embed_texts)

    retrieved = path2.retrieve_chunks(
        client=object(),
        question="find beta",
        chunks=chunks,
        embedding_model="fake",
        top_k=2,
        batch_size=8,
    )

    assert [item.chunk_id for item in retrieved] == [1, 2]
    assert retrieved[0].rank == 1
    assert retrieved[0].score > retrieved[1].score


def test_existing_page_images_ignores_empty_files_and_sorts(tmp_path):
    (tmp_path / "page_0002.png").write_bytes(b"not really a png")
    (tmp_path / "page_0001.png").write_bytes(b"not really a png")
    (tmp_path / "page_0003.png").write_bytes(b"")
    (tmp_path / "notes.txt").write_text("ignore me")

    pages = path1.existing_page_images(tmp_path)

    assert [page.name for page in pages] == ["page_0001.png", "page_0002.png"]


def test_retrieve_pages_uses_page_number_from_filename(monkeypatch, tmp_path):
    image_12 = tmp_path / "page_0012.png"
    image_2 = tmp_path / "page_0002.png"
    for path in [image_12, image_2]:
        Image.new("RGB", (8, 8), color="white").save(path)

    class FakeClipModel:
        def encode(self, values, **_kwargs):
            first = values[0]
            if isinstance(first, Image.Image):
                return np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
            return np.asarray([[1.0, 0.0]], dtype=np.float32)

    monkeypatch.setattr(path1, "load_clip_model", lambda _name: FakeClipModel())

    retrieved = path1.retrieve_pages(
        question="find first image",
        image_paths=[image_12, image_2],
        retrieval_model="fake",
        top_k=1,
        batch_size=2,
        retrieval_backend="sentence-transformers",
    )

    assert retrieved[0].page == 12
    assert retrieved[0].image_path == str(image_12)


def test_image_to_data_url_returns_jpeg_data_url_and_removes_temp_file(tmp_path):
    image_path = tmp_path / "page_0001.png"
    Image.new("RGB", (20, 20), color="white").save(image_path)

    data_url = path1.image_to_data_url(image_path, max_side=10)

    assert data_url.startswith("data:image/jpeg;base64,")
    assert not image_path.with_suffix(".qa_resized.jpg").exists()


def test_answer_from_chunks_sends_chunk_context_to_responses_api():
    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="answer")

    fake_client = SimpleNamespace(responses=FakeResponses())
    retrieved = [
        path2.RetrievedChunk(
            rank=1,
            score=0.99,
            chunk_id=7,
            source="book.md",
            text="Evidence about latent variables.",
        )
    ]

    answer = path2.answer_from_chunks(
        client=fake_client,
        question="What are latent variables?",
        retrieved=retrieved,
        answer_model="fake-model",
    )

    prompt = captured["input"][0]["content"][0]["text"]
    assert answer == "answer"
    assert captured["model"] == "fake-model"
    assert "[chunk 7" in prompt
    assert "Evidence about latent variables." in prompt


def test_answer_from_pages_sends_page_labels_and_images(monkeypatch, tmp_path):
    image_path = tmp_path / "page_0004.png"
    Image.new("RGB", (20, 20), color="white").save(image_path)
    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="visual answer")

    fake_client = SimpleNamespace(responses=FakeResponses())
    retrieved = [
        path1.RetrievedPage(
            rank=1,
            score=0.88,
            page=4,
            image_path=str(image_path),
        )
    ]

    answer = path1.answer_from_pages(
        client=fake_client,
        question="What is shown?",
        retrieved=retrieved,
        vision_model="fake-vision",
        max_image_side=10,
    )

    content = captured["input"][0]["content"]
    assert answer == "visual answer"
    assert captured["model"] == "fake-vision"
    assert any(item.get("type") == "input_text" and "page 4" in item.get("text", "") for item in content)
    assert any(item.get("type") == "input_image" for item in content)
