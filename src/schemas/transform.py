from pydantic import BaseModel, Field
from fastapi import Form


class TransformModel(BaseModel):
    height: int = Field(None, gt=-1)
    width: int = Field(None, gt=-1)
    crop: str = Field("fill", max_length=10)
    blur: int = Field(100, gt=0, le=2000)
    angle: int = Field(0, gt=-360, le=360)
    opacity: int = Field(100, gt=-1, le=101)


class TransformResponse(BaseModel):
    transform_url: str
