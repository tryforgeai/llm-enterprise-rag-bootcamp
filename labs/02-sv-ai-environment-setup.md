# SupportVectors AI Environment Setup

Date: 2026-06-13

Status: verified

Working project: `labs/sv-ai-course-lab`

Source guide: `SV AI Environment Setup.pdf`

## What The Environment Provides

- Python 3.12.7
- `uv` dependency and virtual-environment management
- isolated `.venv`
- `svlearn-bootcamp` and its AI/ML dependencies
- PyTorch, Transformers, scikit-learn, Jupyter, OpenAI SDK, and related libraries
- `src/` package structure and `tests/`
- MkDocs documentation structure
- reproducible dependency lockfile

## Standard Workflow From The Guide

```text
clone ai_environment
-> uv init a Python 3.12 project
-> copy ensure_config.sh and docs.tgz
-> run ensure_config.sh
-> provide module and project metadata
-> install dependencies
-> build and test
```

## Machine-Specific Adaptations

### Use The Existing Python 3.12.7

The generated `.python-version` initially contained `3.12`. That made `uv` try to download a newer Python build even though Python 3.12.7 was already installed locally.

The project now pins:

```text
3.12.7
```

### Use Native TLS

The first dependency request failed with `UnknownIssuer` because the default certificate bundle did not include the local enterprise certificate chain.

The secure fix is:

```bash
uv --native-tls sync
```

This uses the macOS trusted certificate store. TLS verification remains enabled.

### Use BOOTCAMP_ROOT_DIR

The PDF requires changing:

```text
PROJECT_ROOT_DIR
```

to:

```text
BOOTCAMP_ROOT_DIR
```

The generated `.env` has been corrected.

### Keep API Keys Empty

The configurator writes a fake OpenAI key placeholder. It was replaced with an empty value. A real key should be added only when a lab requires it and must never be committed.

### Configurator Failure Behavior

`ensure_config.sh` does not stop when `uv` fails. It can print `SETUP COMPLETE` even when dependencies and tests did not run successfully.

Always verify independently:

```bash
uv run python src/test_setup.py
uv build
uv run mkdocs build
```

## Daily Use

```bash
cd "labs/sv-ai-course-lab"
source .env
uv --native-tls sync
uv run python src/test_setup.py
```

If `uv` is not found in a non-interactive shell, use:

```bash
~/.local/bin/uv
```

## Verification Result

- Python: 3.12.7
- `svlearn-bootcamp`: 0.1.7
- PyTorch: 2.12.0
- Transformers: 5.12.0
- scikit-learn: 1.9.0
- environment self-test: passed
- Python source and wheel build: passed
- MkDocs build: passed with upstream deprecation and offline-CDN warnings

## Learning

The environment is reproducible because the Python version, dependency declarations, and `uv.lock` are explicit. A successful setup message is not enough; import, build, and documentation checks are part of the setup contract.
