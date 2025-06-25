FROM python:3.12.5-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

# Проверяем содержимое папки /app до и после копирования
RUN echo "Before copy:" && ls -l /app

RUN chmod +x ./docker/entrypoint.sh
COPY ./docker/entrypoint.sh /app/entrypoint.sh

RUN echo "After copy:" && ls -l /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 9000
ENTRYPOINT ["/app/entrypoint.sh"]










