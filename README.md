# UCMe

A college-focused matchmaking app built with FastAPI (backend) and React (frontend).

## Project Structure

```
UCMe
├── backend/                     # FastAPI API
│   ├── main.py                  # App bootstrap, CORS, static mounts (/uploads)
│   ├── database.py              # SQLAlchemy engine/session (PostgreSQL required)
│   ├── models/                  # SQLAlchemy models (User, Image, Swipe, Match, Message)
│   ├── schemas/                 # Pydantic schemas (request/response)
│   ├── routes/                  # API routes: auth, profile, images, interactions, recommendations, messages
│   ├── utils/                   # JWT auth, email/Redis verification utils
│   ├── uploads/                 # Image files stored locally and served at /uploads
│   └── requirements.txt         # Backend dependencies
└── frontend/                    # React app (Create React App)
    ├── src/components/          # Pages & features
    ├── src/services/            # API clients (axios)
    ├── src/contexts/            # Auth context
    └── package.json
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (required – ARRAY columns are used)
- (Optional) Redis for verification codes
- (Optional) SMTP provider (SMTP2Go recommended) for email verification

## Environment

Create `backend/.env` using `backend/env.example` as a reference. Key variables:

- DATABASE_URL: PostgreSQL URL (e.g. `postgresql://user:pass@localhost/ucme_db`)
- SECRET_KEY: JWT signing key
- CORS_ORIGINS: Comma-separated list, e.g. `http://localhost:3000`
- SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD (optional)
- REDIS_HOST, REDIS_PORT (optional)

Frontend expects the backend URL via `REACT_APP_API_URL` at build/runtime. For local dev:

```
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
```

## Install & Run

### Backend

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

### Frontend

```
cd frontend
npm install
npm start
```

App: `http://localhost:3000`

## Features

- Authentication
  - Email login with verification code (UC domains enforced)
  - JWT stored in localStorage (dev)
- Discover
  - Swipe-like UI; like/pass via `/interactions`
  - Card content scrolls for long bios/classes/interests
- Matches
  - Grid view of matched users
  - Starts conversations from a match
- Messaging
  - Conversations list with unread counts
  - Conversation detail with read receipts (opening marks as read)
  - Bubble colors: sent (UC Blue, right), received (UC Gold, left)
- Profile
  - Edit profile and preferences
  - Images: upload up to 3; set primary; remove image
  - Primary image is shown across Discover/Matches/Messages

## Images – How it works

- Uploads go to `backend/uploads/images` and are served at `/uploads` (mounted in `main.py`).
- API routes (see `backend/routes/images.py`):
  - `POST /images/upload` (multipart form: `file`, `isPrimary` bool) – max 3 images enforced.
  - `PUT  /images/{imageId}/set-primary` – sets an image as primary (unsets others).
  - `DELETE /images/{imageId}` – deletes an image (cannot delete the only primary if it’s the only image).
- Frontend resolves relative `imageUrl` values by prefixing with `REACT_APP_API_URL`.

## API Overview 

- Auth (`backend/routes/auth.py`)
  - `POST /auth/login/sendVerification` – request code
  - `POST /auth/login` – verify code, returns JWT
  - `POST /auth/register` – registration (with verification)
- Profile (`backend/routes/profile.py`)
  - `GET  /profile/me` – current user (images eager-loaded)
  - `PUT  /profile/update` – update profile
  - `PUT  /profile/preferences` – update preferences
  - `GET  /profile/viewProfile/{userId}` – view others (Approved only)
- Images (`backend/routes/images.py`) – see section above
- Interactions (`backend/routes/interactions.py`)
  - `POST /interactions/like?targetId=` – like
  - `POST /interactions/pass?targetId=` – pass
  - `GET  /interactions/matches` – list matches
- Recommendations (`backend/routes/recommendations.py`)
  - `GET /recommendations/discover` – discover feed
- Messages (`backend/routes/messages.py`)
  - `GET  /messages/conversations` – list summaries (with unreadCount)
  - `GET  /messages/conversations/{id}` – detail (messages + otherUser)
  - `POST /messages/conversations` – create or return existing conversation
  - `POST /messages/conversations/{id}/messages` – send message
  - `PUT  /messages/conversations/{id}/read` – mark as read

## Backend Notes

- Database: `backend/database.py` enforces PostgreSQL URLs.
- CORS: configured in `main.py` via `CORS_ORIGINS` (defaults include localhost:3000).
- Static: `app.mount("/uploads", StaticFiles(directory="uploads"))` serves uploaded images.
- JWT: utilities in `backend/utils/jwt_auth.py`.
- Email/Redis: utilities in `backend/utils/auth.py`; app runs without SMTP/Redis (codes logged).

## Frontend Notes

- Auth context (`src/contexts/AuthContext.js`) loads the full profile on login/app start so name/id are available in the UI.
- Services (`src/services/*`) use `REACT_APP_API_URL` and attach `Authorization: Bearer <token>`.
- Messaging UI lives under `src/components/messaging/` and styles under `src/styles/messaging/`.



## Scripts

- Backend: `uvicorn main:app --reload`
- Frontend: `npm start` (dev), `npm run build` (prod)

## License

For educational use. Not affiliated with the University of California in any way, developed as a fun project idea by Amir Kiadi
