from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product
from app.schemas import ProductSchema
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class ProductService:
    
    @staticmethod
    async def get_all_products(
        db: AsyncSession
    ):
        try:
            result = await db.execute(select(Product))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def add_product(
        db: AsyncSession, 
        product_data: ProductSchema
    ):
        try:
            new_product = Product(**product_data.dict())
            db.add(new_product)
            await db.commit()
            await db.refresh(new_product)
            return new_product
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
