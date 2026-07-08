# SupportVectors Classroom Environment

Status: accepted

Date: 2026-06-13

## Context

Week 02 requires a consistent Python environment for AI, embedding, Transformer, and RAG labs. SupportVectors provides an `ai_environment` configurator based on `uv` and Python 3.12.

The stock configurator attempted to download another Python version, encountered an enterprise TLS certificate error, and continued after failed commands. Its generated `.env` also used the old `PROJECT_ROOT_DIR` name and a fake OpenAI key.

## Decision

Use an isolated classroom project at `labs/sv-ai-course-lab` with:

- `uv`
- Python 3.12.7
- `svlearn-bootcamp`
- the generated `src/`, tests, and MkDocs structure
- `uv.lock` as the reproducibility record
- macOS native TLS for dependency downloads

Use `BOOTCAMP_ROOT_DIR`, keep API keys empty by default, and require explicit self-test and build verification after setup.

## Consequences

- Course experiments have a stable environment separate from notes and Avaloka production code.
- The project includes a large transitive AI/ML dependency set, so new packages should still be added only when a lab requires them.
- The configurator's final success message is not treated as proof of successful setup.
- Real API keys remain local and uncommitted.

## Affected Files

- `labs/sv-ai-course-lab/`
- `labs/02-sv-ai-environment-setup.md`
- `tasks/T012-setup-sv-ai-environment.md`
- `tasks/index.md`
- `docs/decisions/decision-log.md`
- `docs/product/version-roadmap.md`

## Follow-Up Checks

- Run the environment self-test before the next coding lab.
- Add lab-specific packages through `uv add`.
- Rebuild documentation after adding notebooks.

