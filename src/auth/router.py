from fastapi import APIRouter, Depends

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import async_session_maker, get_async_session
from src.auth.models import UserInfo, User
from src.auth.schemas import AddUserInfo

router = APIRouter(
    prefix="/userInfo",
    tags=["userInfo"]
)


@router.post("/addInfo")
async def add_user_info(user_info: AddUserInfo, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(UserInfo).values(**user_info.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/changeInfo")
async def add_user_info(user_info: AddUserInfo, session: AsyncSession = Depends(get_async_session)):
    stmt = update(UserInfo).values(**user_info.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/getInfo")
async def add_user_info(user_id: int, session: AsyncSession = Depends(get_async_session)):
    info = select(UserInfo).where(UserInfo.user_id == user_id)
    messages = await session.execute(info)
    return messages.scalars().all()

