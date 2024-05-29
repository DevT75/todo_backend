from pydantic import BaseModel, Field
from typing import Optional

class TodoBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreateSchema(TodoBaseSchema):
    pass

class TodoUpdateSchema(TodoBaseSchema):
    pass

class TodoResponseSchema(TodoBaseSchema):
    id: str = Field(..., description="The unique identifier of the todo item")

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str

class UserResponseSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    class config:
        orm_mode = True

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str