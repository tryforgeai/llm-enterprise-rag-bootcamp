# Decision Log

This file records accepted product, architecture, process, safety, and project-governance decisions.

If documents conflict, follow the newest accepted decision here, then update affected docs. Detailed decision files may also live in the root `decisions/` folder.

## 2026-08-01 — Make Avaloka Calibration R1 The Next Execution Slice
## 2026-08-14 — Establish The First Measured Eval Baseline With A Deliberately Weak Retriever

Status: Accepted

### Context

Week 06 established Avaloka's trust-boundary vocabulary, and Week 07/08 established the measurement discipline needed to prove whether retrieval, grounding, refusal, and humility actually work. The project already had decisions to treat existing Avaloka behavior as the baseline and benchmark Memory Reader V0 before adding advanced retrieval infrastructure.

### Decision

Make Avaloka Calibration R1 the next execution slice: build the first Care Card / Memory Reader gold eval scaffold, unknown/abstention cases, Baifa / Dharma boundary cases, and a calibration trace contract before embeddings, reranking, RAPTOR, GraphRAG, vector databases, or fine-tuning.

### Rationale

Avaloka's highest-risk failure is not low novelty; it is unsupported certainty over personal memory. Calibration requires domain-specific gold cases, retrieval metrics, claim grounding, and abstention measurement rather than model self-reported confidence or public benchmarks.

### Consequences

- T008 becomes the active anchor for measurable retrieval work.
- T002 receives the first eval-case structure needed by the benchmark.
- Advanced retrieval components remain deferred until measured failures justify them.
- `templates/calibration-agent-trace.json` records the minimum evidence needed to diagnose answerability and failure class.

### Affected Docs

- `decisions/2026-08-01-avaloka-calibration-r1.md`
- `PROJECT_PLAN.md`
- `tasks/index.md`
- `evals/avaloka-memory-reader-v0/`
- `evals/avaloka-unknown-calibration-v0/`
- `evals/avaloka-baifa-dharma-boundary-v0/`
- `templates/calibration-agent-trace.json`

Weeks 07, 08, and 09 taught retrieval evaluation, generator evaluation, and governed-corpus design across three full class sessions. Meanwhile `evals/` and `traces/` were still empty, and every remaining v0.1 exit criterion was blocked behind the missing eval set. The project was accumulating evaluation theory while having nothing of its own to evaluate.

The architecture escalation rule in `PROJECT_PLAN.md` requires a named failure and a comparison baseline before any component is added. Without a baseline, that rule was unenforceable: no upgrade could be justified or refused on evidence.

### Decision

Build the first 10 agentic RAG eval cases against the existing Week 04 Xennials FactoidWiki index, and score them with a standard-library-only runner and a deliberately weak agent: BM25 retrieval and a rule-based decision function.

Reject three tempting alternatives:

- Waiting for a good retriever before writing evals. That inverts the dependency; the evals are what tell us which retriever is good.
- Using dense retrieval as the baseline. It requires the classroom endpoint at `10.0.10.51`, which makes the baseline unreproducible off the course network.
- Using BM25 score as the confidence signal. It is unbounded and corpus-relative, so it cannot be thresholded across cases. Use the fraction of question terms covered by the best retrieved record instead: bounded, interpretable, checkable by hand, and — as EV-006 proves — wrong in an instructive way.

### Rationale

A weak baseline that runs everywhere is worth more than a strong one that runs only in class. The value of the first baseline is not its score but the failures it names.

### Consequences

- Mean recall@5 0.333, nDCG@5 0.377, MRR 0.600, decision accuracy 0.900, safety pass rate 0.900, NRR 0.667, with 6 of 10 cases passing. These are now the numbers any upgrade must beat.
- Three of the four failures are retrieval failures, which fixes the upgrade order: retrieval first, and still not GraphRAG. Dense retrieval is the first experiment to run, because the Week 04 index already carries the vectors and only the query-side endpoint is missing.
- A verification pass caught two bugs before the numbers were trusted: an nDCG normalization error, and a label leak where the decision policy read the case file's own `min_distinct_evidence` field. Numeric pass bars are now enforced fields rather than prose, which moved the headline from 7 of 10 to 6 of 10. An eval harness gets evaluated too.
- `traces/` is no longer empty. Each run writes one trace per case, satisfying that v0.1 exit criterion mechanically rather than by hand.
- Generated text is still not scored. Week 08's FActScore, ECE, and RAGAS faithfulness need a model in the loop and remain unimplemented.
- EV-009 stands in for Avaloka memory scoping but is not a substitute for T003.

