from dishka import (
    Provider,
    Scope,
)

from use.application.auth.service import AuthService
from use.application.broker_publisher.service import BrokerPublisherService
from use.application.cache.service import CacheService
from use.application.cookie.service import CookieService
from use.application.identityProvider.service import IdentityProvider
from use.application.stats.service import StatsService
from use.application.task.service import TaskService
from use.application.user.service import UserService


def service_provider() -> Provider:
    provider = Provider()
    provider.provide(UserService, scope=Scope.REQUEST)
    provider.provide(AuthService, scope=Scope.REQUEST)
    provider.provide(CookieService, scope=Scope.REQUEST)
    provider.provide(TaskService, scope=Scope.REQUEST)
    provider.provide(IdentityProvider, scope=Scope.REQUEST)
    provider.provide(BrokerPublisherService, scope=Scope.REQUEST)
    provider.provide(CacheService, scope=Scope.APP)
    provider.provide(StatsService, scope=Scope.REQUEST)

    return provider


def get_use_cases_providers() -> list[Provider]:
    return [
        service_provider(),
    ]
