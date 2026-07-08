#  ------------------------------------------------------------------------------------------------------------
#   Copyright (c) 2024.  SupportVectors AI Lab
#   This code is part of the training material, and therefore part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------------------

import base64
import os
from functools import wraps
from urllib.parse import urlparse, unquote

import requests
from litellm import completion
from openai import OpenAI

from ray_cluster_access import config

# Default text chat on the vLLM server. Pass model= to sv_openai_completion / sv_completion to override.
DEFAULT_TEXT_CHAT_MODEL = "openai/gpt-oss-20b"
# Legacy text chat model (disabled in sv_vllm_setup router config).
LEGACY_TEXT_CHAT_MODEL = "openai/gpt-oss-120b"
# Alternative text chat model on the same vLLM host (reasoning-focused distill of Qwen).
ALTERNATIVE_TEXT_CHAT_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
# Vision-language chat (text + image messages).
DEFAULT_VL_CHAT_MODEL = "Qwen/Qwen3-VL-8B-Instruct"
# Image generation model routed by sv_vllm_setup.
DEFAULT_IMAGE_GEN_MODEL = "Qwen/Qwen-Image"
# Video generation model routed by sv_vllm_setup.
DEFAULT_VIDEO_GEN_MODEL = "Wan-AI/Wan2.2-T2V-A14B"

_cluster = config["cluster_access_api"]
embed_base_url = _cluster["embed_base_url"]
chat_base_url = _cluster["chat_base_url"]
embed_text_base_url = f"{embed_base_url}/embed-text/v1/embeddings"
embed_text_multivector_base_url = (
    f"{embed_base_url}/embed-text/v1/multivector-embeddings"
)
embed_image_base_url = f"{embed_base_url}/embed-image/v1/embeddings"
embed_image_multivector_base_url = (
    f"{embed_base_url}/embed-image/v1/multivector-embeddings"
)
# ColBERT-style multi-vector text embeddings (late interaction over token embeddings).
DEFAULT_COLBERT_MODEL = "lightonai/GTE-ModernColBERT-v1"
# ColPali-style multi-vector image/text embeddings (late interaction over visual tokens).
DEFAULT_COLPALI_MODEL = "TomoroAI/tomoro-colqwen3-embed-4b"
chat_api_base_url = f"{chat_base_url}/v1"
_sv_openai_client = OpenAI(
    base_url=chat_api_base_url,
    api_key="sv-openai-api-key",
)


def _is_http_url(image_source: str) -> bool:
    parsed = urlparse(image_source)
    return parsed.scheme in {"http", "https"}


def _convert_image_to_base64(image_source: str) -> str:
    """Convert an image from URL or local path to base64.

    Args:
        image_source (str): URL (http/https) or local file path.

    Returns:
        str: Base64-encoded image bytes (no data URI prefix).
    """
    if _is_http_url(image_source):
        response = requests.get(image_source, timeout=30)
        response.raise_for_status()
        image_bytes = response.content
    else:
        parsed = urlparse(image_source)
        if parsed.scheme == "file":
            file_path = unquote(parsed.path)
        else:
            file_path = image_source
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image not found at path: {file_path}")
        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

    return base64.b64encode(image_bytes).decode("utf-8")


def embed_text(
    data_sentences: list[str], model_name: str, batch_size: int = 50
) -> list[list[float]]:
    """Embed text using the SupportVectors cluster embedding API.

    Args:
        data_sentences (List[str]): List of text to embed
        model_name (str): Name of the model to use
        batch_size (int): Batch size to use for sending requests to the backend API. Default is 50.
    Returns:
        List[List[float]]: List of embeddings
    """
    embeddings = []
    for start in range(0, len(data_sentences), batch_size):
        batch = data_sentences[start : start + batch_size]

        # NOTE: If we want matryoshka embedding with truncated dimensions,
        # we can add the following to the request:
        # "truncate_dim": 64 (or any other truncated dimension on which the model is trained)

        response = requests.post(
            embed_text_base_url, json={"model": model_name, "input": batch}
        )
        response.raise_for_status()
        embedding_response = response.json()["data"]
        print(f"Batch {start} to {start + batch_size} processed successfully")
        embeddings.extend([item["embedding"] for item in embedding_response])

    return embeddings


