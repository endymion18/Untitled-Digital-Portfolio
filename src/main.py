from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router import users_router, avatar_router
from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.database import get_async_session
from src.portfolio.router import portfolio_router
from src.services.router import services_router

app = FastAPI(
    title="Untitled Digital Portfolio"
)

origins = [
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(services_router)

# @app.on_event("startup")
# async def startup_event():
#     session = get_async_session()
#     await add_tags(session)
