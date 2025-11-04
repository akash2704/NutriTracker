from app.database import SessionLocal
from app.models import Food, FoodCategory
from data.pdf_extractor import NINDataExtractor, NIN_PDF_PATH

# Get a new database session
db = SessionLocal()

def seed_database():
    print("🌱 Starting database seeding...")
    
    try:
        # --- 1. Create our default Category ---
        
        # Check if the category already exists
        category_name = "Cooked Preparations"
        category = db.query(FoodCategory).filter_by(name=category_name).first()
        
        if not category:
            print(f"Creating category: {category_name}")
            category = FoodCategory(name=category_name)
            db.add(category)
            db.commit() # Commit to get the new ID
            db.refresh(category)
        else:
            print(f"Category '{category_name}' already exists.")

        # --- 2. Get our Extracted Data ---
        print("Extracting food data from PDF...")
        extractor = NINDataExtractor(NIN_PDF_PATH)
        foods_to_add = extractor.extract_cooked_food_data()
        
        # Filter out the 'Annexure' bug we found
        foods_to_add = [f for f in foods_to_add if "Annexure" not in f["description"]]
        
        print(f"Found {len(foods_to_add)} foods to add.")

        # --- 3. Seed the Foods ---
        new_foods = []
        for food_data in foods_to_add:
            # Check if food already exists
            existing_food = db.query(Food).filter_by(name=food_data["description"]).first()
            if not existing_food:
                new_food = Food(
                    name=food_data["description"],
                    category_id=category.id  # <-- Here's the magic link!
                    # We will add calories later when we build the full FoodNutrient model
                )
                new_foods.append(new_food)

        if new_foods:
            print(f"Adding {len(new_foods)} new foods to the database...")
            db.add_all(new_foods)
            db.commit()
        else:
            print("All foods from the extractor are already in the database.")
            
        print("✅ Seeding complete!")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        db.rollback() # Roll back any changes if an error happens
    finally:
        db.close() # Always close the session

if __name__ == "__main__":
    seed_database()