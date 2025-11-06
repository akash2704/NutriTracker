from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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

# Custom OpenAPI schema to fix API Gateway paths
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Nutrition Tracker API",
        version="0.1.0",
        description="API for the NIN-based Indian Nutrition Tracker",
        routes=app.routes,
    )
    
    # Fix server URLs for API Gateway
    openapi_schema["servers"] = [
        {"url": "https://x3qavb8llb.execute-api.ap-south-1.amazonaws.com/Prod"}
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Handle CORS origins with fallback
origins_env = os.getenv("ALLOWED_ORIGINS", "")
if origins_env:
    origins = origins_env.split(",")
else:
    origins = ["*"]  # Fallback for development

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
# AWS Lambda handler
from mangum import Mangum
handler = Mangum(app)

# In the future, you will add more routers here:
# from .routers import users, auth
# app.include_router(users.router)
# app.include_router(auth.router)