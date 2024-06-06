@echo off
cd C:\Program Files\Mechademy\data-connector-main
call .venv\Scripts\activate
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
