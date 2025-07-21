# UCMe

A college-specific dating app built with React, FastAPI and PostgreSQL.

## Project Structure

```
ucme/
├── backend/            # FastAPI backend
│   ├── main.py         # FastAPI app entry point
│   ├── database.py     # SQLAlchemy DB connection
│   ├── models/
│   │   └── user.py     # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py     # Pydantic schemas
│   ├── routes/
│   │   └── auth.py     # Auth endpoints
│   ├── utils/
│   │   └── auth.py     # Password hashing, JWT
│   ├── requirements.txt
│   └── .env
├── .gitignore
└── README.md
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL + SQLAlchemy

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL database

### 1. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Edit backend/.env with your database URL and JWT secret
```

### 3. Start Development Server

```bash
cd backend
uvicorn main:app --reload
```

The API will run on `http://localhost:8000`.

## Features (MVP)

- User authentication (signup/login)
- Profile creation and editing
- Swipe interface for discovering matches
- Chat functionality for matched users
- College verification system

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login