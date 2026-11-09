from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Tags(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str


class Category(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str


class Pet(BaseModel):
    model_config = ConfigDict(
        strict=True,
        validate_by_name=True,
        validate_by_alias=True
    )

    id: int
    name: str
    status: Literal['available', 'pending', 'sold']
    photo_urls: list[str] = Field(alias='photoUrls')
    tags: list[Tags] | None = None
    category: Category | None = None