# Developer Landing API

Backend-сервис для лендинга разработчика с API для обработки обращений, AI-анализом сообщений, отправкой email-уведомлений и защитой от спама.

Проект выполнен в рамках тестового задания Backend Developer.

---

# Features

## Backend

- REST API на FastAPI
- Валидация входных данных через Pydantic
- Сохранение обращений в SQLite
- Отправка email-уведомлений через SMTP
- Копия письма пользователю
- - AI-анализ обращений через Groq API
- Автоматическая классификация сообщений
- Анализ тональности
- Генерация автоматического ответа
- Rate limiting для защиты от спама
- Глобальная обработка ошибок
- Логирование запросов
- CORS настройка
- Swagger / OpenAPI документация

## Frontend

- Vue.js 3
- Vite
- Форма обратной связи
- Отправка данных через REST API

---

# Tech Stack

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Groq API (Llama models)
- SMTP Gmail
- Pytest

## Frontend

- Vue.js 3
- Vite

## Infrastructure

- Docker
- Docker Compose
- Environment variables (.env)

---

# Project Structure

```
developer-landing-api/

├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Configuration and logging
│   ├── database/         # Database connection
│   ├── models/           # SQLAlchemy models
│   ├── repositories/     # Database operations
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   │   ├── ai_service.py
│   │   ├── email_service.py
│   │   ├── rate_limiter.py
│   │   └── metrics_service.py
│   ├── utils/            # Helpers and middleware
│   └── main.py           # Application entry point
│
├── frontend/             # Vue.js frontend
│
├── tests/                # Automated tests
│
├── storage/              # JSON storage for metrics/rate limit
│
├── static/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```

---

# Architecture

Проект построен по слоистой архитектуре:

```
Controller Layer
        |
        |
Service Layer
        |
        |
Repository Layer
        |
        |
Database
```

## Flow обработки обращения:

```
User
 |
 |
Frontend form
 |
 |
POST /api/contact
 |
 |
Validation
 |
 |
Repository
 |
 |
Database
 |
 |
AI Analysis
 |
 |
Email Notification
 |
 |
Response
```

---

# Installation

## Requirements

- Python 3.11+
- Node.js 18+
- Docker (optional)

---

# Backend Setup

Clone repository:

```bash
git clone https://github.com/Akiro291/developer-landing-api.git

cd developer-landing-api
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
copy .env.example .env
```

Configure variables in `.env`.

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend available:

```
http://localhost:8000
```

---

# Frontend Setup

Go to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run:

```bash
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# Docker

Build and run:

```bash
docker-compose up --build
```

Backend:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

# Environment Variables

Example:

```
DATABASE_URL=sqlite:///./test_task.db

DEBUG=True

GROQ_API_KEY=your_key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SMTP_USERNAME=email@gmail.com
SMTP_PASSWORD=app_password

SMTP_FROM_EMAIL=email@gmail.com

RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

CORS_ORIGINS=*
```

---

# API Documentation

Swagger:

```
GET /docs
```

ReDoc:

```
GET /redoc
```

---

# API Endpoints

## Create Contact

```
POST /api/contact
```

Request:

```json
{
  "name": "Alex",
  "email": "alex@example.com",
  "phone": "+79990000000",
  "comment": "I want to know more about your services"
}
```

Response:

```json
{
  "id": 1,
  "name": "Alex",
  "email": "alex@example.com",
  "phone": "89990000000",
  "comment": "...",
  "ai_category": "question",
  "ai_sentiment": "neutral",
  "ai_response": "Спасибо за обращение..."
}
```

---

## Get Contact

```
GET /api/contact/{id}
```

---

## Health Check

```
GET /api/system/health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

# AI Integration

Для AI-функций используется Groq API с Llama-моделью.

После получения обращения сервис:

1. Отправляет комментарий пользователя в AI Service.
2. AI анализирует сообщение.
3. Получает:
   - категорию обращения;
   - тональность сообщения;
   - автоматический ответ пользователю.
4. Сохраняет результат вместе с обращением

Пример:

Input:

```
Мне нужна консультация по вашему продукту
```

AI:

```
category: question

sentiment: neutral

response:
Спасибо за обращение. Мы свяжемся с вами в ближайшее время.
```

---

# AI Fallback

Если AI сервис недоступен:

- обращение сохраняется;
- email отправляется;
- API продолжает работать;
- используется стандартный ответ.

Это предотвращает падение сервиса при проблемах внешнего AI API.

---

# Email Integration

Используется SMTP Gmail.

После отправки формы:

1. Владелец получает уведомление о новом обращении.
2. Пользователь получает подтверждение.

---

# Rate Limiting

Для защиты от спама реализован rate limiting.

Настройки:

```
RATE_LIMIT_REQUESTS=10

RATE_LIMIT_WINDOW=60
```

Пример:

10 запросов за 60 секунд с одного клиента.

---

# Error Handling

Добавлен глобальный обработчик ошибок:

- корректные HTTP статус-коды;
- логирование исключений;
- безопасные ответы клиенту.

---

# Logging

Все важные события записываются в лог:

- API запросы;
- ошибки;
- ошибки AI;
- ошибки отправки email.

---

# Testing

Установка:

```bash
pip install -r requirements-dev.txt
```

Запуск:

```bash
pytest tests/ -v
```

---

# AI Usage During Development

Для разработки использовались AI-инструменты:

- генерация вспомогательного кода;
- анализ архитектуры;
- поиск ошибок;
- улучшение документации.

Все сгенерированные части были проверены и адаптированы вручную.

---

# Future Improvements

Возможные улучшения:

- PostgreSQL вместо SQLite
- Redis для rate limiting
- JWT authentication для админ-панели
- Kubernetes deployment
- CI/CD pipeline
- расширенная аналитика обращений

---

# License

MIT