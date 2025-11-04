import re
import csv
import json
import openpyxl
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models import (
    Nutrient, FoodCategory, Food, FoodNutrient, 
    DemographicGroup, RDA, Base, 
    GenderEnum, ActivityLevelEnum
)
# from data.pdf_extractor import NINDataExtractor, NIN_PDF_PATH  <- REMOVED

# --- DEFINE ALL DATA SOURCE PATHS ---
DATA_DIR = Path(__file__).parent / "data"
# Level 1: Raw Foods (from the CSV you found)
IFCT_CSV_PATH = DATA_DIR / "IFCT_2017.csv" # <-- UPDATED
# Level 3: Branded Foods (your XLSX)
INDB_XLSX_PATH = DATA_DIR / "Anuvaad_INDB_2024.11.xlsx"


# --- 1. SEED NUTRIENTS (Lookup Table) ---
# UPDATED based on the rich data from the IFCT CSV
NUTRIENTS_LIST = [
    # Primary Macros
    {"name": "Energy", "unit": "kcal"},
    {"name": "Protein", "unit": "g"},
    {"name": "Carbohydrate", "unit": "g"},
    {"name": "Fat", "unit": "g"}, # Generic total fat
    {"name": "Visible Fat", "unit": "g"}, # For RDA
    {"name": "Fibre", "unit": "g"},
    {"name": "Free Sugar", "unit": "g"},
    
    # Minerals
    {"name": "Calcium", "unit": "mg"},
    {"name": "Iron", "unit": "mg"},
    {"name": "Magnesium", "unit": "mg"},
    {"name": "Phosphorus", "unit": "mg"},
    {"name": "Potassium", "unit": "mg"},
    {"name": "Sodium", "unit": "mg"},
    {"name": "Zinc", "unit": "mg"},
    {"name": "Copper", "unit": "mg"},
    {"name": "Manganese", "unit": "mg"},
    {"name": "Molybdenum", "unit": "mg"},
    {"name": "Selenium", "unit": "µg"},
    {"name": "Chromium", "unit": "mg"},
    
    # Vitamins (Raw)
    {"name": "Vitamin A (Retinol)", "unit": "µg"}, 
    {"name": "Beta-Carotene", "unit": "µg"}, 
    {"name": "Vitamin C", "unit": "mg"}, 
    {"name": "Vitamin D2", "unit": "µg"},
    {"name": "Vitamin D3", "unit": "µg"},
    {"name":"Vitamin E", "unit": "mg"},
    {"name": "Vitamin K1", "unit": "µg"},
    {"name": "Vitamin K2", "unit": "µg"},
    {"name": "Folic Acid", "unit": "µg"}, 
    {"name": "Thiamin", "unit": "mg"}, 
    {"name": "Riboflavin", "unit": "mg"}, 
    {"name": "Niacin", "unit": "mg"}, 
    {"name": "Vitamin B5", "unit": "mg"},
    {"name": "Pyridoxin", "unit": "mg"}, 
    {"name": "Vitamin B7", "unit": "µg"},
    {"name": "Vitamin B12", "unit": "µg"},
    
    # Fats (Raw)
    {"name": "Cholesterol", "unit": "mg"},
    {"name": "Saturated Fat (SFA)", "unit": "mg"},
    {"name": "Monounsaturated Fat (MUFA)", "unit": "mg"},
    {"name": "Polyunsaturated Fat (PUFA)", "unit": "mg"},
    
    # --- NEW CALCULATED/AGGREGATE NUTRIENTS ---
    # These are what we will calculate and store
    {"name": "Total Vitamin A (RAE)", "unit": "µg"},
    {"name": "Total Vitamin D", "unit": "µg"},
    {"name": "Total Vitamin K", "unit": "µg"},
    {"name": "Total Tocopherols (Vitamin E)", "unit": "mg"},
    {"name": "Total Carotenoids", "unit": "µg"},
    {"name": "Total Unsaturated Fat", "unit": "g"},
    {"name": "Total Essential Amino Acids", "unit": "g"},
    {"name": "Total Non-Essential Amino Acids", "unit": "g"},
    {"name": "Total Amino Acids", "unit": "g"},
    {"name": "Total Organic Acids", "unit": "g"},
    {"name": "Phytate", "unit": "mg"},
    {"name": "Saponins", "unit": "mg"},
]