def embed_text_colbert(
    data_sentences: list[str],
    model_name: str = DEFAULT_COLBERT_MODEL,
    is_query: bool = False,
    batch_size: int = 50,
) -> list[list[list[float]]]:
    """Embed text as ColBERT multi-vector embeddings via the SV cluster API.

    Args:
        data_sentences (List[str]): List of text to embed.
        model_name (str): ColBERT model id (default: GTE-ModernColBERT-v1).
        is_query (bool): When True, encode inputs as search queries rather than documents.
        batch_size (int): Batch size for API requests. Default is 50.
    Returns:
        List[List[List[float]]]: Per-input token embeddings (num_tokens x dim).
    """
    embeddings = []
    for start in range(0, len(data_sentences), batch_size):
        batch = data_sentences[start : start + batch_size]
        payload: dict = {"model": model_name, "input": batch}
        if is_query:
            payload["is_query"] = True

        response = requests.post(embed_text_multivector_base_url, json=payload)
        response.raise_for_status()
        embedding_response = response.json()["data"]
        print(f"Batch {start} to {start + batch_size} processed successfully")
        embeddings.extend([item["embedding"] for item in embedding_response])

    return embeddings


def embed_colpali(
    data_images: list[str],
    data_texts: list[str],
    model_name: str = DEFAULT_COLPALI_MODEL,
    batch_size: int = 8,
) -> list[list[list[float]]]:
    """Embed images and/or text as ColPali multi-vector embeddings via the SV cluster API.

    Args:
        data_images (List[str]): List of image URLs or local paths to embed.
        data_texts (List[str]): List of text strings to embed (e.g. search queries).
        model_name (str): ColPali model id (default: tomoro-colqwen3-embed-4b).
        batch_size (int): Batch size for API requests (max 8). Default is 8.
    Returns:
        List[List[List[float]]]: Per-input token embeddings (num_tokens x dim), ordered
            as [image_1, …, image_n, text_1, …, text_m].
    """
    base64_images = [_convert_image_to_base64(image_url) for image_url in data_images]
    data_inputs = base64_images + data_texts
    embeddings = []
    for start in range(0, len(data_inputs), batch_size):
        batch = data_inputs[start : start + batch_size]
        response = requests.post(
            embed_image_multivector_base_url,
            json={"model": model_name, "input_type": "auto", "input": batch},
        )
        response.raise_for_status()
        embedding_response = response.json()["data"]
        print(f"Batch {start} to {start + batch_size} processed successfully")
        embeddings.extend([item["embedding"] for item in embedding_response])

    return embeddings


def embed_image(
    data_images: list[str],
    data_texts: list[str],
    model_name: str,
    batch_size: int = 50,
) -> list[list[float]]:
    """Embed images and/or text using multimodal embedding models on the SV cluster.

    Args:
        data_images (List[str]): List of image URLs or local paths to embed
        data_texts (List[str]): List of text to embed
        model_name (str): Name of the multi-modal model (CLIP, SigLIP, ONNX, etc.)
        batch_size (int): Batch size to use for sending requests to the backend API. Default is 50.
    Returns:
        List[List[float]]: List of embeddings
    """
    base64_images = [_convert_image_to_base64(image_url) for image_url in data_images]
    data_inputs = base64_images + data_texts
    embeddings = []
    for start in range(0, len(data_inputs), batch_size):
        batch = data_inputs[start : start + batch_size]
        response = requests.post(
            embed_image_base_url,
            json={"model": model_name, "input_type": "auto", "input": batch},
        )
        response.raise_for_status()
        embedding_response = response.json()["data"]
        print(f"Batch {start} to {start + batch_size} processed successfully")
        embeddings.extend([item["embedding"] for item in embedding_response])

    return embeddings


