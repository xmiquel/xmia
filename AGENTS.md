# Workflow: Feature Development via Pull Requests

Todas las nuevas features se desarrollan mediante Pull Requests para que GitHub Actions verifique lint, typechecks y tests automáticamente.

## Proceso

1. **Proponer cambio** — `/opsx-propose <descripción>` crea proposal, design, specs y tasks
2. **Implementar** — `/opsx-apply` ejecuta las tareas; se trabaja en `main` directamente (no branches locales)
3. **Crear branch y PR** — Al terminar la implementación:
   - `git checkout -b <tipo>/<nombre>` (ej: `feat/nueva-feature`, `fix/bug-xyz`)
   - `git push origin <branch>`
   - `gh pr create --title "<mensaje>" --body "<descripción>" --draft`
4. **Esperar checks de CI** — `gh run watch` hasta que todos los checks pasen
5. **Mergear** — `git checkout main && git merge <branch> && git push origin main`
6. **Limpiar** — `git branch -d <branch> && git push origin --delete <branch>`
7. **Sincronizar specs y archivar** — `/opsx-archive` (pregunta si sync specs primero)

## Comandos útiles

| Acción | Comando |
|--------|---------|
| Ver checks del PR | `gh pr checks` |
| Esperar workflow | `gh run watch` |
| Listar workflows recientes | `gh run list --workflow "PR Checks" --limit 3` |
| Ver logs de un job | `gh run view <id> --log --job <job-id>` |
| Crear PR desde el branch actual | `gh pr create --title "..." --body "..." --draft` |

## CI Pipeline

El workflow `PR Checks` corre automáticamente en cada PR a `main`:
- **Backend**: `ruff` → `mypy` → `pytest` (ubuntu-latest, uv + caching)
- **Frontend**: `eslint` → `tsc` → `vitest` (ubuntu-latest, npm + caching)

Todos los checks deben pasar antes de mergear.
