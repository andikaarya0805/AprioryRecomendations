@echo off
echo Starting Apriori Recommendation System...

echo Starting Backend (FastAPI)...
start "Backend Server" cmd /k "cd backend && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0"

echo Starting Frontend (Next.js)...
start "Frontend Server" cmd /k "cd frontend && npm install && npm run dev -- -H 0.0.0.0"

echo System started!
echo --------------------------------------------------
echo [ LOCAL ACCESS ]
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000/docs
echo.
echo [ NETWORK ACCESS ]
echo Use your IP address (e.g., http://192.168.100.189:3000)
echo JANGAN buka http://0.0.0.0:3000 di browser (itu salah).
echo --------------------------------------------------
pause
