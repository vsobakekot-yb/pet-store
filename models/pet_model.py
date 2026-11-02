from typing import Literal

from pydantic import BaseModel, ConfigDict


class Pet(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    name: str
    status: Literal['available', 'pending', 'sold']
    photoUrls: list[str]
