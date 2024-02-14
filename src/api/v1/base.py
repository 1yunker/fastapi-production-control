import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# from core.config import app_settings
from core.logger import LOGGING
from db.db import get_session

from schemas.batch import BatchRequest

router = APIRouter()

logging.basicConfig = LOGGING
logger = logging.getLogger()


@router.post(
    '/batch',
    status_code=status.HTTP_201_CREATED,
    description='Добавление сменного задания (партии).')
async def create_batch(bathes: list[BatchRequest],
                       db: AsyncSession = Depends(get_session)):
    pass