def get_sv_openai_client() -> OpenAI:
    """Return an OpenAI client for chat completions on the SupportVectors vLLM server.

    Pass `model` to `sv_openai_completion` (e.g. `DEFAULT_TEXT_CHAT_MODEL`,
    `ALTERNATIVE_TEXT_CHAT_MODEL`, or `DEFAULT_VL_CHAT_MODEL`).
    """
    return _sv_openai_client


@wraps(_sv_openai_client.chat.completions.create)
def sv_openai_completion(*, model: str = DEFAULT_TEXT_CHAT_MODEL, **kwargs):
    """Chat completion via the OpenAI client (vLLM, OpenAI-compatible API).

    Args:
        model: Chat model id. Defaults to `DEFAULT_TEXT_CHAT_MODEL`; use
            `ALTERNATIVE_TEXT_CHAT_MODEL` for DeepSeek-R1-Distill-Qwen-7B, or
            `DEFAULT_VL_CHAT_MODEL` for vision-language.
        **kwargs: Passed to `chat.completions.create` (e.g. `messages`, `max_tokens`).
    """
    kwargs.pop("model", None)
    return _sv_openai_client.chat.completions.create(model=model, **kwargs)


@wraps(completion)
def sv_completion(*, model: str = DEFAULT_TEXT_CHAT_MODEL, **kwargs):
    """Chat completion via LiteLLM (vLLM, OpenAI-compatible API).

    Args:
        model: Chat model id. Defaults to `DEFAULT_TEXT_CHAT_MODEL`; use
            `ALTERNATIVE_TEXT_CHAT_MODEL` for DeepSeek-R1-Distill-Qwen-7B, or
            `DEFAULT_VL_CHAT_MODEL` for vision-language.
        **kwargs: Passed to LiteLLM `completion`.
    """
    kwargs.pop("model", None)
    kwargs.pop("api_base", None)
    kwargs.pop("api_key", None)
    return completion(
        model="openai/" + model,
        api_base=chat_api_base_url,
        api_key="sv-openai-api-key",
        **kwargs,
    )


