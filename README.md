# 📝 Notes API

## 📋 Описание

Notes API — это веб-приложение на FastAPI, позволяющее управлять заметками с разграничением прав доступа по ролям `User` и `Admin`. Данные хранятся в PostgreSQL. Приложение поддерживает авторизацию через JWT и логгирование действий пользователей.

---

## 💠 Функциональность

### Роль `User`:

* Создание, чтение, обновление и удаление  своих заметок.

### Роль `Admin`:

* Доступ ко **всем** заметкам.
* Получение заметок конкретного пользователя.
* Получить конкретную заметку.
* Восстановление удалённых заметок.

---

## ⚙️ Установка и запуск (Docker)

### 1. Клонируй репозиторий

---

### 2. Создай файл `.env` рядом с docker-compose. Пример содержимого:

```env
POSTGRES_DB=notesdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password1234
POSTGRES_PORT=5432
POSTGRES_HOST=notesdb

JWT_SECRET_KEY=supersecretkey
```

---

### 3. Собери и запусти Docker-контейнеры

```bash
docker-compose up -d --build
```

---

### 4. Примени миграции

```bash
docker exec -it notesapp alembic upgrade head
```

---

### 5. Инициализируй пользователей

```bash
docker exec -it notesapp python -m src.main init
```

---

### 6. Swagger UI

📖 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Авторизация

1. Данные для авторизации с ролью User

   * `username`: user@mail.ru
   * `password`: user123

2. Данные для авторизации с ролью Admin

   * `username`: admin@mail.ru
   * `password`: admin123

---

## 🔮 API маршруты

| Метод  | URL                                | Описание                          |
|--------|------------------------------------|-----------------------------------|
| POST   | `/auth/token`                      | Получить JWT токен                |
| POST   | `/note/`                           | Создать заметку (User)            |
| GET    | `/note/`                           | Список своих заметок (User)       |
| GET    | `/note/{note_id}`                  | Своя заметка (User)               |
| PUT    | `/note/{note_id}`                  | Обновить свою заметку (User)      |
| DELETE | `/note/{note_id}`                  | Удалить свою заметку (User)       |
| GET    | `/admin/notes/`                    | Все заметки (Admin)               |
| GET    | `/admin/notes/{note_id}`           | Чтение конкретной заметки (Admin) |
| GET    | `/admin/users/{user_id}/notes/`    | Заметки юзера (Admin)             |
| POST   | `/admin/notes/{note_id}/restore`   | Восстановить удаленную заметку (Admin)|


---

## 🛠 Дополнительно

* Все действия логгируются в файл.
