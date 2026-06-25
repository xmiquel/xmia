## Context

The project has two distinct codebases — Python backend (`src/`) and TypeScript/React frontend (`frontend/`) — each with its own toolchain, dependency management, and test framework. Currently there are no automated CI checks; every PR requires manual `pytest`, `vitest`, `ruff`, `mypy`, `eslint`, and `tsc` runs. This design introduces GitHub Actions as the CI platform, running all quality gates in parallel on every pull request to `main`.

## Goals / Non-Goals

**Goals:**
- Automatic lint, typecheck, and test execution on every PR
- Fast feedback: parallel backend and frontend jobs
- Dependency caching for both `uv` (Python) and `npm` (Node)
- Fail-fast: any failing step blocks merging
- Clear PR status badges

**Non-Goals:**
- Deployment or release workflows (deferred)
- Windows-specific runners (MT5 not needed for CI — fake adapter tests are sufficient)
- Docker-based builds or services

## Decisions

1. **Single workflow file `pr.yml`** instead of splitting into multiple files. The project is small; one file is simpler to maintain. If jobs grow, they can be extracted later.

2. **Dependency caching:** `uv` cache via `~/.cache/uv` and `npm` cache via `~/.npm`. Restore on key hash of lock files; save if miss. Keeps install <30s on cache hit.

3. **uv for Python** (matching project standard). Use `uv sync --frozen` to install from lockfile without upgrading.

4. **Parallel jobs** (`backend` and `frontend`) rather than a single sequential job. PR feedback arrives in ~2 min instead of ~4 min.

5. **`ubuntu-latest` runner** rather than `windows-latest`. The CI does not need MT5 (fakes cover all automated tests). Ubuntu is faster, cheaper, and has better uv/npm caching behavior. A Windows matrix job could be added later if MT5 integration tests are needed.

6. **`ruff check` + `mypy`** for backend lint/typecheck (matching `pyproject.toml` config). **`eslint` + `tsc --noEmit`** for frontend.

## Risks / Trade-offs

- **`mypy --strict` may be noisy** on first run → Mitigation: pin mypy config in `pyproject.toml`; if issues arise, add per-file ignores rather than relaxing globally.
- **`uv sync --frozen` fails if lockfile is stale** → Mitigation: developers run `uv lock` before commit; CI failure is a correct signal, not a problem.
- **No live MT5 tests** → False negatives are unlikely since fakes cover all current scenarios. Add `windows-latest` matrix job if MT5 coverage is needed later.
- **`npm ci` fails if `package-lock.json` is out of sync** → Same as uv; correct signal.
