from typing import Optional

from pydantic import BaseModel


class CreateProject(BaseModel):
    name: str
    description: str


class UpdateProject(BaseModel):
    name: Optional[str]
    description: Optional[str]


class AddImage(BaseModel):
    id: int
    project_id: int


class AddTag(BaseModel):
    id: int
    name: str
