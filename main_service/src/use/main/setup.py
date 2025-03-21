import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from use.main.di.main import container_factory
from use.presentation.auth.api_router import router as auth_router
from use.presentation.common.exc_handlers import init_exc_handlers
from use.presentation.common.middlewares.setup import init_middleware
from use.presentation.stats.api_router import router as stats_router
from use.presentation.task.api_router import router as task_router
from use.presentation.user.api_router import router as user_router


def init_routers(app: FastAPI) -> None:
    routers = (auth_router, user_router, task_router, stats_router)

    for router in routers:
        app.include_router(router, prefix="/api/v1")


def init_di(app_: FastAPI) -> None:
    container = container_factory()

    setup_dishka(container, app_)


def init_logger() -> logging.Logger:
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        log_file_path = (Path(__file__).parent / "../../../logs.log").resolve()

        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(
            filename=log_file_path,
            mode="a",
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator[None, None]:
    logger = init_logger()
    logger.info(
        "Application is starting...",
        extra={"request_method": None, "request_url": None},
    )

    broker: RabbitBroker = await app_.state.dishka_container.get(RabbitBroker)
    await broker.start()

    yield

    await broker.close()
    logger.info(
        "Application is stopping...",
        extra={"request_method": None, "request_url": None},
    )


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    init_di(app)
    init_routers(app)
    init_exc_handlers(app)
    init_middleware(app)

    return app
