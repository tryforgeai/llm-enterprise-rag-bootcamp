# Document Gardening Checklist

## Purpose

Keep the repository readable for humans and agents by making active docs current and moving stale material into `archive/`.

## Run When

- project direction changes
- target user changes
- MVP scope changes
- validation results arrive
- architecture changes
- an agent is confused by old docs
- before major implementation work

## Check Active Docs

- [ ] `README.md`
- [ ] `AGENTS.md`
- [ ] `docs/product/product-vision.md`
- [ ] `docs/product/version-roadmap.md`
- [ ] `docs/decisions/decision-log.md`
- [ ] `docs/`
- [ ] active plans/specs/runbooks

## Check For Stale Direction

Search for:

- old target users
- old product positioning
- old architecture
- old success criteria
- old version assumptions
- decisions not reflected in roadmap
- contradicted non-goals
- duplicate plans
- deprecated implementation details

## Classify Each Doc

- Active: current source of truth
- Superseded: move to archive
- Reference: historical only
- Draft: not yet approved

## Archive Rule

Move superseded docs to:

`archive/YYYY-MM-DD-superseded-docs/`

Add an archive README explaining:

- archive date
- why the docs were archived
- which active docs replace them

## Completion Criteria

- [ ] A new agent can understand current direction from active docs.
- [ ] Old direction is archived or clearly marked as not current.
- [ ] README links to current docs.
- [ ] AGENTS.md links to current docs.
- [ ] Version roadmap reflects the current accepted decision.
- [ ] Decision log explains meaningful direction changes.
- [ ] No active docs contradict each other.
