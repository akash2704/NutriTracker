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
        
        # You are correct to use a free-tier model. 'gemini-1.5-flash' is perfect for this.
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={
                "temperature": 0.5, # Slightly higher temp for more creative meal ideas
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,
                "response_mime_type": "application/json" # We are telling the model to output JSON!
            }
        )
    
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
            'heavy': 1.725
        }
        # Fallback to sedentary if activity level is somehow not matching
        return bmr * multipliers.get(activity_level, 1.2)
    
    def get_weight_loss_calories(self, tdee: float) -> float:
        """Apply a sustainable 500 calorie deficit for weight loss."""
        return tdee - 500
    
    async def generate_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates personalized diet and exercise recommendations
        based on the user's complete profile.
        """
        
        age = (date.today() - user_profile['birth_date']).days // 365
        bmr = self.calculate_bmr(
            user_profile['weight_kg'],
            user_profile['height_cm'],
            age,
            user_profile['gender']
        )
        tdee = self.calculate_tdee(bmr, user_profile['activity_level'])
        weight_loss_calories = self.get_weight_loss_calories(tdee)
        
        bmi = user_profile['weight_kg'] / ((user_profile['height_cm'] / 100) ** 2)
        
        # User preferences
        dietary = user_profile.get('dietary_preference') or "balanced"
        budget = user_profile.get('budget_range') or "moderate"
        cuisine = user_profile.get('preferred_cuisine') or "Indian"

        # --- THIS IS THE NEW "GREAT" PROMPT ---
        # It's highly specific, demands JSON, and matches your frontend.
        
        prompt = f"""
        You are NutriCoach, an expert Indian nutritionist and motivational coach.
        
        My User's Profile:
        - Age: {age}
        - Gender: {user_profile['gender']}
        - BMI: {bmi:.1f} (Weight: {user_profile['weight_kg']}kg, Height: {user_profile['height_cm']}cm)
        - Goal: Weight Loss
        - Daily Calorie Target: {weight_loss_calories:.0f} kcal (which is TDEE {tdee:.0f} - 500)
        - Preferences: {dietary}, {budget} budget, {cuisine} cuisine.

        Your Task:
        Generate an actionable and encouraging plan. You MUST respond ONLY with a single, valid JSON object.
        Do NOT wrap the JSON in ```json markdown.
        
        Use this exact JSON structure:
        {{
          "greeting": "A short, encouraging welcome message for the user.",
          "weekly_goal": "A simple, clear goal for the week (e.g., 'Aim for 0.5kg to 1kg of weight loss this week by staying consistent.')",
          "meal_plan": {{
            "breakfast": "A {cuisine} {dietary} breakfast idea, fitting the calories (~300-400 kcal). Be specific, e.g., '2 Besan Chillas with 1 cup Curd'.",
            "lunch": "A {cuisine} {dietary} lunch idea, fitting the calories (~400-500 kcal). e.g., '1 bowl Rajma + 1 cup Brown Rice + Salad'.",
            "dinner": "A {cuisine} {dietary} dinner idea, fitting the calories (~400-500 kcal). e.g., '150g Grilled Paneer Tikka + Sautéed Veg'.",
            "snack": "A healthy, {budget}-friendly snack idea (~150-200 kcal). e.g., 'A handful of roasted chana or an apple'."
          }},
          "exercise_plan": [
            "A simple, actionable exercise for today (e.g., '30-minute brisk walk in your neighborhood.')",
            "Another exercise recommendation (e.g., '15 minutes of bodyweight squats and lunges at home.')"
          ],
          "pro_tips": [
            "A key pro-tip about hydration or meal timing (e.g., 'Drink a full glass of water 20 minutes before each meal.')",
            "A motivational tip to stay on track (e.g., 'Don't worry about one bad meal! Consistency is what matters most.')"
          ]
        }}
        """
        
        try:
            # We explicitly ask for a JSON response, which gemini-1.5-flash supports.
            # The model will follow the structure in the prompt.
            response = self.model.generate_content(prompt)
            
            # The response.text *is* the JSON string
            return {
                'bmr': round(bmr),
                'tdee': round(tdee),
                'target_calories': round(weight_loss_calories),
                'bmi': round(bmi, 1),
                'recommendations': response.text, # This is now a JSON string
                'preferences': {
                    'dietary': dietary,
                    'budget': budget,
                    'cuisine': cuisine
                },
                'status': 'success'
            }
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            return {
                'bmr': round(bmr),
                'tdee': round(tdee),
                'target_calories': round(weight_loss_calories),
                'bmi': round(bmi, 1),
                'recommendations': f'{{"error": "Unable to generate AI recommendations. Please try again later."}}',
                'status': 'error',
                'preferences': {
                    'dietary': dietary,
                    'budget': budget,
                    'cuisine': cuisine
                }
            }