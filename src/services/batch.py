from datetime import datetime
import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import LOGGING
from db.db import get_session
from models.models import Batch as BatchModel
from schemas.batch import BatchCreate, BatchUpdate

from .base import RepositoryDB


class RepositoryBatch(RepositoryDB[BatchModel, BatchCreate, BatchUpdate]):
    pass


batch_crud = RepositoryBatch(BatchModel)

logging.basicConfig = LOGGING
logger = logging.getLogger()


async def create_batches(
        batches: list[BatchCreate],
        db: AsyncSession = Depends(get_session)
):
    # Write batches in DB
    batch_objects = list()
    for batch in batches:
        try:
            if batch.is_closed:
                batch.closed_at = datetime.now()
            else:
                batch.closed_at = None
            batch_obj = await batch_crud.get_by_number_and_date(
                db=db, number=batch.number, date=batch.date
            )
            if not batch_obj:
                batch_obj = await batch_crud.create(
                    db=db, obj_in=batch
                )
            else:
                batch_obj = await batch_crud.update(
                    db=db, db_obj=batch_obj, obj_in=batch
                )
            batch_objects.append(batch_obj)
        except Exception as err:
            logger.error(f'{err}')
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Error: {err}'
            )

    return batch_objects


async def read_batch(
        id: int,
        db: AsyncSession = Depends(get_session)
):
    batch = await batch_crud.get(db=db, id=id)
    if batch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch doesn't exists"
        )
    return batch


async def update_batch(
        id: int,
        batch: BatchUpdate,
        db: AsyncSession = Depends(get_session)
):
    batch_obj = await read_batch(id, db)
    if batch.is_closed:
        batch.closed_at = datetime.now()
    else:
        batch.closed_at = None
    batch_obj = await batch_crud.update(
        db=db, db_obj=batch_obj, obj_in=batch
    )
    if batch_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch doesn't exists"
        )
    return batch_obj


async def read_batches(
    is_closed: bool = None,
    number: int = None,
    date: str = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    kwargs = dict()
    if is_closed is not None:
        kwargs['is_closed'] = is_closed
    if number is not None:
        kwargs['number'] = number
    if date is not None:
        kwargs['date'] = datetime.strptime(date, "%Y-%m-%d")

    batches = await batch_crud.get_multi(
        db=db, skip=skip, limit=limit, **kwargs
    )
    if not batches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batches not found"
        )
    return batches
