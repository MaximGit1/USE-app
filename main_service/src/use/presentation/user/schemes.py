from pydantic import BaseModel

from use.entities.user.enums import RoleEnum
from use.entities.user.value_objects import RawPassword, Username


class UserCreateScheme(BaseModel):
    username: str
    password: str

    def get_data(self) -> tuple[Username, RawPassword]:
        return Username(self.username), RawPassword(self.password)

class UserRoleScheme(BaseModel):
    role: str

    def get_role(self) -> RoleEnum:
        match self.role:
            case "user":
                return RoleEnum.USER
            case "admin":
                return RoleEnum.ADMIN
            case _:
                return RoleEnum.GUEST
