# Project Gotchas

This file records active traps future humans and agents should check before changing project direction, tasks, labs, or governance.

## 2026-07-18 — Course Week Is Not Product Version

Status: Active

### Trigger

Updating the roadmap after a new class or lab is completed.

### Symptom

Later-week artifacts make the project appear ready to advance from v0.1 even though canonical traces, eval cases, memory policy, or the minimal loop are still missing.

### Cause

Course chronology and agent-first product maturity are separate dimensions.

### Avoidance

Update the roadmap stage to the current course week, but advance the product version only when its explicit exit criteria are satisfied.

### Evidence

- `docs/product/version-roadmap.md`
- `decisions/2026-07-18-align-governance-with-week-06.md`

## 2026-07-18 — RAG Gardening Hits Are Usually False Positives

Status: Active

### Trigger

Running the agent-first document-gardening command in this repository.

### Symptom

Most active documents are proposed as superseded merely because they mention RAG or long-term memory.

### Cause

The generic scanner treats these phrases as possible stale direction, but RAG is the course subject and memory is an explicit Avaloka research boundary.

### Avoidance

Treat garden output as candidate-only. Never use `garden --apply` without manually proving that each document conflicts with newer authority. Track scanner tuning under T005.

### Evidence

- `tasks/T005-gardening-false-positives.md`
- `docs/product/product-vision.md`

## 2026-07-18 — Lab Verification Depends On The Intended Environment

Status: Active

### Trigger

Running Week 03 or Curriculum Weaver tests with the system Python or a machine-specific cached browser runtime.

### Symptom

Tests fail before exercising project behavior because dependencies such as NumPy or Playwright cannot be resolved.

### Cause

Some labs assume their verified `uv` environment, while the Curriculum Weaver smoke test currently references a machine-specific bundled Playwright location.

### Avoidance

Read the lab README and environment setup first. Distinguish dependency/bootstrap failures from product-test failures, and remove machine-specific runtime paths when that lab is next modified.

### Evidence

- `labs/02-sv-ai-environment-setup.md`
- `course/week_03/tests/test_qa_paths.py`
- `labs/curriculum-weaver-lite/scripts/smoke-test.cjs`

## 2026-07-18 — Run Week 03 Pytest From Its Project Directory

Status: Active

### Trigger

Invoking the Week 03 environment from the repository root while leaving pytest's collection directory unspecified.

### Symptom

Pytest collects unrelated lab files and reports an import mismatch because multiple labs contain a module named `test_setup.py`.

### Cause

Selecting a `uv` project does not automatically change the process working directory used by pytest discovery.

### Avoidance

Run the documented commands after `cd course/week_03`, or explicitly pass `course/week_03/tests` to pytest.

### Evidence

- `course/week_03/pyproject.toml`
- `course/week_03/README.md`
