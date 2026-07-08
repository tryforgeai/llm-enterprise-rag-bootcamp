# LARQL Learning Note

Status: Active research note

Date: 2026-06-07

Primary source:

- [chrishayuk/larql](https://github.com/chrishayuk/larql)

Relevant research foundations:

- [Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913)
- [Knowledge Neurons in Pretrained Transformers](https://arxiv.org/abs/2104.08696)
- [Mass-Editing Memory in a Transformer](https://arxiv.org/abs/2210.07229)

## Executive View

LARQL is an experimental Rust system for reorganizing transformer weights into a queryable format called a **vindex** and interacting with it through **LQL**, the Lazarus Query Language.

Its central metaphor is:

> The model is the database.

This is useful, but should not be interpreted literally. A model does not contain clean relational rows with authoritative provenance. LARQL derives queryable features and associations from embeddings, FFN gate vectors, down projections, probes, and inference traces.

The most useful mental model is:

```text
transformer weights
-> reorganized feature index
-> browse and trace learned associations
-> optionally create reversible knowledge-edit patches
-> evaluate the edited model
```

## What LARQL Adds

### Vindex

A vindex reorganizes model weights for queryability:

```text
gate vectors -> KNN feature index
embedding matrix -> token lookup
down projections -> feature-to-output metadata
model metadata -> layers, provenance, quantization, tokenizer
```

Repository documentation describes three practical extraction levels:

| Level | Main purpose |
| --- | --- |
| browse | `DESCRIBE`, `WALK`, and feature queries without a full forward pass |
| inference | browse plus local `INFER` |
| all | inference plus compilation of edits into a new model |

### LQL

LQL exposes several classes of operation:

- lifecycle: `EXTRACT`, `USE`, `COMPILE`, `DIFF`
- browsing: `DESCRIBE`, `WALK`, `SELECT`
- inference: `INFER`
- tracing: `TRACE`, decomposition by layer or component
- mutation: `INSERT`, `UPDATE`, `DELETE`, `MERGE`
- patches: create, save, apply, inspect, and remove overlays

### Read-Only Model Inspection

Example:

```sql
USE "gemma3-4b.vindex";
DESCRIBE "France";
WALK "The capital of France is" TOP 10;
TRACE "The capital of France is" FOR "Paris";
```

This can help explore:

- token and feature neighborhoods
- which layers contribute to an answer
- attention versus FFN contribution
- when an answer becomes dominant in the residual stream
- whether a proposed model edit changes the intended trajectory

### Reversible Model Editing

LARQL represents edits as patch overlays rather than immediately overwriting the base vindex:

```sql
BEGIN PATCH "example.vlp";

INSERT INTO EDGES (entity, relation, target)
VALUES ("Atlantis", "capital-of", "Poseidon");

SAVE PATCH;
```

This makes experiments reversible and diffable. A patch may later be compiled into a standalone vindex or model.

## What Must Not Be Assumed

### 1. A Described Edge Is Not A Database Fact

`DESCRIBE "France"` returns inferred associations supported by model features and probes. It does not prove:

- that the relation is consistently expressed under paraphrase
- that the model will use it in every context
- that the fact is current
- that the association has a traceable original source
- that the edge is isolated from other concepts

### 2. No GPU Does Not Mean No Compute Cost

Browse operations can run without a GPU. Full inference can also use CPU paths, but repository benchmarks show CPU inference is much slower than accelerated inference. Vindex extraction and storage still require substantial disk, RAM, and time.

### 3. Model Editing Needs More Than One Prompt

After an edit, evaluate:

- **efficacy**: does the target prompt produce the new fact?
- **paraphrase generalization**: do semantically equivalent prompts use it?
- **locality**: are unrelated facts preserved?
- **neighborhood effects**: are related entities damaged?
- **consistency**: does the edit survive different contexts and generation settings?
- **reversibility**: does removing the patch restore the baseline?
- **portability**: does recompilation preserve the behavior?

### 4. Repository Results Are Not Independent Validation

LARQL is young and evolving rapidly. Its detailed benchmarks and experiments are valuable engineering evidence, but many headline claims currently come from the project itself rather than peer-reviewed or independently reproduced evaluations.

## Relationship To Course Concepts

| Course concept | Relationship to LARQL |
| --- | --- |
| RAG | RAG retrieves external evidence; LARQL inspects or edits internal parameters |
| Vector search | Both use vector similarity, but LARQL indexes model features rather than document chunks |
| GraphRAG | GraphRAG constructs an external entity and relationship graph; LARQL derives graph-like associations from model internals |
| Text-to-SQL | LQL offers a database-like language, but its target is a vindex rather than business tables |
| Fine-tuning | LARQL patches targeted weight structures without ordinary gradient fine-tuning |
| Grounding | LARQL can inspect internal trajectories, but internal association is not external evidence or citation grounding |
| Eval | Every browse result and mutation needs behavioral, locality, and falsification tests |
| Trace | Residual-stream tracing is LARQL's most directly relevant agent-observability capability |

## Relationship To Avaloka

LARQL could eventually help Avaloka with:

- inspecting what a local model associates with crisis, blame, karma, illness, and compassion concepts
- comparing model versions before and after safety changes
- tracing where unsafe or overconfident answer tokens become dominant
- testing reversible patches for narrow behavior or factual errors
- studying whether a local model encodes undesirable associations

LARQL should not replace Avaloka's external evidence and memory systems:

- private user memory needs permission scopes and deletion
- safety policies need explicit versioning and auditability
- current facts need freshness and provenance
- Buddhist or care sources need source attribution
- user-specific facts should not be baked into shared model weights

Recommended boundary:

```text
external RAG and Care Card
-> current, private, attributable, permission-scoped knowledge

LARQL
-> model inspection, mechanistic traces, and controlled research edits
```

## Learning Path

### Phase 1: Foundations

Learn:

- transformer embedding and unembedding matrices
- residual stream
- attention versus FFN/MLP
- gated FFNs: gate, up, and down projections
- FFNs as key-value memories
- knowledge neurons
- model editing: ROME and MEMIT
- logit lens, activation patching, ablation, and steering

Success criterion:

Explain what a LARQL edge represents and why it is not equivalent to a stored relational fact.

### Phase 2: Read-Only LARQL

Use a small supported model or prebuilt browse vindex.

Practice:

```text
USE
SHOW MODELS / LAYERS / FEATURES / RELATIONS
DESCRIBE
WALK
EXPLAIN WALK
TRACE
INFER
```

Do not mutate or compile yet.

Success criterion:

Create a report comparing `DESCRIBE`, `WALK`, `TRACE`, and actual `INFER` behavior on a fixed set of factual and safety-sensitive prompts.

### Phase 3: Falsification

Build cases containing:

- true facts
- false premises
- ambiguous relations
- paraphrases
- negation
- multilingual prompts
- polysemous entities
- knowledge outside the model's likely training distribution

Measure:

- edge precision
- paraphrase consistency
- layer stability
- `DESCRIBE` to `INFER` agreement
- false association rate
- latency and disk/RAM cost

### Phase 4: Reversible Patch Experiment

Create one synthetic, harmless fact that cannot be confused with real user or medical data.

Run:

```text
baseline inference
-> create patch
-> apply patch
-> target and paraphrase evals
-> locality and neighborhood evals
-> remove patch
-> verify baseline restoration
```

Only after this should compilation into a new model be considered.

### Phase 5: Avaloka Research Experiment

Use LARQL read-only inspection on a local model to study one narrow question, for example:

> Where and how does the model begin to prefer karma-blame language over conditions-based, non-blaming language?

This experiment must not use real private user memories.

## First Experiment

Start with read-only browsing, not model editing.

Suggested dataset:

1. ten stable public facts
2. five false-premise prompts
3. five paraphrase groups
4. five ambiguous entity or relation cases
5. five Avaloka safety-language probes using synthetic scenarios

For each case record:

- `DESCRIBE` result
- `WALK` result
- `TRACE` or layer trajectory where available
- `INFER` top-k
- expected answer
- agreement or contradiction
- confidence interpretation
- failure notes

## Current Recommendation

Learn LARQL now as a **research and interpretability tool**.

Do not yet:

- integrate it into Avaloka runtime
- store private memory in weight patches
- treat feature edges as grounded facts
- use it to replace RAG
- compile edited production models

The first adoption decision should wait for a read-only reproduction with measured precision and failure cases.