### Affected Docs

- `evals/`
- `traces/`
- `README.md`, `PROJECT_PLAN.md`, `docs/product/version-roadmap.md`
- `tasks/index.md`, `tasks/T002-first-agentic-rag-evals.md`, `tasks/T025`, `tasks/T026`

## 2026-08-14 — Advance Governance Stage To Week 09

Status: Accepted

### Context

`README.md`, `PROJECT_PLAN.md`, and `docs/product/version-roadmap.md` all described the course as active in Week 07 while Week 08 and Week 09 had already been taught and captured. Week 09's own material argues that a knowledge object which has changed since it was last verified is a governance failure; the project's governance docs were exactly that.

### Decision

Advance the stated stage to Week 09 without advancing the product version. v0.1 remains open because its agent-first exit criteria — memory scope policy, the runnable loop, and the Memory Reader benchmark — are still incomplete.

### Consequences

- Course capture and product version are explicitly decoupled, as they were for the Week 06 alignment decision.
- The Week 04 and Week 05 note gap is now recorded in the roadmap rather than silently absent (T027).
- Remaining v0.1 work shrinks to three items: T003 memory scopes, T004 runnable loop, T008 Memory Reader benchmark.

### Affected Docs

- `README.md`, `PROJECT_PLAN.md`, `docs/product/version-roadmap.md`, `tasks/index.md`

## 2026-07-26 — Create A Cross-Project Method Toolkit

Status: Accepted

### Context

Reusable methods were distributed across weekly notes, notebooks, labs, and
implementation-specific README files, making adoption by another project depend
on knowledge of the bootcamp's internal history.

### Decision

Create `toolkit/` as a provider-neutral, repository-relative method layer. Give
methods stable IDs and record their problem, selection conditions, measurements,
failure signals, evidence, and maturity. Require cross-project adoption to state
a baseline, trace contract, safety boundary, evaluation plan, and removal
criterion.

### Rationale

The original artifacts should preserve learning history and implementation
evidence, while future projects need a compact interface for choosing and
reimplementing methods without copying local infrastructure or restricted source.

### Consequences

- `course/`, `labs/`, and `resources/` remain the evidence layer.
- `toolkit/` becomes the reusable selection and adoption layer.
- Toolkit inclusion does not imply production validation.
- New methods must preserve provenance, portability, and evidence-driven
  escalation.

### Affected Docs

- `toolkit/`
- `README.md`
- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `PROJECT_PLAN.md`
- `decisions/2026-07-26-create-cross-project-method-toolkit.md`
- `tasks/T023-create-cross-project-method-toolkit.md`

## 2026-07-25 — Advance Governance Stage To Week 07 Evaluation

Status: Accepted

### Context

The remote course history added Week 07 evaluation notes and runnable metric demos after the Week 06 governance and portability work was created locally.

### Decision

Advance the active course stage to Week 07 while retaining product version v0.1. Make the immediate milestone a real retrieval-evaluation baseline that connects Week 07 metrics to T002 eval cases and T008 Memory Reader benchmarking.

### Rationale

Week 07 adds the measurement vocabulary needed to close the existing v0.1 evidence gaps, but pre-class notes and metric demonstrations do not yet satisfy the required canonical eval set, trace, memory policy, or Avaloka baseline.

### Consequences

- README, roadmap, and project plan now identify Week 07 as current.
- T021 remains doing until live discussion, a real baseline artifact, and concrete Avaloka evaluation design are captured.
- v0.1 remains active.

### Affected Docs

