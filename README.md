# TechSupport API
API системы обращения в техническую поддержку.


## Технологии и инструменты

- `Python` (фреймворк: `Django` + `Django REST Framework`) 
- `PostgreSQL` - основная БД
- `Redis` - NoSQL БД для кэширования и работы с фоновыми задачами
- `Docker` и `Docker Compose`
- `Nginx` - веб-сервер
- **Хранение файлов**: локальное хранилище

### Python-пакеты

- `Django` — основа проекта, веб-фреймворк.
- `Django REST Framework` — создание API на Django.
- `Django Channels` — поддержка WebSocket и асинхронных задач.
- `channels-redis` — Redis для работы Django Channels.
- `Celery` — выполнение фоновых задач.
- `django-redis` — кэш и очереди через Redis.
- `Uvicorn` — ASGI-сервер для запуска проекта (ASGI-сервер необходим для работы с Django Channels)
- `psycopg2` — подключение к базе данных PostgreSQL.
- `python-dotenv` — загрузка настроек из `.env` файла.
- `Djoser` — регистрация, логин, восстановление пароля.
- `drf-spectacular` — автогенерация документации API.
- `djangorestframework-simplejwt` — JWT-аутентификация.
- `django-cors-headers` — поддержка CORS-заголовков.
- `django-filter` — фильтрация данных в API.
- `filetype` — определение типа файлов.
- `nh3` — очистка HTML от опасного кода (защита от XSS).
- `websockets` — работа с WebSocket-соединениями.
- `pytest` — библиотека для тестирования.
- `pytest-django`, `pytest-asyncio`, `pytest-mock` — плагины Pytest.


## API-методы

### Краткий показ документации


### Подробное описание

Находится в руководстве пользователя.


## Структура проекта

### Приложения:

`techsupport` - основное приложение с конфигурацией проекта.

`users` - API пользователей, аутентификация и методы пользователя.

`tickets` - API обращений. Содержит логику работы с обращениями, категориями, комментариями к обращениям.
`custom_admin` - API админ-панели.

`notifications` - API уведомлений и WebSocket-консьюмеры.

`api` - объединение всех URL приложения, настройка OpenAPI-документации.

### Также:
`tests` - unit-тесты


## Сборка проекта через Docker

`docker-compose up -d --build`

**Добавление суперпользователя**:

`docker-compose exec web python manage.py createsuperuser`


## Установка проекта без Docker

**Клонирование репозитория**:

`git clone https://github.com/nshib00/techsupport-app.git`


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

