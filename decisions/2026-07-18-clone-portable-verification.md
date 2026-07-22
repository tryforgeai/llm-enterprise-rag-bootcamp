# Require Clone-Portable Repository Verification

Status: accepted

Date: 2026-07-18

## Context

The Week 03 tests and Curriculum Weaver smoke test could not be reproduced from an arbitrary clone. Python dependencies were implicit, Playwright and Chrome paths were tied to one workstation, the browser test expected a separately started fixed-port server, and committed code and records contained machine locations.

## Decision

- Store only repository-relative filesystem paths in committed code and metadata.
- Use a Week 03 `pyproject.toml` plus `uv.lock` for the offline Python unit suite.
- Use root `package.json` plus `package-lock.json` for browser verification.
- Use the Playwright-managed Chromium build instead of a system browser path.
- Make the Curriculum Weaver smoke test start and stop its own ephemeral local server.
- Write screenshots and test results only to the operating system temporary directory.

## Consequences

- A contributor can verify the supported suites from any clone location using the README commands.
- Dependency upgrades become explicit lockfile changes.
- Browser verification no longer assumes a username, Codex runtime cache, installed Chrome path, or fixed port.
- Generated artifacts must be checked for leaked machine paths before being committed.

## Affected Files

- `README.md`
- `package.json`
- `package-lock.json`
- `course/week_03/README.md`
- `course/week_03/pyproject.toml`
- `course/week_03/uv.lock`
- `course/week_03/contextual_chunk_pdf.py`
- `course/week_03/capstone_contextual_chunks/stats.json`
- `labs/curriculum-weaver-lite/README.md`
- `labs/curriculum-weaver-lite/scripts/smoke-test.cjs`
- `scripts/render_architecture_png.mjs`
- project governance and historical Markdown files that contained machine paths

## Follow-Up Checks

- Run both locked test suites after dependency changes.
- Scan committed text for user-specific filesystem prefixes before committing.
- Keep local environments, browser binaries, and temporary outputs out of Git.
