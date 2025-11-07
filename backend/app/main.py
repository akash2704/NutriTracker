from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import os
import time
from collections import defaultdict

# Load environment variables
load_dotenv()

# Rate limiting storage
request_counts = defaultdict(list)
RATE_LIMIT = 60  # requests per minute
WINDOW_SIZE = 60  # seconds

async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware to prevent DDoS and control costs"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old requests outside the window
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip] 
        if current_time - req_time < WINDOW_SIZE
    ]
    
    # Check if rate limit exceeded
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Add current request
    request_counts[client_ip].append(current_time)
    
    response = await call_next(request)
    return response

# 1. Import the 'router' object from our new file
from .routers import general, foods, users, auth, foodLog, dashboard, profile, recipe, recommendations # <-- This is correct

# 2. Create the main FastAPI app instance
app = FastAPI(
    title="Nutrition Tracker API",
    description="API for the NIN-based Indian Nutrition Tracker",
    version="0.1.0"
)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

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