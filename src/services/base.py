from datetime import date, datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import and_, null, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(
    Repository,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(
            self, db: AsyncSession, id: Any
    ) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_by_number_and_date(
            self, db: AsyncSession, number: int, date: date
    ) -> Optional[ModelType]:
        statement = (
            select(self._model)
            .where(
                and_(self._model.number == number,
                     self._model.date == date)
            )
        )
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_by_code(
            self, db: AsyncSession, code: str
    ) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.code == code)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(
            self, db: AsyncSession, *args, skip=0, limit=100, **kwargs
    ) -> List[ModelType]:
        statement = (
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(skip)
            .limit(limit)
        )
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(
            self, db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        db_obj = self._model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        statement = (
            update(self._model).
            where(self._model.id == db_obj.id).
            values(obj_in.model_dump(exclude_unset=True)).
            returning(self._model)
        )
        await db.execute(statement=statement)
        await db.commit()
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> None:
        db_obj = db.get(self._model, id)
        await db.delete(db_obj)
        return None
