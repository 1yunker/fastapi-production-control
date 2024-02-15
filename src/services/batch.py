from datetime import datetime
import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import LOGGING
from db.db import get_session
from models.models import Batch as BatchModel
from schemas.batch import BatchRequest

from .base import RepositoryDB


class RepositoryFile(RepositoryDB[BatchModel, BatchRequest, BatchRequest]):
    pass


batch_crud = RepositoryFile(BatchModel)

logging.basicConfig = LOGGING
logger = logging.getLogger()


async def create_batches(
        batches: list[BatchRequest],
        db: AsyncSession = Depends(get_session)
):
    # Write batches in DB
    batch_objects = list()
    for batch in batches:
        try:
            batch_obj = await batch_crud.create(
                db=db,
                obj_in=BatchModel(**batch.model_dump(exclude_none=True))
            )
            batch_objects.append(batch_obj)
        except Exception as err:
            logger.error(f'{err}')
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Error: {err}'
            )

    return batch_objects
