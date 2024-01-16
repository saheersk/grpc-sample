FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /task-flask

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_ENV='development'
ENV FLASK_APP run.py:create_app
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["sh", "-c", "export FLASK_APP=run && python -m flask run --host=0.0.0.0 --port=5000"]