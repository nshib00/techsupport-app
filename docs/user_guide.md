# TechSupport API. Руководство пользователя

В данном руководстве содержится подробное описание всех методов API, их параметров и возможных HTTP-кодов ответа.


Версия API: `v1`

Префикс URL: `api/v1/`


## Содержание
- [Аутентификация](#auth)
    - [Логин](#auth-login)
    - [Логаут](#auth-logout)
    - [Обновление токенов](#auth-refresh)
    - [Проверка валидности токенов](#auth-verify)
- [Методы пользователя](#users)  
- [Обращения (тикеты)](#tickets)
- [Методы сотрудника поддержки](#support)  
- [Методы администратора](#admin)
- [Уведомления](#notifications)
    - [WebSocket](#websocket)
- [Документация OpenAPI](#docs)



<a name="auth"></a> 
## Аутентификация

Используется аутентификация через **JWT-токены**.

После входа пользователь получает пару токенов:  
- **access-токен** — используется для аутентификации в заголовках запросов;
- **refresh-токен** — используется для обновления access-токена.

Токен передаётся в заголовке:

```http
Authorization: Bearer <ваш_access_token>
```


<a name="auth-login"></a> 
### Логин

**POST** `api/v1/auth/login/` 
 
Аутентификация по email/паролю. Возвращает пару токенов.

**Тело запроса:**
```json
{
  "username": "your-username",
  "password": "your-password"
}
```

**Ответ (200):**
```json
{
  "access": "access-токен пользователя...",
  "refresh": "refresh-токен пользователя..."
}
```

<a name="auth-logout"></a> 
### Логаут

**POST** `api/v1/auth/logout/` 

Выход пользователя. Refresh-токен помещается в чёрный список в БД.

**Заголовки:**
```http
Content-Type: application/json
```


**Тело запроса:**
```json
{
  "refresh": "refresh-токен пользователя..."
}
```

**Ответ (205):**  
```http
HTTP/1.1 205 Reset Content
```

**Ошибки:**
- **400** — refresh-токен отсутствует, не найден или недействителен.


<a name="auth-refresh"></a> 
### Обновление токена

**POST** `api/v1/auth/token/refresh/`  
Принимает refresh-токен и возвращает новую пару токенов: access и refresh.

**Заголовки:**
```http
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "refresh": "текущий refresh-токен..."
}
```

**Ответ (200):**
```json
{
  "access": "новый access-токен...",
  "refresh": "новый refresh-токен..."
}
```

### Проверка валидности токена
<a name="auth-verify"></a> 

**POST** `api/v1/auth/token/verify/`  
Позволяет проверить, действителен ли access-токен.

**Тело запроса:**
```json
{
  "token": "access-токен..."
}
```

**Ответ (200):**
```json
{}
```

**Ошибка (401 Unauthorized):**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

## Методы пользователя
<a name="users"></a> 

Все методы требуют авторизации (кроме регистрации).

### Регистрация

**POST** `api/v1/users/register/` 

Создание нового пользователя.

**Заголовки:**
```http
Content-Type: application/json
```

**Пример запроса:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password"
}
```

**Пример ответа (201):**  
```http
HTTP/1.1 201 Created

{
  "email": "user@example.com",
  "username": "username",
  "id": 1
}
```

### Получение данных текущего пользователя

**GET** `api/v1/users/me/`

Возвращает информацию о текущем авторизованном пользователе.

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Ответ (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username"
}
```
### Сброс пароля (запрос)

**POST** `api/v1/auth/users/reset_password/`  

Отправляет на email ссылку для восстановления пароля.

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "email": "user@example.com"
}
```

**Ответ (204):**  
```http
HTTP/1.1 204 No Content
```


### Сброс пароля (подтверждение)

**POST** `api/v1/auth/users/reset_password_confirm/`

Подтверждение восстановления пароля.

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "uid": "<uid из письма>",
  "token": "<token из письма>",
  "new_password": "newSecurePassword123"
}
```

**Ответ (204):**  
```http
HTTP/1.1 204 No Content
```

---

<a name="tickets"></a>
## Обращения (тикеты)

Все методы требуют авторизации.

### Получение списка тикетов пользователя

**GET** `api/v1/tickets/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Параметры:**

| Параметр | Тип   | Описание                      |
|----------|--------|-------------------------------|
| status   | string | Фильтрация по статусу тикета |

**Ответ (200):**
```json
[
  {
    "id": 1,
    "subject": "Ошибка авторизации",
    "status": "open",
    "created_at": "2025-06-25T09:30:00Z"
  }
]
```

**Ошибки:**

- `400 Bad Request` — передан невалидный статус:
```json
{
  "status": "Недопустимое значение. Возможные значения: open, in_progress, resolved, closed"
}
```

- `401 Unauthorized` — пользователь не авторизован.


### 🔹 Создание нового тикета

**POST** `api/v1/tickets/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Поля формы:**

| Поле        | Тип               | Обязательное | Описание                                       |
|-------------|--------------------|--------------|------------------------------------------------|
| subject     | string             | да            | Тема обращения                                 |
| category    | int                | да             | ID категории                                    |
| description | string             | да             | Подробное описание проблемы                    |
| attachments | list[file]         | нет            | До 10 файлов (расширения: `.jpg`, `.png`, ...)|

#### Разрешенные расширения файлов для вложений:
- `.jpg`, `.jpeg`
- `.png`
- `.webp`
- `.txt`
- `.log`
- `.docx`
- `.pdf`
- `.xlsx`

#### Разрешенные MIME-типы для вложений:

  - `image/jpeg`, `image/png`, `image/webp'`
  - `text/plain`
  - `application/pdf`
  - `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (для .docx-файлов)
  - `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (для .xlsx-файлов)
  - `application/zip` (иногда .docx и .xlsx файлы распознаются как application/zip)


**Ответ (201):**
```json
{
  "id": 2,
  "subject": "Не отображается страница",
  "status": "open"
}
```

**Ошибки:**

- `400 Bad Request` — ошибка валидации (например, слишком много вложений):
```json
{
  "attachments": "Нельзя загружать больше 10 вложений к обращению."
}
```

- `401 Unauthorized` — пользователь не авторизован.


### Получение деталей тикета

**GET** `api/v1/tickets/{id}/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Ответ (200):**
```json
{
  "id": 2,
  "subject": "Проблема с авторизацией",
  "description": "После логина выбрасывает на 500",
  "status": "open",
  "category": {
    "id": 1,
    "name": "Авторизация"
  }
}
```

**Ошибки:**

- `401 Unauthorized` — пользователь не авторизован.
- `404 Not Found` — тикет не найден или принадлежит другому пользователю.


### Получение списка категорий тикетов

**GET** `api/v1/tickets/categories/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Ответ (200):**
```json
[
  {
    "id": 1,
    "name": "Авторизация"
  },
  {
    "id": 2,
    "name": "Интерфейс"
  }
]
```

**Ошибки:**

- `401 Unauthorized` — пользователь не авторизован.


### Получение комментариев к тикету

**GET** `api/v1/tickets/{id}/comments/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Ответ (200):**
```json
[
  {
    "id": 10,
    "text": "Спасибо за обращение, мы начали работать над этим",
    "is_internal": false,
    "user": {
      "id": 5,
      "email": "agent@example.com"
    }
  }
]
```

**Ошибки:**

- `401 Unauthorized` — пользователь не авторизован.


### Создание комментария к тикету

**POST** `api/v1/tickets/{id}/comments/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "text": "Можно подробнее описать проблему?",
  "is_internal": false
}
```

**Ответ (201):**
```json
{
  "id": 11,
  "text": "Можно подробнее описать проблему?",
  "is_internal": false
}
```

**Ошибки:**

- `400 Bad Request` — ошибка валидации:
```json
{
  "text": [
    "Это поле обязательно."
  ]
}
```

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — если пользователь не имеет прав на создание внутреннего (`is_internal = true`) комментария (могут только пользователи с ролями SUPPORT или ADMIN).

---

## Методы сотрудника поддержки
<a name="support"></a>

Все методы требуют прав сотрудника поддержки (`role = User.Role.SUPPORT` у пользователя) и аутентификацию через JWT.

### Получение списка тикетов

**GET** `api/v1/support/tickets/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Параметры запроса (необязательные):**

| Параметр     | Тип   | Описание                                                |
|--------------|--------|---------------------------------------------------------|
| status       | string | Фильтр по статусу (`open`, `in_progress`, `resolved`, `closed`) |
| assigned_to  | int    | ID пользователя, назначенного на тикет                 |
| category     | int    | ID категории тикета                                     |

**Ответ (200):**
```json
[
  {
    "id": 1,
    "title": "Не работает сервис",
    "status": "open",
    "assigned_to": null,
    "category": {
      "id": 2,
      "name": "Ошибки системы"
    },
    "created_at": "2025-06-25T10:00:00Z"
  },
  ...
]
```
**Ошибки:**

- `401 Unauthorized` — пользователь не аутентифицирован.
- `403 Forbidden` — у пользователя нет прав сотрудника поддержки.


### Получение тикета по ID

**GET** `api/v1/support/tickets/{id}/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Ответ (200):**
```json
{
  "id": 1,
  "title": "Ошибка 500",
  "description": "Сервис падает при отправке формы",
  "status": "open",
  "assigned_to": {
    "id": 4,
    "username": "support_agent"
  },
  "category": {
    "id": 3,
    "name": "Бэкенд"
  },
  "created_at": "2025-06-25T09:30:00Z"
}
```

**Ошибки:**

- `401 Unauthorized` — неавторизован.
- `403 Forbidden` — нет доступа к тикету.
- `404 Not Found` — тикет с указанным ID не существует.


###  Назначение сотрудника на тикет

**PATCH** `api/v1/support/tickets/{id}/assign/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "assigned_to": 4
}
```
`assigned_to` - ID сотрудника поддержки, которому назначается тикет.

**Ответ (200):**
```json
{
  "id": 1,
  "assigned_to": 4
}
```

**Ошибки:**

- `400 Bad Request` — ошибка валидации (например, отсутствует поле `assigned_to`).
- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав для выполнения действия.
- `404 Not Found` — тикет или пользователь не найден.

### Обновление статуса тикета

**PATCH** `api/v1/support/tickets/{id}/status/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "status": "in_progress"
}
```
> Поле `status` может принимать одно из четырех значений: **open**, **in_progress**, **resolved**, **closed**.

> При установке статуса в **closed** поля `closed_at` и `closed_by` ринимают значения, отличные от null:
- `closed_at` - время закрытия тикета.
- `closed_by` - ID пользователя, закрывшего тикет.

**Ответ (200):**

Тикет не закрыт:
```json
{
  "id": 1,
  "status": "in_progress",
  "updated_at": "2025-06-25T14:10:00Z",
  "closed_at": null,
  "closed_by": null
}
```

Тикет закрыт:
```json
{
  "id": 1,
  "status": "closed",
  "updated_at": "2025-06-25T14:10:00Z",
  "closed_at": "2025-06-25T14:10:00Z",
  "closed_by": 1
}
```

**Ошибки:**

- `400 Bad Request` — передан несуществующий статус или не назначен ответственный.
```json
{
  "assigned_to": [
    "Нельзя изменить статус, пока не назначен ответственный сотрудник."
  ]
}
```

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — у пользователя нет доступа к тикету.
- `404 Not Found` — тикет с указанным ID не найден.

---

<a name="admin"></a>
## Методы администратора

> Все методы требуют авторизации и прав доступа админа (пользователь должен иметь роль `User.Role.ADMIN`).

### Получение полного списка пользователей

**GET** `api/v1/admin/users/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Параметры:**

| Параметр | Тип   | Описание                      |
|----------|--------|-------------------------------|
| role     | string | Фильтрация пользователей по роли (admin, user, support) |

**Пример ответа (200):**
```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "role": "admin"
  },
  {
    "id": 2,
    "email": "user@example.com",
    "role": "user",
  }, 
  {
    "id": 3,
    ...
  },
  ...
]
```

**Ошибки:**

- `400 Bad Request` — некорректный параметр запроса:
```json
{
  "role": "Недопустимое значение. Возможные значения: admin, user, support"
}
```

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав для просмотра списка пользователей как администратор.


### Изменение роли пользователя

**PATCH** `api/v1/admin/users/{id}/role/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "role": "support"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "support"
}
```

**Ошибки:**

- `400 Bad Request` — некорректная роль пользователя:
```json
{
  "role": "Роль должна быть user или support"
}
```

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав для изменения роли пользователя (доступно только администраторам).
- `404 Not Found` — пользователь с указанным ID не найден.

### Просмотр истории изменений тикетов

**GET** `api/v1/admin/ticket-history/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Параметры:**

| Параметр           | Тип   | Описание                         |
|--------------------|--------|----------------------------------|
| ticket             | int   | ID тикета                        |
| changed_by         | int   | ID пользователя, который изменил тикет |
| field              | string| Название изменённого поля        |
| changed_at__gte    | datetime | Начало интервала изменений     |
| changed_at__lte    | datetime | Конец интервала изменений       |

**Ответ (200):**
```json
[
  {
    "ticket": 1,
    "changed_by": 2,
    "field": "status",
    "old_value": "open",
    "new_value": "in_progress",
    "changed_at": "2025-06-25T10:00:00Z"
  },
  ...
]
```

**Ошибки:**

- `400 Bad Request` — передано некорретное значение для одного или нескольких фильтров.
- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав для просмотра истории изменений тикетов.

---

### Создание категории тикетов

**POST** `api/v1/admin/tickets/categories/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "name": "Ошибка с оплатой"
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "name": "Ошибка с оплатой"
}
```

**Ошибки:**

- `400 Bad Request` — некорректные данные для создания категории:
```json
{
  "name": "Это поле обязательно."
}
```

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав для работы с категориями.
- `409 Conflict` — категория с таким названием уже существует:
```json
{
  "name": "Категория с таким названием уже существует"
}
```

---

### Обновление категории тикетов

**PATCH** `api/v1/admin/tickets/categories/{id}/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "name": "Ошибка с подключением"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "Ошибка с подключением"
}
```

**Ошибки:**

- `400 Bad Request` — некорректные данные для обновления категории:
```json
{
  "name": "Это поле обязательно."
}
```

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав для обновления категории.
- `404 Not Found` — категория не найдена.
- `409 Conflict` — категория с таким названием уже существует:
```json
{
  "name": "Категория с таким названием уже существует"
}
```

---

### Удаление категории тикетов

**DELETE** `api/v1/admin/tickets/categories/{id}/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Ответ (204):**
```json
HTTP/1.1 204 No Content
```

**Ошибки:**

- `401 Unauthorized` — пользователь не авторизован.
- `403 Forbidden` — нет прав на удаление категории.
- `404 Not Found` — категория не найдена.

---

<a name="notifications"></a>
## Уведомления


> Все методы требуют авторизации через JWT.


### Получение списка уведомлений

**GET** `api/v1/notifications/`

**Заголовки:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Пример ответа (200):**
```json
[
  {
    "id": 1,
    "message": "Новый тикет был создан.",
    "is_read": false,
    "created_at": "2025-06-27T10:15:00Z"
  },
  {
    "id": 2,
    "message": "Комментарий был добавлен к вашему тикету.",
    "is_read": true,
    "created_at": "2025-06-26T08:30:00Z"
  },
  {
    "id": 3,
    ...
  },
  ...
]
```

**Ошибки:**
-  `401 Unauthorized` — пользователь не авторизован.

### Пометить уведомление как прочитанное

**PATCH** `api/v1/notifications/{id}/mark-as-read/`

**Тело запроса:**
```json
{
  "is_read": true
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "message": "Новый тикет был создан.",
  "is_read": true,
  "created_at": "2025-06-27T10:15:00Z"
}
```

**Ошибки:**
- `401 Unauthorized` — пользователь не авторизован.
- `404 Not Found` — уведомление с указанным ID не найдено.


### Уведомления в реальном времени (WebSocket)

> Для получения уведомлений в реальном времени используется WebSocket. После подключения, пользователю или сотруднику поддержки автоматически приходят уведомления.

**WebSocket URL:** `ws://<host>/ws/notifications/` *(настройка зависит от вашей конфигурации Django Channels)*

#### Общие особенности

- Подключение происходит только для аутентифицированных пользователей.
- Используется базовый класс [BaseNotificationConsumer](../notifications/consumers/base.py), переопределяющий два метода:
  - `send_json` - для корректной отправки символов кириллицы;
  - `connect` - для проверки, является ли пользователь аутентифицированным, при установке соединения.

#### Пользовательские уведомления

**Канал:** `user_<user_id>`

Пользователь получает уведомления, направленные только ему (например, ответ на тикет).

**Поведение:**
- При подключении аутентифицированный пользователь присоединяется к группе `user_<user_id>`.
- После отключения — покидает группу.
- Входящие события отправляются через метод `notify`.

Реализация находится в классе UserNotificationConsumer [в этом файле](../notifications/consumers/user.py).

#### Уведомления поддержки

**Канал**: `support`

Сотрудники поддержки получают уведомления о новых тикетах, созданных пользователями.

Поведение:

  - При подключении проверяется роль пользователя (`is_support()`).
  - **Только сотрудники поддержки** могут подключиться к каналу **support**.
  - Уведомления отправляются через метод `notify_new_ticket`.


Реализация (класс SupportNotificationConsumer) - [в этом файле](../notifications/consumers/support.py).

---

<a name="docs"></a> 
## Документация OpenAPI 

Документация API генерируется автоматически на основе OpenAPI 3.0 с помощью библиотеки `drf-spectacular`.

### Swagger UI

**GET** `api/v1/schema/swagger-ui/`

Интерактивная документация с возможностью просмотра всех доступных эндпоинтов и их тестирования напрямую из браузера.

**Краткий показ документации** имеется в файле [README.md](../README.md#docs).


### OpenAPI-схема в виде файла

**GET** `api/v1/schema/`

Позволяет получить OpenAPI-схему в формате **JSON** или **YAML**.