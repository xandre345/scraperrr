@echo off
echo Starting AI News Dashboard...
echo Open http://127.0.0.1:8000 in your browser.
python -m uvicorn app.backend.main:app --reload --host 127.0.0.1 --port 8000
pause
