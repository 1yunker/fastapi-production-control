import logging
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import LOGGING
from db.db import get_session
from models.models import Product as ProductModel
from schemas.product import ProductCreate, ProductRequest, ProductUpdate

from .base import RepositoryDB
from .batch import batch_crud


class RepositoryProduct(
    RepositoryDB[ProductModel, ProductCreate, ProductUpdate]
):
    pass


product_crud = RepositoryProduct(ProductModel)

logging.basicConfig = LOGGING
logger = logging.getLogger()


async def create_products(
        products: list[ProductRequest],
        db: AsyncSession = Depends(get_session)
):
    product_objects = list()
    for product in products:
        try:
            product_obj = await product_crud.get_by_code(
                db=db,
                code=product.code
            )
            # Игнорируем продукцию, если она уже существует
            if not product_obj:
                batch_obj = await batch_crud.get_by_number_and_date(
                    db=db,
                    number=product.batch_number,
                    date=product.batch_date
                )
                if batch_obj:
                    product_obj = await product_crud.create(
                        db=db,
                        obj_in=ProductCreate(code=product.code,
                                             batch_id=int(batch_obj.id))
                    )
                    product_objects.append(product_obj)
        except Exception as err:
            logger.error(f'{err}')
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Error: {err}'
            )

    return product_objects


async def aggregate_product(
        product: ProductCreate,
        db: AsyncSession = Depends(get_session)
):
    product_obj = await product_crud.get_by_code(
        db=db,
        code=product.code
    )
    if product_obj:
        if product_obj.aggregated_at:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Unique code already used at '
                       f'{product_obj.aggregated_at}'
            )
        if product.batch_id != product_obj.batch_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Unique code is attached to another batch'
            )
        product_obj = await product_crud.update(
            db=db,
            db_obj=product_obj,
            obj_in=ProductUpdate(is_aggregated=True,
                                 aggregated_at=datetime.now())
        )
        return product_obj.code
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Product not found'
    )
