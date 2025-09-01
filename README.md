# Auth Service

A Django-based authentication microservice built for **Bill Station** internship task.  
It provides user registration, login with JWT, password reset with Redis, and deployment readiness.

---

## 🚀 Features

- **PostgreSQL integration** (via `dj_database_url`) for production-ready database support.
- **Custom User model** with email as username for modern auth workflows.
- **JWT authentication** (via `rest_framework_simplejwt`) for secure stateless login.
- **Password reset with Redis**:
  - Reset tokens cached for 10 minutes.
  - Password securely updated after token verification.
- **Swagger/OpenAPI docs** (via `drf_yasg`) for easy API exploration.
- **Custom response format** using DRF renderers & exception handlers for a more friendly api response.

---

## ⚙️ Environment Variables

Create a `.env` file in the project root or use the sample in the .env-example file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
```

---

## 📦 Setup Instructions

1. Clone repo and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:

   ```bash
   python manage.py migrate
   ```

3. Start development server:

   ```bash
   python manage.py runserver
   ```

---

## 🔑 API Endpoints

- **Register:** `POST /api/register/`
- **Login (JWT):** `POST /api/login/`
- **Request password reset:** `POST /api/password-reset/request/`
- **Reset password:** `POST /api/password-reset/`

Swagger UI available at:

```bash
/docs/
```

---

## 🛠 Deployment

- Configured for **Railway/Render** deployment.
- Environment variables control `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, and `DEBUG`.

### Deployment Command

In production, run with **Gunicorn** instead of the dev server:

```bash
gunicorn auth_service.wsgi:application --bind 0.0.0.0:$PORT
```

If using a **Procfile** (Heroku/Railway style):

```
web: gunicorn auth_service.wsgi:application --bind 0.0.0.0:$PORT
```

### Static Files (Optional but Recommended)

Even for a pure API, Django Admin needs static files.  
Add this in `settings.py`:

```python
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
```

Then before deploying, run:

```bash
python manage.py collectstatic --noinput
```
