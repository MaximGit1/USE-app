from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response

from use.application.auth.service import AuthService
from use.application.broker_publisher.service import BrokerPublisherService
from use.application.cookie.exceptions import CookieIsNoneError
from use.application.cookie.service import CookieService
from use.application.identityProvider.service import IdentityProvider
from use.application.user.response.models import (
    UserIdResponse,
)
from use.application.user.service import UserService
from use.entities.user.enums import RoleEnum
from use.presentation.auth.schemes import RoleRequest, UserLoginInput
from use.presentation.user.schemes import UserCreateScheme

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/register/", status_code=201)
async def create_user(
    user_data: UserCreateScheme,
    user_service: FromDishka[UserService],
) -> UserIdResponse:
    username, password = user_data.get_data()

    return await user_service.create_user(username=username, password=password)


@router.post("/login/")
async def login(
    user_data: UserLoginInput,
    user_service: FromDishka[UserService],
    auth_service: FromDishka[AuthService],
    cookie_service: FromDishka[CookieService],
    response: Response,
) -> None:
    username, password = user_data.get_data()
    user_id = await user_service.authenticate_user(
        username=username, password=password
    )
    token = auth_service.login_user(user_id=user_id)

    cookie_service.update_service(response=response)
    cookie_service.set_access_token(token)


@router.post(
    "/logout/",
    summary="Logout user",
)
async def logout(
    response: Response,
    cookie_service: FromDishka[CookieService],
) -> None:
    cookie_service.update_service(response=response)
    cookie_service.delete_access_token()


@router.post("/verify-role/")
async def verify_current_user_role(
    idp: FromDishka[IdentityProvider],
    broker: FromDishka[BrokerPublisherService],
    role: RoleRequest,
    request: Request,
) -> bool:
    idp.update_service(request=request)
    try:
        current_id = idp.get_current_user_id()
        return await broker.auth_verify_user_role(
            role=role.get_role(), user_id=current_id
        )
    except CookieIsNoneError:
        return RoleEnum.validate_role(
            user_role=RoleEnum.GUEST, min_role=role.get_role()
        )


@router.post(
    "/my-id/",
    summary="Get current user id",
)
async def get_current_user_id(
    idp: FromDishka[IdentityProvider],
    request: Request,
) -> UserIdResponse:
    idp.update_service(request=request)
    return UserIdResponse(user_id=idp.get_current_user_id())


@router.post("/check/")
async def verify_authenticated(
    cookie_service: FromDishka[CookieService],
    request: Request,
) -> bool:
    cookie_service.update_service(request=request)
    return cookie_service.verify_user_context()
