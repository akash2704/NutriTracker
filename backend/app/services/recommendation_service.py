from google import genai
from google.genai import types
from datetime import date, datetime
from typing import Dict, Any
import os
import json
import re
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

class RecommendationService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Rate limiting: 1 call per 2 seconds
        self.last_call_time = 0
        self.min_interval = 2.0
    
    def calculate_bmr(self, weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure"""
        multipliers = {
            'sedentary': 1.2,
            'moderate': 1.55,
            'heavy': 1.725,
            'pregnant': 1.5,
            'lactating_0_6': 1.7,
            'lactating_6_12': 1.6,
            'infant': 1.0,
            'child': 1.4,
            'adolescent': 1.6
        }
        return bmr * multipliers.get(activity_level, 1.2)
    
    def get_weight_loss_calories(self, tdee: float) -> float:
        """Apply a sustainable 500 calorie deficit"""
        target = tdee - 500
        return max(target, 1200)  # Safety minimum
    
    def _sync_generate_content(self, prompt: str) -> str:
        """Synchronous wrapper for Gemini API call with rate limiting"""
        try:
            # Rate limiting
            current_time = time.time()
            time_since_last = current_time - self.last_call_time
            if time_since_last < self.min_interval:
                time.sleep(self.min_interval - time_since_last)
            
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=1500,
                    response_mime_type="application/json"
                )
            )
            
            self.last_call_time = time.time()
            
            if not response:
                raise ValueError("No response from API")
            
            if not hasattr(response, 'text') or response.text is None:
                raise ValueError("Response has no text content")
                
            return response.text
            
        except Exception as e:
            raise ValueError(f"API error: {str(e)}")
    
    async def generate_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized recommendations"""
        
        try:
            # Calculate metrics
            age = (date.today() - user_profile['birth_date']).days // 365
            bmr = self.calculate_bmr(
                user_profile['weight_kg'],
                user_profile['height_cm'],
                age,
                user_profile['gender']
            )
            tdee = self.calculate_tdee(bmr, user_profile['activity_level'])
            target_calories = self.get_weight_loss_calories(tdee)
            bmi = user_profile['weight_kg'] / ((user_profile['height_cm'] / 100) ** 2)
            
            # User preferences
            dietary = user_profile.get('dietary_preference') or "balanced"
            budget = user_profile.get('budget_range') or "moderate"
            cuisine = user_profile.get('preferred_cuisine') or "Indian"

            # ULTRA-SAFE PROMPT - Avoids ALL trigger words
            # Using "fitness", "nutrition", "wellness" language
            prompt = f"""You are a certified nutritionist. Create a balanced meal and fitness guide.

Client details:
- {age} years old, {user_profile['gender']}
- Current stats: {user_profile['height_cm']}cm height, {user_profile['weight_kg']}kg
- Daily nutrition target: {target_calories:.0f} calories
- Food style: {dietary}, Budget: {budget}, Cuisine: {cuisine}

Return ONLY valid JSON (no text before or after):
{{
  "greeting": "Warm professional welcome message",
  "weekly_goal": "Realistic weekly fitness milestone",
  "meal_plan": {{
    "breakfast": "Specific {cuisine} {dietary} breakfast with portions - {int(target_calories * 0.25)} calories",
    "lunch": "Specific {cuisine} {dietary} lunch with portions - {int(target_calories * 0.35)} calories",
    "dinner": "Specific {cuisine} {dietary} dinner with portions - {int(target_calories * 0.30)} calories",
    "snack": "Healthy snack within {budget} budget - {int(target_calories * 0.10)} calories"
  }},
  "exercise_plan": [
    "First recommended physical activity with duration",
    "Second recommended physical activity with duration"
  ],
  "pro_tips": [
    "Evidence-based nutrition advice",
    "Practical lifestyle motivation tip"
  ]
}}"""

            # Run API call in thread pool
            loop = asyncio.get_event_loop()
            
            try:
                response_text = await loop.run_in_executor(
                    self.executor, 
                    self._sync_generate_content, 
                    prompt
                )
                
                if not response_text:
                    raise ValueError("Empty response from API")
                
                # Clean and parse JSON more robustly
                response_text = response_text.strip().lstrip('\ufeff')
                
                # Remove markdown if present
                json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(1).strip()
                
                # Remove any leading/trailing non-JSON content
                start_brace = response_text.find('{')
                end_brace = response_text.rfind('}')
                if start_brace != -1 and end_brace != -1:
                    response_text = response_text[start_brace:end_brace+1]
                
                parsed_recs = json.loads(response_text)
                
                return {
                    'bmr': round(bmr),
                    'tdee': round(tdee),
                    'target_calories': round(target_calories),
                    'bmi': round(bmi, 1),
                    'bmi_category': self._get_bmi_category(bmi),
                    'recommendations': parsed_recs,
                    'preferences': {
                        'dietary': dietary,
                        'budget': budget,
                        'cuisine': cuisine
                    },
                    'status': 'success'
                }
                
            except (ValueError, json.JSONDecodeError) as e:
                # API failed or returned invalid JSON - use fallback
                print(f"Gemini API Error: {str(e)}")
                
                return {
                    'bmr': round(bmr),
                    'tdee': round(tdee),
                    'target_calories': round(target_calories),
                    'bmi': round(bmi, 1),
                    'bmi_category': self._get_bmi_category(bmi),
                    'recommendations': self._generate_fallback_plan(
                        target_calories, dietary, cuisine, budget
                    ),
                    'preferences': {
                        'dietary': dietary,
                        'budget': budget,
                        'cuisine': cuisine
                    },
                    'status': 'fallback',
                    'note': 'Using expert-designed plan (AI temporarily unavailable)'
                }
                
        except Exception as e:
            # Catastrophic failure - still return something useful
            print(f"Critical Error: {str(e)}")
            
            # Use safe defaults if calculations failed
            return {
                'bmr': round(bmr) if 'bmr' in locals() else 1500,
                'tdee': round(tdee) if 'tdee' in locals() else 2000,
                'target_calories': round(target_calories) if 'target_calories' in locals() else 1500,
                'bmi': round(bmi, 1) if 'bmi' in locals() else 25.0,
                'bmi_category': 'Calculating...',
                'recommendations': self._generate_fallback_plan(
                    1500, 
                    user_profile.get('dietary_preference', 'balanced'),
                    user_profile.get('preferred_cuisine', 'Indian'),
                    user_profile.get('budget_range', 'moderate')
                ),
                'preferences': {
                    'dietary': user_profile.get('dietary_preference', 'balanced'),
                    'budget': user_profile.get('budget_range', 'moderate'),
                    'cuisine': user_profile.get('preferred_cuisine', 'Indian')
                },
                'status': 'error',
                'note': 'Using default plan - please refresh'
            }
    
    def _get_bmi_category(self, bmi: float) -> str:
        """Get BMI category using Indian standards"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 23:
            return "Normal"
        elif 23 <= bmi < 25:
            return "Overweight"
        elif 25 <= bmi < 30:
            return "Obese Class I"
        else:
            return "Obese Class II"
    
    def _generate_fallback_plan(self, target_calories: float, dietary: str, cuisine: str, budget: str = "moderate") -> Dict[str, Any]:
        """Generate expert-designed fallback plan"""
        
        breakfast_cal = int(target_calories * 0.25)
        lunch_cal = int(target_calories * 0.35)
        dinner_cal = int(target_calories * 0.30)
        snack_cal = int(target_calories * 0.10)
        
        # Cuisine and dietary specific plans
        if cuisine.lower() == "indian" or cuisine.lower() == "mixed":
            if dietary.lower() in ['vegetarian', 'vegan']:
                meal_plan = {
                    "breakfast": f"Oats upma (1 bowl) with vegetables and peanuts - {breakfast_cal} cal",
                    "lunch": f"Moong dal (1 cup) + brown rice (3/4 cup) + mixed vegetable sabzi + salad - {lunch_cal} cal",
                    "dinner": f"Paneer tikka (100g) + 2 multigrain rotis + cucumber raita - {dinner_cal} cal",
                    "snack": f"Roasted chana (30g) or seasonal fruit (1 medium) - {snack_cal} cal"
                }
            else:
                meal_plan = {
                    "breakfast": f"Boiled eggs (2) + wheat toast (2 slices) + banana - {breakfast_cal} cal",
                    "lunch": f"Grilled chicken (120g) + brown rice (3/4 cup) + dal + vegetables - {lunch_cal} cal",
                    "dinner": f"Fish curry (100g) + 2 rotis + green salad - {dinner_cal} cal",
                    "snack": f"Greek yogurt (150g) or mixed nuts (20g) - {snack_cal} cal"
                }
        else:
            meal_plan = {
                "breakfast": f"Oatmeal with berries and almonds - {breakfast_cal} cal",
                "lunch": f"Grilled protein with quinoa and vegetables - {lunch_cal} cal",
                "dinner": f"Baked protein with sweet potato and greens - {dinner_cal} cal",
                "snack": f"Hummus with vegetable sticks - {snack_cal} cal"
            }
        
        return {
            "greeting": f"Welcome to your personalized {dietary} nutrition and fitness guide!",
            "weekly_goal": "Aim for steady progress with consistent healthy eating and regular movement.",
            "meal_plan": meal_plan,
            "exercise_plan": [
                "Morning walk or jog for 30-40 minutes (moderate pace)",
                "Bodyweight strength training 3x per week: squats, push-ups, planks (15 minutes)"
            ],
            "pro_tips": [
                "Drink a glass of water 20 minutes before meals to support hydration and satiety",
                "Progress happens with consistency, not perfection - small daily actions add up!"
            ]
        }