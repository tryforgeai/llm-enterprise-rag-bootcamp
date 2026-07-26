# Create A Cross-Project Method Toolkit

Status: accepted

Date: 2026-07-26

## Context

Course notes, notebooks, labs, and runnable demonstrations contain reusable
methods, but discovering and adopting them requires understanding the repository's
weekly history and implementation-specific folders. Future projects need a stable
selection interface without copying machine settings, secrets, vendor choices, or
restricted training source.

## Decision

Add `toolkit/` as the project-independent method layer. Keep original notes and
code as evidence, and describe each reusable method with a stable ID, problem,
minimal approach, selection criteria, measurements, failure signals, source
links, and maturity. Provide an adoption template that requires a baseline,
trace contract, safety boundary, evaluation plan, and removal criterion.

## Consequences

- Course history remains under `course/`, `labs/`, and `resources/`.
- Other projects can adopt methods without adopting Avaloka or SupportVectors
  infrastructure.
- Toolkit maturity does not imply production validation in another domain.
- New methods must retain provenance and portability.
- Architecture complexity remains gated by measured failures.

## Affected Files

- `toolkit/README.md`
- `toolkit/method-catalog.md`
- `toolkit/project-adoption-template.md`
- `README.md`
- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `docs/decisions/decision-log.md`
- `decisions/index.md`
- `PROJECT_PLAN.md`
- `tasks/index.md`
- `tasks/T023-create-cross-project-method-toolkit.md`

## Follow-Up Checks

- Validate internal Markdown links.
- Keep committed paths repository-relative.
- Extend the catalog when future course methods are captured.
- Add executable reference packages only when licensing and cross-project demand
  justify maintaining them.
