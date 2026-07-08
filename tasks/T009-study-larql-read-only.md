# T009: Study LARQL Through A Read-Only Reproduction

Status: todo

## Goal

Understand LARQL's vindex, LQL browsing, residual tracing, and relationship to RAG and model editing before making any Avaloka integration decision.

## Scope

- Read the LARQL quick start, LQL guide, vindex specification, and working model.
- Read The Illustrated Transformer and explain Query, Key, Value, causal attention, the residual stream, and the MLP/FFN path.
- Review the FFN key-value memory, Knowledge Neurons, and MEMIT papers.
- Use a supported small model or prebuilt browse vindex.
- Run `DESCRIBE`, `WALK`, `TRACE`, and `INFER` on a fixed test set.
- Compare inferred edges with actual model behavior.
- Record disk, RAM, latency, precision, paraphrase consistency, and false associations.
- Keep the experiment read-only.

## Safety Boundary

- Do not use real Avaloka user data.
- Do not insert medical, crisis, spiritual-authority, or private personal facts.
- Do not compile or deploy an edited model during this task.
- Do not treat vindex edges as externally grounded evidence.

## Done When

- A reproducible environment and command log exists.
- At least 30 cases have results.
- `DESCRIBE` to `INFER` agreement is measured.
- At least five failure cases are documented.
- A recommendation is made: continue, narrow the research scope, or stop.

## Reference

- `resources/tools/larql-learning-note.md`
