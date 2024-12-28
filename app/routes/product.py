from fastapi import APIRouter, Depends
from services.product import ProductService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import ProductSchema
from app.db import get_db

product_router = APIRouter()

@product_router.post("/", response_model=ProductSchema)
async def create_product(
    product: ProductSchema, 
    db: AsyncSession = Depends(get_db)
):
    return await ProductService.add_product(db, product)

@product_router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    return await ProductService.get_all_products(db)
