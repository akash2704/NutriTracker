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
        self.model = genai.GenerativeModel('gemini-pro')
    
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
        
        # Calculate user's age
        birth_date = user_profile['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Calculate BMI
        height_m = user_profile['height_cm'] / 100
        bmi = user_profile['weight_kg'] / (height_m ** 2)
        
        # Calculate calorie needs
        bmr = self.calculate_bmr(
            user_profile['weight_kg'], 
            user_profile['height_cm'], 
            age, 
            user_profile['gender']
        )
        tdee = self.calculate_tdee(bmr, user_profile['activity_level'])
        weight_loss_calories = self.get_weight_loss_calories(tdee)
        
        # Get preferences
        dietary = user_profile.get('dietary_preference', 'mixed')
        budget = user_profile.get('budget_range', 'medium')
        cuisine = user_profile.get('preferred_cuisine', 'indian')
        
        # Create shorter, focused prompt for faster response
        prompt = f"""Create a weight loss plan for a {age}yr old {user_profile['gender']} (BMI: {bmi:.1f}, {dietary}, {budget} budget, likes {cuisine} food).
        
Target: {weight_loss_calories:.0f} calories/day

Provide ONLY:
1. Daily meal calories: breakfast/lunch/dinner/snacks
2. Macros: protein/carbs/fats in grams  
3. 5 specific {dietary} {cuisine} foods
4. 3 simple exercises
5. Weekly weight loss target

Keep response under 200 words, focus on {cuisine} cuisine."""
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                'bmr': round(bmr),
                'tdee': round(tdee),
                'target_calories': round(weight_loss_calories),
                'bmi': round(bmi, 1),
                'recommendations': response.text,
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
                'recommendations': f'Unable to generate AI recommendations. Error: {str(e)}',
                'status': 'error',
                'error': str(e)
            }
