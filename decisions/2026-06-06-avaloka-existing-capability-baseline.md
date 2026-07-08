# Treat Avaloka As An Existing Capability Baseline

Status: accepted

Date: 2026-06-06

## Context

Week 01 concepts map closely to ideas already present in Avaloka AI: intent and risk classification, scoped memory use, safe next-step decisions, guardian review, grounding, traces, and evaluation. Avaloka may not use the newest named retrieval techniques, but many of the underlying product and safety principles already exist.

Treating Avaloka as a greenfield RAG project would risk rebuilding existing capability and confusing newer infrastructure with better product behavior.

## Decision

Use the existing Avaloka system as the baseline implementation. The course will:

1. name and document capabilities that already exist
2. make implicit behavior observable through traces and metrics
3. evaluate existing behavior before replacing it
4. identify concrete gaps
5. add advanced techniques only when a measured gap justifies them

The goal is not to maximize the number of current techniques installed. The goal is to improve Avaloka's Helpful, Harmless, and Honest behavior with the smallest justified architecture.

## Consequences

- Course labs should compare against Avaloka's current behavior, not only a toy RAG baseline.
- Existing product intuition is treated as an asset that needs formalization and evidence.
- New techniques such as SAGE, RAPTOR, GraphRAG, semantic cache, or fine-tuning must demonstrate incremental value.
- The first integration task is a capability and evidence audit, not an immediate rewrite.

## Affected Files

- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `tasks/T007-audit-existing-avaloka-capabilities.md`

## Follow-Up Checks

- Map each Week 01 concept to existing, partial, missing, or unknown Avaloka capability.
- Identify where implementation evidence, traces, or evals are missing.
- Select the first upgrade from measured gaps rather than technical novelty.
