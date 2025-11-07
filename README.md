# NutriTracker - AI-Powered Indian Nutrition & Fitness Tracker

[![CI/CD Pipeline](https://github.com/akash2704/NutriTracker/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/akash2704/NutriTracker/actions)
[![Tests](https://github.com/akash2704/NutriTracker/workflows/Pull%20Request%20Checks/badge.svg)](https://github.com/akash2704/NutriTracker/actions)
[![Coverage](https://codecov.io/gh/akash2704/NutriTracker/branch/master/graph/badge.svg)](https://codecov.io/gh/akash2704/NutriTracker)

> **Live Demo**: [https://nutritracker-frontend.vercel.app](https://nutri-tracker-rust.vercel.app/dashboard)

A comprehensive nutrition tracking application built with FastAPI and React, featuring personalized weight loss recommendations powered by Google Gemini AI.

## 🎯 Project Overview

**The Challenge**: 
Most nutrition tracking applications focus on Western diets and lack comprehensive data for Indian foods, leaving a significant gap in the market for culturally relevant nutrition tracking.

**The Solution**:
NutriTracker addresses this gap by utilizing official Indian government nutrition databases (IFCT 2017 & INDB 2024) containing 50,000+ Indian foods, combined with Google Gemini AI for intelligent, personalized recommendations.

**Key Differentiators**:
- **Accuracy**: Official Indian nutrition data from government sources
- **Cultural Relevance**: Comprehensive Indian food database with regional cuisines
- **AI Integration**: Personalized meal planning based on individual health metrics
- **Scalability**: Built with modern tech stack for enterprise-grade performance

## 📋 API Documentation

Since the hosted API docs are currently unavailable, here's the complete API reference:

### Base URL
```
Development: http://localhost:8000
```

### Authentication Endpoints
```http
POST /auth/register
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response: {"message": "User registered. Please verify your email."}

POST /auth/login  
Content-Type: application/json
{
  "username": "user@example.com",
  "password": "securepassword"
}
Response: {"access_token": "jwt_token", "token_type": "bearer"}

POST /auth/verify-otp
Content-Type: application/json
{
  "email": "user@example.com",
  "otp": "123456"
}
Response: {"message": "Email verified successfully"}
```

### User & Profile Endpoints
```http
GET /users/me
Authorization: Bearer {jwt_token}
Response: {"id": 1, "email": "user@example.com", "is_verified": true}

GET /profile/me
Authorization: Bearer {jwt_token}
Response: {
  "birth_date": "1990-01-01",
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 70,
  "activity_level": "moderate"
}

POST /profile/me
Authorization: Bearer {jwt_token}
Content-Type: application/json
{
  "birth_date": "1990-01-01",
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 70,
  "activity_level": "moderate",
  "dietary_preference": "vegetarian",
  "budget_range": "medium"
}
```

### Food & Nutrition Endpoints
```http
GET /foods/?search={query}&limit=20
Response: {
  "foods": [
    {
      "id": 1,
      "name": "Rice, raw",
      "calories_per_100g": 345,
      "protein_g": 6.8,
      "carbs_g": 78.2,
      "fat_g": 0.5
    }
  ]
}

GET /foods/{food_id}
Response: {
  "id": 1,
  "name": "Rice, raw",
  "calories_per_100g": 345,
  "protein_g": 6.8,
  "carbs_g": 78.2,
  "fat_g": 0.5,
  "fiber_g": 0.2,
  "calcium_mg": 10
}

POST /food-log/
Authorization: Bearer {jwt_token}
Content-Type: application/json
{
  "food_id": 1,
  "quantity_g": 100,
  "meal_type": "breakfast"
}
Response: {"message": "Food logged successfully"}
```

### Dashboard & Analytics
```http
GET /dashboard/
Authorization: Bearer {jwt_token}
Response: {
  "daily_nutrition": {
    "calories": 1850,
    "protein": 65,
    "carbs": 230,
    "fat": 62
  },
  "weekly_average": {...},
  "goal_progress": {...}
}
```

### AI Recommendations
```http
GET /recommendations/
Authorization: Bearer {jwt_token}
Response: {
  "bmr": 1680,
  "tdee": 2310,
  "target_calories": 1810,
  "bmi": 22.9,
  "recommendations": {
    "greeting": "Welcome to your personalized nutrition guide!",
    "meal_plan": {
      "breakfast": "Oats upma with vegetables - 450 calories",
      "lunch": "Dal rice with mixed vegetables - 630 calories",
      "dinner": "Roti with paneer curry - 540 calories",
      "snack": "Mixed nuts and fruit - 180 calories"
    },
    "exercise_plan": [
      "30-minute brisk walk daily",
      "Strength training 3x per week"
    ]
  }
}
```

### Recipe Processing
```http
POST /recipe/parse
Authorization: Bearer {jwt_token}
Content-Type: multipart/form-data
file: recipe.pdf (or)
Content-Type: application/json
{
  "recipe_text": "Ingredients: 1 cup rice, 2 cups water..."
}
Response: {
  "ingredients": [...],
  "total_nutrition": {...}
}
```

### Rate Limiting
- **Limit**: 60 requests per minute per IP address
- **Response**: `429 Too Many Requests` when exceeded
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## 🌟 Key Features

### 🍛 Comprehensive Indian Food Database
- **50,000+ Indian foods** from IFCT 2017 and INDB 2024
- Accurate macro and micronutrient data for traditional Indian dishes
- Regional cuisine coverage (North, South, East, West Indian foods)

### 🤖 AI-Powered Personalization
- **Google Gemini AI** integration for intelligent meal planning
- Personalized recommendations based on BMR, TDEE, and health goals
- Budget-aware suggestions (low, medium, high budget ranges)
- Dietary preference support (vegetarian, non-vegetarian, vegan)

### 📊 Smart Analytics Dashboard
- Visual nutrition tracking with charts and progress indicators
- Daily, weekly, and monthly nutrition insights
- BMI calculation and health goal monitoring
- Calorie deficit tracking for weight management

### 🔍 Recipe Intelligence
- **PDF recipe parser** - Upload recipe PDFs and get ingredient breakdown
- Text recipe analysis with automatic nutrition calculation
- Save and organize favorite recipes with nutritional data

### 🛡️ Enterprise-Grade Security
- JWT-based authentication with email verification
- Rate limiting to prevent DDoS attacks and control API costs
- Secure password hashing with bcrypt
- CORS protection and input validation

## 🏗️ Technical Architecture

### Backend (FastAPI + PostgreSQL)
```
├── FastAPI Framework - High-performance async API
├── PostgreSQL - Robust relational database
├── SQLAlchemy ORM - Type-safe database operations
├── Google Gemini AI - Intelligent recommendations
├── JWT Authentication - Secure user sessions
├── Rate Limiting - DDoS protection & cost control
└── AWS Lambda - Serverless deployment
```

### Frontend (React + Tailwind)
```
├── React 18 - Modern UI framework
├── Tailwind CSS - Utility-first styling
├── React Router - Client-side navigation
├── Context API - State management
├── React Hook Form - Form validation
└── Lucide Icons - Beautiful iconography
```

### Infrastructure & Deployment
```
├── AWS Lambda - Serverless backend hosting
├── AWS API Gateway - API management & routing
├── Vercel - Frontend hosting & CDN
├── PostgreSQL - Database hosting
└── GitHub Actions - CI/CD pipeline
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Google Gemini API key

### 1. Clone & Setup
```bash
git clone https://github.com/akash2704/NutriTracker.git
cd NutriTracker
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies with UV
uv sync

# Environment setup
cp .env.example .env
# Add your DATABASE_URL, SECRET_KEY, and GEMINI_API_KEY

# Database setup
uv run alembic upgrade head
uv run python seed.py  # Load 50K+ Indian foods

# Start server
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
```env
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost:5432/nutritracker
SECRET_KEY=your-super-secret-key
GEMINI_API_KEY=your-gemini-api-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Email configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 📱 Usage Guide

### 1. **User Registration & Profile Setup**
- Sign up with email verification
- Complete health profile (age, height, weight, activity level)
- Set dietary preferences and budget range

### 2. **Food Logging & Tracking**
- Search from 50,000+ Indian foods
- Log meals with accurate portions
- Track daily macro and micronutrient intake

### 3. **AI-Powered Recommendations**
- Get personalized meal plans based on your profile
- Receive calorie targets for healthy weight management
- Follow exercise suggestions tailored to your fitness level

### 4. **Recipe Analysis**
- Upload recipe PDFs or paste recipe text
- Get automatic ingredient breakdown with nutrition facts
- Save recipes for future meal planning

### 5. **Progress Monitoring**
- View nutrition dashboard with visual insights
- Track BMI changes and goal progress
- Monitor daily calorie intake vs targets

## 🔧 API Documentation

### Core Endpoints

#### Authentication
```http
POST /auth/register     # User registration
POST /auth/login        # User login
POST /auth/verify-otp   # Email verification
```

#### Food & Nutrition
```http
GET  /foods/            # Search Indian foods
GET  /foods/{id}        # Get food details
POST /food-log/         # Log food intake
GET  /dashboard/        # Nutrition analytics
```

#### AI Recommendations
```http
GET  /recommendations/  # Get personalized meal plans
```

#### Recipe Processing
```http
POST /recipe/parse      # Parse recipe text/PDF
```

### Rate Limiting
- **60 requests per minute** per IP address
- Prevents DDoS attacks and controls API costs
- Returns `429 Too Many Requests` when exceeded

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing
```bash
# Test API endpoints
curl -X GET "https://x3qavb8llb.execute-api.ap-south-1.amazonaws.com/Prod/foods/?search=rice"
```

## 🚀 Deployment

### Backend (AWS Lambda)
```bash
# Deploy to AWS Lambda
cd backend
zip -r nutritracker-backend.zip . -x "*.git*" "*.pytest_cache*" "__pycache__*"
# Upload to AWS Lambda with lambda_handler.handler
```

### Frontend (Vercel)
```bash
# Deploy to Vercel
cd frontend
npm run build
vercel --prod
```

### Environment Setup
- Set `GEMINI_API_KEY` in Lambda environment variables
- Configure `DATABASE_URL` for production database
- Update CORS origins in production

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with proper testing
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open Pull Request

### Code Standards
- **Backend**: Follow PEP 8, use type hints, write docstrings
- **Frontend**: Use ESLint, Prettier, and component-based architecture
- **Testing**: Maintain >80% code coverage
- **Documentation**: Update README for new features

## 📊 Project Metrics

- **50,000+** Indian foods in database
- **15+** API endpoints
- **JWT** secure authentication
- **Rate limited** to 60 req/min
- **Responsive** design for all devices
- **AI-powered** personalized recommendations

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Core nutrition tracking
- ✅ AI recommendations
- ✅ Recipe parsing
- ✅ User authentication

### Phase 2 (Next)
- [ ] Mobile app (React Native)
- [ ] Barcode scanning for packaged foods
- [ ] Meal planning calendar
- [ ] Social features & community

### Phase 3 (Future)
- [ ] Integration with fitness trackers
- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Offline mode capability
- [ ] Advanced analytics & insights

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IFCT 2017** - Indian Food Composition Tables by National Institute of Nutrition
- **INDB 2024** - Indian Nutrient Database for comprehensive food data
- **Google Gemini AI** - Powering intelligent recommendations
- **FastAPI & React Communities** - For excellent frameworks and documentation

## 📞 Contact & Support

- **Developer**: Akash Kallai
- **Email**: akashkallai@example.com
- **GitHub**: [@akash2704](https://github.com/akash2704)
- **Issues**: [GitHub Issues](https://github.com/akash2704/NutriTracker/issues)

---

**Built with ❤️ for healthier living in India**

> *"Technology should make healthy living accessible to everyone, regardless of their cultural background or economic status."* - Project Philosophy
