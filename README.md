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
- SMTP email service (SMTP2Go recommended, Gmail, SendGrid, etc.)

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
# SMTP2Go (recommended):
SMTP_HOST=mail.smtp2go.com
SMTP_PORT=2525
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-api-key
SMTP_TLS=true
SMTP_SSL=false
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

### Email Setup with SMTP2Go

For reliable email delivery, we recommend using SMTP2Go:

1. **Sign up** at [SMTP2Go.com](https://www.smtp2go.com/) (1000 emails/month free)
2. **Get credentials** from Settings → API Keys
3. **Configure** your `.env` file with SMTP2Go settings
4. **Test** email sending with the provided test script

See `backend/SMTP2GO_SETUP.md` for detailed configuration instructions.

### Registration & Email Verification
- `POST /auth/send-verification` - Send magic code to email
- `POST /auth/verify-email` - Verify email with magic code
- `POST /auth/register` - Complete user registration
- `POST /auth/resend-email` - Resend verification code

## Registration Flow

1. **Send Verification**: User provides UC email → Magic code sent
2. **Verify Email**: User enters magic code → Email verified
3. **Complete Registration**: User provides profile data → Account created
