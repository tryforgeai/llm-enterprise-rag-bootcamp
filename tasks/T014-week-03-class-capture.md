# T014 Week 03 Class Capture

Status: done

Date: 2026-06-20

## Goal

Capture Week 03 material on chunking as an irreversible representation decision, chunking failure modes, contextual and late chunking, page-image retrieval, and representation tournaments.

## Working File

`course/week_03/week-03.zh.md`

## Source

`course/week_03/week-3-summer-lesson-plan.pdf`

## Done Criteria

- [x] Lesson-plan PDF is read and summarized.
- [x] Core concepts and failure modes are recorded.
- [x] Better-chunking and no-chunking routes are distinguished.
- [x] One agent capability is identified.
- [x] Avaloka retrieval implications are recorded.
- [x] Follow-up questions are captured.
- [x] Classroom screenshots and related video discussion are added.
- [x] Punctuation-sensitive embedding test script is created.
- [x] Classroom discussion, code, or lab results are added.
- [x] At least one Week 03 eval artifact is created.

## 2026-06-20 Update

Created the first Week 03 record from the lesson-plan PDF:

- chunking as an ontological decision rather than harmless preprocessing
- first projection / embedding as irreversible information loss
- mixing principle and centroid delusion
- failure modes: broken endophora, discourse severing, negation/scope traps, definition-use chains, bridging inference, genre blindness, and embedding-space distortion
- chunking taxonomy: fixed, recursive, semantic, hierarchical, contextual, and late chunking
- page-image retrieval with ColPali-style late interaction as an alternative to parse-and-chunk
- representation tournament as the evidence-driven way to choose a decomposition strategy
- Avaloka implication: Care Card and wisdom retrieval need explicit representation and metadata tests before embeddings or richer retrieval are added

## 2026-06-20 Classroom / Video Additions

Added today's discussion notes to `course/week_03/week-03.zh.md`:

- why small chunks are pure but can forget referents, conditions, scope, and safety boundaries
- examples from screenshots: broken endophora, discourse relation failure, negation/scope traps, bridging inference, genre blindness, centroid delusion, query-chunk asymmetry, and punctuation-sensitive meaning
- RAG-is-dead clarification from Jeff Huber / Chroma and Kuba Rogut / Turbopuffer: naive top-k vector RAG is the failed pattern; retrieval is evolving into context engineering and agentic search
- current Codex context model: not automatic vault-level RAG, but LLM + conversation context + explicit tool retrieval
- Loop Engineer connection: recurring agent loops need durable project memory, triggers, verification, and logs; this project already has the seed structure through `tasks/`, `docs/`, `course/`, `traces/`, `evals/`, and the decision log

## 2026-06-20 Code Addition

Created `course/week_03/punctuation_embedding_test.py`:

- compares the three `Eats, shoots, and leaves` variants with cosine similarity
- calls the SupportVectors classroom embedding API for BERT and MiniLM when run
- optionally runs a local fine-tuned SentenceTransformer checkpoint if `--fine-tuned-model-path` or `SUBJECT_FINETUNED_MODEL_PATH` is provided
- supports `EMBED_BASE_URL` and `EMBED_API_TOKEN`
- includes `--include-comma-variant` for the possible classroom screenshot variant
- syntax check passed with project Python and pycache redirected to `/private/tmp`

## 2026-06-20 Code Update

Updated `course/week_03/punctuation_embedding_test.py` using the cosine histogram script as the reference pattern:

- added `COLLECTION_PATHS` and default output discovery for the three exported Week 1 projector collections
- added local-only `--inspect-collections`, `--plot-collections`, and `--only-collections` modes
- reused the cosine summary idea: random-pair mean/std plus same-subject vs different-subject gap
- kept exported `vectors.tsv` analysis separate from new sentence embedding, because exported vectors cannot embed new text
- added a dimension mismatch warning; the current fine-tuned export is labeled `384d` but loads as `768d`

## 2026-06-20 Cosine Notebook Alignment

Refined `course/week_03/punctuation_embedding_test.py` after reviewing the classroom cosine-similarity notebook:

