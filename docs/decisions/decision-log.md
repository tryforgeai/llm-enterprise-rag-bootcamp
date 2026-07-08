# Decision Log

This file records accepted product, architecture, process, safety, and project-governance decisions.

If documents conflict, follow the newest accepted decision here, then update affected docs. Detailed decision files may also live in the root `decisions/` folder.

## Decision Template

```md
## YYYY-MM-DD — Decision Title

Status: Accepted / Superseded / Rejected

### Context

What changed or what question needed a decision?

### Decision

What did we decide?

### Rationale

Why is this the right decision now?

### Consequences

What changes because of this?

### Affected Docs

- 
```

## 2026-07-08 — Initialize Git Version Control

Status: Accepted

### Context

The project had an agent-first document scaffold but was not yet a Git repository.

### Decision

Initialize this project as a local Git repository and use a conservative `.gitignore` to keep local secrets, system files, local tool session folders, caches, dependency folders, build outputs, logs, nested `.git` metadata, and generated lab artifacts out of version control.

### Rationale

Future agents and humans need a durable history for project documents, labs, decisions, task updates, traces, and eval artifacts. Git is the smallest appropriate version-control layer for that workflow.

### Consequences

The repository can now support reviewable changes and commits. `.env`, `.DS_Store`, local tool session folders, cache folders, virtual environments, dependencies, build outputs, logs, nested `.git` metadata, and generated lab artifacts should remain untracked. The empty nested Git metadata in `course/week_03/week-03-in-person-lab/` was preserved as an ignored `.git.nested-backup-20260708/` folder so the lab source can be tracked by the root repository.

### Affected Docs

- `.gitignore`
- `decisions/2026-07-08-initialize-git-version-control.md`
- `tasks/T018-initialize-git-version-control.md`
- `tasks/index.md`

## 2026-07-08 — Keep Secrets Out Of Git

Status: Accepted

### Context

The project now has a Git repository, and course labs use API keys, access tokens, and local machine-specific environment values.

### Decision

Use the ignored root `.env` file as the only place for real local secrets and machine-specific values. Commit `.env.example` with variable names only. Source code must read credentials from environment variables rather than hardcoding key or token values.

### Rationale

Secrets committed to Git can leak through normal pushes, clones, or history. Keeping real values in ignored local files preserves reproducibility without exposing credentials.

### Consequences

`.env`, `.env.*`, private key files, service account JSON, credential JSON, `.envrc`, and local security reports remain ignored. The SV cluster OpenAI-compatible helper reads `SV_OPENAI_API_KEY` or `OPENAI_API_KEY` from the environment. Agents must run a secret check before committing credential-related changes.

### Affected Docs

- `.gitignore`
- `.env.example`
- `.env` (ignored local file)
- `AGENTS.md`
- `README.md`
- `labs/sv_ray_cluster_access/src/ray_cluster_access/sv_cluster_access_api.py`
- `labs/sv_ray_cluster_access/.env.example`
- `course/week_04/chunking_pipeline/.env.example`
- `decisions/2026-07-08-keep-secrets-out-of-git.md`
- `tasks/T019-keep-secrets-out-of-git.md`

## 2026-06-01 — Make The Bootcamp Project Agent-First

Status: Accepted

### Context

The project began as a learning system for an enterprise RAG bootcamp. That was useful, but Avaloka AI needs course concepts to become agent capabilities.

### Decision

Treat RAG as the evidence and memory substrate inside this agent loop:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

### Rationale

Avaloka needs decisions about when to retrieve, when to use memory, when to ask, when to refuse, and how to evaluate outcomes. Plain retrieve-and-answer demos are not enough.

### Consequences

Weekly notes, labs, evals, and application maps should identify agent behavior, trace fields, and eval cases.

### Affected Docs

