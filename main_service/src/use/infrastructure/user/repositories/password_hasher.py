from bcrypt import checkpw, gensalt, hashpw

from use.application.user.protocols import PasswordHasherProtocol
from use.entities.user.value_objects import HashedPassword, RawPassword


class PasswordHasherRepository(PasswordHasherProtocol):
    def hash_password(self, password: RawPassword) -> HashedPassword:
        hashed_password = hashpw(
            password=password.value.encode(),
            salt=gensalt(),
        )
        return HashedPassword(hashed_password)

    def validate_password(
        self, password: RawPassword, hashed_password: HashedPassword
    ) -> bool:
        return checkpw(
            password=password.value.encode(),
            hashed_password=hashed_password.value,
        )
