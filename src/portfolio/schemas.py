from pydantic import BaseModel


class CreateProject(BaseModel):
    id: int
    user_id: int
    description: str
    project_name: str


class AddImage(BaseModel):
    id: int
    project_id: int


class AddTag(BaseModel):
    id: int
    name: str
