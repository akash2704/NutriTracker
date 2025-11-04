# NutriTracker - Indian Nutrition & Fitness Tracker

A comprehensive nutrition tracking application built with FastAPI and React, featuring personalized weight loss recommendations powered by AI.

## 🌟 Features

### Core Functionality
- **Food Database**: 50,000+ Indian foods from IFCT 2017 and INDB 2024
- **Nutrition Tracking**: Log meals with accurate macro and micronutrient data
- **Recipe Parser**: Extract ingredients and nutrition from recipe text/PDFs
- **Dashboard Analytics**: Visual insights into daily nutrition intake
- **User Profiles**: Complete health and dietary preference management

### AI-Powered Recommendations
- **Personalized Diet Plans**: AI-generated meal plans using Gemini API
- **Weight Loss Goals**: Calculated BMR, TDEE, and calorie targets
- **Dietary Preferences**: Vegetarian, non-vegetarian, and vegan options
- **Budget-Aware**: Recommendations based on low, medium, high budgets
- **Cuisine Preferences**: Indian, continental, or mixed cuisine options

### User Management
- **Secure Authentication**: JWT-based login with email verification
- **Profile Management**: Height, weight, activity level, dietary preferences
- **Progress Tracking**: BMI calculation and goal monitoring

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Primary database
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Google Gemini AI**: Personalized recommendations
- **JWT**: Secure authentication
- **Pydantic**: Data validation

### Frontend
- **React**: Modern UI framework
- **Tailwind CSS**: Utility-first styling
- **React Router**: Client-side routing
- **Lucide Icons**: Beautiful icons
- **React Hook Form**: Form management

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- UV package manager
- Google Gemini API key

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd fitness-tracker
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL, secret key, and Gemini API key

# Run database migrations
uv run alembic upgrade head

# Seed database with food data
uv run python seed.py

# Start development server
uv run uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Environment Variables

Create `backend/.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/nutrition_db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=your-gemini-api-key

# Optional: Email configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

## 🗄️ Database Setup

### PostgreSQL Setup
```sql
CREATE DATABASE nutrition_db;
CREATE USER nutrition_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nutrition_db TO nutrition_user;
```

### Migration Commands
```bash
# Create new migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## 🔑 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/verify-otp` - Email verification

### User Management
- `GET /users/me` - Get current user
- `GET /profile/me` - Get user profile
- `POST /profile/me` - Create/update profile

### Food & Nutrition
- `GET /foods/` - Search foods
- `GET /foods/{id}` - Get food details
- `POST /food-log/` - Log food intake
- `GET /dashboard/` - Get nutrition dashboard

### AI Recommendations
- `GET /recommendations/` - Get personalized recommendations

### Recipe Processing
- `POST /recipe/parse` - Parse recipe text/PDF

## 📱 Usage

### 1. User Registration
- Sign up with email and password
- Verify email with OTP
- Complete profile with health metrics

### 2. Profile Setup
- Enter birth date, gender, height, weight
- Set activity level and dietary preferences
- Choose budget range and cuisine preferences

### 3. Food Logging
- Search from 50,000+ Indian foods
- Log meals with quantities
- Track macros and micronutrients

### 4. Recipe Processing
- Upload recipe PDFs or paste text
- Get ingredient breakdown with nutrition
- Save recipes for future reference

### 5. AI Recommendations
- Get personalized meal plans
- View calorie targets for weight loss
- Follow exercise suggestions

## 🏗️ Project Structure

```
fitness-tracker/
├── backend/
│   ├── app/
│   │   ├── models.py          # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   └── dependencies.py    # Auth dependencies
│   ├── alembic/              # Database migrations
│   ├── data/                 # Food database files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── context/         # React context
│   │   └── services/        # API services
│   └── package.json
└── README.md
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend (Railway/Heroku)
1. Set environment variables
2. Configure PostgreSQL database
3. Run migrations: `alembic upgrade head`
4. Deploy with: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy `dist/` folder
3. Configure API base URL

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IFCT 2017**: Indian Food Composition Tables
- **INDB 2024**: Indian Nutrient Database
- **Google Gemini AI**: Personalized recommendations
- **Unsplash**: Food imagery
- **React & FastAPI Communities**: Amazing frameworks

## 📞 Support

For support, email support@nutritracker.com or create an issue on GitHub.

## 🔮 Roadmap

- [ ] Mobile app (React Native)
- [ ] Barcode scanning
- [ ] Meal planning calendar
- [ ] Social features & sharing
- [ ] Integration with fitness trackers
- [ ] Multi-language support
- [ ] Offline mode

---

**Built with ❤️ for healthier living in India**
