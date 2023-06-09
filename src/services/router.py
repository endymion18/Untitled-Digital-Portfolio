from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import get_async_session
from src.auth.models import User
from src.portfolio.models import Project
from src.services.models import Comment

services_router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@services_router.post("/comment")
async def add_comment(content: str, project_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    if len(content) > 500:
        raise HTTPException(status_code=400, detail="Comment is too long")
    stmt = insert(Comment).values(content=content, user_id=user.id, project_id=project_id).returning(Comment)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


@services_router.put("/comment")
async def change_comment(content: str, comment_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    if len(content) > 500:
        raise HTTPException(status_code=400, detail="Comment is too long")
    user_id = await session.execute(select(Comment.user_id).where(Comment.id == comment_id))
    user_id = user_id.scalar()
    if user_id != user.id:
        raise HTTPException(status_code=401, detail="Wrong user")
    stmt = update(Comment).where(Comment.id == comment_id).values(content=content, date=func.now()).returning(Comment)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


@services_router.get("/comment")
async def get_comment(comment_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(Comment).where(Comment.id == comment_id))
    stmt = stmt.scalar()
    return stmt


@services_router.get("/comment/project")
async def get_comment_by_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(Comment).where(Comment.project_id == project_id))
    stmt = stmt.scalars().all()
    return stmt


@services_router.get("/comment/user")
async def get_comments_by_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(Comment).where(Comment.user_id == user_id))
    stmt = stmt.scalars().all()
    return stmt


@services_router.delete("/comment")
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    stmt = delete(Comment).where(Comment.id == comment_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@services_router.put("/rating/like")
async def like(project_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    rating = await session.execute(select(Project.rating).where(Project.id == project_id))
    rating = rating.scalar() + 1
    stmt = update(Project).where(Project.id == project_id) \
        .values(rating=rating).returning(Project)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


@services_router.put("/rating/dislike")
async def dislike(project_id: int, session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(current_user)):
    rating = await session.execute(select(Project.rating).where(Project.id == project_id))
    rating = rating.scalar()
    if rating > 0:
        rating -= 1
    stmt = update(Project).where(Project.id == project_id) \
        .values(rating=rating).returning(Project)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()
