import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.batch import BatchCreate, BatchResponse, BatchUpdate
from schemas.product import ProductCreate, ProductRequest
from services.batch import (
    create_batches,
    read_batch,
    read_batches,
    update_batch,
)
from services.product import aggregate_product, create_products

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
    response_model=BatchResponse,
    description='Получение сменного задания (партии) по ID.')
async def get_batch(
    id: int,
    db: AsyncSession = Depends(get_session)
):
    return await read_batch(id=id, db=db)


@router.patch(
    '/batches/{id}/',
    description='Изменение сменного задания (партии) по ID.')
async def patch_batch(
    id: int,
    batch: BatchUpdate,
    db: AsyncSession = Depends(get_session)
):
    return await update_batch(id=id, batch=batch, db=db)


@router.get(
    '/batches',
    response_model=list[BatchResponse],
    description='Получение сменных заданий (партий) по различным фильтрам.')
async def get_batches(
    db: AsyncSession = Depends(get_session),
    is_closed: bool = None,
    number: int = None,
    date: datetime.date = None,
    skip: int = 0,
    limit: int = 100
):
    return await read_batches(
        is_closed=is_closed,
        number=number,
        date=date,
        skip=skip,
        limit=limit,
        db=db
    )


@router.post(
    '/products',
    status_code=status.HTTP_201_CREATED,
    description='Добавление продукции для сменного задания (партии).')
async def post_products(
    products: list[ProductRequest],
    db: AsyncSession = Depends(get_session)
):
    return await create_products(products, db)


@router.post(
    '/products/aggregate',
    status_code=status.HTTP_202_ACCEPTED,
    description='Аггрегация продукции по ID сменного задания (партии).')
async def post_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_session)
):
    return await aggregate_product(product, db)
