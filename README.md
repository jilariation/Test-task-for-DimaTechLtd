# Асинхронное веб-приложение

Это асинхронное веб-приложение, следующее парадигме REST API. Оно использует Sanic в качестве веб-фреймворка, PostgreSQL в качестве базы данных и SQLAlchemy для работы с базой данных. Приложение контейнеризировано с использованием Docker и может быть легко настроено и запущено как с помощью Docker Compose, так и напрямую на хост-машине.

## Возможности

### Пользователи
- Аутентификация по email/паролю.
- Получение своих данных (id, email, полное имя).
- Получение списка своих аккаунтов и их балансов.
- Получение списка своих платежей.

### Администраторы
- Аутентификация по email/паролю.
- Получение своих данных (id, email, полное имя).
- Создание/удаление/обновление пользователей.
- Получение списка пользователей и их аккаунтов с балансами.

### Вебхук для платежей
- Реализация маршрута для симуляции обработки вебхука от внешней платежной системы.
- Структура JSON объекта для вебхука:
    - `transaction_id`: уникальный идентификатор транзакции во внешней системе.
    - `account_id`: уникальный идентификатор аккаунта пользователя.
    - `user_id`: уникальный идентификатор пользователя.
    - `amount`: сумма для пополнения счета пользователя.
    - `signature`: подпись объекта.
- Проверка подписи объекта.
- Проверка наличия у пользователя указанного аккаунта; если нет, создание аккаунта.
- Сохранение транзакции в базе данных.
- Добавление суммы транзакции к балансу аккаунта пользователя.
- Уникальность транзакций; транзакция с тем же `transaction_id` должна быть обработана только один раз.

Пример (для эндпоинта `webhook/payment`):
```json
{
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "user_id": 1,
  "account_id": 1,
  "amount": 100,
  "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
}
```

## Быстрый старт

### Запуск без Docker Compose

1. Клонируйте репозиторий:
```bash
git clone https://github.com/jilariation/Test-task-for-DimaTechLtd
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
```
3. Активируйте виртуальное окружение:
 - На Linux/macOS:
   ```bash
   source venv/bin/activate
   ```
   - На Windows:
   ```bash
   ./.venv/Scripts/activate
   ```
4. Установите зависимости:
```bash
   pip install -r requirements.txt
```
5. Измените в файлах config.py `DATABASE_URL`, а в alembic.ini `sqlalchemy.url` в соответствии с вашей БД и пользователем БД

6. Запустите сервер базы данных PostgreSQL (убедитесь, что он запущен и доступен).
7. Примените миграции базы данных:
```bash
alembic upgrade head
```
8. Запустите приложение:
```bash
sanic app:app --host=0.0.0.0 --port=8000
```

## Пользователи по умолчанию для тестирования
- Администратор
  - Email: testadmin@example.com
  - Пароль: 123456
- Пользователь
  - Email: testuser@example.com
  - Пароль: 123456

## API Эндпоинты
- Пользователи (через JWT токен, кроме регистрации и авторизации. Сам токен получаешь при авторизации)
  - `POST /register`: Регистрация нового пользователя
  ```json
  {
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "password123"
  }
  ```
  - `POST /login`: Вход пользователя
  ```json
  {
  "email": "user@example.com",
  "password": "password123"
  }
  ```
  - `GET /user/about`: Получить данные текущего пользователя
  ```json
  {
  "id": 1,
  "email": "testuser@example.com",
  "full_name": "Test User"
  }
  ```
  - `GET /user/accounts`: Получить аккаунты и балансы текущего пользователя
  ```json
  {
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "password123"
  }
  ```
  - `GET /users/payments`: Получить платежи текущего пользователя
  ```json
  [
    {
        "id": 1,
        "balance": 1100.0
    }
  ]
  ```

- Администраторы (все через JWT token, получаешь при авторизации)
  - `POST /users/create`: Создать пользователя
  ```json
  {
  "email": "user2@example.com",
  "full_name": "John Doe",
  "password": "password123"
  }
  ```
  - `DELETE /users/delete/<user_id>`: Удалить пользователя
  ```json
  {"message": "User deleted successfully"}
  ```
  - `PUT /users/update/<user_id>`: Обновить пользователя
  ```json
  {
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "password123"
  }
  ```
  - `GET /users`: Список пользователей (просто вывод информации о пользователях)