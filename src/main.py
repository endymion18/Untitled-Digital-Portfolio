from fastapi import FastAPI, Depends

from src.auth.router import router as user_info_router
from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Untitled Digital Portfolio"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["user"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["user"],
)

app.include_router(user_info_router)

# @app.on_event("startup")
# async def startup_event():
#     add_tags()
