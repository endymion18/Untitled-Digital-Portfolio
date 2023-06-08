import os.path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import async_session_maker, get_async_session
from src.auth.models import UserInfo, User, Avatar
from src.auth.schemas import AddUserInfo, ChangeUserInfo
from src.portfolio.router import change_info

users_router = APIRouter(
    tags=["UserInfo"],
)

avatar_router = APIRouter(
    tags=["Avatar"]
)


@users_router.post("/addInfo")
async def add_user_info(user_info: AddUserInfo, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    stmt = insert(UserInfo).values(**user_info.dict(), user_id=user.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
    # return user_info.dict()


@users_router.put("/changeInfo")
async def change_user_info(user_info: ChangeUserInfo, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    user_id = user.id
    info = await session.execute(select(UserInfo).where(UserInfo.user_id == user_id))
    info = info.scalar()
    info = await change_info(info, user_info)
    stmt = update(UserInfo). \
        where(UserInfo.user_id == user_id). \
        values(first_name=info.first_name,
               last_name=info.last_name,
               is_designer=info.is_designer,
               city=info.city,
               description=info.description)
    await session.execute(stmt)
    await session.commit()
    return info
    # return user_info.dict()


@users_router.get("/getInfo")
async def get_user_info(user_id: int, session: AsyncSession = Depends(get_async_session)):
    info = select(UserInfo).where(UserInfo.user_id == user_id)
    user_info = await session.execute(info)
    return user_info.scalar()


@users_router.put("/changeUserStatus")
async def change_user_status(is_user_designer: bool, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    stmt = update(UserInfo).where(UserInfo.user_id == user.id).values(is_designer=is_user_designer)
    await session.execute(stmt)
    await session.commit()
    user_status = "designer" if is_user_designer else "buyer"
    return {"User status successfully changed to": user_status}


@users_router.get("/getUserIdByEmail")
async def get_user_id(user_email: str, session: AsyncSession = Depends(get_async_session)):
    user_id = await session.execute(select(User).where(User.email == user_email))
    user_id = user_id.scalar().id
    return {"User id": user_id}


@avatar_router.post("/addAvatar", tags=["Avatar"])
async def add_user_avatar(avatar: UploadFile = File(...), user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    user_id = user.id
    filepath = await upload_avatar(avatar, user_id)
    stmt = insert(Avatar).values(path=filepath, user_id=user_id)
    await session.execute(stmt)
    await session.commit()
    return {"Successfully uploaded. Filepath": filepath}


@avatar_router.get("/getAvatarPath", tags=["Avatar"])
async def get_avatar_path(user_id: int, session: AsyncSession = Depends(get_async_session)):
    filepath = await session.execute(select(Avatar).where(Avatar.user_id == user_id))
    filepath = filepath.scalar().path
    return {"Filepath to user avatar": filepath}


@avatar_router.put("/changeAvatar", tags=["Avatar"])
async def change_user_avatar(avatar: UploadFile = File(...), user: User = Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    user_id = user.id
    await delete_avatar(user_id, session)
    filepath = await upload_avatar(avatar, user_id)
    stmt = update(Avatar).values(path=filepath, user_id=user.id)
    await session.execute(stmt)
    await session.commit()
    return {"Successfully updated. Filepath": filepath}


@avatar_router.delete("/deleteAvatar", tags=["Avatar"])
async def delete_user_avatar(user: User = Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    user_id = user.id
    filepath = await delete_avatar(user_id, session)
    stmt = delete(Avatar).where(Avatar.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
    return {"Successfully deleted.": filepath}


async def upload_avatar(file, user_id):
    ext = os.path.splitext(file.filename)[1]
    filename = f'{user_id}' + ext
    path = f'avatars/{filename}'
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    with open(path, "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()

    return path


async def delete_avatar(user_id, session):
    filepath = await session.execute(select(Avatar).where(Avatar.user_id == user_id))
    filepath = filepath.scalar().path
    try:
        os.remove(filepath)
    except Exception as e:
        print(e)
    return filepath
