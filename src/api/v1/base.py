from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.batch import BatchCreate, BatchResponse, BatchUpdate
from services.batch import create_batches, read_batch, update_batch

router = APIRouter()


@router.post(
    '/batches',
    status_code=status.HTTP_201_CREATED,
    description='Добавление сменных заданий (партий).')
async def post_batches(
    batches: list[BatchCreate],
    db: AsyncSession = Depends(get_session)
):
    return await create_batches(batches, db)


@router.get(
    '/batches/{id}/',
    # response_model=BatchResponse,
    description='Получение сменного задания (партии) по ID.')
async def get_batch(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    return await read_batch(id, db)


@router.patch(
    '/batches/{id}/',
    # response_model=BatchResponse,
    description='Изменение сменного задания (партии) по ID.')
async def patch_batch(
    id: int,
    batch: BatchUpdate,
    db: AsyncSession = Depends(get_session)
):
    return await update_batch(id, batch, db)
