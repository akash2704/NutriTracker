from fastapi import APIRouter

# 1. Create a new APIRouter
# This is like a "mini" FastAPI app
router = APIRouter()

# 2. Define the route on the 'router' object
# We've just moved this from main.py
@router.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Hello, Nutrition Tracker!"}

# You can add other "general" routes here, like:
@router.get("/health")
def read_health():
    """
    A 'health check' endpoint that services can use
    to see if the API is alive.
    """
    return {"status": "ok"}