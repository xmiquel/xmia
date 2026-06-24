from contextlib import asynccontextmanager

from fastapi import FastAPI

from mt5.config import MT5Config
from mt5.live import LiveMT5Adapter
from mt5.protocol import MT5Adapter
from src.api.errors import add_error_handlers
from src.api.routers.account import router as account_router
from src.api.routers.rates import router as rates_router
from src.api.routers.symbols import router as symbols_router


def create_app(adapter: MT5Adapter | None = None) -> FastAPI:
    if adapter is None:
        config = MT5Config.from_env()
        adapter = LiveMT5Adapter()
        adapter.initialize(
            path=config.terminal_path,
            login=config.account_number,
            password=config.password,
            server=config.server,
        )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.adapter = adapter
        yield
        adapter.shutdown()

    app = FastAPI(lifespan=lifespan, title="mi-api")
    add_error_handlers(app)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    app.include_router(account_router)
    app.include_router(symbols_router)
    app.include_router(rates_router)

    return app


app = create_app()