def sv_generate_image(
    *,
    prompt: str,
    model: str = DEFAULT_IMAGE_GEN_MODEL,
    height: int = 512,
    width: int = 512,
    num_inference_steps: int = 30,
    guidance_scale: float = 4.0,
    num_images: int = 1,
) -> dict:
    """Generate image(s) via the router's OpenAI-compatible images endpoint."""
    response = requests.post(
        f"{chat_api_base_url}/images/generations",
        headers={"Content-Type": "application/json"},
        json={
            "model": model,
            "prompt": prompt,
            "height": height,
            "width": width,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def sv_generate_video(
    *,
    prompt: str,
    model: str = DEFAULT_VIDEO_GEN_MODEL,
    height: int = 480,
    width: int = 832,
    num_frames: int = 49,
    num_inference_steps: int = 30,
    guidance_scale: float = 5.0,
) -> dict:
    """Generate a video via the router's OpenAI-compatible videos endpoint."""
    response = requests.post(
        f"{chat_api_base_url}/videos/generations",
        headers={"Content-Type": "application/json"},
        json={
            "model": model,
            "prompt": prompt,
            "height": height,
            "width": width,
            "num_frames": num_frames,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
        },
        timeout=300,
    )
    response.raise_for_status()
    return response.json()


def test_embed_text(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2", batch_size: int = 50
):
    """Test the embed_text function."""
    data_sentences = [
        "Hello, world!",
        "This is a test sentence.",
        "This is another test sentence.",
    ]
    embeddings = embed_text(data_sentences, model_name, batch_size)
    print(f"Generated {len(embeddings)} embeddings for the input sentences")
    print(f"Size of the embeddings: {len(embeddings[0])}")
    print(f"First 10 values of the first embedding: {embeddings[0][:10]}")


def test_embed_text_colbert(
    model_name: str = DEFAULT_COLBERT_MODEL,
):
    """Test ColBERT multi-vector text embeddings (single query input)."""
    data_sentences = ["What is ColBERT?"]
    embeddings = embed_text_colbert(data_sentences, model_name, is_query=True)
    token_embeddings = embeddings[0]
    print(f"Generated {len(embeddings)} ColBERT embedding(s) for the input")
    print(f"Num tokens: {len(token_embeddings)}, dim: {len(token_embeddings[0])}")
    print(f"First 10 values of the first token embedding: {token_embeddings[0][:10]}")


def test_embed_colpali(
    model_name: str = DEFAULT_COLPALI_MODEL,
    sample_image: str = "https://supportvectors.ai/logo-poster-transparent.png",
    sample_text: str = "SupportVectors offers courses on AI/ML",
):
    """Test ColPali multi-vector embeddings for a sample image and text query."""
    data_images = [sample_image]
    data_texts = [sample_text]
    embeddings = embed_colpali(data_images, data_texts, model_name)
    image_token_embeddings = embeddings[0]
    text_token_embeddings = embeddings[1]
    print(f"Generated {len(embeddings)} ColPali embedding(s) for the input")
    print(
        f"Image — num tokens: {len(image_token_embeddings)}, "
        f"dim: {len(image_token_embeddings[0])}"
    )
    print(
        f"Text — num tokens: {len(text_token_embeddings)}, "
        f"dim: {len(text_token_embeddings[0])}"
    )
    print(
        f"First 10 values of the first image token embedding: "
        f"{image_token_embeddings[0][:10]}"
    )
    print(
        f"First 10 values of the first text token embedding: "
        f"{text_token_embeddings[0][:10]}"
    )


def test_embed_image(
    model_name: str = "google/siglip2-base-patch16-224", batch_size: int = 50
):
    """Test the embed_image function."""
    data_images = [
        "https://supportvectors.ai/logo-poster-transparent.png",
        "docs/images/logo-poster.png",
    ]
    data_texts = ["SupportVectors offers courses on AI/ML"]
    embeddings = embed_image(data_images, data_texts, model_name, batch_size)
    print(f"Generated {len(embeddings)} embeddings for the input images and text")
    print(f"Size of the embeddings: {len(embeddings[0])}")
    print(f"First 10 values of the first embedding: {embeddings[0][:10]}")


def test_embed_image_onnx(
    model_name: str = "onnxmodelzoo/arcfaceresnet100-11-int8", batch_size: int = 50
):
    """Test embed_image with an ONNX model (images only)."""
    data_images = [
        "https://supportvectors.ai/logo-poster-transparent.png",
        "docs/images/logo-poster.png",
    ]
    embeddings = embed_image(data_images, [], model_name, batch_size)
    print(f"Generated {len(embeddings)} embeddings for the input images")
    print(f"Size of the embeddings: {len(embeddings[0])}")
    print(f"First 10 values of the first embedding: {embeddings[0][:10]}")


def test_openai_text_chat():
    """Test OpenAI chat with the default text model."""
    response = sv_openai_completion(
        messages=[{"role": "user", "content": "Why is the sky blue?"}]
    )
    print(response.choices[0].message.content)


def test_openai_legacy_text_chat():
    """Legacy test for openai/gpt-oss-120b (kept disabled in __main__)."""
    response = sv_openai_completion(
        model=LEGACY_TEXT_CHAT_MODEL,
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    )
    print(response.choices[0].message.content)


def test_litellm_text_chat():
    """Test LiteLLM chat with the default text model."""
    response = sv_completion(
        messages=[{"role": "user", "content": "Tell me a new joke"}]
    )
    print(response.choices[0].message.content)


def test_openai_alternative_text_chat():
    """Test OpenAI chat with ALTERNATIVE_TEXT_CHAT_MODEL (DeepSeek-R1-Distill-Qwen-7B)."""
    response = sv_openai_completion(
        model=ALTERNATIVE_TEXT_CHAT_MODEL,
        messages=[{"role": "user", "content": "Explain recursion in one paragraph."}],
    )
    print(response.choices[0].message.content)


def test_litellm_alternative_text_chat():
    """Test LiteLLM chat with ALTERNATIVE_TEXT_CHAT_MODEL (DeepSeek-R1-Distill-Qwen-7B)."""
    response = sv_completion(
        model=ALTERNATIVE_TEXT_CHAT_MODEL,
        messages=[{"role": "user", "content": "What is a binary search tree?"}],
    )
    print(response.choices[0].message.content)


def _vl_chat_messages(image_path: str = "./images/phys_img.jpeg") -> list[dict]:
    image_b64 = _convert_image_to_base64(image_path)
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "I am a physics student and came across this notes. "
                        "Can you explain it? Put this explanation as a tutorial in a latex document."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                },
            ],
        }
    ]


