# TechSupport API
API системы обращения в техническую поддержку.

## 📌 Возможности
### 👤 Пользовательская часть
- Регистрация и вход по email/паролю
- Восстановление пароля
- Создание обращения:
  - Тема, категория, описание
  - Прикрепление файлов (скриншоты, логи и т.д.)
- Просмотр и фильтрация заявок по статусу
- Комментирование заявок
- Уведомления:
  - Email-уведомления
  - Внутрисистемные уведомления (через WebSocket)

### 🛠 Административная панель

#### Для поддержки:
- Просмотр всех обращений
- Назначение ответственного
- Изменение статуса заявки
- Уведомления о новых обращениях

#### Для администраторов:
- Управление категориями обращений (создание, обновление, удаление)
- Просмотр истории обращений
- Изменение роли пользователей (обычный пользователь/сотрудник поддержки)

## 🛡️ Безопасность
- Ролевая модель доступа (пользователь, сотрудник поддержки, администратор)
- Использование только ORM-запросов, без сырого SQL
- Валидация в сериализаторах (очистка от небезопасных html-тегов) для защиты от XSS
- Хэширование паролей, хранение хэшей
- Ограничения по типу, количеству и размеру файлов при создании вложений к обращениям


## ⚡Производительность
- Кэширование через Redis
- Асинхронная обработка фоновых задач через Celery

## ⚙️ Технологии и инструменты

- **Python** (**Django** + **Django REST Framework**)
- **PostgreSQL**
- **Redis**
- **Docker** + **Docker Compose**
- **Nginx**
- Хранение файлов: локальное

### 📦 Используемые Python-пакеты

- `Django` — основа проекта, веб-фреймворк.
- `Django REST Framework` — создание API на Django.
- `Poetry` — управление зависимостями. 
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


## 📑 Документация API

### Swagger UI

Доступен по URL: `/api/v1/schema/swagger-ui`

**Краткая демонстрация:**

![techsupport_api](https://github.com/user-attachments/assets/bb222f5b-9dcb-43d7-b598-d0dd2af7fbdf)


Методы API подробно описаны в руководстве пользователя.


## Структура проекта

### Приложения:
- `techsupport` - конфигурация проекта
- `users` - аутентификация и пользователи
- `tickets` - обращения, категории, комментарии
- `custom_admin` - админ-панель.
- `notifications` - уведомления и WebSocket
`api` - объединение всех эндпоинтов, настройка OpenAPI-документации

### Прочее:
`tests` - unit-тесты
`docker` - shell-скрипты, настройка Nginx
`media` - хранение файлов (вложения к обращениям)


## 🚀 Установка и запуск проекта


### Через Docker

```
git clone https://github.com/nshib00/techsupport-app.git
`cd techsupport
docker-compose up -d --build
```

**Создание суперпользователя**:

`docker-compose exec web python manage.py createsuperuser`

---

### Локально (виртуальное окружение Poetry)

#### Установка:
```
git clone https://github.com/nshib00/techsupport-app.git
poetry install
poetry env activate
<копирование и вставка команды, которую выдаст poetry env activate>
```

#### Запуск:

**Uvicorn**:
`uvicorn techsupport.asgi:application --host 127.0.0.1 --port 9000 --reload`

> Вместо 9000 может быть любой другой порт.

**Redis**:
`redis-cli`

**Celery**:

Unix:

`celery -A techsupport worker --loglevel=info`

Windows:

`celery -A techsupport worker --loglevel=info --pool=solo`
