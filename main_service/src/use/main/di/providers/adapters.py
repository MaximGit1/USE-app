import os
from collections.abc import AsyncIterator
from typing import NewType

import redis.asyncio as redis
from dishka import (
    Provider,
    Scope,
    from_context,
    provide,
)
from faststream.rabbit import RabbitBroker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from use.application.auth.protocols import JWTManageProtocol
from use.application.broker_publisher.protocol import (
    BrokerUSEPublisherProtocol,
)
from use.application.cache.protocol import CacheProtocol
from use.application.common.protocols.uow import UoWProtocol
from use.application.cookie.interactor import CookieManagerInteractor
from use.application.task.protocols import (
    TaskCreateProtocol,
    TaskDeleteProtocol,
    TaskReadProtocol,
    TaskUpdateProtocol,
)
from use.application.user.protocols import (
    PasswordHasherProtocol,
    UserCreateProtocol,
    UserReadProtocol,
    UserUpdateProtocol,
)
from use.infrastructure.auth.repositories import AccessManagerRepository
from use.infrastructure.broker_publisher.repository import BrokerUSEPublisher
from use.infrastructure.cache.repository import CacheRepository
from use.infrastructure.cookie.repositories import (
    CookieAccessManagerRepository,
)
from use.infrastructure.database.uow import SqlAlchemyUoW
from use.infrastructure.task.repositories.add import TaskCreateRepository
from use.infrastructure.task.repositories.deleted import TaskDeletedRepository
from use.infrastructure.task.repositories.read import TaskReadRepository
from use.infrastructure.task.repositories.update import TaskUpdateRepository
from use.infrastructure.user.repositories import (
    PasswordHasherRepository,
    UserCreateRepository,
    UserReadRepository,
    UserUpdateRepository,
)
from use.main.config import (
    Config,
    CookieConfig,
    JWTConfig,
    PostgresConfig,
)

DBURI = NewType("DBURI", str)


Base = declarative_base()

class DBProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_engine(
        self,
        config: PostgresConfig
    ) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            config.uri,
            echo=config.debug,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def sessionmaker(
        self,
        engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_uow(
        self,
        session: AsyncSession
    ) -> AsyncIterator[UoWProtocol]:
        async with session.begin():
            yield SqlAlchemyUoW(session)

class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_postgres_config(self, config: Config) -> PostgresConfig:
        return config.db

    @provide(scope=Scope.APP)
    def get_jwt_config(self, config: Config) -> JWTConfig:
        return config.jwt

    @provide(scope=Scope.APP)
    def get_cookie_config(self, config: Config) -> CookieConfig:
        return config.cookie


def repository_provider() -> Provider:
    provider = Provider()
    provider.provide(
        UserCreateRepository,
        scope=Scope.REQUEST,
        provides=UserCreateProtocol,
    )
    provider.provide(
        PasswordHasherRepository,
        scope=Scope.APP,
        provides=PasswordHasherProtocol,
    )
    provider.provide(
        UserReadRepository,
        scope=Scope.REQUEST,
        provides=UserReadProtocol,
    )
    provider.provide(
        UserUpdateRepository,
        scope=Scope.REQUEST,
        provides=UserUpdateProtocol,
    )
    provider.provide(
        AccessManagerRepository,
        scope=Scope.APP,
        provides=JWTManageProtocol,
    )
    provider.provide(
        CookieAccessManagerRepository,
        scope=Scope.REQUEST,
        provides=CookieManagerInteractor,
    )
    provider.provide(
        TaskCreateRepository,
        scope=Scope.REQUEST,
        provides=TaskCreateProtocol,
    )

    provider.provide(
        TaskReadRepository,
        scope=Scope.REQUEST,
        provides=TaskReadProtocol,
    )

    provider.provide(
        TaskUpdateRepository,
        scope=Scope.REQUEST,
        provides=TaskUpdateProtocol,
    )
    provider.provide(
        CacheRepository,
        scope=Scope.APP,
        provides=CacheProtocol,
    )

    provider.provide(
        BrokerUSEPublisher,
        scope=Scope.APP,
        provides=BrokerUSEPublisherProtocol,
    )

    provider.provide(
        TaskDeletedRepository,
        scope=Scope.REQUEST,
        provides=TaskDeleteProtocol,
    )

    return provider


def create_rabbit_broker() -> RabbitBroker:
    return RabbitBroker(
        url=f"amqp://{os.getenv('RABBITMQ_USER', 'guest')}"
            f":{os.getenv('RABBITMQ_PASS', 'guest')}"
            f"@{os.getenv('RABBITMQ_HOST', 'rabbitmq')}"
            f":{os.getenv('RABBITMQ_PORT', '5672')}/"
    )


def create_redis_client() -> Redis:
    return redis.from_url("redis://redis:6379?decode_responses=True")  # type: ignore


def broker_provider() -> Provider:
    provider = Provider()
    provider.provide(
        create_rabbit_broker, scope=Scope.APP, provides=RabbitBroker
    )

    return provider


def cache_provider() -> Provider:
    provider = Provider()
    provider.provide(create_redis_client, scope=Scope.APP, provides=Redis)

    return provider


def get_adapters_providers() -> list[Provider]:
    return [
        ConfigProvider(),
        DBProvider(),
        repository_provider(),
        broker_provider(),
        cache_provider(),
    ]