def seed_nutrients(db: Session):
    print("Seeding nutrients...")
    nutrient_map = {}
    for item in NUTRIENTS_LIST:
        db_nutrient = db.query(Nutrient).filter_by(name=item["name"]).first()
        if not db_nutrient:
            db_nutrient = Nutrient(name=item["name"], unit=item["unit"])
            db.add(db_nutrient)
            # print(f"  Adding Nutrient: {item['name']}") # Too verbose now
        nutrient_map[item["name"]] = db_nutrient
    db.commit()
    print(f"✅ Nutrients seeded/updated. Total: {len(nutrient_map)}")
    return nutrient_map

# --- 2. SEED DEMOGRAPHIC GROUPS (Lookup Table) ---
DEMOGRAPHIC_GROUPS_LIST = [
    {"name": "Man - Sedentary", "gender": GenderEnum.male, "activity_level": ActivityLevelEnum.sedentary, "age_min_years": 19, "age_max_years": 100},
    {"name": "Man - Moderate", "gender": GenderEnum.male, "activity_level": ActivityLevelEnum.moderate, "age_min_years": 19, "age_max_years": 100},
    {"name": "Man - Heavy", "gender": GenderEnum.male, "activity_level": ActivityLevelEnum.heavy, "age_min_years": 19, "age_max_years": 100},
    {"name": "Woman - Sedentary", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.sedentary, "age_min_years": 19, "age_max_years": 100},
    {"name": "Woman - Moderate", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.moderate, "age_min_years": 19, "age_max_years": 100},
    {"name": "Woman - Heavy", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.heavy, "age_min_years": 19, "age_max_years": 100},
    {"name": "Pregnant woman", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.pregnant, "age_min_years": 19, "age_max_years": 50},
    {"name": "Lactation 0-6 months", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.lactating_0_6, "age_min_years": 19, "age_max_years": 50},
    {"name": "Lactation 6-12 months", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.lactating_6_12, "age_min_years": 19, "age_max_years": 50},
    {"name": "Infants 0-6 months", "gender": None, "activity_level": ActivityLevelEnum.infant, "age_min_years": 0, "age_max_years": 0.5},
    {"name": "Infants 6-12 months", "gender": None, "activity_level": ActivityLevelEnum.infant, "age_min_years": 0.5, "age_max_years": 1},
    {"name": "Children 1-3 years", "gender": None, "activity_level": ActivityLevelEnum.child, "age_min_years": 1, "age_max_years": 3},
    {"name": "Children 4-6 years", "gender": None, "activity_level": ActivityLevelEnum.child, "age_min_years": 4, "age_max_years": 6},
    {"name": "Children 7-9 years", "gender": None, "activity_level": ActivityLevelEnum.child, "age_min_years": 7, "age_max_years": 9},
    {"name": "Boys 10-12 years", "gender": GenderEnum.male, "activity_level": ActivityLevelEnum.adolescent, "age_min_years": 10, "age_max_years": 12},
    {"name": "Girls 10-12 years", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.adolescent, "age_min_years": 10, "age_max_years": 12},
    {"name": "Boys 13-15 years", "gender": GenderEnum.male, "activity_level": ActivityLevelEnum.adolescent, "age_min_years": 13, "age_max_years": 15},
    {"name": "Girls 13-15 years", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.adolescent, "age_min_years": 13, "age_max_years": 15},
    {"name": "Boys 16-17 years", "gender": GenderEnum.male, "activity_level": ActivityLevelEnum.adolescent, "age_min_years": 16, "age_max_years": 17},
    {"name": "Girls 16-17 years", "gender": GenderEnum.female, "activity_level": ActivityLevelEnum.adolescent, "age_min_years": 16, "age_max_years": 17},
]
def seed_demographic_groups(db: Session):
    print("Seeding demographic groups...")
    group_map = {}
    for item in DEMOGRAPHIC_GROUPS_LIST:
        db_group = db.query(DemographicGroup).filter_by(name=item["name"]).first()
        if not db_group:
            db_group = DemographicGroup(**item)
            db.add(db_group)
        group_map[item["name"]] = db_group
    db.commit()
    print("✅ Demographic groups seeded.")
    return group_map

