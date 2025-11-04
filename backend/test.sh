#!/bin/bash
#
# This script tests the full user flow:
# 1. Logs in as a user and gets a token.
# 2. Uses the token to log a new food entry for a specific date.
# 3. Uses the token again to get the dashboard analysis for that same date.
#
# Assumes the user 'test@example.com' with password 'password123' exists
# and has had their UserProfile manually created in the database.

# Exit immediately if a command fails
set -e

# --- Configurable ---
BASE_URL="http://127.0.0.1:8000"
USER_EMAIL="test@example.com"
USER_PASS="password123"
LOG_DATE="2025-10-31" # The date we will log food for

# --- 1. LOGIN & GET TOKEN ---
echo "--- 1. Logging in as $USER_EMAIL... ---"
TOKEN_RESPONSE=$(curl -s -X 'POST' \
  "$BASE_URL/auth/token" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "username=$USER_EMAIL&password=$USER_PASS")

# Use jq to parse the JSON and extract the token.
TOKEN=$(echo $TOKEN_RESPONSE | jq -r .access_token)

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ ERROR: Could not get token. Login failed."
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi
echo "✅ Login successful. Token received."


# --- 2. LOG A FOOD ENTRY ---
echo -e "\n--- 2. Logging a food entry for date: $LOG_DATE ---"
LOG_RESPONSE=$(curl -s -X 'POST' \
  "$BASE_URL/food-logs/" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "food_id": 1, 
    "quantity_grams": 150,
    "log_date": "'"$LOG_DATE"'",
    "meal_type": "Lunch"
  }')

echo "✅ Food log created:"
echo $LOG_RESPONSE | jq


# --- 3. GET THE DASHBOARD ---
echo -e "\n--- 3. Fetching dashboard for $LOG_DATE... ---"
DASHBOARD_RESPONSE=$(curl -s -X 'GET' \
  "$BASE_URL/dashboard/?log_date=$LOG_DATE" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

echo "✅ Dashboard analysis complete:"
echo $DASHBOARD_RESPONSE | jq
```