- added `--explain-cosine` for the toy vector demo: same direction, perpendicular, and opposite
- added same-subject grid plotting across models and subjects
- added MiniLM anchor same-vs-different plotting to make the gap visually obvious
- kept the three-model same-vs-different comparison and one-line gap summary
- configured Matplotlib cache to use a writable temp directory in local Codex runs

## 2026-06-20 Punctuation API Result

Recorded the SupportVectors API run in `course/week_03/week-03.zh.md`:

- BERT: `cos(1,2)=0.9041`, `cos(1,3)=0.7610`, `cos(2,3)=0.7908`
- MiniLM: `cos(1,2)=0.9231`, `cos(1,3)=0.4605`, `cos(2,3)=0.5065`
- both models detect that the panda sentence is closer to the no-comma eating sentence than to the comma action-list sentence
- both models still rank sentence 1 and sentence 2 highest, so lexical overlap beats punctuation-controlled syntax
- script verdict was refined to report these two checks separately

## 2026-06-20 PDF To Textbook Script

Created `course/week_03/pdf_to_textbook.py` for the Path #2 experiment:

- implements `PDF -> parser -> text/Markdown textbook`
- defaults to `course/week_03/PRML.pdf`
- prefers Docling when installed, because it can preserve richer document structure
- falls back to `pypdf` for plain page text extraction
- supports `--engine auto|docling|pypdf`, `--format md|txt`, `--max-pages`, and `--out-dir`
- smoke-tested PRML first three pages with `pypdf`

## 2026-06-20 Representation Tournament QA Scripts

Created two separate PRML QA scripts:

- `course/week_03/path1_page_image_qa.py`: `PDF -> page images -> CLIP-like page retrieval -> OpenAI vision answer`
- `course/week_03/path2_text_chunk_qa.py`: `PDF/textbook -> chunks -> OpenAI text embeddings -> OpenAI text answer`
- both scripts read `OPENAI_API_KEY` from the project root `.env` without printing it
- both scripts save run JSON under `course/week_03/runs/`
- syntax and help checks passed without live API calls
- local machine still needs a full PDF renderer dependency such as `pymupdf` for complete Path #1 page-image extraction

## 2026-06-20 QA Script Unit Tests

Added `course/week_03/tests/test_qa_paths.py`:

- tests text chunk overlap and word offsets
- tests text retrieval ranking with fake embeddings
- tests page image discovery and filtering
- tests page-image retrieval preserves page numbers from filenames such as `page_0012.png`
- tests image data URL generation and temporary file cleanup
- tests OpenAI request payload construction for both chunk QA and page-image QA without making network calls
- fixed Path #1 page-number reporting to parse the page number from the image filename
- local checks passed: script `py_compile` and `pytest course/week_03/tests/test_qa_paths.py`
- live OpenAI smoke test was not run because external disclosure of local PRML/workspace content requires separate explicit approval

## 2026-06-20 ColQwen3 And Comparison UI

Updated Path #1 and added an interactive comparison UI:

- Path #1 now defaults to `DEFAULT_MODEL_ID = "TomoroAI/tomoro-colqwen3-embed-4b"`
- added `--retrieval-backend colqwen3|sentence-transformers`
- added ColQwen3-style multi-vector late-interaction scoring for page-image retrieval
- kept the old SentenceTransformer/CLIP path as a baseline backend
- added `course/week_03/qa_compare_app.py` Streamlit UI to run Path #1 and Path #2 side by side
- UI shows commands, answers, retrieved pages/chunks, and run JSON paths
- unit tests expanded to cover default model, backend parsing, and UI command construction
- local checks passed: `pytest course/week_03/tests/test_qa_paths.py` reports 10 tests passing
- Streamlit UI started at `http://localhost:8503`

## 2026-06-20 Page Image Data Check

Verified `course/week_03/data/pages` for PRML:

- `PRML.pdf` has 749 pages
- `data/pages` contains 749 PNG files
- filenames are continuous from `page_0001.png` through `page_0749.png`
- no missing page numbers, no extra page numbers, no empty files, and no unreadable PNGs
- updated Path #1 and the comparison UI to default to `course/week_03/data/pages`
- local checks passed again: `pytest course/week_03/tests/test_qa_paths.py` reports 10 tests passing

