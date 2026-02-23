## Accounts App

### Purpose

The `accounts` app manages:

- Custom `User` model (email‑based login).
- `Student` profile.
- Authentication and JWT token flow.
- User profile, progress and history endpoints.

### Models

- **User**
  - **id**: `UUIDField`, primary key.
  - **email**: `EmailField`, unique, indexed, used for login.
  - **password**: hashed (via `AbstractBaseUser`).
  - **created_at**: `DateTimeField`.
  - **is_active**, **is_staff**, **is_superuser**: standard Django flags.

- **Student**
  - **id**: `UUIDField`, primary key.
  - **user**: `OneToOneField` → `User`.
  - **first_name**, **last_name**: `CharField`.
  - **date_of_birth**: `DateField`, optional.
  - **current_grade**: `ForeignKey` → `education.Grade`.
  - **created_at**: `DateTimeField`.
  - **indexes**: composite index on `(last_name, first_name)` for fast lookup.

### Exposed API Endpoints

All URLs are prefixed with `/api/` by the project router.

- **POST `/api/auth/register`**
  - **Auth**: public.
  - **Body**:
    - `email` (string)
    - `password` (string, min 8)
    - `first_name`, `last_name`
    - `date_of_birth` (optional, `YYYY-MM-DD`)
    - `current_grade` (optional, UUID of `Grade`)
  - **Response (201)**:
    - `user`: `User` object.
    - `access`: JWT access token.
    - `refresh`: JWT refresh token.

- **POST `/api/auth/login`**
  - **Auth**: public.
  - **Body**:
    - `email`, `password`
  - **Response (200)**: SimpleJWT pair `{ "access": "...", "refresh": "..." }`.

- **POST `/api/auth/logout`**
  - **Auth**: required.
  - **Body**: `{ "refresh": "<refresh_token>" }`.
  - **Response (204)**: refresh token blacklisted (best‑effort).

- **POST `/api/auth/refresh-token`**
  - **Auth**: public.
  - **Body**: `{ "refresh": "<refresh_token>" }`.
  - **Response (200)**: `{ "access": "<new_access_token>" }`.

- **GET `/api/auth/me`**
  - **Auth**: required.
  - **Response (200)**:
    - `user`: basic user info.
    - `student`: student profile.

- **GET `/api/users/profile`**
  - **Auth**: required.
  - **Response (200)**: full `Student` profile.

- **PUT `/api/users/profile`**
  - **Auth**: required.
  - **Body**: any subset of student fields (`first_name`, `last_name`, `date_of_birth`, `current_grade`).
  - **Response (200)**: updated profile.

- **GET `/api/users/progress`**
  - **Auth**: required.
  - **Response (200)**: progress overview (delegates to `progress` app service).

- **GET `/api/users/history`**
  - **Auth**: required.
  - **Response (200)**: chronological activity history.

### Business Rules

- A `Student` profile is created or ensured for each authenticated `User`.
- Users can only access their **own** profile, progress and history (enforced by permissions and per‑query filters).
- Email is the unique login identifier.

### Verification Examples

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"StrongPass123","first_name":"Ada","last_name":"Lovelace"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"StrongPass123"}'

# Current user
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

