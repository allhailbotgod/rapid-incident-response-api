# Rapid Incident Response API

A RESTful API for a Rapid Incident Response System built with **FastAPI**. The API serves as the backend for a React Native application, enabling users to report emergencies quickly while allowing emergency personnel to manage and respond to incidents efficiently.

---

## Overview

Rapid Incident Response API is designed to provide a centralised backend for emergency incident reporting and response management. It allows users to submit emergency reports with their location and supporting media while providing a secure platform for managing incidents throughout their lifecycle.

The project follows RESTful API principles and is built using a modular architecture to ensure scalability, maintainability, and ease of development.

---

## Features

- JWT Authentication
- User registration and login
- Role-based access control
- Emergency incident reporting
- GPS location support
- Image and video uploads
- Incident status tracking
- Incident priority classification
- PostgreSQL database integration
- Alembic database migrations
- Interactive API documentation with Swagger UI

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| Python | Backend Language |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database Migrations |
| Pydantic | Data Validation |
| JWT | Authentication |
| Uvicorn | ASGI Server |

---

## Project Structure

```text
.
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── agencies/
    ├── auth/
    ├── medic/
    ├── reports/
    ├── roles/
    ├── sos/
    ├── status/
    ├── users/
    ├── utils/
    ├── config.py
    ├── database.py
    ├── main.py
    ├── models.py
│   └── routers.py
│
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

The project follows a **Separation of Concerns** architecture where each feature is organised into its own module.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/allhailbotgod/rapid-incident-response-api.git

cd rapid-incident-response-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Linux/macOS**

```bash
source venv/bin/activate
```

**Windows**

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Rename the `.env.example` file in the project root to `.env`.

Edit necessary values

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost/database_name

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive documentation.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Development Status

This project is currently under active development.

Planned features include:

- Real-time incident updates
- Push notifications
- Automatic incident assignment
- Emergency contact notifications
- Incident analytics
- Administrative dashboard
- AI integration

---

## Author

Developed with ♥ by **Ezenwa Gerald**.

---

## License

This project is intended for educational purposes and personal development.