## 2026-06-20 In-Person Lab Audit

Inspected `course/week_03/week-03-in-person-lab`:

- lab is a standalone visual-vs-text retrieval comparison for PRML
- Team 1 builds page-image retrieval with CLIP and SigLIP2
- Team 2 builds text chunk retrieval with MiniLM sentence-transformer embeddings
- `compare.py` compares CLIP and SigLIP2 from the command line
- `app.py` provides a Gradio UI comparing CLIP, SigLIP2, and Text/MiniLM retrieval side by side
- existing `data/pages` contains 749 continuous PRML page PNGs
- existing FAISS metadata covers 749 CLIP page vectors, 749 SigLIP2 page vectors, and 4,636 text chunks through page 749
- Python syntax checks passed for `utils.py`, `team1_visual.py`, `team2_text.py`, `compare.py`, and `app.py`
- current global `python3` environment is missing the lab runtime dependencies (`faiss`, `torch`, `transformers`, `sentence_transformers`, `pdf2image`, `pdfplumber`, `gradio`, `PIL`, `numpy`), so the lab needs its requirements installed or a prepared virtual environment before it can run locally
- Poppler is installed at `/opt/homebrew/bin/pdftoppm`

## 2026-06-20 Capstone Contextual Chunking

Created `course/week_03/contextual_chunk_pdf.py` and processed a local capstone source PDF (not committed):

- extracted 213 PDF pages, with text on 203 pages
- generated 266 regular overlapping chunks
- generated 266 contextual chunks with local document title, page range, section hint, and keyword context prefix
- wrote outputs to `course/week_03/capstone_contextual_chunks/`
- output files: `regular_chunks.jsonl`, `contextual_chunks.jsonl`, `stats.json`, and `preview.md`
- implementation is deterministic and does not call an external LLM or network API

## 2026-06-22 Progress Summary

Added a `本周进度总览` section to `course/week_03/week-03.zh.md`:

- summarized the Week 03 learning arc from naive chunking to representation design
- listed mastered concepts: small chunk amnesia, centroid delusion, semantic/neural chunking, contextual chunking, late chunking, page-image retrieval, and representation tournaments
- summarized completed artifacts: punctuation embedding test, PRML QA paths, Streamlit comparison UI, in-person lab audit, and capstone contextual chunks
- recorded the remaining gap: create one Week 03 eval artifact / representation tournament

## 2026-06-27 QA Pair Embedding Demo

Created `course/week_04/qa_pair_embedding_demo/` as a standalone UI artifact:

- demonstrates the Berlin paragraph as one source chunk
- extracts five self-contained factoids
- creates five generated QA-pair index records with pointers back to the source chunk
- runs an offline cosine-search demo over query-shaped QA records versus the whole-paragraph baseline
- shows that the query "What is the capital of Germany?" retrieves `qa_f2`, while "What is Germany's most populous city?" retrieves `qa_f3`
- includes the SupportVectors cluster embedding payload for replacing the transparent demo embedding with real `Qwen/Qwen3-Embedding-0.6B` vectors
- verified in Chrome at desktop and mobile widths with no console errors

Added `course/week_04/prml-chapter-selection.md`:

- selected PRML Chapter 2, `Probability Distributions`, for the abstractive summarization experiment
- selected PRML Chapter 3, `Linear Models for Regression`, as the paired chapter
- recorded approximate book/PDF page ranges, rationale, important topics, summary targets, and planned retrieval artifacts

Extracted full PRML chapter text into Week 04 Markdown files:

- `course/week_04/prml_chapter_02_probability_distributions.md`
- `course/week_04/prml_chapter_03_linear_models_for_regression.md`
- Chapter 2 extraction covers PDF pages 86-155 with 70 page markers
- Chapter 3 extraction covers PDF pages 156-196 with 41 page markers
- each file preserves source metadata and `## PDF Page ...` boundaries for later chunking and summarization

## 2026-07-18 Governance Closeout

Marked this task done because every stated done criterion is satisfied. Week 03 has durable notes, code experiments, representation comparisons, tests, an eval artifact, Avaloka implications, and follow-up questions. Later Week 04 work remains tracked separately rather than keeping the Week 03 capture task artificially open.
