# UCMe

A college-specific dating app built with the MERN stack (MongoDB, Express, React, Node.js).

## Project Structure

```
ucme/
├── client/             # React frontend
│   ├── public/         # Static files
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Page components
│   │   │   ├── Signup.js
│   │   │   ├── Login.js
│   │   │   └── Home.js
│   │   ├── App.js      # Main App component
│   │   └── index.js    # React entry point
│   ├── tailwind.config.js
│   └── package.json
├── server/             # Express backend
│   ├── config/
│   │   └── db.js       # MongoDB connection
│   ├── models/
│   │   └── User.js     # User model
│   ├── routes/
│   │   └── auth.js     # Authentication routes
│   ├── controllers/    # Route controllers
│   ├── index.js        # Express server
│   └── package.json
├── .env.example        # Environment variables template
├── .gitignore
└── README.md
```

## Tech Stack

- **Frontend**: React + Tailwind CSS + React Router
- **Backend**: Node.js + Express
- **Database**: MongoDB + Mongoose ODM
- **Authentication**: JWT + bcryptjs

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- MongoDB (local installation or MongoDB Atlas)

### 1. Clone and Install

```bash
# Install server dependencies
cd server
npm install

# Install client dependencies
cd ../client
npm install
```

### 2. Environment Setup

```bash
# Create .env file in the server directory
cp .env.example server/.env

# Edit server/.env with your MongoDB URI and JWT secret
```

### 3. Start Development Servers

```bash
# Terminal 1: Start backend server
cd server
npm run dev

# Terminal 2: Start frontend
cd client
npm start
```

The React app will run on `http://localhost:3000` and the Express server on `http://localhost:5000`.

## Features (MVP)

- ✅ User authentication (signup/login)
- ✅ Responsive UI with Tailwind CSS
- ✅ React Router navigation
- ✅ MongoDB user storage
- ✅ JWT-based authentication
- 🚧 Profile creation and editing
- 🚧 Swipe interface for discovering matches
- 🚧 Chat functionality for matched users
- 🚧 College verification system

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login

## Project Status

**SCAFFOLDED** - Basic folder structure and dependencies set up. Ready for development.
