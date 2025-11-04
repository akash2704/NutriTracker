from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# This 'Base' is the "master translator" we talked about.
# All our model classes will inherit from this.
Base = declarative_base()

class FoodCategory(Base):
    __tablename__ = "food_categories"

    # Define the columns for this table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) # e.g., "Cereals"
    
    # --- The Relationship (Part 1) ---
    # This 'foods' property is a "magic" property.
    # It gives us a list of all Food objects in this category.
    # 'back_populates' links it to the 'category' property in the Food class.
    foods = relationship("Food", back_populates="category")

    def __repr__(self):
        # A helpful function for printing (e.g., <FoodCategory(name=Cereals)>)
        return f"<FoodCategory(name={self.name})>"


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True) # e.g., "Rice"
    
    # --- The Relationship (Part 2) ---
    # This column holds the ID of the category this food belongs to.
    category_id = Column(Integer, ForeignKey("food_categories.id"))

    # This 'category' property is the other side of the magic.
    # It gives us the *one* FoodCategory object this food belongs to.
    category = relationship("FoodCategory", back_populates="foods")

    # We'll add nutrition columns later (e.g., calories, protein)
    # For example:
    # calories_per_100g = Column(Float)
    # protein_per_100g = Column(Float)

    def __repr__(self):
        return f"<Food(name={self.name})>"