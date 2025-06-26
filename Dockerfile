FROM python:3.12.5-slim

WORKDIR /app

# создание непривилегированного пользователя для celery
RUN useradd -ms /bin/bash celeryuser

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

COPY . .

RUN chown -R celeryuser:celeryuser /app

COPY ./docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 9000
ENTRYPOINT ["/app/entrypoint.sh"]










