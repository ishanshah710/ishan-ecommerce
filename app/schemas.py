from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int

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
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True
