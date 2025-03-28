from abc import abstractmethod
from typing import Protocol

from use.entities.user.value_objects import HashedPassword, RawPassword


class PasswordHasherProtocol(Protocol):
    @abstractmethod
    def hash_password(self, password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def validate_password(
        self, password: RawPassword, hashed_password: HashedPassword
    ) -> bool: ...
