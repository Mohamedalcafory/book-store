# 📚 Online Book Store API

A REST API for managing an online book store built with Flask, featuring simplified book management and user authentication. This project implements a read-intensive book catalog system optimized for performance and scalability.

## 🚀 Features

### ✅ Implemented Features
- **Book Management**: Full CRUD operations for books with pagination, search, and filtering
- **User Management**: User registration, authentication
- **JWT Authentication**: Secure token-based authentication system with role-based permissions
- **Swagger Documentation**: Interactive API documentation with Flask-RESTX
- **Database Migrations**: Alembic-based database schema management
- **Input Validation**: Comprehensive data validation with Marshmallow schemas
- **Error Handling**: Proper HTTP status codes and error responses
- **Pagination Support**: Efficient data retrieval for large datasets
- **Multi-parameter Filtering**: Filter books by price range, release date, category, and authors

### 🚧 Planned Features
- **Caching Layer**: Redis implementation for query result caching and performance optimization
- **Full Dockerization**: Complete Docker Compose setup with MySQL database container
- **Stock Notifications**: Manager notifications when book stock falls below threshold
- **Advanced Performance**: TTL caching, LRU cache for book details, cursor-based pagination

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
app/
├── controllers/     # API endpoints and request handling
├── models/         # Database models (SQLAlchemy)
├── repositories/   # Data access layer
├── services/       # Business logic layer
├── schemas/        # Data validation schemas (Marshmallow)
└── utils/          # Utility functions and exceptions
```

## 📋 API Endpoints

### Core API Endpoints

#### Book Management
- `POST /books` - Create new book
- `GET /books` - List books with filtering and pagination
  - Query parameters: `category`, `authors`, `min_price`, `max_price`, `start_date`, `end_date`, `search`, `page`, `per_page`
- `GET /books/{id}` - Get specific book details
- `PATCH /books/{id}` - Update book details

#### User Management
- `POST /users/signUp` - User registration
- `POST /users/login` - User authentication
- `POST /users/change-password` - Change user password (Authenticated users)
- `POST /users/logout` - Invalidate user tokens
- `GET /users/profile` - Get current user profile


## 🛠️ Technology Stack

### Core Technologies
- **Backend Framework**: Flask 3.0.3 with Flask-RESTX 1.3.0
- **Database**: SQLAlchemy 2.0.35 with MySQL support (SQLite for development)
- **Authentication**: JWT (Flask-JWT-Extended 4.6.0) with role-based access control
- **Data Validation**: Marshmallow 4.0.1 schemas for request/response validation
- **API Documentation**: Swagger/OpenAPI via Flask-RESTX
- **Database Migrations**: Alembic 1.13.2 for schema management
- **Environment Management**: python-dotenv 1.0.1

### Architecture Components
1. **API Layer**: Flask-RESTX controllers for request handling
2. **Business Logic Layer**: Service classes for core business operations  
3. **Data Access Layer**: Repository pattern for database interactions
4. **Authentication Layer**: JWT-based authentication system
5. **Caching Layer**: Redis (planned for enhanced performance)
6. **Database Layer**: MySQL for production, SQLite for development

### Deployment & Containerization
- **Containerization**: Docker with Docker Compose
- **Current Setup**: Partial dockerization (app containerized, MySQL on host)
- **Planned Enhancement**: Full Docker Compose with MySQL container

## 🎯 System Design Highlights

This project implements a **read-intensive book catalog system** designed according to the following principles:

### Key Design Decisions
- **Simplified Data Model**: Authors and categories as string fields (no complex joins)
- **Performance-First**: 90% read, 10% write workload optimization
- **Scalable Architecture**: Clean separation of concerns with repository pattern

### Performance Optimization Strategy
- **Query Optimization**: Composite indexing on (category, price, release_date)
- **Efficient Pagination**: Supports large datasets without performance degradation
- **Caching Strategy**: Planned Redis implementation for 5-minute TTL on frequent queries

### Scale Estimation
- **Data Scale**: 10,000-100,000 books, 1,000-10,000 users
- **Query Performance**: Designed for 100-1000 QPS during peak hours
- **Storage Estimation**: ~1KB per book, 100MB - 1GB total book data

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL/PostgreSQL (or SQLite for development)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohamedalcafory/book-store.git
   cd book-store
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

5. **Database setup**
   ```bash
   # Initialize database migrations
   flask db init
   
   # Create initial migration
   flask db migrate -m "Initial migration"
   
   # Apply migrations
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## 📖 API Documentation