- `README.md`
- `PROJECT_PLAN.md`
- `course/week-01.md`
- `labs/01-minimal-rag-demo-plan.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `decisions/2026-06-01-agent-first-project.md`

## 2026-06-01 — Require Decision Logging

Status: Accepted

### Context

Important project direction changes can get lost in scattered notes or chat context.

### Decision

Important decisions must be recorded in `docs/decisions/decision-log.md` and, when useful, as detailed files in `decisions/`.

### Rationale

Future agents need repository-visible reasons, not hidden chat memory.

### Consequences

Agents must check decision logs before changing direction and update them before final response when meaningful decisions change.

### Affected Docs

- `AGENTS.md`
- `docs/decisions/decision-log.md`
- `decisions/index.md`

## 2026-06-01 — Install Agent-First Bootstrap Skill Scaffold

Status: Accepted

### Context

The local skill `agent-first-project-bootstrap` exists and validates when installed at `~/.codex/skills/agent-first-project-bootstrap`. Its standard audit expects active source-of-truth docs under `docs/`.

### Decision

Use the installed skill scaffold as the project governance layer while preserving the project-specific bootcamp files already created.

### Rationale

The skill gives a repeatable audit/bootstrap/garden workflow and a clearer source-of-truth structure for future agents.

### Consequences

`docs/` becomes the active governance layer. Existing root folders such as `course/`, `labs/`, `tasks/`, `traces/`, `evals/`, and `decisions/` remain project-specific working areas.

### Affected Docs

- `AGENTS.md`
- `README.md`
- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `docs/decisions/decision-log.md`
- `docs/engineering/harness-engineering-setup.md`
- `docs/experiments/validation-runbook.md`
- `docs/product/quality-checklist.md`

## 2026-06-01 — Make Agent-First Bootstrap A Global Codex Default

Status: Accepted

### Context

`agent-first-project-bootstrap` was already installed in `~/.codex/skills`, but it did not appear in the current session's visible skill list. That caused unnecessary GitHub lookup and delayed use of the local skill.

### Decision

Update global Codex instructions in `~/.codex/AGENTS.md` so future sessions check local skills before searching externally, and prefer `agent-first-project-bootstrap` for new, under-scaffolded, or agent-ready project work.

### Rationale

This makes agent-first project governance a default Codex behavior on this machine instead of a per-project convention.

### Consequences

Future project bootstrap/review requests should start by checking `~/.codex/skills/agent-first-project-bootstrap`, running its audit, and using its bootstrap before inventing a custom scaffold.

### Affected Docs

- `~/.codex/AGENTS.md`
- `docs/decisions/decision-log.md`

## 2026-06-06 — Switch From Pre-Class Preparation To Active Course Execution

Status: Accepted

### Context

The Summer 2026 LLM and Enterprise RAG Bootcamp started on June 6, 2026. The project should no longer optimize its current workflow around pre-class preparation.

### Decision

Keep the pre-class plan as reference, but make the active workflow:

```text
live class -> capture -> agent capability -> Avaloka application -> eval -> next lab task
```

### Rationale

The highest-value work now is converting each live class into durable notes, questions, evals, and implementation tasks while the material is fresh.

### Consequences

- `course/week-01.md` becomes the immediate working document.
- The roadmap stage changes to active course / Week 01.
- Pre-class preparation remains historical reference and is not deleted.

### Affected Docs

- `README.md`
- `PROJECT_PLAN.md`
- `course/00-course-overview.md`
- `course/week-01.md`
- `docs/product/version-roadmap.md`
- `tasks/index.md`

## 2026-06-06 — Require Evidence Before Increasing Architecture Complexity

Status: Accepted

### Context

The course introduces hybrid retrieval, adaptive selection, RAPTOR, GraphRAG, and fine-tuning. Installing these techniques before establishing a baseline would create architecture inundation and make failures harder and more expensive to diagnose.

### Decision

Start Avaloka and bootcamp labs from the smallest complete, observable baseline. Add a component only when traces and domain-specific evals demonstrate a failure that the component is expected to address.

Every escalation must name its target failure, success metric, expected operating cost, comparison baseline, and removal criterion.

### Rationale

Scale changes which architecture is appropriate, but anticipated future scale is not sufficient evidence for current complexity. Each component must earn its place through measurable improvement.

### Consequences

- GraphRAG and fine-tuning remain deferred until eval evidence supports them.
- New retrieval layers must be measurable and reversible.
- Project reviews should remove components that do not improve their named eval.

### Affected Docs

- `course/week-01.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `decisions/2026-06-06-evidence-driven-architecture-escalation.md`

