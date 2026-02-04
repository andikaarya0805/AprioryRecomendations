@echo off
echo Starting Apriori Recommendation System...

echo Starting Backend (FastAPI)...
start "Backend Server" cmd /k "cd backend && pip install -r requirements.txt && uvicorn main:app --reload"

echo Starting Frontend (Next.js)...
start "Frontend Server" cmd /k "cd frontend && npm install && npm run dev"

echo System started!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000/docs
pause
