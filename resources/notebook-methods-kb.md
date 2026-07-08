# Notebook Methods KB

Date: 2026-06-15

Purpose: summarize the reusable AI, embedding, retrieval, and RAG methods found in the project's official Jupyter notebooks so future work can quickly find the right technique.

Scope:

- Included: project and course notebooks under `course/` and `labs/`.
- Excluded: `.ipynb_checkpoints/` automatic backups and third-party notebooks inside `.venv/`.
- Helper notebooks such as `supportvectors-common.ipynb` are recorded once as environment utilities, even when copied into multiple course folders.

## Quick Method Index

| Need | Use This Method | Notebook Source |
| --- | --- | --- |
| Explain why high-dimensional embeddings behave strangely | concentration of measure, nearest-neighbor collapse | `course/embeddings_projection/docs/notebooks/00-some-math-experiments.ipynb` |
| Turn logits into probabilities | softmax and temperature | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/03_softmax_temperature.ipynb` |
| Explain next-token prediction | probability distribution over vocabulary | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/02_probability_next_token.ipynb` |
| Explain model training | cross-entropy, gradient updates, bigram language model | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/09_loss_and_training.ipynb` |
| Show a tiny GPT-like model | NumPy bigram GPT, logits table, learned transition probabilities | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/10_mini_gpt_numpy.ipynb` |
| Explain embeddings from scratch | toy 2D word vectors | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/04_embeddings.ipynb` |
| Compare semantic similarity | dot product and cosine-style direction similarity | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/05_dot_product_similarity.ipynb` |
| Explain attention | scaled dot-product attention, weights, heatmaps | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/06_attention_scores.ipynb`, `07_attention_heatmaps.ipynb` |
| Explain transformer block internals | Q/K/V projections, residuals, layer norm, feed-forward | `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/08_transformer_block_step_by_step.ipynb` |
| Diagnose raw BERT embeddings | anisotropy and PCA visualization | `course/embeddings_projection/docs/notebooks/01-encoder-embeddings.ipynb` |
| Compare sentence embedding models | BERT vs BGE / SentenceTransformer | `course/embeddings_projection/docs/notebooks/01-encoder-embeddings.ipynb` |
| Measure embedding retrieval quality | cosine histograms, intra/inter/gap | `course/rag_2026_week2_uslab/docs/notebooks/embedding/cosine_similarity_histograms*.ipynb` |
| Fine-tune embeddings for a labeled domain | CoSENT / InfoNCE contrastive fine-tuning | `course/embeddings_projection/docs/notebooks/03-ft-encoder-embeddings.ipynb` |
| Do text-to-image retrieval | SigLIP / CLIP shared image-text embedding space | `course/embeddings_projection/docs/notebooks/02-siglip-embeddings.ipynb` |
| Search an image collection | Qdrant image search with natural-language query | `course/llm_rag_week_1/unsplash_collection/docs/notebooks/search_collection.ipynb` |
| Evaluate multimodal fine-tuning | CLIP MNIST before/after SupCon, kNN, silhouette, cosine gap | `course/rag_2026_week2_uslab/docs/notebooks/embedding/clip_mnist_contrastive.ipynb` |

## Core Notebook Methods

### 1. Tokens And Text

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/01_tokens_and_text.ipynb`

Method:

```text
raw text
-> normalize text
-> split into tokens
-> build vocabulary
-> map tokens to integer IDs
```

Code pattern:

```python
tokens = text.lower().replace(".", "").split()
vocab = {tok: i for i, tok in enumerate(sorted(set(tokens)))}
ids = [vocab[t] for t in tokens]
```

Use when:

- explaining why LLMs do not directly read words like humans
- debugging tokenization, chunking, or vocabulary coverage
- teaching the first step from language to computation

RAG / Avaloka use:

- Chunking and retrieval quality begin before embeddings. If tokenization is bad, embeddings and retrieval inherit the damage.
- For multilingual or Tibetan work, tokenization and normalization need explicit testing.

