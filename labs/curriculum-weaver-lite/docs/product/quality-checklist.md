# Quality Checklist

Use this checklist before shipping important outputs, responses, product changes, or user-facing behavior.

## Project-Specific Boundaries

- The UI must show the learning process, not a generic chatbot answer.
- The system must distinguish static demo data from real AI/RAG modules.
- Every lesson should show source cards.
- The path should respect prerequisite order.
- The app should work on desktop and mobile.
- No invented citation, unsupported equation, or real private student data.

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
- [ ] For UI changes, desktop and mobile smoke tests pass.
- [ ] For planner changes, prerequisite order still makes sense.
- [ ] For source changes, citations remain visible.

## Final Question

Would a new agent reading only `README.md`, `AGENTS.md`, and `docs/` understand why this change exists and how to verify it?
