from fastapi import FastAPI, Depends

from src.auth.router import users_router, avatar_router
from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.portfolio.router import portfolio_router

app = FastAPI(
    title="Untitled Digital Portfolio"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(users_router)
app.include_router(avatar_router)
app.include_router(portfolio_router)
# @app.on_event("startup")
# async def startup_event():
#     add_tags()
