from fastapi import FastAPI, Depends


from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.portfolio.router import add_tags

app = FastAPI(
    title="Untitled Digital Portfolio"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


# @app.on_event("startup")
# async def startup_event():
#     add_tags()
