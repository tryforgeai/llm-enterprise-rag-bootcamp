
# Microsoft's GraphRAG

README borrowed from ms graphrag tutorials under ai agents bootcamp repo

## Steps to run this project

### Basic setup
```
uv sync
uv add graphrag
uv run graphrag init --root sv_docs/
```

This will create a directory "sv_docs"
### Configurations

In the file `sv_docs/.env`
set 
`GRAPHRAG_API_KEY="support_vectors"`

Update `sv_docs/settings.yaml` for your use case:
- model
- model_supports_json
- entity_types
- other configurations

We have a sample `settings.yaml`: `docs/sample/settings.yaml` which works for local LLMs.
While using local LLM, you need to ensure that ollama or vllm is available on the urls with the models are served.
You need both the chat model and the embedding model(`nomic-embed-text`)

You can choose to just copy the setting.yaml we provide:
```
cp docs/sample/settings.yaml sv_docs/settings.yaml
```

### Get the corpus docs

```
cd sv_docs
mkdir input
cd input
## Add all corpus docs here
cd ../../
```

GraphRAG only ingests **plain text (`.txt`)**, CSV, or JSON—not PDF. If your docs are PDFs, convert them first:

```bash
uv run scripts/pdf_to_txt.py [input_dir] [output_dir]
# input_dir:  folder with PDFs (searched recursively, including subfolders). Default: sv_docs/input
# output_dir: where to write .txt files. Default: same as input_dir
# Example: uv run scripts/pdf_to_txt.py sv_docs/data sv_docs/input
```

### Index

```
uv run graphrag index --root ./sv_docs --verbose
```
The logs are at: `sv_docs/logs/indexing-engine.log`

Wait till you see: `All workflows completed successfully.` or `Pipeline completed`


### Visualize graph, communities, and summaries

After indexing, you can generate interactive visualizations from the output artifacts:

```bash
uv run scripts/visualize_graphrag.py --root ./sv_docs
```

This writes three HTML files under `sv_docs/output/`:

- **graphrag_graph.html** — Interactive graph (nodes colored by root community). Open in a browser; drag nodes, zoom, hover for community summary.
- **graphrag_communities.html** — Hierarchy of communities and sub-communities with LLM-generated titles, summaries, ratings, and findings.
- **graphrag_community_tree.html** — Interactive dendrogram of the community hierarchy (D3 tree layout). Hover nodes for titles and summaries; zoom and pan to explore.

Use `--no-browser` to skip opening the files automatically.

### Query

#### Global Search

**What it does**: Maps over all community reports to answer corpus-wide questions about themes, structure, and high-level patterns.
```
uv run graphrag query --root ./sv_docs --method global <<global_query>>
```

#### Local Search

**What it does**: Starts from specific entities in the graph (people, places, concepts) and explores their neighborhood plus linked text chunks.
```
uv run graphrag query --root ./sv_docs --method local <<local_query>>
```

#### DRIFT Search

**What it does**: Combines global and local—first consults community reports for context, generates follow-up questions, then does local-style searches to refine the answer.

```
uv run graphrag query --root ./sv_docs --method drift <<evolution_query>>
```

## Quick Reference Table

| Query Type | Best For | Example |
|:-----------|:---------|:--------|
| **Global** | Themes, structure, corpus-wide patterns | <<global_query>> |
| **Local** | Specific entities, characters, events | <<local_query>> |
| **DRIFT** | Concept evolution, theme + entity connections | <<evolution_query>> |



## Rule of Thumb

- **Global**: "What/How does the *whole book* say about X?"
- **Local**: "Tell me about *this specific character/place/event*"
- **DRIFT**: "How does *concept/theme X* develop through *specific story elements*?" (needs both breadth and depth)

## Troubleshooting

### "Graph Extraction failed. No entities detected during extraction"

This usually means **every** entity-extraction LLM call failed, so the graph ends up empty. Check `sv_docs/logs/indexing-engine.log` for the underlying error.

**If you see `'list' object is not an iterator` (or `OpenAIHTTPException` from Ray Serve):**

- The **LLM server** (e.g. Ray Serve at your `api_base`) is rejecting the chat completion request. The client sends a normal list of messages; the server has a bug or incompatibility.
- **Fix options:**
  1. **Use a different completion model** – In `sv_docs/settings.yaml`, point `default_completion_model` to an endpoint that works (e.g. real OpenAI API, or another local server like Ollama/vLLM that is known to work with OpenAI-style chat).
  2. **Fix the server** – If you control the Ray Serve LLM deployment, update it so it correctly accepts the OpenAI chat completion payload (messages as a list). The error originates in `ray.llm._internal.serve.core.configs.openai_api_models`.
- **Quick test:** Use the sample config that uses a local LLM:  
  `cp docs/sample/settings.yaml sv_docs/settings.yaml` and ensure Ollama/vLLM is running at the URLs in that config.