# --- 3. SEED RDA (The "Goal" Data) ---
RDA_DATA_MAP = {
    # We use our hard-coded NIN data, not the global 'intake.csv'
    "Man - Sedentary": [("Energy", 2320), ("Protein", 60), ("Visible Fat", 25), ("Calcium", 600), ("Iron", 17), ("Total Vitamin A (RAE)", 600), ("Thiamin", 1.2), ("Riboflavin", 1.4), ("Niacin", 16), ("Pyridoxin", 2.0), ("Vitamin C", 40), ("Folic Acid", 200), ("Vitamin B12", 1), ("Magnesium", 340), ("Zinc", 12)],
    "Man - Moderate": [("Energy", 2730), ("Protein", 60), ("Visible Fat", 30), ("Calcium", 600), ("Iron", 17), ("Thiamin", 1.4), ("Riboflavin", 1.6), ("Niacin", 18)],
    "Man - Heavy": [("Energy", 3490), ("Protein", 60), ("Visible Fat", 40), ("Calcium", 600), ("Iron", 17), ("Thiamin", 1.7), ("Riboflavin", 2.1), ("Niacin", 21)],
    "Woman - Sedentary": [("Energy", 1900), ("Protein", 55), ("Visible Fat", 20), ("Calcium", 600), ("Iron", 21), ("Total Vitamin A (RAE)", 600), ("Thiamin", 1.0), ("Riboflavin", 1.1), ("Niacin", 12), ("Pyridoxin", 2.0), ("Vitamin C", 40), ("Folic Acid", 200), ("Vitamin B12", 1), ("Magnesium", 310), ("Zinc", 10)],
    "Woman - Moderate": [("Energy", 2230), ("Protein", 55), ("Visible Fat", 25), ("Calcium", 600), ("Iron", 21), ("Thiamin", 1.1), ("Riboflavin", 1.3), ("Niacin", 14)],
    "Woman - Heavy": [("Energy", 2850), ("Protein", 55), ("Visible Fat", 30), ("Calcium", 600), ("Iron", 21), ("Thiamin", 1.4), ("Riboflavin", 1.7), ("Niacin", 16)],
    "Pregnant woman": [("Energy", 2250), ("Protein", 78), ("Visible Fat", 30), ("Calcium", 1200), ("Iron", 35), ("Total Vitamin A (RAE)", 800), ("Thiamin", 1.2), ("Riboflavin", 1.4), ("Niacin", 14), ("Pyridoxin", 2.5), ("Vitamin C", 60), ("Folic Acid", 500), ("Vitamin B12", 1.2), ("Magnesium", 310), ("Zinc", 12)],
    "Lactation 0-6 months": [("Energy", 2400), ("Protein", 74), ("Visible Fat", 30), ("Calcium", 1200), ("Iron", 21), ("Total Vitamin A (RAE)", 950), ("Thiamin", 1.3), ("Riboflavin", 1.5), ("Niacin", 16), ("Pyridoxin", 2.5), ("Vitamin C", 80), ("Folic Acid", 300), ("Vitamin B12", 1.5), ("Magnesium", 310), ("Zinc", 12)],
    "Lactation 6-12 months": [("Energy", 2420), ("Protein", 68), ("Visible Fat", 30), ("Calcium", 1200), ("Iron", 21), ("Total Vitamin A (RAE)", 950), ("Thiamin", 1.2), ("Riboflavin", 1.4), ("Niacin", 15), ("Pyridoxin", 2.5), ("Vitamin C", 80), ("Folic Acid", 300), ("Vitamin B12", 1.5), ("Magnesium", 310), ("Zinc", 12)],
    "Infants 0-6 months": [("Energy", 92*5.4), ("Protein", 1.16*5.4), ("Visible Fat", 19), ("Calcium", 500), ("Iron", 5), ("Thiamin", 0.2), ("Riboflavin", 0.3), ("Niacin", 710), ("Pyridoxin", 0.1), ("Vitamin C", 25), ("Folic Acid", 25), ("Vitamin B12", 0.2), ("Magnesium", 30)],
    "Infants 6-12 months": [("Energy", 80*8.4), ("Protein", 1.69*8.4), ("Visible Fat", 19), ("Calcium", 500), ("Iron", 5), ("Thiamin", 0.3), ("Riboflavin", 0.4), ("Niacin", 650), ("Pyridoxin", 0.4), ("Vitamin C", 25), ("Folic Acid", 25), ("Vitamin B12", 0.2), ("Magnesium", 45)],
    "Children 1-3 years": [("Energy", 1060), ("Protein", 16.7), ("Visible Fat", 27), ("Calcium", 600), ("Iron", 9), ("Thiamin", 0.5), ("Riboflavin", 0.6), ("Niacin", 8), ("Pyridoxin", 0.9), ("Vitamin C", 40), ("Folic Acid", 80), ("Vitamin B12", 0.2-1.0), ("Magnesium", 50), ("Zinc", 5)],
    "Children 4-6 years": [("Energy", 1350), ("Protein", 20.1), ("Visible Fat", 25), ("Calcium", 600), ("Iron", 13), ("Thiamin", 0.7), ("Riboflavin", 0.8), ("Niacin", 11), ("Pyridoxin", 0.9), ("Vitamin C", 40), ("Folic Acid", 100), ("Magnesium", 70), ("Zinc", 7)],
    "Children 7-9 years": [("Energy", 1690), ("Protein", 29.5), ("Visible Fat", 30), ("Calcium", 600), ("Iron", 16), ("Thiamin", 0.8), ("Riboflavin", 1.0), ("Niacin", 13), ("Pyridoxin", 1.6), ("Vitamin C", 40), ("Folic Acid", 120), ("Magnesium", 100), ("Zinc", 8)],
    "Boys 10-12 years": [("Energy", 2190), ("Protein", 39.9), ("Visible Fat", 35), ("Calcium", 800), ("Iron", 21), ("Thiamin", 1.1), ("Riboflavin", 1.3), ("Niacin", 15), ("Pyridoxin", 1.6), ("Vitamin C", 40), ("Folic Acid", 140), ("Magnesium", 120), ("Zinc", 9)],
    "Girls 10-12 years": [("Energy", 2010), ("Protein", 40.4), ("Visible Fat", 35), ("Calcium", 800), ("Iron", 27), ("Thiamin", 1.0), ("Riboflavin", 1.2), ("Niacin", 13), ("Pyridoxin", 1.6), ("Vitamin C", 40), ("Folic Acid", 160), ("Magnesium", 120), ("Zinc", 9)],
    "Boys 13-15 years": [("Energy", 2750), ("Protein", 54.3), ("Visible Fat", 45), ("Calcium", 800), ("Iron", 32), ("Thiamin", 1.4), ("Riboflavin", 1.6), ("Niacin", 16), ("Pyridoxin", 2.0), ("Vitamin C", 40), ("Folic Acid", 150), ("Magnesium", 165), ("Zinc", 11)],
    "Girls 13-15 years": [("Energy", 2330), ("Protein", 51.9), ("Visible Fat", 40), ("Calcium", 800), ("Iron", 27), ("Thiamin", 1.2), ("Riboflavin", 1.4), ("Niacin", 14), ("Pyridoxin", 2.0), ("Vitamin C", 40), ("Folic Acid", 210), ("Magnesium", 165), ("Zinc", 11)],
    "Boys 16-17 years": [("Energy", 3020), ("Protein", 61.5), ("Visible Fat", 50), ("Calcium", 800), ("Iron", 28), ("Thiamin", 1.5), ("Riboflavin", 1.8), ("Niacin", 17), ("Pyridoxin", 2.0), ("Vitamin C", 40), ("Folic Acid", 200), ("Magnesium", 195), ("Zinc", 12)],
    "Girls 16-17 years": [("Energy", 2440), ("Protein", 55.5), ("Visible Fat", 35), ("Calcium", 800), ("Iron", 26), ("Thiamin", 1.0), ("Riboflavin", 1.2), ("Niacin", 14), ("Pyridoxin", 2.0), ("Vitamin C", 40), ("Folic Acid", 235), ("Magnesium", 195), ("Zinc", 12)],
}
def seed_rda(db: Session, group_map: dict, nutrient_map: dict):
    print("Seeding RDA data...")
    for group_name, nutrients in RDA_DATA_MAP.items():
        demographic_group = group_map.get(group_name)
        if not demographic_group: continue
        
        for nutrient_name, value in nutrients:
            nutrient = nutrient_map.get(nutrient_name)
            if not nutrient:
                print(f"  Skipping RDA for unknown nutrient: {nutrient_name}")
                continue
            
            db_rda = db.query(RDA).filter_by(
                demographic_group_id=demographic_group.id,
                nutrient_id=nutrient.id
            ).first()
            
            if not db_rda:
                db_rda = RDA(
                    demographic_group_id=demographic_group.id,
                    nutrient_id=nutrient.id,
                    recommended_value=value
                )
                db.add(db_rda)
    
    db.commit()
    print("✅ RDA data seeded.")


