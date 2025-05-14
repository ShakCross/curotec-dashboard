# Data Processing API

This is a Django-based API for data processing with a clean architecture approach. It demonstrates efficient data handling patterns using Python's functional capabilities and SQLAlchemy integration.

## Project Structure

The project follows a clean architecture pattern with:
- Domain layer: Pure business logic
- Application layer: Use cases and business logic coordination
- Infrastructure layer: Database models, repositories
- Interface layer: API views and serializers

## Features

- API endpoint for accepting JSON data with numeric and string fields
- Multiple transformation operations (filtering, sorting, aggregation)
- Efficient data handling with SQLAlchemy
- Clean architecture separation of concerns
- Robust data validation with Pydantic 1.10.13

## Setup and Installation

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- PostgreSQL 15 (provided via Docker)

### Setup

1. **Clone the repository**

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Start PostgreSQL with Docker**
   ```
   docker-compose up -d
   ```

5. **Run database migrations**
   ```
   cd data_processing_api
   python manage.py migrate
   ```

6. **Run the development server**
   ```
   python manage.py runserver
   ```

## API Endpoints

### Process Data
- `POST /api/data/process/`
  - Accepts a JSON array of objects with numeric and string fields
  - Returns processed data with assigned IDs
  - Input is validated using Pydantic schemas

### Transform Data
- `GET /api/data/transform/filter/` - Filter data
  - Query params: `field`, `value`, `operator` (optional, default: "eq")
  - Operators: "eq", "neq", "gt", "lt", "contains"
  - Parameters are validated using Pydantic schemas

- `GET /api/data/transform/sort/` - Sort data
  - Query params: `field`, `ascending` (optional, default: true)
  - Parameters are validated using Pydantic schemas

- `GET /api/data/transform/aggregate/` - Aggregate data
  - Query params: `field`, `operation` (optional, default: "sum") 
  - Operations: "sum", "avg", "min", "max", "count"
  - Parameters are validated using Pydantic schemas

## Running Tests

```
cd data_processing_api
pytest
```

## Validation Examples

The project includes a demonstration script showing how to use Pydantic validation:

```
cd scripts
python validation_example.py
```

This script demonstrates:
- Data validation for individual items and datasets
- Strong typing and automatic type conversion
- Validation of API parameters
- Custom validation rules
- Integration with domain models 