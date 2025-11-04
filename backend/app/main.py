from fastapi import FastAPI

# 1. Import the 'router' object from our new file
from .routers import general

# 2. Create the main FastAPI app instance
app = FastAPI(
    title="Nutrition Tracker API",
    description="API for the NIN-based Indian Nutrition Tracker",
    version="0.1.0"
)

# 3. "Include" the router
# This tells the main 'app' to add all the routes
# from the 'general.router' object.
app.include_router(general.router)

# In the future, you will add more routers here:
# from .routers import foods, users, auth
# app.include_router(foods.router)
# app.include_router(users.router)
# app.include_router(auth.router)