### 2. Next-Token Probability

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/02_probability_next_token.ipynb`

Method:

```text
current context
-> candidate next tokens
-> probability assigned to each candidate
-> choose or sample next token
```

Code pattern:

```python
words = ["mat", "moon", "car"]
probs = [0.625, 0.125, 0.25]
plt.bar(words, probs)
```

Use when:

- explaining that generation is probabilistic
- showing why the highest-probability token is not the only possible token
- connecting surprise / NLL to model behavior

RAG / Avaloka use:

- RAG grounding changes the probability distribution by putting relevant evidence in context.
- Safety policy should alter what outputs are allowed, not only what is likely.

### 3. Softmax And Temperature

Sources:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/03_softmax_temperature.ipynb`
- `course/embeddings_projection/docs/notebooks/00-some-math-experiments.ipynb`

Method:

```text
logits / raw scores
-> divide by temperature T
-> exponentiate
-> normalize
-> probability distribution
```

Code pattern:

```python
def softmax_with_temperature(logits, temperature=1.0):
    z = np.asarray(logits) / temperature
    z = z - z.max()
    exp_z = np.exp(z)
    return exp_z / exp_z.sum()
```

Temperature reading:

| T | Effect |
| --- | --- |
| low | sharper, more deterministic, more argmax-like |
| 1 | normal softmax scale |
| high | flatter, more exploratory |

Use when:

- explaining sampling behavior
- explaining attention weights
- interpreting InfoNCE and contrastive learning
- tuning factual RAG response generation

RAG / Avaloka use:

- Use lower temperature for grounded factual answers and safety-sensitive outputs.
- Temperature is a runtime decoding parameter, not a learned model weight.
- In retrieval, softmax over scores can create a confidence distribution, but it should not replace provenance or permission checks.

### 4. Toy Embeddings

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/04_embeddings.ipynb`

Method:

```text
word/token
-> numeric vector
-> plot in low-dimensional space
-> nearby vectors represent related meanings
```

Code pattern:

```python
emb = {
    "cat": np.array([0.9, 0.8]),
    "dog": np.array([0.8, 0.7]),
    "pizza": np.array([-0.8, -0.5]),
}
```

Use when:

- teaching embeddings as "meaning coordinates"
- explaining why semantic search can compare text numerically
- showing why individual dimensions are usually less important than relationships

RAG / Avaloka use:

- Care memories, wisdom notes, and user-safe facts can be embedded, but vector closeness is only a candidate signal.

### 5. Dot Product Similarity

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/05_dot_product_similarity.ipynb`

Method:

```text
vector A · vector B
-> larger positive score means more aligned
-> negative score means opposing direction
```

Code pattern:

```python
score = cat @ dog
```

Use when:

- explaining similarity scores
- explaining attention score calculation
- explaining why normalized dot product becomes cosine similarity

RAG / Avaloka use:

- Dense retrieval ranking is often "query vector dot document vector" or cosine similarity.
- A high dot product is not factual proof; it is a retrieval signal.

### 6. Attention Scores

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/06_attention_scores.ipynb`

Method:

```text
Q, K, V
-> scores = QK^T / sqrt(d_k)
-> weights = softmax(scores)
-> output = weights V
```

Code pattern:

```python
out, weights, scores = scaled_dot_product_attention(X, X, X)
```

Use when:

- explaining "soft lookup" or "differentiable dictionary lookup"
- showing how tokens decide which other tokens matter
- connecting attention to retrieval intuition

RAG / Avaloka use:

- Internal attention is not the same as external RAG retrieval, but the mental model is similar: score candidates, normalize weights, blend values.
- For explanations, save scores and weights in traces when building toy models.

### 7. Attention Heatmaps

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/07_attention_heatmaps.ipynb`

Method:

```text
attention weight matrix
-> rows are queries / current tokens
-> columns are keys / tokens attended to
-> heatmap shows where attention mass goes
```

Code pattern:

```python
plt.imshow(weights)
plt.xticks(range(len(words)), words)
plt.yticks(range(len(words)), words)
```

