from pydantic import BaseModel


class CreateProject(BaseModel):
    name: str
    description: str


class AddImage(BaseModel):
    id: int
    project_id: int


class AddTag(BaseModel):
    id: int
    name: str