# --- 4. SEED FOOD CATEGORIES ---
# SIMPLIFIED based on your request
FOOD_CATEGORIES_LIST = [
    "Raw Ingredients (IFCT)",
    "Branded Foods (INDB)",
    # "Cooked Preparations (NIN)" <-- REMOVED
]

def seed_food_categories(db: Session):
    print("Seeding food categories...")
    category_map = {}
    for cat_name in FOOD_CATEGORIES_LIST:
        db_cat = db.query(FoodCategory).filter_by(name=cat_name).first()
        if not db_cat:
            db_cat = FoodCategory(name=cat_name)
            db.add(db_cat)
            print(f"  Adding Category: {cat_name}")
        category_map[cat_name] = db_cat
    db.commit()
    print("✅ Food categories seeded.")
    return category_map

# --- 5. Level 1 Seeder (CSV) ---

# This helper function safely converts CSV values to float
def get_val(row, key, default=0.0):
    try:
        val = row.get(key)
        if val is None or val == 'NaN' or val == '':
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

# This maps our DB Nutrient Names to the CSV Headers from the JS Doc
IFCT_HEADER_MAP = {
    "Energy": "enerc",
    "Protein": "protcnt",
    "Fat": "fatce",
    "Carbohydrate": "choavldf",
    "Fibre": "fibtg",
    "Free Sugar": "fsugar",
    "Calcium": "ca",
    "Iron": "fe",
    "Magnesium": "mg",
    "Phosphorus": "p",
    "Potassium": "k",
    "Sodium": "na",
    "Zinc": "zn",
    "Copper": "cu",
    "Manganese": "mn",
    "Molybdenum": "mo",
    "Selenium": "se",
    "Chromium": "cr",
    "Vitamin A (Retinol)": "retol",
    "Beta-Carotene": "cartb",
    "Vitamin C": "vitc",
    "Vitamin D2": "ergcal",
    "Vitamin D3": "chocal",
    "Vitamin E": "vite", # This is α-Tocopherol equivalent
    "Vitamin K1": "vitk1",
    "Vitamin K2": "vitk2",
    "Folic Acid": "folsum",
    "Thiamin": "thia",
    "Riboflavin": "ribf",
    "Niacin": "nia",
    "Vitamin B5": "pantac",
    "Pyridoxin": "vitb6c",
    "Vitamin B7": "biot",
    "Vitamin B12": "vitb", # Note: IFCT uses 'vitb' for B12
    "Cholesterol": "cholc",
    "Saturated Fat (SFA)": "fasat",
    "Monounsaturated Fat (MUFA)": "fams",
    "Polyunsaturated Fat (PUFA)": "fapu",
    "Phytate": "phytac",
    "Saponins": "sapon",
    
    # Raw values for calculation
    "raw_tocpha": "tocpha",
    "raw_tocphb": "tocphb",
    "raw_tocphg": "tocphg",
    "raw_tocphd": "tocphd",
    "raw_toctra": "toctra",
    "raw_toctrb": "toctrb",
    "raw_toctrg": "toctrg",
    "raw_toctrd": "toctrd",
    "raw_cartoid": "cartoid",
    "raw_fauns": "fauns",
    "raw_amiace": "amiace",
    "raw_amiacce": "amiacce",
    "raw_amiacne": "amiacne",
    "raw_amiac": "amiac",
    "raw_orgac": "orgac",
}