Use when:

- visualizing attention patterns
- explaining causal attention and which earlier tokens are visible
- debugging whether a toy model is looking at expected positions

RAG / Avaloka use:

- Heatmaps are good teaching tools, but not full explanations of model behavior.
- For product systems, pair attention-style interpretation with retrieval traces and evidence IDs.

### 8. Transformer Block Step By Step

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/08_transformer_block_step_by_step.ipynb`

Method:

```text
X
-> Q = XWq, K = XWk, V = XWv
-> attention
-> output projection
-> residual add
-> layer normalization
-> feed-forward network
```

Code pattern:

```python
Q, K, V = X @ Wq, X @ Wk, X @ Wv
attn_out, weights, scores = scaled_dot_product_attention(Q, K, V)
residual = X + attn_out @ Wproj
normalized = layer_norm(residual)
```

Use when:

- explaining where Q/K/V come from
- explaining residual connections and layer normalization
- teaching what a transformer block actually computes

RAG / Avaloka use:

- Helps distinguish internal model computation from external retrieval architecture.
- Useful for explaining why fine-tuning changes many learned matrices, not only final probabilities.

### 9. Loss And Training

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/09_loss_and_training.ipynb`

Method:

```text
input
-> model scores
-> softmax probabilities
-> cross-entropy loss
-> gradient update
-> repeat until loss falls
```

Code pattern:

```python
p = softmax(scores)
loss = cross_entropy(p, target)
grad = p.copy()
grad[target] -= 1
scores -= learning_rate * grad
```

For an input-dependent toy model:

```python
x = one_hot(word2idx[cur])
scores = x @ W
p = softmax(scores)
grad_scores = p
grad_scores[word2idx[nxt]] -= 1
grad_W += np.outer(x, grad_scores)
W -= learning_rate * grad_W
```

Use when:

- explaining backpropagation at the smallest possible scale
- showing how increasing one correct probability lowers loss
- connecting MLE, NLL, and cross-entropy

RAG / Avaloka use:

- Fine-tuning requires labeled examples and a loss that encodes the desired behavior.
- Prefer retrieval and eval improvements before fine-tuning Avaloka behavior.

### 10. Mini GPT In NumPy

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/llm_basics/10_mini_gpt_numpy.ipynb`

Method:

```text
tiny corpus
-> vocabulary and token IDs
-> bigram training pairs
-> learn logits table
-> softmax each row to predict next token
-> generate short sequence
```

Code pattern:

```python
model = TinyBigramGPT(vocab_size=len(vocab), seed=0)
for epoch in range(50):
    loss = model.train_step(x_ids, y_ids, lr=0.2)
probs = model.predict_next_probs(vocab["the"])
```

Use when:

- teaching how a language model learns transition structure
- visualizing logits before and after training
- explaining why generated text follows learned data distribution

RAG / Avaloka use:

- Good for teaching why pretraining captures patterns but not necessarily truth.
- Use traces to distinguish model-generated probability from retrieved evidence.

## Embedding And Retrieval Evaluation Methods

### 11. High-Dimensional Geometry Experiments

Source:

- `course/embeddings_projection/docs/notebooks/00-some-math-experiments.ipynb`

Methods:

- concentration of measure in high dimensions
- collapse of intuitive nearest-neighbor distances
- inverse-transform sampling for high-dimensional unit ball / hypersphere
- softmax temperature over generated logits
- Shannon entropy as uncertainty measure

Code patterns:

```python
vectors = generate_random_unit_vectors(n_vectors, d)
cosines = compute_cosine_similarities(vectors)
```

```python
dmin, dmax, ratio = distance_stats(reference, points)
```

Use when:

- explaining why high-dimensional vector search is unintuitive
- motivating careful evaluation of nearest neighbors
- explaining why random high-dimensional vectors can have surprising geometry

RAG / Avaloka use:

- Do not trust vector search by intuition alone. Measure distributions, gaps, and retrieval metrics.
- Hard negatives matter because "nearest" can become unstable in high-dimensional spaces.

### 12. BERT Encoder Embeddings And Anisotropy

Source:

- `course/embeddings_projection/docs/notebooks/01-encoder-embeddings.ipynb`

Method:

```text
subject-labeled text chunks
-> encode with raw BERT
-> PCA to 2D
-> visualize narrow cone / anisotropy
-> repeat with BGE / SentenceTransformer
```

Models:

- `google-bert/bert-base-uncased`
- `BAAI/bge-base-en-v1.5`

Code patterns:

```python
model = SentenceTransformer("google-bert/bert-base-uncased")
embeddings = model.encode(data_sentences)
pca_embeddings = PCA(n_components=2).fit_transform(embeddings)
```

Alternative cluster API:

```python
embeddings = embed_text(data_sentences, model_name)
```

Use when:

- showing why raw BERT embeddings are often not ideal for sentence retrieval
- comparing a base encoder with a retrieval-oriented sentence model
- teaching anisotropy visually

RAG / Avaloka use:

- Raw BERT can make unrelated memories look too similar.
- Sentence-transformer-style models are better baselines for dense retrieval.

### 13. Cosine Similarity Explanation

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/embedding/cosine_similarity_histograms_explanation.ipynb`

