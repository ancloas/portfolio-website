rem Activate virtual environment
call .venv\Scripts\activate

rem Navigate to backend directory
cd backend-portfolio



rem Run database migrations
alembic upgrade head

rem Start the FastAPI server
uvicorn main:app --reload