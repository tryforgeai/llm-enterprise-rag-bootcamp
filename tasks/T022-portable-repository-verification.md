# T022 Portable Repository Verification

Status: done

Date: 2026-07-18

## Goal

Make the committed project runnable from any clone location without depending on one user's directories, cached runtimes, system browser, or globally installed Python packages.

## Done Criteria

- [x] Committed text contains no user- or machine-specific absolute filesystem paths.
- [x] Week 03 has a locked `uv` environment and documented test command.
- [x] Curriculum Weaver resolves Playwright from the repository lockfile.
- [x] Curriculum Weaver launches Playwright-managed Chromium and its own ephemeral HTTP server.
- [x] Browser screenshots and results go to the operating system temporary directory.
- [x] Root README documents clone-to-test commands.
- [x] Week 03 unit suite passes.
- [x] Curriculum Weaver desktop/mobile smoke test passes without console errors.
- [x] A clean external copy passes the offline verification commands.

## Evidence

- `package.json`
- `package-lock.json`
- `course/week_03/pyproject.toml`
- `course/week_03/uv.lock`
- `course/week_03/README.md`
- `labs/curriculum-weaver-lite/scripts/smoke-test.cjs`
- `scripts/render_architecture_png.mjs`
- `README.md`
