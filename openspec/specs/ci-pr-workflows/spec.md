# CI PR Workflows

Automated quality checks for every pull request targeting `main`, covering Python backend and TypeScript frontend.

---

## Requirement: PR CI Pipeline

The system SHALL run automated quality checks on every pull request targeting the `main` branch. The pipeline SHALL execute backend and frontend checks in parallel. A pull request SHALL NOT be merged if any check fails.

### Scenario: Backend checks pass
- **WHEN** a PR is opened or updated targeting `main`
- **THEN** the CI SHALL install Python dependencies with `uv sync --frozen`
- **AND** SHALL run `ruff check src/`
- **AND** SHALL run `mypy src/`
- **AND** SHALL run `pytest tests/`
- **AND** SHALL report success only if all three pass

### Scenario: Frontend checks pass
- **WHEN** a PR is opened or updated targeting `main`
- **THEN** the CI SHALL install Node dependencies with `npm ci`
- **AND** SHALL run `npx eslint src/`
- **AND** SHALL run `npx tsc --noEmit`
- **AND** SHALL run `npx vitest run`
- **AND** SHALL report success only if all three pass

### Scenario: Dependency caching
- **WHEN** the CI pipeline runs
- **THEN** the `uv` cache SHALL be restored from `~/.cache/uv` keyed on `uv.lock` hash
- **AND** the `npm` cache SHALL be restored from `~/.npm` keyed on `package-lock.json` hash
- **AND** on cache miss, the caches SHALL be saved after install completes

### Scenario: PR blocks on failure
- **GIVEN** any CI check fails (lint error, type error, or test failure)
- **WHEN** the pipeline completes
- **THEN** the overall status SHALL be failure
- **AND** the PR SHALL show a red checkmark or "checks failed" status
