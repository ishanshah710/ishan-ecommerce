import pytest
from httpx import AsyncClient
from app.main import app
from sqlalchemy.ext.asyncio import AsyncSession
import os


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000') as client:
        yield client

# Async test to add a product
@pytest.mark.asyncio
async def test_add_product(client: AsyncClient, db_session: AsyncSession):
    # Prepare test data
    product_data = {
        "id": 1,
        "name": "iphone-13",
        "description": "I PHONE 12",
        "price": "15000",
        "stock": 50
    }

    # Send POST request to add product
    response = await client.post("/products", json=product_data)
    
    # Assert the response is successful
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    

# Async test to handle invalid product data
@pytest.mark.asyncio
async def test_add_invalid_product_name(client: AsyncClient):
    invalid_product_data = {
        "name": "",
        "description": "",  
        "price": 10,        
        "stock": 100
    }

    # Send POST request with invalid data
    response = await client.post("/products", json=invalid_product_data)
    
    # Assert 422 Unprocessable Entity for invalid data
    assert response.status_code == 422
    assert "name" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_negative_price(client: AsyncClient):
    invalid_product_data = {
        "name": "iphone",
        "description": "",  
        "price": -10,        
        "stock": 100
    }

    # Send POST request with invalid data
    response = await client.post("/products", json=invalid_product_data)
    
    # Assert 422 Unprocessable Entity for invalid data
    assert response.status_code == 422
    assert "price" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_negative_stock(client: AsyncClient):
    invalid_product_data = {
        "name": "iphone",
        "description": "",  
        "price": 10,        
        "stock": -100
    }

    # Send POST request with invalid data
    response = await client.post("/products", json=invalid_product_data)
    
    # Assert 422 Unprocessable Entity for invalid data
    assert response.status_code == 422
    assert "stock" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient):
    response = await client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # adding product and then checking
    product_data = {
        "id": 11,
        "name": "iphone-14",
        "description": "I PHONE 14",
        "price": "15000",
        "stock": 20
    }

    # Send POST request to add product
    await client.post("/products", json=product_data)

    response = await client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == product_data["name"]
