# SV Cluster Access

A Python client library for SupportVectors-hosted AI services: text and image embeddings, text chat, and vision-language (VL) chat completions. Part of the SupportVectors AI bootcamp training material.

---

## Project Structure

```
sv_ray_cluster_access/
├── src/
│   ├── ray_cluster_access/
│   │   ├── __init__.py                 # Loads config.yaml via svlearn-bootcamp
│   │   └── sv_cluster_access_api.py    # Embeddings and chat (text + VL)
│   └── test_setup.py                   # Verifies environment and configuration
├── config.yaml                         # Service base URLs
├── pyproject.toml                      # Package metadata and dependencies
├── .env.example                        # Template for required environment variables
└── docs/                               # MkDocs site assets and notebooks
```

---

## Module Overview

| Component | Purpose |
|-----------|---------|
| `sv_cluster_access_api` | Text and multimodal embeddings; text chat (`openai/gpt-oss-20b`, or `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`); VL chat (`Qwen/Qwen3-VL-8B-Instruct`) with text + image messages |

Chat uses a single vLLM host and port. Embeddings use a separate port on the same machine.

---

## Prerequisites

- **Python >= 3.12**
- **[uv](https://docs.astral.sh/uv/)** (recommended package/project manager)
- Network access to the SupportVectors cluster (services run on private IPs)

---

## Installation

1. **Clone the repository** and `cd` into this project folder.

2. **Create the `.env` file** from the template and fill in your paths:

   ```bash
   cp .env.example .env
   # Edit .env — see "Environment Variables" below
   ```

3. **Install dependencies** with `uv`:

   ```bash
   uv sync
   ```

   This installs the two direct dependencies declared in `pyproject.toml`:
   - `litellm` — unified `completion()` interface across LLM providers
   - `svlearn-bootcamp` — `ConfigurationMixin` for loading `config.yaml`

4. **Verify the setup** (optional):

   ```bash
   uv run python src/test_setup.py
   ```

   This script prints your Python version, working directory, relevant environment variables, and confirms the `ray_cluster_access` package can be imported.

---

## Configuration

### Environment Variables (`.env`)

Copy `.env.example` and set these values for your machine:

| Variable | Purpose |
|----------|---------|
| `BOOTCAMP_ROOT_DIR` | Absolute path to this project folder. Used by `svlearn-bootcamp` to locate `config.yaml`. |
| `PROJECT_PYTHON` | Path to the virtual environment's Python interpreter (e.g. `.venv/bin/python`). |
| `PYTHONPATH` | Should include `src/` so that `ray_cluster_access` is importable. |
| `OPENAI_API_KEY` | Your OpenAI API key (needed only for direct OpenAI calls; the SV cluster uses a placeholder key). |

### Service URLs (`config.yaml`)

```yaml
cluster_access_api:
  embed_base_url: http://10.0.10.51:8123   # Embedding service
  chat_base_url:  http://10.0.10.51:8000   # Chat (vLLM, OpenAI-compatible /v1)
```

Loaded at import time by `ray_cluster_access/__init__.py` via `ConfigurationMixin` and `python-dotenv`.

---

## API Reference (`sv_cluster_access_api`)

### Text Embeddings

**Endpoint:** `POST {embed_base_url}/embed-text/v1/embeddings`

**Function:** `embed_text(data_sentences, model_name, batch_size=50)`

- **`data_sentences`** — list of strings to embed.
- **`model_name`** — e.g. `"sentence-transformers/all-MiniLM-L6-v2"`.
- **`batch_size`** — inputs per API call (default 50).
- **Returns:** `list[list[float]]` — one vector per input string.

```python
from ray_cluster_access.sv_cluster_access_api import embed_text

texts = ["Hello, world!", "Another sentence."]
embeddings = embed_text(texts, model_name="sentence-transformers/all-MiniLM-L6-v2")
```

---

### Image / Multimodal Embeddings

**Endpoint:** `POST {embed_base_url}/embed-image/v1/embeddings`

**Function:** `embed_image(data_images, data_texts, model_name, batch_size=50)`

- **`data_images`** — HTTP/HTTPS URLs or local file paths (sent as base64).
- **`data_texts`** — companion text strings (may be empty).
- **`model_name`** — e.g. `"google/siglip2-base-patch16-224"` or `"onnxmodelzoo/arcfaceresnet100-11-int8"`.
- **Returns:** embeddings ordered as `[image_1, …, image_n, text_1, …, text_m]`.

```python
from ray_cluster_access.sv_cluster_access_api import embed_image

embeddings = embed_image(
    ["https://example.com/photo.png", "path/to/local.jpg"],
    ["A short caption"],
    model_name="google/siglip2-base-patch16-224",
)
```

Image-only (ONNX):

```python
embeddings = embed_image(
    data_images=["img1.png", "img2.png"],
    data_texts=[],
    model_name="onnxmodelzoo/arcfaceresnet100-11-int8",
)
```

---

### Chat Completions

**Endpoint:** `{chat_base_url}/v1` (OpenAI-compatible)

| Function | Description |
|----------|-------------|
| `get_sv_openai_client()` | Pre-configured `OpenAI` client for the vLLM server. |
| `sv_openai_completion(model=..., **kwargs)` | OpenAI `chat.completions.create`; default model is text chat. |
| `sv_completion(model=..., **kwargs)` | Same via LiteLLM `completion()`. |

**Chat models** (module constants; pass `model=` to override the default):

| Constant | Value | Use |
|----------|-------|-----|
| `DEFAULT_TEXT_CHAT_MODEL` | `openai/gpt-oss-20b` | Default text-only chat |
| `ALTERNATIVE_TEXT_CHAT_MODEL` | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | Optional text chat (same vLLM host) |
| `DEFAULT_VL_CHAT_MODEL` | `Qwen/Qwen3-VL-8B-Instruct` | Text + image chat |

**Text chat:**

```python
from ray_cluster_access.sv_cluster_access_api import sv_openai_completion

response = sv_openai_completion(
    messages=[{"role": "user", "content": "Why is the sky blue?"}]
)
print(response.choices[0].message.content)
```

**Text chat with DeepSeek** (same endpoint; set `model` explicitly):

```python
from ray_cluster_access.sv_cluster_access_api import (
    ALTERNATIVE_TEXT_CHAT_MODEL,
    sv_openai_completion,
)

response = sv_openai_completion(
    model=ALTERNATIVE_TEXT_CHAT_MODEL,
    messages=[{"role": "user", "content": "Explain recursion simply."}],
)
print(response.choices[0].message.content)
```

**VL chat (text + image):**

```python
from ray_cluster_access.sv_cluster_access_api import (
    DEFAULT_VL_CHAT_MODEL,
    _convert_image_to_base64,
    sv_openai_completion,
)

image_b64 = _convert_image_to_base64("./images/phys_img.jpeg")

response = sv_openai_completion(
    model=DEFAULT_VL_CHAT_MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Explain this image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                },
            ],
        }
    ],
    max_tokens=5000,
)
print(response.choices[0].message.content)
```

`_convert_image_to_base64(image_source)` accepts an HTTP(S) URL or local path.

---

## Endpoint Summary

| Host:port | Endpoint | Method | Model / purpose |
|-----------|----------|--------|-----------------|
| `10.0.10.51:8123` | `/embed-text/v1/embeddings` | POST | Text embeddings |
| `10.0.10.51:8123` | `/embed-image/v1/embeddings` | POST | Image + text embeddings |
| `10.0.10.51:8000` | `/v1` (chat) | OpenAI client | `openai/gpt-oss-20b` (default text) |
| `10.0.10.51:8000` | `/v1` (chat) | OpenAI client | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` (optional text) |
| `10.0.10.51:8000` | `/v1` (chat) | OpenAI client | `Qwen/Qwen3-VL-8B-Instruct` (text + images) |

---

## Running the Built-in Tests

The module includes `test_*` helpers and a `__main__` block:

```bash
uv run python -m ray_cluster_access.sv_cluster_access_api
```

Runs embedding tests, default and DeepSeek text chat (OpenAI + LiteLLM each), ONNX image embedding, and VL chat with image. Requires network access to the SV cluster and `./images/phys_img.jpeg` for VL tests.
