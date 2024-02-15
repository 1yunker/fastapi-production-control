from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.batch import BatchRequest
from services.batch import create_batches

router = APIRouter()


@router.post(
    '/batches',
    status_code=status.HTTP_201_CREATED,
    description='Добавление сменных заданий (партий).')
async def post_batches(
    bathes: list[BatchRequest],
    db: AsyncSession = Depends(get_session)
):
    return await create_batches(bathes, db)