Method:

```text
unit-normalize vectors
-> cosine = dot product
-> sample same-subject pairs
-> sample different-subject pairs
-> compare histograms
-> compute gap
```

Code patterns:

```python
def normalize_rows(matrix):
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.clip(norms, 1e-12, None)
```

```python
same = labels[i] == labels[j]
intra = cos[same]
inter = cos[~same]
gap = intra.mean() - inter.mean()
```

Use when:

- teaching cosine similarity from first principles
- explaining same-class vs different-class separation
- preparing someone to read the expert histogram notebook

RAG / Avaloka use:

- Use `gap` as an early signal that an embedder separates relevant memories from distractors.

### 14. Cosine Similarity Histogram Expert View

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/embedding/cosine_similarity_histograms.ipynb`

Method:

```text
load exported vectors.tsv and metadata.tsv
-> sample random pair cosines
-> plot overall cosine histograms
-> split into intra-label and inter-label pairs
-> compute mean, std, intra, inter, gap
```

Compared collections:

- BERT anisotropic subject embeddings
- MiniLM isotropic subject embeddings
- fine-tuned subject embeddings

Core metrics:

| Metric | Meaning |
| --- | --- |
| `mean` | average random-pair similarity |
| `std` | spread of random-pair similarity |
| `intra` | average same-label similarity |
| `inter` | average different-label similarity |
| `gap` | `intra - inter`; larger is better |

Use when:

- deciding whether an embedding model is good enough for semantic retrieval
- comparing base, sentence, and fine-tuned embeddings
- diagnosing anisotropy

RAG / Avaloka use:

- Before replacing Memory Reader V0 with vector search, build a labeled same/different set and compute these histograms.
- A model that "looks good" on one query can still be unsafe if hard negatives overlap.

### 15. Fine-Tuned Sentence Transformer Embeddings

Source:

- `course/embeddings_projection/docs/notebooks/03-ft-encoder-embeddings.ipynb`

Method:

```text
subject-labeled text chunks
-> train / load fine-tuned SentenceTransformer checkpoint
-> encode same data
-> PCA visualize embeddings
-> compare across contrastive objectives and scale / temperature
```

Fine-tuning approaches:

- CoSENTLoss: pair ranking based on similarity ordering
- InfoNCE: softmax over positive and negative candidates
- scale is inverse temperature; higher scale means lower temperature and sharper contrast

Code patterns:

```python
finetuned_model = SentenceTransformer(finetuned_model_dir)
finetuned_embeddings = finetuned_model.encode(data_sentences)
```

Checkpoint pattern:

```python
checkpoint_pattern = f"{results_dir}/{results_sub_dir}_scale_{scale}/checkpoint-*"
latest_checkpoint = sorted(checkpoint_dirs, key=lambda x: int(x.split("checkpoint-")[-1]))[-1]
```

Use when:

- a general embedding model does not separate a domain-specific task
- labeled positive/negative pairs exist
- you need to test whether contrastive fine-tuning improves retrieval structure

RAG / Avaloka use:

- Fine-tuning is not the first move. Use it only after baseline retrieval metrics show a specific failure and you have labels.
- For Avaloka, hard negatives should include similar wording with different risk or permission scope.

## Multimodal Retrieval Methods

### 16. SigLIP Image Embeddings

Source:

- `course/embeddings_projection/docs/notebooks/02-siglip-embeddings.ipynb`

Method:

```text
CIFAR-10 images
-> save sampled images
-> encode images with SigLIP
-> PCA / t-SNE / UMAP visualization
-> compare image and text embeddings with cosine similarity
```

Model:

- `google/siglip2-base-patch16-224`

Code patterns:

```python
siglip_image_embeddings = embed_image(image_paths, [], siglip_model_name)
pca_embeddings = PCA(n_components=2).fit_transform(np.array(siglip_image_embeddings))
```

Image-text comparison:

```python
embeddings = embed_image([image1], ["Image of a kitten", "Image of a dog"], siglip_model_name)
image_vec = l2_normalize(np.asarray(embeddings[0]))
text_vec = l2_normalize(np.asarray(embeddings[1]))
score = np.dot(image_vec, text_vec)
```

Use when:

- retrieving images by text query
- comparing an image to candidate captions
- introducing multimodal shared embedding spaces

RAG / Avaloka use:

- Useful for screenshots, diagrams, handwritten notes, whiteboards, or lecture images.
- Store source, permission, OCR text, caption, timestamp, and provenance with every image embedding.
- Image-text similarity is not proof of truth or authorization.

### 17. Unsplash Natural-Language Image Search

Source:

- `course/llm_rag_week_1/unsplash_collection/docs/notebooks/search_collection.ipynb`

Method:

```text
natural-language text query
-> embed query
-> search Qdrant image collection
-> return top-N image matches
-> display result thumbnails and scores
```

Code pattern:

```python
results = search_collection(query_text="To love a dog", top_n=5)
display_search_results(results=results, query_text=query_text)
```

One-step API:

```python
search_and_display(query_text="sunset over the ocean", top_n=DEFAULT_TOP_N)
```

Use when:

- building a text-to-image retrieval demo
- testing CLIP/SigLIP collection search
- explaining vector database top-k retrieval

RAG / Avaloka use:

- Same shape as text RAG, but retrieved objects are images.
- Need metadata and permission checks before using images in user-facing answers.

### 18. CLIP MNIST Contrastive Fine-Tuning

Source:

- `course/rag_2026_week2_uslab/docs/notebooks/embedding/clip_mnist_contrastive.ipynb`

Method:

```text
MNIST images
-> frozen CLIP image encoder
-> train projection head with supervised contrastive loss
-> compare before and after embeddings
-> evaluate with t-SNE, cosine gap, kNN accuracy, silhouette score
```

Metrics:

| Metric | Meaning |
| --- | --- |
| cosine gap | same-digit similarity minus different-digit similarity |
| kNN accuracy | local separability of the embedding space |
| silhouette | cluster tightness and separation |

Code patterns:

```python
before = np.load(DATA / "before_test.npy")
after = np.load(DATA / "after_test.npy")
labels = np.load(DATA / "labels_test.npy")
```

```python
clf = KNeighborsClassifier(n_neighbors=10, metric="cosine").fit(Xtr, ytr)
acc = accuracy_score(yte, clf.predict(Xte))
sil = silhouette_score(emb, labels, metric="cosine")
```

Use when:

- a multimodal model loosely captures a domain but needs task-specific separation
- evaluating whether contrastive training tightened clusters
- teaching before/after fine-tuning effects

RAG / Avaloka use:

- If Avaloka later retrieves diagrams or images by emotional/practice category, use similar before/after evals before trusting a fine-tuned image embedder.

## Support And Environment Utility Methods

### 19. SupportVectors Common Notebook

Sources:

- `course/embeddings_projection/docs/notebooks/supportvectors-common.ipynb`
- `course/llm_rag_week_1/embeddings_projection/docs/notebooks/supportvectors-common.ipynb`
- `course/llm_rag_week_1/unsplash_collection/docs/notebooks/supportvectors-common.ipynb`
- `course/rag_2026_week2_uslab/docs/notebooks/embedding/supportvectors-common.ipynb`
- `labs/sv-ai-course-lab/docs/notebooks/supportvectors-common.ipynb`

Method:

```text
load common plotting and ML imports
set notebook style
load .env
add project src/ to sys.path
provide display helpers
```

Useful helpers:

- `sv_table_styles()`
- `format_vertical_headers(df)`
- `use_default_plot_style(enable_tex=False)`
- `copyrights()`
- `add_svlib()`

Use when:

- a notebook starts with `%run supportvectors-common.ipynb`
- imports or plotting style seem to come from nowhere
- local `src/` package needs to be importable inside Jupyter

RAG / Avaloka use:

- Treat this as classroom infrastructure, not a RAG method.
- Useful pattern: keep notebook environment setup explicit and reusable.

## Practical Selection Guide

### If You Need To Build A Basic Text RAG Retriever

Start with:

1. `04_embeddings.ipynb` for the embedding idea.
2. `05_dot_product_similarity.ipynb` for vector scoring.
3. `01-encoder-embeddings.ipynb` for choosing a sentence embedding baseline.
4. `cosine_similarity_histograms_explanation.ipynb` for checking same/different separation.

Minimum eval:

```text
labeled queries
-> relevant chunks
-> candidate embedding model
-> Recall@k / MRR / NDCG
-> cosine same/different gap
-> hard-negative error rate
```

### If You Need To Explain An LLM From Scratch

Use:

1. `01_tokens_and_text.ipynb`
2. `02_probability_next_token.ipynb`
3. `03_softmax_temperature.ipynb`
4. `09_loss_and_training.ipynb`
5. `10_mini_gpt_numpy.ipynb`

Mental model:

```text
text -> tokens -> IDs -> scores -> softmax -> loss -> gradient updates -> generated sequence
```

### If You Need To Explain Attention

Use:

1. `05_dot_product_similarity.ipynb`
2. `06_attention_scores.ipynb`
3. `07_attention_heatmaps.ipynb`
4. `08_transformer_block_step_by_step.ipynb`

Mental model:

```text
query asks
key matches
value returns
softmax decides weight
weighted sum creates contextual representation
```

### If You Need To Decide Whether Fine-Tuning Is Worth It

Use:

1. `cosine_similarity_histograms.ipynb`
2. `03-ft-encoder-embeddings.ipynb`
3. `clip_mnist_contrastive.ipynb` for the multimodal analogy

Decision rule:

```text
Do not fine-tune because it sounds advanced.
Fine-tune only when baseline eval shows a measurable failure and labels exist.
```

### If You Need Multimodal RAG

Use:

1. `02-siglip-embeddings.ipynb`
2. `search_collection.ipynb`
3. `clip_mnist_contrastive.ipynb`

Required metadata:

```text
source
timestamp
license / permission
uploader or owner
OCR text
caption
embedding model version
collection version
```

## Avaloka Integration Notes

For Avaloka AI, these notebooks imply the following baseline method order:

```text
1. Keep deterministic Memory Reader V0 as the baseline.
2. Build labeled query-memory eval pairs.
3. Test a sentence embedding model with Recall@k, MRR, NDCG, and hard-negative errors.
4. Plot same-memory-intent vs different-memory-intent cosine histograms.
5. Only consider fine-tuning if the baseline embedder fails on a named metric.
6. Preserve permission, privacy, risk, freshness, and provenance filters outside the vector score.
```

Important warning:

```text
vector similarity is a candidate retrieval signal,
not proof of truth,
not proof of permission,
not proof of safety,
and not a substitute for evals.
```

