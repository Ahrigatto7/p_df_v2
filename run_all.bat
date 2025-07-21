
@echo off
echo [1/2] Starting FastAPI backend server...
start cmd /k "cd backend && uvicorn api_router:app --reload --port 8000"

timeout /t 3 > nul

echo [2/2] Starting Streamlit frontend dashboard...
start cmd /k "streamlit run app.py"

exit
