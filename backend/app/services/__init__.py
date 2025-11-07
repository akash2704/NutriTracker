"""
This file "exposes" all service functions
so they can be imported from the 'services' package.
"""
from .food_service import (
    get_food_by_id, 
    get_foods, 
    search_foods_by_name,
    create_food,
    get_food_by_name
)
from .auth_service import (
    create_user,
    verify_user_otp,
    get_user_by_email,
    authenticate_user)
from .foodLog_service import (
    create_log_entry,
    get_food_logs
)

from .dashboard_service import get_dashboard_data
from .profile_service import (
    create_or_update_profile,
    get_profile
)
# The __all__ list controls what 'from app.services import *' would import
# It's good practice, but this is where your error was.
__all__ = [
    "get_food_by_id", 
    "get_foods", 
    "search_foods_by_name",
    "create_food",
    "get_food_by_name",
    "create_user",
    "verify_user_otp",
    "get_user_by_email",
    "authenticate_user",
    "create_log_entry",
    "get_food_logs",
    "get_dashboard_data", # <-- THIS COMMA WAS MISSING
    "create_or_update_profile",
    "get_profile"
]