- `README.md`
- `PROJECT_PLAN.md`
- `docs/product/version-roadmap.md`
- `tasks/T021-week-07-class-capture.md`
- `decisions/2026-07-25-week-07-evaluation-stage.md`

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

## 2026-07-18 — Align Governance With Week 06 Without Advancing The Product Version

Status: Accepted

### Context

Course work has advanced through Week 06 and now includes representation experiments, derived retrieval artifacts, graph-shaped learning artifacts, a pedagogy-first UI demo, and a runnable mocked guardrailed RAG pipeline. The root roadmap still described the project as active Week 03, while several foundational v0.1 exit criteria remain incomplete.

### Decision

Update the active stage and scope to reflect Week 06, close T014 because all of its stated criteria are satisfied, and keep T011, T015, and T020 active because their eval, feedback, or implementation criteria remain open. Keep the product version at v0.1 until the first 10 eval cases, Avaloka memory policy, canonical trace, and minimal trace-and-eval loop exist.

### Rationale

Course chronology and product maturity measure different things. Governance should accurately reflect completed learning artifacts without implying that the agent-first product loop has reached v0.2 readiness.

### Consequences

- The roadmap now reports active course / Week 06.
- v0.1 scope records the Week 03 through Week 06 artifacts already created.
- T014 is done; T011, T015, and T020 remain doing.
- The immediate product focus remains evals, memory scope, canonical traces, the minimal runnable loop, and the Memory Reader V0 benchmark.
- `docs/knowledge/` now holds active gotchas and important fix evidence for future agents.
- `README.md`, `AGENTS.md`, and `PROJECT_PLAN.md` now point agents at the Week 06 governance state and current v0.1 milestone.

### Affected Docs

- `docs/product/version-roadmap.md`
- `tasks/index.md`
- `tasks/T014-week-03-class-capture.md`
- `docs/decisions/decision-log.md`
- `decisions/2026-07-18-align-governance-with-week-06.md`
- `README.md`
- `AGENTS.md`
- `PROJECT_PLAN.md`
- `docs/knowledge/gotchas.md`
- `docs/knowledge/fix-log.md`

## 2026-07-18 — Require Clone-Portable Repository Verification

Status: Accepted

### Context

Week 03 tests depended on globally available Python packages, browser scripts imported Playwright and Chrome from one machine, and several committed records contained user-specific absolute paths.

### Decision

Use repository-relative paths in committed code and metadata. Lock Week 03 test dependencies with `uv`; lock browser verification dependencies at the repository root with npm; use Playwright-managed Chromium; and make the Curriculum Weaver smoke test start its own ephemeral local server.

### Rationale

A Git repository is not reproducible when successful verification depends on the original author's username, clone directory, global packages, browser installation, or fixed local port.

### Consequences

- `uv sync --frozen && uv run pytest` is the Week 03 verification path.
- `npm ci`, `npx playwright install chromium`, and `npm test` are the browser verification path.
- Generated metadata must use repository-relative labels and must not persist machine locations.
- Local dependency directories and temporary test outputs remain ignored.

### Affected Docs

- `README.md`
- `course/week_03/README.md`
- `course/week_03/pyproject.toml`
- `course/week_03/uv.lock`
- `package.json`
- `package-lock.json`
- `labs/curriculum-weaver-lite/README.md`
- `labs/curriculum-weaver-lite/scripts/smoke-test.cjs`
- `scripts/render_architecture_png.mjs`
- `docs/knowledge/gotchas.md`
- `docs/knowledge/fix-log.md`
- `tasks/T022-portable-repository-verification.md`
- `decisions/2026-07-18-clone-portable-verification.md`

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
- `course/week_01/week-01.md`
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

- `course/week_01/week-01.md` becomes the immediate working document.
- The roadmap stage changes to active course / Week 01.
- Pre-class preparation remains historical reference and is not deleted.

### Affected Docs

- `README.md`
- `PROJECT_PLAN.md`
- `course/00-course-overview.md`
- `course/week_01/week-01.md`
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

- `course/week_01/week-01.md`
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
