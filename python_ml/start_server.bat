@echo off
REM Script to start the Python ML API server on Windows

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Start the server
python -m uvicorn api.main:app --reload --port 8000

