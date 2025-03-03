from pydantic import BaseModel

from use.entities.user.enums import RoleEnum
from use.entities.user.value_objects import RawPassword, Username


class UserLoginInput(BaseModel):
    username: str
    password: str

    def get_data(self) -> tuple[Username, RawPassword]:
        return Username(self.username), RawPassword(self.password)

class RoleRequest(BaseModel):
    role: RoleEnum

    def get_role(self) -> RoleEnum:
        return self.role
