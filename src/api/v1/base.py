from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.batch import BatchRequest, BatchResponse
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


# @router.get(
#         '/batches/{id}/',
#         response_model=BatchRead,
#         description='Добавление сменных заданий (партий).')
# def get_batch(id: int, db: Session = Depends(get_db)):
#     batch = db.query(Batch).get(id)
#     if batch is None:
#         raise HTTPException(status_code=404, detail="Batch doesn't exists")
#     return batch

# @router.get(
#     '/files/download',
#     status_code=status.HTTP_200_OK,
#     description='Скачать файл по переданному пути или по идентификатору.'
# )
# @cache(expire=60)
# async def download_file_by_path_or_id(
#         path: str,
#         db: AsyncSession = Depends(get_session),
#         user=Depends(manager)
# ):
#     return await download_file(path, db, user)