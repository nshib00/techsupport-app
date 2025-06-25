# TechSupport API
API системы обращения в техническую поддержку.

## Настройка проекта



**Создание виртуального окружения (Poetry)**:

```poetry install```


**Активация Poetry**:

```poetry env activate```

```<копирование и вставка команды, которую выдаст poetry env activate>```

**Uvicorn**:
`uvicorn techsupport.asgi:application --host 127.0.0.1 --port 9000 --reload`

**Redis**:
`redis-cli`

**Celery**:
`celery -A techsupport worker --loglevel=info --pool=threads`


## Документация OpenAPI (Swagger UI)
Доступна по URL: `/api/v1/schema/swagger-ui`

