import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    code: str = Field(..., alias="УникальныйКодПродукта")
    batch_number: int = Field(..., alias="НомерПартии")
    batch_date: datetime.date = Field(..., alias="ДатаПартии")


class ProductUpdate(BaseModel):
    is_aggregated: bool
    aggregated_at: datetime.datetime


class ProductAggregate(BaseModel):
    code: str
    batch_id: int


class ProductRead(BaseModel):
    id: int
    code: str
    batch_number: int
    batch_date: datetime.date

    is_aggregated: bool
    aggregated_at: Optional[datetime.datetime]
