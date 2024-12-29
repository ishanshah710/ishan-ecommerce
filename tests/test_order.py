import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient
from app.models import Product
from app.main import app
from app.db import Base
from dotenv import load_dotenv
import os
from httpx import AsyncClient

# Load environment variables from .env file
load_dotenv()

# Create a test database engine
test_engine = create_async_engine(os.getenv("DATABASE_URL", ""), future=True, echo=True)

# Create a test session maker
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)

# Create a fixture for db_session
@pytest.fixture(scope="function")
async def db_session():
    # Create tables before running the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a session for the test
    async with TestSessionLocal() as session:
        yield session

    # Drop tables after the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Create an AsyncClient instance
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000') as client:
        yield client

# Test Order Creation (Valid Scenario)
@pytest.mark.asyncio
async def test_create_order_valid(client, db_session):
    # Step 1: Add a product to the database
    product = Product(id=101, name="Laptop", description="Gaming laptop", price=1500.0, stock=5)
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    # Step 2: Create an order with the added product
    order_data = {
        "products": [{"product_id": 101, "quantity": 2}]
    }
    response = await client.post("/orders", json=order_data)

    # Assert the response status code and data
    assert response.status_code == 201
    data = response.json()

    # Assert the order details
    assert data["status"] == "completed"
    assert data["total_price"] == 2 * 1500.0
    assert len(data["products"]) == 1
    assert data["products"][0]["product_id"] == product.id
    assert data["products"][0]["quantity"] == 2

# Test for insufficient stock when creating an order
@pytest.mark.asyncio
async def test_create_order_insufficient_stock(client, db_session):
    # Step 1: Add a product to the database
    product = Product(id=102,name="Laptop", description="Gaming laptop", price=1500.0, stock=1)
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    # Step 2: Create an order with more quantity than available stock
    order_data = {
        "products": [{"product_id": product.id, "quantity": 2}]
    }
    response = await client.post("/orders/", json=order_data)

    # Assert the response status code and error message
    assert response.status_code == 400  # Should return a 422 for insufficient stock
    assert "Insufficient stock for product 102" in response.json()["detail"]

# Test for product not found in order creation
@pytest.mark.asyncio
async def test_create_order_product_not_found(client, db_session):
    # Step 1: Create an order with a non-existent product ID
    order_data = {
        "products": [{"product_id": 9999, "quantity": 2}]
    }
    response = await client.post("/orders/", json=order_data)

    # Assert the response status code and error message
    assert response.status_code == 404  # Should return a 404 for product not found
    assert f"Product with ID {9999} not found" in response.json()["detail"]
