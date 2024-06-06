@echo off
cd C:\Program Files\Mechademy\data-connector-main
call .venv\Scripts\activate
poetry run celery -A src.celery.celery worker --loglevel=info
