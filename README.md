# mi-api

![PR Checks](https://github.com/xmiquel/xmia/actions/workflows/pr.yml/badge.svg)

Proyecto Python gestionado con `uv`.

## Requisitos

- Python 3.11 o superior.
- `uv` instalado en el sistema.

## Configuración inicial

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone <URL_DEL_REPO>
cd mi-api
```

Sincroniza el entorno del proyecto:

```bash
uv sync
```

`uv sync` instala las dependencias definidas en `pyproject.toml` y prepara el entorno virtual del proyecto [web:604][web:656].

## Variables de entorno

Crea un fichero `.env` en la raíz del proyecto. `python-dotenv` permite cargar variables desde ese archivo durante el desarrollo [web:616][web:657].

Ejemplo:

```env
APP_ENV=development
OPENAI_API_KEY=tu_clave_aqui
```

## Desarrollo

Ejecuta comandos dentro del entorno del proyecto con `uv run` [web:604][web:656].

### Ejecutar la aplicación

```bash
uv run python main.py
```

### Ejecutar tests

```bash
uv run pytest
```

### Revisar código con Ruff

```bash
uv run ruff check .
```

### Formatear código

```bash
uv run ruff format .
```

## Gestión de dependencias

Añadir una dependencia de runtime:

```bash
uv add nombre-paquete
```

Añadir una dependencia de desarrollo:

```bash
uv add --dev nombre-paquete
```

`uv add` actualiza las dependencias del proyecto en `pyproject.toml` [web:601][web:656].

## Estructura recomendada

```text
mi-api/
├── .env
├── .gitignore
├── .python-version
├── .venv/
├── pyproject.toml
├── README.md
├── main.py
└── tests/
```

Si el proyecto se empaqueta como módulo Python, conviene añadir una carpeta de paquete, por ejemplo `mi_api/`, con su `__init__.py`, para evitar problemas con la instalación editable del proyecto [web:632][web:640].

## Notas

- No guardar secretos reales en Git.
- Mantener `.env` fuera del repositorio.
- Usar `uv run ...` en lugar de invocar directamente herramientas instaladas fuera del entorno.