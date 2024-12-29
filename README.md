# Ishan - FastAPI E-Commerce Application

---

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone (https://github.com/ishanshah710/ishan-ecommerce.git)
```

### 2. Configure Environment Variables

Create a `.env` file in the project root and add the following environment variables:

```env
DATABASE_URL=postgresql+asyncpg://user:password@db/ecommerce_db
```

### 3. Build and Run the Docker Containers

Use the following command to build and run the application:

```bash
docker-compose up --build
```

This will:
- Build the FastAPI application image.
- Start the application on `http://localhost:8000`.
- Start the PostgreSQL database container.
- Product and Order tables are also created in PostgreSQL db
---

## API Information

Once the application is running, you can access the API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

#### **Product Endpoints**
- `POST /products`: Add a new product.
- `GET /products`: Retrieve all products.

#### **Order Endpoints**
- `POST /orders`: Create a new order.

---

## Running Tests

Tests are implemented using `pytest` and `httpx`.

### 1. Run Tests in Docker Container

Build and run the test cases inside the `web` container:

```bash
docker exec -it <container_name> 
pytest
```

### 2. Test Coverage

Test cases cover:
- Product creation with valid and invalid data.
- Order creation with valid data.
- Handling insufficient stock and non-existent products in orders.

---

## Additional Notes

- Modify the `docker-compose.yml` or `.env` file for custom configurations.
- The application uses SQLAlchemy for database interactions and Pydantic for schema validation.
