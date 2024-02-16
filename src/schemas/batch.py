import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BatchRequest(BaseModel):
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


class BatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # id: int
    # description: str
    # work_center: str
    # shift: str

    # squad: str
    # number: int
    # date: datetime.date
    # nomenclature: str

    # code_ekn: str
    # work_center_id: str
    # start_date: datetime.datetime
    # end_date: datetime.datetime

    # is_closed: bool
    # closed_at: Optional[datetime.datetime]

    products: Optional[list[str]]
