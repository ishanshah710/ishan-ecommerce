from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1, description="Quantity must be at least 1")

class OrderCreate(BaseModel):
    products: List[OrderItem]

class OrderResponse(OrderCreate):
    id: int
    total_price: float
    status: str

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    description: str
    price: float = Field(..., ge=0, description="Price must be non-negative")
    stock: int = Field(..., ge=0, description="Stock must be non-negative")


    class Config:
        orm_mode = True
