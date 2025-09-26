# 📚 Online Book Store API

A comprehensive REST API for managing an online book store built with Flask, featuring books, authors, categories, and user management with JWT authentication.

## 🚀 Features

- **Book Management**: Full CRUD operations for books with pagination, search, and filtering
- **Author Management**: Complete author lifecycle management with biography and metadata
- **Category Management**: Organize books with categories and descriptions
- **User Management**: User registration, authentication, and profile management
- **JWT Authentication**: Secure token-based authentication system
- **Swagger Documentation**: Interactive API documentation with Flask-RESTX
- **Database Migrations**: Alembic-based database schema management
- **Input Validation**: Comprehensive data validation with Marshmallow schemas
- **Error Handling**: Proper HTTP status codes and error responses

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

### Books
- `GET /api/books` - List books with pagination and filtering
- `POST /api/books` - Create a new book
- `GET /api/books/{id}` - Get book details
- `PATCH /api/books/{id}` - Update book
- `DELETE /api/books/{id}` - Delete book

### Authors
- `GET /api/authors` - List authors with pagination and search
- `POST /api/authors` - Create a new author
- `GET /api/authors/{id}` - Get author details
- `PATCH /api/authors/{id}` - Update author
- `DELETE /api/authors/{id}` - Delete author

### Categories
- `GET /api/categories` - List categories with pagination and search
- `POST /api/categories` - Create a new category
- `GET /api/categories/{id}` - Get category details
- `PATCH /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Users
- `GET /api/users` - List users (admin only)
- `POST /api/users` - Register new user
- `GET /api/users/{id}` - Get user profile
- `PATCH /api/users/{id}` - Update user profile
- `DELETE /api/users/{id}` - Delete user account

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.3
- **Database**: SQLAlchemy 2.0.35 with MySQL/PostgreSQL support
- **API Documentation**: Flask-RESTX 1.3.0
- **Authentication**: Flask-JWT-Extended 4.6.0
- **Data Validation**: Marshmallow 4.0.1
- **Database Migrations**: Alembic 1.13.2
- **Environment Management**: python-dotenv 1.0.1

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL/PostgreSQL (or SQLite for development)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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

## 📊 Database Schema

### Core Models

- **User**: User accounts with authentication
- **Author**: Book authors with biography and metadata
- **Category**: Book categories for organization
- **Book**: Books with relationships to authors and categories

### Relationships
- Author → Books (One-to-Many)
- Category → Books (One-to-Many)
- User → Books (One-to-Many, for book creators)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /api/users` with user details
2. **Login**: `POST /api/auth/login` with credentials
3. **Access Token**: Include `Authorization: Bearer <token>` in requests
4. **Refresh Token**: Use refresh token to get new access tokens

## 📝 Example Usage

### Creating a Book

```bash
curl -X POST "http://localhost:5000/api/books" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "title": "The Great Gatsby",
    "description": "A classic American novel",
    "price": 12.99,
    "author_id": 1,
    "category_id": 1,
    "stock": 50,
    "creator": "admin"
  }'
```

### Listing Authors with Search

```bash
curl "http://localhost:5000/api/authors?search=Fitzgerald&page=1&per_page=10"
```

## 🐳 Docker Support

The application includes Docker configuration for easy deployment:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📈 Performance Features

- **Pagination**: All list endpoints support pagination
- **Search & Filtering**: Search by name, filter by category/author
- **Database Indexing**: Optimized queries with proper indexing
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Proper HTTP status codes and error messages

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive data validation and sanitization
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Support**: Configurable Cross-Origin Resource Sharing
- **Rate Limiting**: Built-in request rate limiting (configurable)


## 🗺️ Roadmap

- [ ] Advanced search with full-text search
- [ ] Book reviews and ratings
- [ ] Shopping cart functionality
- [ ] Order management system
- [ ] Email notifications
- [ ] File upload for book covers
- [ ] Advanced analytics and reporting
- [ ] Multi-language support

---

**Happy Coding! 📚✨**
