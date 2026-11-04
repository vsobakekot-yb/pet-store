from typing import Literal

from pydantic import BaseModel, ConfigDict

class Tags(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str


class Category(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str


class Pet(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str
    status: Literal['available', 'pending', 'sold']
    photoUrls: list[str]
    tags: list[Tags]
    category: list[Category]
