from fastapi import APIRouter, Depends

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import async_session_maker, get_async_session
from src.auth.models import UserInfo, User
from src.auth.schemas import AddUserInfo

portfolio_router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio"]
)





