# UCMe

A college-specific dating app built with FastAPI and PostgreSQL.

## Project Structure

```
UCMe-Matchmaking-Application/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI app entry point
│   ├── database.py            # SQLAlchemy DB connection & session
│   ├── models/
│   │   └── user.py           # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py           # Pydantic request/response schemas
│   ├── routes/
│   │   ├── register.py       # User registration with email verification
│   │   └── auth.py           # Authentication endpoints
│   ├── utils/
│   │   └── auth.py           # Email verification & magic codes
│   ├── requirements.txt       # Python dependencies
│   └── env.example           # Environment variables template
├── .gitignore
└── README.md
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL + SQLAlchemy
- **Email**: SMTP with magic code verification
- **Cache**: Redis for verification codes
- **Authentication**: Email verification system

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Redis server (for verification codes)
- SMTP email service (Gmail, SendGrid, etc.)

### 1. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup

Copy `env.example` to `.env` and configure:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/ucme

# Email Configuration (for verification codes)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
APP_NAME=UCMe

# Redis Configuration (for storing verification codes)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3. Start Development Server

```bash
cd backend
uvicorn main:app --reload
```

The API will run on `http://localhost:8000`.

## Features (Implemented)

- ✅ **Email verification system** with magic codes
- ✅ **UC email validation** (restricted to UC domains)
- ✅ **User registration** with profile creation
- ✅ **Database models** for user data
- 🚧 **User authentication** (login system)
- 🚧 **Profile editing**
- 🚧 **Swipe interface** for discovering matches
- 🚧 **Chat functionality** for matched users

## API Endpoints

### Registration & Email Verification
- `POST /auth/send-verification` - Send magic code to email
- `POST /auth/verify-email` - Verify email with magic code
- `POST /auth/register` - Complete user registration
- `POST /auth/resend-email` - Resend verification code

### Authentication
- `POST /auth/login` - User login (basic implementation)

## Registration Flow

1. **Send Verification**: User provides UC email → Magic code sent
2. **Verify Email**: User enters magic code → Email verified
3. **Complete Registration**: User provides profile data → Account created

## Project Status

**DEVELOPMENT** - Email verification system implemented. Ready for authentication and core features.