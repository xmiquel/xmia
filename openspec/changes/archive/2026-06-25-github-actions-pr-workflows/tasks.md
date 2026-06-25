# GitHub Actions PR Workflows — Implementation Plan

**Goal:** Add automated CI checks for every PR to `main` — backend (ruff, mypy, pytest) and frontend (eslint, tsc, vitest).

**Files:**
- New: `.github/workflows/pr.yml`
- Modified: README.md (status badge)

---

## 1. Create PR Workflow

- [x] 1.1 Create `.github/workflows/pr.yml` with `on: pull_request` trigger targeting `main`
- [x] 1.2 Add `backend` job: checkout, setup Python 3.12, install uv, `uv sync --frozen`, run `ruff check src/`
- [x] 1.3 Add `mypy` step to backend job: `mypy src/`
- [x] 1.4 Add `pytest` step to backend job: `pytest tests/`
- [x] 1.5 Add `frontend` job: checkout, setup Node 20, `npm ci`, run `npx eslint src/`
- [x] 1.6 Add `tsc` step to frontend job: `npx tsc --noEmit`
- [x] 1.7 Add `vitest` step to frontend job: `npx vitest run`
- [x] 1.8 Add `uv` caching (via `astral-sh/setup-uv` with `enable-cache: true`)
- [x] 1.9 Add `npm` caching (via `actions/setup-node` with `cache: npm`)

## 2. Verify

- [x] 2.1 Push to a branch and open a draft PR to verify workflow runs
- [x] 2.2 Confirm all checks pass on the PR
- [x] 2.3 Add CI status badge to README.md
- [x] 2.4 Commit and finalize
