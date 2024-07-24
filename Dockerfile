FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

RUN alembic upgrade head

CMD ["sanic", "app:app", "--host=0.0.0.0", "--port=8000"]