def test_openai_vl_chat(image_path: str = "./images/phys_img.jpeg"):
    """Test OpenAI chat with the default VL model and a text + image message."""
    response = sv_openai_completion(
        model=DEFAULT_VL_CHAT_MODEL,
        messages=_vl_chat_messages(image_path),
        max_tokens=5000,
    )
    print(response.choices[0].message.content)


def test_litellm_vl_chat(image_path: str = "./images/phys_img.jpeg"):
    """Test LiteLLM chat with the default VL model and a text + image message."""
    response = sv_completion(
        model=DEFAULT_VL_CHAT_MODEL,
        messages=_vl_chat_messages(image_path),
        max_tokens=5000,
    )
    print(response.choices[0].message.content)


def test_generate_image(model_name: str = DEFAULT_IMAGE_GEN_MODEL):
    """Test image generation using the configured image generation model."""
    result = sv_generate_image(
        model=model_name,
        prompt="A cinematic sunrise over mountains, ultra-detailed, warm lighting",
    )
    outputs = result.get("data", [])
    print(f"Generated {len(outputs)} image output item(s) using model {model_name}")
    if outputs:
        print(f"First output keys: {list(outputs[0].keys())}")


def test_generate_video(model_name: str = DEFAULT_VIDEO_GEN_MODEL):
    """Test video generation using the configured video generation model."""
    result = sv_generate_video(
        model=model_name,
        prompt="A drone flythrough over a futuristic city at dusk, smooth camera motion",
    )
    outputs = result.get("data", [])
    print(f"Generated {len(outputs)} video output item(s) using model {model_name}")
    if outputs:
        print(f"First output keys: {list(outputs[0].keys())}")


if __name__ == "__main__":
    print("Testing embed_text function")
    test_embed_text()
    print("--------------------------------")
    print("Testing embed_text_colbert function")
    test_embed_text_colbert()
    print("--------------------------------")
    print("Testing embed_colpali function")
    test_embed_colpali()
    print("--------------------------------")
    print("Testing embed_image function")
    test_embed_image()
    print("--------------------------------")
    print("Testing OpenAI text chat")
    test_openai_text_chat()
    # print("--------------------------------")
    # print("Testing OpenAI legacy text chat (GPT-OSS 120B)")
    # test_openai_legacy_text_chat()
    print("--------------------------------")
    print("Testing LiteLLM text chat")
    test_litellm_text_chat()
    print("--------------------------------")
    print("Testing OpenAI alternative text chat (DeepSeek)")
    test_openai_alternative_text_chat()
    print("--------------------------------")
    print("Testing LiteLLM alternative text chat (DeepSeek)")
    test_litellm_alternative_text_chat()
    print("--------------------------------")
    print("Testing embed_image with ONNX model")
    test_embed_image_onnx()
    print("--------------------------------")
    print("Testing OpenAI VL chat")
    test_openai_vl_chat()
    print("--------------------------------")
    print("Testing LiteLLM VL chat")
    test_litellm_vl_chat()
    print("--------------------------------")
    print("Testing image generation")
    test_generate_image()
    print("--------------------------------")
    print("Testing video generation")
    test_generate_video()
    print("--------------------------------")
