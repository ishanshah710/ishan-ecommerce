from fastapi import APIRouter, Depends, HTTPException
from services.order import OrderService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import OrderCreate, OrderResponse
from app.models import Order
from app.db import get_db

order_router = APIRouter()

@order_router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await OrderService.create_order(db, order)
