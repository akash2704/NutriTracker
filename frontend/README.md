# Fitness Tracker Frontend

A modern React frontend for the Nutrition Tracker API built with Vite and Tailwind CSS.

## Features

- **Authentication**: Register, verify, and login with JWT tokens
- **Dashboard**: View daily nutrition analysis with gap analysis
- **Food Database**: Search and browse extensive food database
- **Food Logging**: Log meals with quantities and meal types
- **Profile Management**: Create and manage user profiles
- **Analytics**: View nutrition trends over time
- **Responsive Design**: Modern UI with Tailwind CSS

## Tech Stack

- React 19
- Vite
- Tailwind CSS 3
- React Router DOM
- Axios
- React Hook Form
- Lucide React (icons)

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open http://localhost:5173

## Pages

- `/login` - User login
- `/register` - User registration with OTP verification
- `/dashboard` - Nutrition dashboard with gap analysis
- `/foods` - Food database search and browse
- `/log` - Log food consumption
- `/profile` - User profile management
- `/analytics` - Nutrition analytics and trends

## API Integration

The frontend connects to the FastAPI backend running on http://localhost:8000