Once the application is running, you can access the interactive Swagger documentation at:
- **Swagger UI**: `http://localhost:5000/`
- **ReDoc**: `http://localhost:5000/redoc/`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=mysql://username:password@localhost/bookstore
# or for PostgreSQL: postgresql://username:password@localhost/bookstore
# or for SQLite: sqlite:///bookstore.db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 days

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📊 Database Schema (Simplified Design)

### Design Decision: Simplified vs Normalized
**Chosen Approach**: Simplified design with authors and categories as string fields within Book entity.

**Rationale**:
- Reduces complexity for read-heavy workloads
- Eliminates need for complex joins  
- Faster query performance for filtering operations
- Aligns with assignment scope (no complex author/category management required)
- Easier to implement and maintain

### Core Models

#### Book Entity (Primary Model)
```python
Book {
    id: long (PK)
    title: string (indexed)
    authors: string (e.g., "Stephen King, Peter Straub")
    category: string (indexed, e.g., "Fiction", "Horror", "Science")
    description: text
    price: float
    release_date: datetime
    stock: integer
    creator: string (username who added the book)
}
```

#### User Entity
```python
User {
    id: long (PK)
    username: string (unique, indexed)
    email: string (unique, indexed)
    password_hash: string
    is_admin: boolean
    is_active: boolean
    created_at: datetime
    updated_at: datetime
}
```

### Performance Optimizations
- **Database Indexing**: Primary index on book title, composite index on (category, price, release_date)
- **Query Performance**: 90% read, 10% write (read-intensive application)
- **Scale Estimation**: 10,000-100,000 books, 1,000-10,000 users

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /api/users` with user details
2. **Login**: `POST /api/auth/login` with credentials
3. **Access Token**: Include `Authorization: Bearer <token>` in requests
4. **Refresh Token**: Use refresh token to get new access tokens

## 📝 Example Usage

### User Registration
```bash
curl -X POST "http://localhost:5000/users/signUp" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepassword123",
    "is_admin": true
  }'
```

### User Login
```bash
curl -X POST "http://localhost:5000/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "securepassword123"
  }'
```

### Creating a Book
```bash
curl -X POST "http://localhost:5000/books" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "title": "The Great Gatsby",
    "description": "A classic American novel",
    "price": 12.99,
    "author": "F. Scott Fitzgerald",
    "category": "Fiction",
    "stock": 50,
    "creator": "john",
    "release_date": "1925-04-10"
  }'
```

### Listing Books with Filtering
```bash
# Basic listing with pagination
curl "http://localhost:5000/books?page=1&per_page=10"

# Filter by category and price range
curl "http://localhost:5000/books?category=Fiction&min_price=10.00&max_price=20.00"

# Search in title and description
curl "http://localhost:5000/books?search=gatsby&page=1&per_page=10"
```

### API Response Format
```json
{
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "category": "Fiction",
      "price": 12.99,
      "stock": 50,
      "release_date": "1925-04-10"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 150,
    "pages": 15,
    "has_next": true,
    "has_prev": false
  }
}
```

## 🐳 Docker Support

### Current Implementation (Partial Dockerization)
The application includes Docker configuration for easy deployment:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### ⚠️ Current Limitation: External MySQL Dependency

**Current Status**: The application is containerized but **depends on a MySQL server running on the host machine**, not a MySQL Docker container.

**Current Setup Requirements**:
1. **MySQL installed and running on your host machine** (not in Docker)
2. **MySQL configured to accept connections from Docker containers**
3. **Application connects to MySQL via `host.docker.internal:3306`**
4. **Initialize your database with `init.sql` script**
5. **Run `flask db upgrade` for updating your database**

#### Prerequisites for Current Docker Setup:
- MySQL server installed and running on host machine
- MySQL user with proper permissions for external connections
- Database `bookstore` created on the host MySQL instance
