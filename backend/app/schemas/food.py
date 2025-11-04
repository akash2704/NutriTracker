from pydantic import BaseModel
from typing import Optional 

#------------Food Category Schema ------


class FoodCategoryBase(BaseModel):
    name: str

class FoodCategoryCreate(FoodCategoryBase):
    pass

class FoodCategory(FoodCategoryBase):
    id: int 

    class Config :
        orm_model=True 


#----------Food Schema --------------


class FoodBase(BaseModel):
    name: str

class FoodCreate(FoodBase):
    category_id: int

class Food(FoodBase):
    id: int
    category_id: int

    category: FoodCategory

    class Config:
        orm_model=True
        