from app.exceptions import (
    InsufficientInventory, 
    ProductNotFound
)
from app.models import Order, Product
from app.schemas import OrderCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class OrderService:
    @staticmethod
    async def create_order(
        db: AsyncSession, 
        order_data: OrderCreate
    ):
        try:
            total_price = 0.0
            ordered_products = []

            for item in order_data.products:
                result = await db.execute(
                    select(Product).filter(
                        Product.id == item.product_id
                    )
                )
                product = result.scalar_one_or_none()

                if not product:
                    raise ProductNotFound(product_id=item.product_id)
                
                if product.stock < item.quantity:
                    raise InsufficientInventory(product_id=item.product_id)

                product.stock -= item.quantity
                db.add(product)

                total_price += product.price * item.quantity
                ordered_products.append({
                    "product_id": product.id, 
                    "quantity": item.quantity
                })

            # Create the order with initial status as pending
            new_order = Order(total_price=total_price, products=ordered_products)
            db.add(new_order)
            await db.commit()
            await db.refresh(new_order)

            # Update the status to completed (after payment, example comment)
            # Here let's say we are calling some third party payment gateway api or anything
            new_order.status = "completed"  # Payment is done here
            await db.commit()
            await db.refresh(new_order)

            return new_order
        
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            if e.__class__ in (ProductNotFound, InsufficientInventory):
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            else:
                raise HTTPException(status_code=500, detail="Internal server error")