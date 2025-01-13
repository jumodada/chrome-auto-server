from fastapi import APIRouter

from chrome_auto_server.db.models.users import (
    UserCreate,  # type: ignore
    UserRead,  # type: ignore
    UserUpdate,  # type: ignore
    api_users,  # type: ignore
    auth_cookie,  # type: ignore
)

router = APIRouter()

router.include_router(
    api_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    api_users.get_auth_router(auth_cookie),
    prefix="/auth/cookie",
    tags=["auth"],
)
