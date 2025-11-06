import google.generativeai as genai
from datetime import date
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

class RecommendationService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-thinking-exp',  # Reasoning model
            generation_config={
                "temperature": 0.2,
                "response_mime_type": "application/json"  # Force JSON output
            }
        )
    
    def calculate_bmr(self, weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure"""
        multipliers = {
            'sedentary': 1.2,
            'moderate': 1.55,
            'heavy': 1.725
        }
        return bmr * multipliers.get(activity_level, 1.2)
    
    def get_weight_loss_calories(self, tdee: float) -> float:
        """Calculate calories for weight loss (500 cal deficit)"""
        return tdee - 500
    
    async def generate_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Generate personalized recommendations using Gemini API"""
    
    # Calculate user metrics (your existing code)
    birth_date = user_profile['birth_date']
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    height_m = user_profile['height_cm'] / 100
    bmi = user_profile['weight_kg'] / (height_m ** 2)
    
    bmr = self.calculate_bmr(
        user_profile['weight_kg'], 
        user_profile['height_cm'], 
        age, 
        user_profile['gender']
    )
    tdee = self.calculate_tdee(bmr, user_profile['activity_level'])
    target_calories = self.get_weight_loss_calories(tdee)
    
    # Get preferences
    dietary = user_profile.get('dietary_preference', 'mixed')
    budget = user_profile.get('budget_range', 'medium')
    cuisine = user_profile.get('preferred_cuisine', 'indian')
    
    # OPTIMIZED PROMPT - Structured & Personalized
    prompt = f"""You are an expert nutritionist and fitness coach specializing in Indian dietary patterns. Create a personalized weight loss plan.

**USER PROFILE:**
- Age: {age} years | Gender: {user_profile['gender']} | BMI: {bmi:.1f} (Overweight)
- Current Weight: {user_profile['weight_kg']:.1f} kg | Height: {user_profile['height_cm']:.0f} cm
- Activity: {user_profile['activity_level']} | Dietary: {dietary.capitalize()}
- Budget: {budget.capitalize()} | Cuisine: {cuisine.capitalize()}

**CALORIC TARGETS:**
- BMR: {bmr:.0f} kcal (resting metabolism)
- TDEE: {tdee:.0f} kcal (daily expenditure)
- Target: {target_calories:.0f} kcal (500 kcal deficit for 0.5 kg/week loss)

**TASK:** Generate a structured daily plan in STRICT JSON format:

{{
  "calorie_breakdown": {{
    "breakfast": "400 kcal",
    "lunch": "600 kcal",
    "dinner": "600 kcal",
    "snacks": "274 kcal"
  }},
  "macros": {{
    "protein_grams": "140g (30% - muscle preservation)",
    "carbs_grams": "216g (46% - energy)",
    "fat_grams": "50g (24% - hormones)"
  }},
  "foods": [
    "Moong dal cheela (2 pieces) - high protein breakfast",
    "Brown rice with rajma (1 cup) - fiber-rich lunch",
    "Palak paneer (150g) with 2 rotis - iron & calcium",
    "Curd (200g) with cucumber - probiotics",
    "Roasted chana (30g) - protein snack"
  ],
  "exercise": [
    "Brisk walking 40 mins (burns ~200 kcal) - every morning",
    "Bodyweight squats 3×15 + push-ups 3×10 - Mon/Wed/Fri",
    "Yoga/stretching 20 mins - Tue/Thu for flexibility"
  ],
  "weekly_goal": "Lose 0.5-0.75 kg (safe rate). Track weight every Sunday morning. Increase protein if hungry.",
  "tips": [
    "Drink 3L water daily to reduce false hunger",
    "Avoid fried snacks - bake or air-fry instead",
    "Meal prep on Sundays to stay on budget"
  ]
}}

**CONSTRAINTS:**
- Use ONLY whole, minimally processed {dietary} {cuisine} foods
- Keep costs within {budget} budget (mention affordable alternatives)
- Ensure adequate protein (1.6g/kg bodyweight) to prevent muscle loss
- NO liquid calories (juices, sodas)
- Focus on satiety (high fiber, protein, water-rich foods)

Output ONLY valid JSON. No markdown, no explanations outside JSON."""

    try:
        # Configure for structured output
        generation_config = {
            "temperature": 0.3,  # Lower = more consistent
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Parse JSON response
        import json
        import re
        
        # Clean response text
        response_text = response.text.strip()
        
        # Extract JSON if wrapped in markdown
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        
        parsed_recommendations = json.loads(response_text)
        
        return {
            'bmr': round(bmr),
            'tdee': round(tdee),
            'target_calories': round(target_calories),
            'bmi': round(bmi, 1),
            'recommendations': parsed_recommendations,  # Now structured!
            'preferences': {
                'dietary': dietary,
                'budget': budget,
                'cuisine': cuisine
            },
            'status': 'success'
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {str(e)}\nResponse: {response.text}")
        return {
            'bmr': round(bmr),
            'tdee': round(tdee),
            'target_calories': round(target_calories),
            'bmi': round(bmi, 1),
            'recommendations': {
                'error': 'AI returned invalid format',
                'raw_text': response.text
            },
            'status': 'parse_error'
        }
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return {
            'bmr': round(bmr),
            'tdee': round(tdee),
            'target_calories': round(target_calories),
            'bmi': round(bmi, 1),
            'recommendations': {
                'error': f'Unable to generate recommendations: {str(e)}'
            },
            'status': 'error',
            'error': str(e)
        }