## 2026-06-27 — Use SV Cluster For Week 04 FactoidWiki Experiments

Status: Accepted

### Context

Week 04 shifted from raw chunk retrieval toward derived retrieval artifacts: factoids, QA pairs, summaries, and grounded answer synthesis. The Task 2 Xennials demo needed a live source and a real model-backed pipeline.

### Decision

Use Wikipedia as the live source, section-aware raw chunks as the evidence base, SV cluster chat models for factoid and QA-pair generation, SV cluster text embeddings for the vector index, and Streamlit as the lightweight inspection UI.

### Rationale

This keeps the experiment close to the course's FactoidWiki/Dense-X theme while avoiding unnecessary infrastructure. JSON files remain the first storage layer; Qdrant or another vector database can be added later once the artifact behavior is understood.

### Consequences

- Week 04 Task 2 uses `Qwen/Qwen3-VL-8B-Instruct` for factoid generation.
- Week 04 Task 2 uses `Qwen/Qwen3-Embedding-0.6B` for embeddings.
- Streamlit is the intended UI framework for artifact inspection.
- The project keeps local JSON artifacts as the source of truth before introducing Qdrant.

### Affected Docs

- `tasks/T017-week-04-xennials-factoid-wiki.md`
- `course/week_04/task_02_xennials_factoid_wiki/README.md`
- `course/week_04/task_02_xennials_factoid_wiki/sv_factoid_wiki.py`

## 2026-06-06 — Treat Existing Avaloka Capability As The Baseline

Status: Accepted

### Context

Avaloka already appears to implement many of the course's core ideas through intent and risk routing, scoped memory use, guardian review, safety boundaries, traces, and evaluation-oriented design. It does not necessarily use the newest named retrieval techniques.

### Decision

Do not treat Avaloka as a greenfield RAG implementation. First document and evaluate existing capabilities, then add advanced course techniques only for demonstrated gaps.

### Rationale

Product behavior and safety design matter more than collecting fashionable infrastructure. Existing intuition should be made observable and tested before it is replaced.

### Consequences

- Create a capability audit covering implementation evidence, traces, evals, and gaps.
- Use current Avaloka behavior as the comparison baseline.
- Choose future experiments from measured failures rather than novelty.

### Affected Docs

- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `tasks/T007-audit-existing-avaloka-capabilities.md`

## 2026-06-06 — Benchmark The Existing Memory Reader Before Upgrading Retrieval

Status: Accepted

### Context

The Avaloka capability audit found a working deterministic Care Card reader with safety-aware ranking, but no formal retrieval metrics. Advanced retrieval techniques cannot demonstrate incremental value until the current reader has a labeled baseline.

### Decision

Make the first Avaloka course-integration experiment a fixed retrieval benchmark for Memory Reader V0. Measure Recall@5, MRR, NDCG@5, unsafe and stale retrievals, no-match precision, and latency before proposing embeddings, hybrid retrieval, reranking, RAPTOR, or GraphRAG.

### Rationale

The measured failure should choose the component. A semantic paraphrase miss may justify embeddings; a ranking miss may justify reranking; a relationship miss may eventually justify graph retrieval.

### Consequences

- The deterministic reader becomes the comparison baseline.
- New retrieval infrastructure must improve a named metric without weakening privacy or safety.
- GraphRAG, RAPTOR, semantic cache, and fine-tuning remain deferred.

### Affected Docs

