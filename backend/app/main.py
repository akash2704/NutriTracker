from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# 1. Import the 'router' object from our new file
from .routers import general, foods, users, auth, foodLog, dashboard, profile, recipe, recommendations # <-- This is correct

# 2. Create the main FastAPI app instance
app = FastAPI(
    title="Nutrition Tracker API",
    description="API for the NIN-based Indian Nutrition Tracker",
    version="0.1.0"
)

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 3. "Include" the router
app.include_router(general.router)
app.include_router(foods.router) 
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(foodLog.router)
app.include_router(dashboard.router)
app.include_router(profile.router)
app.include_router(recipe.router)
app.include_router(recommendations.router)
# Vercel serverless handler
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    # mangum not installed, skip handler
    pass

# In the future, you will add more routers here:
# from .routers import users, auth
# app.include_router(users.router)
# app.include_router(auth.router)