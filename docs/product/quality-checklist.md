# Quality Checklist

Use this checklist before shipping important outputs, responses, product changes, or user-facing behavior.

## Project-Specific Boundaries

Do not ship if the change:

- treats RAG as the final product rather than an agent substrate
- adds memory retrieval without memory scope rules
- exposes raw private memory
- makes medical, diagnostic, or crisis-treatment claims
- lets old chat context override active docs
- adds complexity before traces and evals exist

## One-Vote Veto

Do not ship if the change:

- violates explicit non-goals
- contradicts current source-of-truth docs
- creates user harm or serious confusion
- claims value that has not been validated
- depends on hidden context outside the repo

## Quality Checks

- [ ] Solves the first use case.
- [ ] Serves the target user.
- [ ] Matches current stage.
- [ ] Avoids non-goals.
- [ ] Has clear acceptance criteria.
- [ ] Has an observable success/failure signal.
- [ ] Updates docs if decisions changed.
- [ ] Includes verification appropriate to risk.
- [ ] Names the agent capability unlocked.
- [ ] Records or references trace/eval evidence when behavior changes.

## Final Question

Would a new agent reading only `README.md`, `AGENTS.md`, and `docs/` understand why this change exists and how to verify it?
