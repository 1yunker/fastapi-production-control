import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .product import ProductRead


class BatchCreate(BaseModel):
    is_closed: bool = Field(..., alias="СтатусЗакрытия")
    description: str = Field(..., alias="ПредставлениеЗаданияНаСмену")
    work_center: str = Field(..., alias="Линия")
    shift: str = Field(..., alias="Смена")

    squad: str = Field(..., alias="Бригада")
    number: int = Field(..., alias="НомерПартии")
    date: datetime.date = Field(..., alias="ДатаПартии")
    nomenclature: str = Field(..., alias="Номенклатура")

    code_ekn: str = Field(..., alias="КодЕКН")
    work_center_id: str = Field(..., alias="ИдентификаторРЦ")
    start_date: datetime.datetime = Field(..., alias="ДатаВремяНачалаСмены")
    end_date: datetime.datetime = Field(..., alias="ДатаВремяОкончанияСмены")

    closed_at: Optional[datetime.datetime] = None


class BatchUpdate(BatchCreate):
    is_closed: Optional[bool] = None
    description: Optional[str] = None
    work_center: Optional[str] = None
    shift: Optional[str] = None

    squad: Optional[str] = None
    number: Optional[int] = None
    date: Optional[datetime.date] = None
    nomenclature: Optional[str] = None

    code_ekn: Optional[str] = None
    work_center_id: Optional[str] = None
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None


class BatchResponse(BaseModel):
    id: int
    description: str
    work_center: str
    shift: str

    squad: str
    number: int
    date: datetime.date
    nomenclature: str

    code_ekn: str
    work_center_id: str
    start_date: datetime.datetime
    end_date: datetime.datetime

    is_closed: bool
    closed_at: Optional[datetime.datetime]

    products: Optional[list[ProductRead]]