def seed_foods_from_ifct_csv(db: Session, category_map: dict, nutrient_map: dict):
    print(f"Seeding Level 1 foods from CSV: {IFCT_CSV_PATH}")
    
    category = category_map["Raw Ingredients (IFCT)"]
    food_count = 0
    nutrient_link_count = 0
    
    try:
        with open(IFCT_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader):
                food_name = row.get("name")
                if not food_name:
                    continue
                
                # 1. Create the food
                db_food = db.query(Food).filter_by(name=food_name).first()
                if not db_food:
                    db_food = Food(name=food_name, category_id=category.id)
                    db.add(db_food)
                    try:
                        db.commit()
                        db.refresh(db_food)
                        food_count += 1
                    except IntegrityError:
                        db.rollback()
                        print(f"  Could not add food: {food_name}")
                        continue
                
                # --- 2. CALCULATIONS (The "Make it Good" part) ---
                # This is where we add the formulas you asked for
                
                # Total Vitamin A (RAE in µg) = Retinol + (Beta-Carotene / 12)
                total_vit_a = get_val(row, 'retol') + (get_val(row, 'cartb') / 12)
                
                # Total Vitamin D (µg) = D2 + D3
                total_vit_d = get_val(row, 'ergcal') + get_val(row, 'chocal')
                
                # Total Vitamin K (µg) = K1 + K2
                total_vit_k = get_val(row, 'vitk1') + get_val(row, 'vitk2')
                
                # Total Tocopherols (Vitamin E in mg)
                total_tocph = get_val(row, 'tocpha') + get_val(row, 'tocphb') + get_val(row, 'tocphg') + get_val(row, 'tocphd')
                
                # Total Tocotrienols (mg)
                total_toctr = get_val(row, 'toctra') + get_val(row, 'toctrb') + get_val(row, 'toctrg') + get_val(row, 'toctrd')
                
                # Store all calculated values in a dict
                calculated_nutrients = {
                    "Total Vitamin A (RAE)": total_vit_a,
                    "Total Vitamin D": total_vit_d,
                    "Total Vitamin K": total_vit_k,
                    "Total Tocopherols (Vitamin E)": total_tocph + total_toctr, # Total Vit E
                    "Total Carotenoids": get_val(row, 'cartoid'),
                    "Total Unsaturated Fat": get_val(row, 'fauns') / 1000, # Convert mg to g
                    "Total Essential Amino Acids": get_val(row, 'amiace') / 1000, # Convert mg to g
                    "Total Non-Essential Amino Acids": get_val(row, 'amiacne') / 1000, # Convert mg to g
                    "Total Amino Acids": get_val(row, 'amiac') / 1000, # Convert mg to g
                    "Total Organic Acids": get_val(row, 'orgac') / 1000, # Convert mg to g
                }

                # --- 3. Link Nutrients (Raw + Calculated) ---
                
                # First, link all the raw, direct-mapped nutrients
                for nutrient_name, csv_header in IFCT_HEADER_MAP.items():
                    if "raw_" in nutrient_name: continue # Skip raw calculation values
                    
                    value = get_val(row, csv_header, default=None)
                    db_nutrient = nutrient_map.get(nutrient_name)
                    
                    if db_nutrient and value is not None:
                        link_nutrient(db, db_food.id, db_nutrient.id, value)
                        nutrient_link_count += 1
                
                # Second, link all the new, calculated nutrients
                for nutrient_name, value in calculated_nutrients.items():
                    db_nutrient = nutrient_map.get(nutrient_name)
                    if db_nutrient and value > 0:
                        link_nutrient(db, db_food.id, db_nutrient.id, value)
                        nutrient_link_count += 1

                if i % 100 == 0:
                    db.commit()
                    print(f"  Processed {i} CSV rows, added {food_count} new foods...")

        db.commit()
        print(f"✅ CSV Seeding Complete. Added {food_count} new foods and {nutrient_link_count} nutrient links.")
        
    except FileNotFoundError:
        print(f"❌ ERROR: CSV file not found at {IFCT_CSV_PATH}")
        print("Please download 'index.csv' (or similar) from the GitHub repo")
        print("and place it in the 'backend/data/' folder.")
    except Exception as e:
        print(f"❌ An error occurred during CSV seeding: {e}")
        db.rollback()


