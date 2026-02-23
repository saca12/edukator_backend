## Intelligent Tutor Backend (Django + DRF)

This repository contains a **production‑ready Django REST backend** for an Intelligent Tutor Application targeting **primary and secondary** education. It exposes a JWT‑secured REST API for user management, pedagogical content, exercises, AI feedback, progress tracking, revision, notifications and offline sync.

### Architecture Overview

- **Frameworks**: Django 6, Django REST Framework, SimpleJWT, django‑filter, python‑dotenv.
- **Database**: PostgreSQL only.
- **Auth**: Custom `User` model with email login and `Student` profile.
- **Apps**:
  - `accounts`: users, students, JWT auth, profile & history.
  - `education`: grades, subjects, chapters, lessons and lesson content.
  - `exercises`: exercises, questions, answers, submissions.
  - `ai`: mock GPT‑style explanations, hints and error analysis.
  - `progress`: lesson progress aggregation and dashboards.
  - `revision`: revision sessions and needed‑revision listing.
  - `notifications`: achievements and notification center primitives.
  - `offline`: offline content registration and sync endpoints.
  - `core`: shared utilities, base models, permissions.

Each app has its own `README.md` documenting models, responsibilities and endpoints.

### Setup Instructions

1. **Create and activate a virtualenv**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

2. **Configure environment**

```bash
cp .env.example .env
# Edit .env to match your PostgreSQL credentials
```

3. **Run migrations and create superuser**

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Start the development server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

### Environment Variables

Loaded from `.env` via `python-dotenv`:

- **Django**
  - `DJANGO_SECRET_KEY`
  - `DJANGO_DEBUG`
  - `DJANGO_ALLOWED_HOSTS`
- **PostgreSQL**
  - `POSTGRES_DB`
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`
  - `POSTGRES_HOST`
  - `POSTGRES_PORT`
- **JWT**
  - `ACCESS_TOKEN_LIFETIME_MIN`
  - `REFRESH_TOKEN_LIFETIME_DAYS`
- **CORS**
  - `CORS_ALLOW_ALL_ORIGINS`

See `DATABASE.md` for more details on the database layer.

### API Authentication Flow

- **Register**: `POST /api/auth/register` → creates `User` + `Student` and returns **access** and **refresh** tokens.
- **Login**: `POST /api/auth/login` (SimpleJWT `TokenObtainPairView`) → returns **access** and **refresh**.
- **Authenticated requests**: include header `Authorization: Bearer <access_token>`.
- **Refresh**: `POST /api/auth/refresh-token` with `{"refresh": "<refresh_token>"}`.
- **Logout**: `POST /api/auth/logout` with `{"refresh": "<refresh_token>"}` to blacklist the token.
- **Current user**: `GET /api/auth/me`.

All other endpoints require a valid JWT and enforce **per‑user data isolation**.

### App‑Level Documentation

Each app provides:

- Purpose and responsibilities.
- Model descriptions.
- Exposed endpoints (method, URL, auth requirements, request/response examples).

Refer to the individual `README.md` files inside each app directory.

### How to Verify Endpoints

After starting the server:

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"StrongPass123","first_name":"Ada","last_name":"Lovelace"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"StrongPass123"}'

# Use returned access token
curl http://localhost:8000/api/subjects \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

For a full list of endpoints and example payloads, see each app’s README plus the verification section at the end of this document.

### Verification: Example curl/Postman Calls

- **Profile**

```bash
curl http://localhost:8000/api/users/profile \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

- **Exercises**

```bash
curl http://localhost:8000/api/exercises \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

- **Progress dashboard**

```bash
curl http://localhost:8000/api/progress/dashboard \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Import these endpoints into Postman by creating a collection with the same URLs and adding a **Bearer Token** auth using the JWT access token.

