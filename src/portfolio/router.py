import os

import random
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import get_async_session
from src.auth.models import UserInfo, User
from src.portfolio.models import Project, Image
from src.portfolio.schemas import CreateProject, UpdateProject
from src.services.models import Comment

portfolio_router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


@portfolio_router.post("/project")
async def add_new_project(project_info: CreateProject, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    stmt = insert(Project).values(user_id=user.id, description=project_info.description,
                                  name=project_info.name).returning(Project)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


@portfolio_router.put("/project")
async def change_project(project_info: UpdateProject, project_id: int,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    cur_project = await session.execute(select(Project).where(Project.id == project_id))
    cur_project = cur_project.scalar()
    cur_project = await change_info(cur_project, project_info)
    stmt = update(Project).where(Project.id == project_id) \
        .values(user_id=user.id, description=cur_project.description,
                name=cur_project.name)
    await session.execute(stmt)
    await session.commit()
    return cur_project


@portfolio_router.get("/project")
async def get_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    project = await session.execute(select(Project).where(Project.id == project_id))
    project = project.scalar()
    return project


@portfolio_router.get("/project/all")
async def get_current_user_projects(user: User = Depends(current_user),
                                    session: AsyncSession = Depends(get_async_session)):
    project = await session.execute(select(Project).where(Project.user_id == user.id))
    project = project.scalars().all()
    return project


@portfolio_router.get("/project/random")
async def get_random_projects(count: int, seed: str,
                              session: AsyncSession = Depends(get_async_session)):
    projects = await session.execute(select(Project))
    projects = projects.scalars().all()
    project_count = len(projects)
    count = project_count if count > project_count else count
    random.seed(seed)
    random_projects = []
    while len(random_projects) < count:
        r = random.choice(projects)
        if not random_projects.__contains__(r):
            random_projects.append(r)
    return random_projects


@portfolio_router.delete("/project")
async def delete_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    images = await session.execute(select(Image.id).where(Image.project_id == project_id))
    images = images.scalars().all()
    for i in images:
        await delete_image(i, session)
    await session.execute(delete(Image).where(Image.project_id == project_id))
    await session.execute(delete(Comment).where(Comment.project_id == project_id))
    stmt = delete(Project).where(Project.id == project_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@portfolio_router.post("/image")
async def add_image_to_project(project_id: int, image: UploadFile = File(...),
                               session: AsyncSession = Depends(get_async_session)):
    image_id = await session.execute(select(Image).where(Image.project_id == project_id))
    image_id = f'{project_id}{len(image_id.scalars().all())}'
    filepath = await upload_image(image, image_id)
    stmt = insert(Image).values(file=filepath, project_id=project_id)
    await session.execute(stmt)
    await session.commit()
    return {"Successfully uploaded. Filepath": image_id}


@portfolio_router.get("/image/all")
async def get_images_by_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    images = await session.execute(select(Image).where(Image.project_id == project_id))
    images = images.scalars().all()
    return images


@portfolio_router.delete("/image")
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


async def change_info(old, new):
    for attr, value in new:
        if value:
            setattr(old, attr, value)
    return old