# --- 6. Level 3 Seeder (XLSX) ---
# This is the map for your 'Anuvaad_INDB_2024.11.xlsx' file
XLSX_HEADER_MAP = {
    "Energy": "energy_kcal",
    "Protein": "protein_g",
    "Carbohydrate": "carb_g",
    "Fat": "fat_g",
    "Fibre": "fibre_g",
    "Free Sugar": "freesugar_g",
    "Calcium": "calcium_mg",
    "Iron": "iron_mg",
    "Magnesium": "magnesium_mg",
    "Phosphorus": "phosphorus_mg",
    "Potassium": "potassium_mg",
    "Sodium": "sodium_mg",
    "Zinc": "zinc_mg",
    "Copper": "copper_mg",
    "Selenium": "selenium_ug",
    "Chromium": "chromium_mg",
    "Manganese": "manganese_mg",
    "Molybdenum": "molybdenum_mg",
    "Vitamin A (Retinol)": "vita_ug",
    "Beta-Carotene": "carotenoids_ug",
    "Vitamin C": "vitc_mg",
    "Vitamin D2": "vitd2_ug",
    "Vitamin D3": "vitd3_ug",
    "Vitamin E": "vite_mg",
    "Vitamin K1": "vitk1_ug",
    "Vitamin K2": "vitk2_ug",
    "Folic Acid": "folate_ug",
    "Thiamin": "vitb1_mg",
    "Riboflavin": "vitb2_mg",
    "Niacin": "vitb3_mg",
    "Vitamin B5": "vitb5_mg",
    "Pyridoxin": "vitb6_mg",
    "Vitamin B7": "vitb7_ug",
    "Vitamin B12": "vitb12_ug",
    "Cholesterol": "cholesterol_mg",
    "Saturated Fat (SFA)": "sfa_mg",
    "Monounsaturated Fat (MUFA)": "mufa_mg",
    "Polyunsaturated Fat (PUFA)": "pufa_mg",
}

