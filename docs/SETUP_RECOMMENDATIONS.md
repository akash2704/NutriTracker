# Weight Loss Recommendations Setup

## Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your-actual-gemini-api-key
```

3. **Get Gemini API Key:**
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Copy it to your `.env` file

## How It Works

### Calorie Calculation
For your profile (Male, 22 years, 179cm, 97kg, sedentary):
- **BMR**: ~2,000 calories (base metabolic rate)
- **TDEE**: ~2,400 calories (total daily expenditure)
- **Weight Loss Target**: ~1,900 calories (500 cal deficit)

### AI Recommendations
The system uses Gemini AI to provide:
- Daily meal breakdown (breakfast, lunch, dinner, snacks)
- Macronutrient targets (protein, carbs, fats)
- Specific food recommendations
- Exercise suggestions
- Weekly weight loss goals

## Usage

1. **Start the backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Access recommendations:**
- Frontend: Visit `/recommendations` page
- API: `GET /recommendations/` (requires authentication)

## Dashboard Features

- **BMI Display**: Shows current BMI (30.3 - overweight)
- **Calorie Targets**: Daily calories for weight loss
- **Metabolic Info**: BMR and TDEE calculations
- **AI Recommendations**: Personalized diet and exercise plan

## Weight Loss Plan

Based on your profile, you should:
- Consume ~1,900 calories daily (500 below maintenance)
- Expect 1-2 lbs weight loss per week
- Focus on protein-rich foods
- Include regular physical activity

The AI will provide specific meal plans and food recommendations tailored to Indian cuisine and your preferences.
