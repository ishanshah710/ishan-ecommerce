from fastapi import HTTPException

class InsufficientInventory(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(status_code=400, detail=f"Insufficient stock for product {product_id}")

class ProductNotFound(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(status_code=404, detail=f"Product with ID {product_id} not found")