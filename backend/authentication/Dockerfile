FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /authentication-fastapi

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["uvicorn", "auth.main:app", "--host", "0.0.0.0", "--port", "8000"]