- `reviews/04-avaloka-week-01-capability-audit.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `tasks/T007-audit-existing-avaloka-capabilities.md`
- `tasks/T008-benchmark-avaloka-memory-reader.md`
- `decisions/2026-06-06-benchmark-memory-reader-before-upgrade.md`

## 2026-06-07 — Study LARQL Before Any Avaloka Adoption

Status: Accepted

### Context

LARQL reorganizes transformer weights into a queryable vindex and exposes browsing, tracing, mutation, and compilation through LQL. It is relevant to model interpretability and knowledge editing, but its inferred edges are not authoritative database facts and its project claims need independent reproduction.

### Decision

Study LARQL through a read-only experiment first. Compare `DESCRIBE`, `WALK`, `TRACE`, and `INFER` on public and synthetic cases before considering model patches or Avaloka integration.

### Rationale

The most valuable immediate capability is inspecting and tracing model behavior. Mutation has a larger evaluation and safety burden, including efficacy, paraphrase generalization, locality, neighborhood effects, consistency, and reversibility.

### Consequences

- LARQL becomes a research and mechanistic-interpretability learning track.
- It is not a replacement for RAG, GraphRAG, Care Card memory, or external grounding.
- No private Avaloka data will be inserted into model weights.
- Mutation and model compilation require a later decision based on read-only evidence.

### Affected Docs

- `resources/tools/larql-learning-note.md`
- `tasks/T009-study-larql-read-only.md`
- `decisions/2026-06-07-study-larql-before-adoption.md`

## 2026-06-13 — Use A Verified SupportVectors Classroom Environment

Status: Accepted

### Context

Week 02 requires a consistent Python environment for AI, embedding, Transformer, and RAG labs. The SupportVectors configurator provides the expected project structure but did not stop after failed dependency commands and required machine-specific Python and TLS handling.

### Decision

Use `labs/sv-ai-course-lab` as the isolated classroom environment with `uv`, Python 3.12.7, `svlearn-bootcamp`, a committed dependency lockfile, and explicit environment, package-build, and documentation verification.

Use macOS native TLS rather than disabling certificate checks. Use `BOOTCAMP_ROOT_DIR`, keep API keys empty by default, and ignore `.env`.

### Rationale

The course needs a reproducible environment without mixing lab dependencies into project notes or Avaloka production code. Verification must reflect actual imports and builds rather than the configurator's success message.

### Consequences

- Future coding labs can share one verified Python environment.
- Lab-specific packages should be added through `uv add`.
- API keys remain local and uncommitted.
- Setup troubleshooting and verification evidence are recorded in the repository.

### Affected Docs

- `labs/sv-ai-course-lab/`
- `labs/02-sv-ai-environment-setup.md`
- `tasks/T012-setup-sv-ai-environment.md`
- `decisions/2026-06-13-supportvectors-classroom-environment.md`

## 2026-06-27 — Build Curriculum Weaver Lite As A Bootcamp Course Lab

Status: Accepted

### Context

The Curriculum Weaver project is part of the LLM and Enterprise RAG Bootcamp course work. It was initially created in the Avaloka AI folder by mistake, but its purpose is to practice course concepts: LLMs, RAG, learner memory, agent tracing, evaluation, and UI testing.

### Decision

Move Curriculum Weaver Lite into `labs/curriculum-weaver-lite/` and treat it as a Bootcamp course lab. The project will start with a static UI demo for learning self-attention, then expand into real ingestion, retrieval, learner memory, LLM lesson synthesis, quiz evaluation, trace dashboard, and tests.

### Rationale

This keeps course exercises inside the course system of record while preserving Avaloka as a downstream application context rather than the owner of this lab.

### Consequences

- Curriculum Weaver Lite lives under `labs/`.
- The course task queue tracks the project as `T015`.
- The detailed decision file is `decisions/2026-06-27-curriculum-weaver-lite-course-project.md`.
- Future agents should read the lab's local `README.md`, `AGENTS.md`, and proposal before changing it.

### Affected Docs

- `labs/curriculum-weaver-lite/`
- `tasks/index.md`
- `tasks/T015-curriculum-weaver-lite.md`
- `decisions/2026-06-27-curriculum-weaver-lite-course-project.md`