def seed_foods_from_xlsx(db: Session, category_map: dict, nutrient_map: dict):
    print(f"Seeding Level 3 foods from XLSX: {INDB_XLSX_PATH}")
    
    category = category_map["Branded Foods (INDB)"]
    food_count = 0
    nutrient_link_count = 0
    
    try:
        workbook = openpyxl.load_workbook(INDB_XLSX_PATH, data_only=True)
        sheet = workbook.active
        
        all_rows = list(sheet.iter_rows())
        header_cells = all_rows[0]
        headers = [cell.value for cell in header_cells]
        data_rows = all_rows[1:]
        
        for i, row in enumerate(data_rows):
            row_data = {headers[idx]: cell.value for idx, cell in enumerate(row)}
            
            food_name = row_data.get('food_name')
            if not food_name:
                continue
                
            db_food = db.query(Food).filter_by(name=food_name).first()
            if not db_food:
                db_food = Food(name=food_name, category_id=category.id)
                db.add(db_food)
                try:
                    db.commit()
                    db.refresh(db_food)
                    food_count += 1
                except IntegrityError:
                    db.rollback()
                    print(f"  Could not add branded food: {food_name}")
                    continue
            
            # Link nutrients
            for nutrient_name, xlsx_header in XLSX_HEADER_MAP.items():
                value = row_data.get(xlsx_header)
                
                if isinstance(value, (int, float)):
                    try:
                        db_nutrient = nutrient_map.get(nutrient_name)
                        if db_nutrient:
                            link_nutrient(db, db_food.id, db_nutrient.id, float(value))
                            nutrient_link_count += 1
                    except (ValueError, TypeError):
                        pass # Skip invalid values
                        
            if i % 100 == 0:
                db.commit()
                print(f"  Processed {i} XLSX rows, added {food_count} new foods...")

        db.commit()
        print(f"✅ XLSX Seeding Complete. Added {food_count} new foods and {nutrient_link_count} nutrient links.")
        
    except FileNotFoundError:
        print(f"❌ ERROR: XLSX file not found at {INDB_XLSX_PATH}")
    except Exception as e:
        print(f"❌ An error occurred during XLSX seeding: {e}")
        db.rollback()

