from pydantic import BaseModel, Field
from typing import Optional


class UserCreateSchema(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = Field(
        None, min_length=10, max_length=10, description="Phone number up to 10 digits"
    )


class UserOutputSchema(BaseModel):
    id: int
    username: str
    role: str
