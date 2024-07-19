FROM python:3.9.13

RUN pip install poetry==1.6.1

WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml ./

RUN poetry install --no-root

COPY . .

RUN useradd -m celeryuser

RUN chown -R celeryuser:celeryuser /app

USER celeryuser

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