# --- 7. Level 2 Seeder (PDF) ---  <-- REMOVED

# Helper function to avoid duplicate links
def link_nutrient(db: Session, food_id: int, nutrient_id: int, value: float):
    if value is None:
        return
        
    existing_link = db.query(FoodNutrient).filter_by(
        food_id=food_id,
        nutrient_id=nutrient_id
    ).first()
    
    if not existing_link:
        db.add(FoodNutrient(
            food_id=food_id,
            nutrient_id=nutrient_id,
            value_per_100g=value
        ))

# --- MAIN EXECUTION ---
def seed_database():
    print("🌱 Starting database seeding...")
    db = SessionLocal()
    try:
        # Seed in logical order
        print("--- 1. Seeding Nutrients (Master List) ---")
        nutrient_map = seed_nutrients(db)
        
        print("\n--- 2. Seeding Demographic Groups ---")
        group_map = seed_demographic_groups(db)
        
        print("\n--- 3. Seeding RDA (The 'Goal') ---")
        seed_rda(db, group_map, nutrient_map)
        
        print("\n--- 4. Seeding Food Categories ---")
        category_map = seed_food_categories(db)
        
        print("\n--- 5. Seeding Level 1: Raw Foods (CSV) ---")
        seed_foods_from_ifct_csv(db, category_map, nutrient_map)
        
        print("\n--- 6. Seeding Level 3: Branded Foods (XLSX) ---")
        seed_foods_from_xlsx(db, category_map, nutrient_map)
        
        # print("\n--- 7. Seeding Level 2: Cooked Recipes (PDF) ---") <-- REMOVED
        # seed_cooked_foods(db, category_map, nutrient_map) <-- REMOVED
        
        print("\n✅✅✅ FULL DATABASE SEEDING COMPLETE! ✅✅✅")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()


