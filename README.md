# Data Processing Application

A full-stack application with Django backend and React frontend for data processing and visualization. This application allows users to create, filter, sort, and aggregate data items with various properties.

## Project Structure

- **Backend**: Django REST API with clean architecture
  - Domain-driven design with clear separation of concerns
  - SQLAlchemy integration for database operations
  - Pydantic validation for robust data handling
  - Comprehensive logging and error handling

- **Frontend**: React application with TypeScript
  - Component-based UI with modern React practices
  - Form handling with validation
  - Data visualization components
  - API integration with error handling
  - Client-side caching with localStorage
  - Real-time data updates with configurable polling

## Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- Docker and Docker Compose (for PostgreSQL database)
- Git

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Backend Setup

1. **Create a virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start PostgreSQL with Docker**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
cd data_processing_api
python manage.py migrate
```

5. **Initialize the database (optional)**
```bash
cd ..
python scripts/init_db.py
python scripts/load_test_data.py  # Load sample data
```

6. **Run the development server**
```bash
cd data_processing_api
python manage.py runserver
```

The backend API will be available at http://localhost:8000/

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start the development server**
```bash
npm start
```

The frontend application will be available at http://localhost:3000/

## API Documentation

### Authentication

The API uses JWT authentication. Most endpoints are currently configured to allow anonymous access for development purposes.

### Data Processing Endpoints

#### Create Products

**Endpoint:** `POST /api/data/process/`

**Description:** Create one or more products with various properties

**Request Body:**
```json
[
  {
    "name": "Product A",
    "price": 25.99,
    "quantity": 10,
    "category": "Electronics"
  },
  {
    "name": "Product B",
    "price": 15.50,
    "quantity": 5,
    "category": "Books"
  }
]
```

**Response (201 Created):**
```json
[
  {
    "id": 1,
    "name": "Product A",
    "price": 25.99,
    "quantity": 10,
    "category": "Electronics"
  },
  {
    "id": 2,
    "name": "Product B",
    "price": 15.50,
    "quantity": 5,
    "category": "Books"
  }
]
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid data format",
  "details": [
    {
      "loc": ["items", 0, "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Get All Products

**Endpoint:** `GET /api/data/products/`

**Description:** Retrieve all products

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Product A",
      "price": 25.99,
      "quantity": 10,
      "category": "Electronics"
    },
    {
      "id": 2,
      "name": "Product B",
      "price": 15.50,
      "quantity": 5,
      "category": "Books"
    }
  ]
}
```

#### Filter Products

**Endpoint:** `GET /api/data/transform/filter/`

**Description:** Filter products by field, value, and operator

**Query Parameters:**
- `field` (required): Field name to filter by (e.g., "name", "price", "category")
- `value` (required): Value to filter by
- `operator` (optional): Comparison operator (default: "eq")
  - Available operators: "eq" (equals), "neq" (not equals), "gt" (greater than), "lt" (less than), "contains" (substring)

**Example Request:**
```
GET /api/data/transform/filter/?field=price&value=20&operator=gt
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Product A",
      "price": 25.99,
      "quantity": 10,
      "category": "Electronics"
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid parameters",
  "details": [
    {
      "loc": ["field"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Sort Products

**Endpoint:** `GET /api/data/transform/sort/`

**Description:** Sort products by field

**Query Parameters:**
- `field` (required): Field name to sort by (e.g., "name", "price", "quantity")
- `ascending` (optional): Sort order (default: true)

**Example Request:**
```
GET /api/data/transform/sort/?field=price&ascending=false
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Product A",
      "price": 25.99,
      "quantity": 10,
      "category": "Electronics"
    },
    {
      "id": 2,
      "name": "Product B",
      "price": 15.50,
      "quantity": 5,
      "category": "Books"
    }
  ]
}
```

#### Aggregate Products

**Endpoint:** `GET /api/data/transform/aggregate/`

**Description:** Aggregate numeric fields using various operations

**Query Parameters:**
- `field` (required): Field name to aggregate (must be numeric, e.g., "price", "quantity")
- `operation` (optional): Aggregation operation (default: "sum")
  - Available operations: "sum", "avg", "min", "max", "count"

**Example Request:**
```
GET /api/data/transform/aggregate/?field=price&operation=avg
```

**Response (200 OK):**
```json
{
  "result": 20.745
}
```

## Frontend Features

- Product listing with filtering and sorting
- Product creation form with validation
- Data visualization components
- Responsive design
- Client-side caching for improved performance
- Real-time data updates with configurable polling

### Client-side Caching

The frontend implements a localStorage-based caching strategy:

- Cache duration configurable per request (default: 5 minutes)
- Automatic cache invalidation when data is modified
- Force refresh option for time-critical data
- Selective caching for different operations

### Real-time Updates

The application includes real-time data updates using polling:

- Configurable polling intervals (default: 10 seconds)
- User controls to enable/disable real-time updates
- Visual indicator for active polling status
- Smart updates that preserve current sorting and filtering

## Testing

### Backend Tests

```bash
cd backend/data_processing_api
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Development

### Backend Development

The backend follows a clean architecture pattern:
- `domain`: Core business logic and models
- `application`: Use cases and services
- `infrastructure`: Database models and repositories
- `interfaces`: API views and serializers

### Frontend Development

The frontend follows a feature-based architecture:
- `app/`: Application setup, routing, and global providers
- `entities/`: Domain models and entity-specific components
- `features/`: Feature-specific components with business logic
- `pages/`: Page components that compose features and widgets
- `shared/`: Reusable components, hooks, utilities, and configurations
- `widgets/`: Composite UI blocks
- `styles/`: Global styles and Tailwind configuration

## Deployment

The project includes an AWS systems design document (`aws_systems_design.md`) that outlines a comprehensive deployment strategy using AWS managed services:

- Frontend hosted on S3 with CloudFront distribution
- Backend containerized with Docker and deployed on ECS/Fargate
- PostgreSQL database on RDS with Multi-AZ configuration
- Redis caching with ElastiCache
- CI/CD pipeline using AWS CodePipeline
- Comprehensive monitoring with CloudWatch

See the `aws_systems_design.md` file for detailed deployment instructions and architecture diagrams.

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Ensure PostgreSQL is running via Docker
   - Check database credentials in settings

2. **API connection errors**
   - Verify backend server is running
   - Check CORS settings if frontend can't connect

3. **Missing dependencies**
   - Run `pip install -r requirements.txt` for backend
   - Run `npm install` for frontend

4. **Caching issues**
   - Clear browser localStorage if experiencing stale data
   - Use the "Force Refresh" button in the UI
   - Disable real-time updates if troubleshooting specific issues

## License

This project is licensed under the MIT License - see the LICENSE file for details. 