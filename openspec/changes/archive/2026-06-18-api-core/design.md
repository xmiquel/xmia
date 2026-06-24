## Context

The MT5 adapter layer (port/adapter) is complete with `LiveMT5Adapter`, `FakeMT5Adapter`, configuration, error types, and reconnect logic. The next step is to expose this functionality via a REST API. FastAPI is already in `pyproject.toml` as a dependency. The project follows a layered architecture with clear separation between Windows-native MT5 integration and the Python application layer.

## Goals / Non-Goals

**Goals:**
- FastAPI application that initializes MT5 on startup and shuts down on stop
- Three read-only REST endpoints: account info, symbol info, market rates
- Optional API Key authentication via `X-API-Key` header (disabled when unset)
- HTTP error handlers translating MT5 adapter exceptions to proper status codes
- Timeframe string-to-constant mapping for the rates endpoint
- Full testability via `FakeMT5Adapter` injection (no live MT5 terminal needed)

**Non-Goals:**
- Position and order management endpoints (future change)
- Deal history endpoint (future change)
- WebSockets or streaming data
- User registration, multi-tenancy, or JWT auth
- Database persistence
- Docker containerization of the API (runs on Windows host)

## Decisions

### 1. Layered Architecture

- **Decision**: Three layers — Router (HTTP concerns) → Service (domain logic) → Adapter (MT5 integration). Routers never import MT5 directly; they depend on the `MT5Adapter` Protocol interface injected via FastAPI dependencies.
- **Rationale**: Matches existing Port/Adapter pattern in the MT5 layer. Services can grow to include validation, caching, or orchestration without changing routers. Adapter injection enables swapping `LiveMT5Adapter` for `FakeMT5Adapter` in tests via `app.dependency_overrides`.
- **Alternatives**: Monolithic routers with inline adapter calls (simpler but harder to test and evolve).

### 2. App Factory Pattern

- **Decision**: `create_app(adapter: MT5Adapter | None = None) -> FastAPI` factory function. When `adapter` is `None`, creates a `LiveMT5Adapter` from env config. Tests pass a `FakeMT5Adapter` directly.
- **Rationale**: Tests can inject a controlled adapter without env vars or global state. The module-level `app = create_app()` enables `uvicorn src.api.main:app`.
- **Alternatives**: Global `app` with monkey-patching (fragile), dependency injection container (overkill for this scope).

### 3. API Key Authentication

- **Decision**: Static API key from `API_KEY` env var. Validated via FastAPI `APIKeyHeader` dependency. When `API_KEY` is unset, auth is disabled (dev mode). `/health` endpoint is always public.
- **Rationale**: Simple, standard for APIs of this scale. The dependency injection point (`verify_api_key`) is a single function — replacing it with JWT auth later requires changing one file and the dependency override.
- **Alternatives**: No auth (insecure for future use), JWT (premature — no multi-user yet).

### 4. Endpoint Prefix

- **Decision**: All business endpoints under `/api/v1/` prefix. Health endpoint at `/health` (no prefix).
- **Rationale**: Versioned API path enables breaking changes in future iterations without affecting existing clients.

### 5. Timeframe as String

- **Decision**: Timeframes are accepted as uppercase strings (`PERIOD_H1`, `PERIOD_M5`, etc.) and mapped to MT5 integer constants via a dict lookup. Invalid strings return HTTP 422.
- **Rationale**: Human-readable in URLs, self-documenting. The mapping dict centralizes the translation — if MT5 constants change or new ones are added, only one file changes.

### 6. Error Translation

- **Decision**: Custom exception handlers registered on the FastAPI app that catch each `MT5Error` subclass and return the appropriate HTTP status (see spec for mapping). Unhandled exceptions return 500 with a generic message (no stack trace exposure).
- **Rationale**: Consistent error format across all endpoints. Prevents sensitive MT5 internals from leaking in responses.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| MT5 terminal must be running for API to start | API won't start if terminal is closed | Fail-fast on startup; clear error message. In dev, use `MT5_FAKE=1` to bypass |
| API Key is static and shared | Cannot revoke individual clients or track usage | Acceptable for v1; migrate to per-user keys or JWT when multi-tenancy is needed |
| Timeframe strings may feel verbose in URLs | Longer query strings | Matches MT5 naming conventions; users already familiar with these constants |
| Service layer is thin (delegates to adapter) | Feels like unnecessary abstraction | Services will grow as validation, caching, and orchestration are added. Better to have the structure in place from the start |
