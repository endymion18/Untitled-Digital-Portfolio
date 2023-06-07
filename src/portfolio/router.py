import os
from typing import Union, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy import insert, select, delete, update, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import async_session_maker, get_async_session
from src.auth.models import UserInfo, User
from src.auth.schemas import AddUserInfo
from src.portfolio.models import Project, Image
from src.portfolio.schemas import CreateProject

portfolio_router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio"]
)


@portfolio_router.post("/addProject")
async def add_new_project(project_info: CreateProject, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    stmt = insert(Project).values(user_id=user.id, description=project_info.description,
                                  project_name=project_info.name)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@portfolio_router.post("/addImage")
async def add_image_to_project(project_id: int, image: UploadFile = File(...),
                               session: AsyncSession = Depends(get_async_session)):
    image_id = await session.execute(select(Image).where(Image.project_id == project_id))
    image_id = f'{project_id}{len(image_id.scalars().all())}'
    filepath = await upload_image(image, image_id)
    stmt = insert(Image).values(file=filepath, project_id=project_id)
    await session.execute(stmt)
    await session.commit()
    return {"Successfully uploaded. Filepath": image_id}


@portfolio_router.delete("/deleteImage")
async def delete_image_from_project(image_id: int,
                                    session: AsyncSession = Depends(get_async_session)):
    filepath = await delete_image(image_id, session)
    stmt = delete(Image).where(Image.id == image_id)
    await session.execute(stmt)
    await session.commit()
    return {"Successfully deleted.": filepath}


async def upload_image(file, project_id):
    ext = os.path.splitext(file.filename)[1]
    filename = f'{project_id}' + ext
    path = f'uploaded_images/{filename}'
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    with open(path, "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()

    return path


async def delete_image(image_id, session):
    filepath = await session.execute(select(Image).where(Image.id == image_id))
    filepath = filepath.scalar().file
    try:
        os.remove(filepath)
    except Exception as e:
        print(e)
    return filepath
