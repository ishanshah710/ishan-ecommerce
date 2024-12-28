from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from app.db import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    status = Column(String, default='pending')
    
    # List of products and quantities (no separate OrderItem model)
    products = Column(JSONB)  # This could be a JSON string or a simple comma-separated list
