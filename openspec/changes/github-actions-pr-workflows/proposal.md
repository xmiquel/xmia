## Why

No CI/CD pipeline exists. Every PR must be manually validated — lint, typecheck, and test on both backend (Python) and frontend (React/TypeScript). This slows down reviews and lets broken code slip through. Adding GitHub Actions for PR workflows ensures consistent, automated quality gates before merge.

## What Changes

- Add `.github/workflows/pr.yml` — runs on every PR to `main`:
  - Backend: install deps with uv, ruff lint, mypy typecheck, pytest
  - Frontend: npm ci, eslint lint, tsc typecheck, vitest test
- Fail the workflow if any step fails
- Cache dependencies across runs to keep builds fast
- Add status badge to README (optional)

## Capabilities

### New Capabilities
- `ci-pr-workflows`: Automated CI checks for pull requests covering Python backend and TypeScript frontend quality gates

### Modified Capabilities
- *(none — no existing spec-level behavior changes)*

## Impact

- New file: `.github/workflows/pr.yml`
- No code changes to backend or frontend source
- No new dependencies
- Does not affect Windows/MT5 runtime
