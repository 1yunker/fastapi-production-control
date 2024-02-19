import datetime

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    code: str = Field(..., alias="УникальныйКодПродукта")
    batch_number: int = Field(..., alias="НомерПартии")
    batch_date: datetime.date = Field(..., alias="ДатаПартии")


class ProductCreate(BaseModel):
    code: str
    batch_id: int


class ProductUpdate(BaseModel):
    is_aggregated: bool
    aggregated_at: datetime.datetime


class ProductRead(BaseModel):
    code: str
