## PostgreSQL Setup

This project uses **PostgreSQL** as the only database engine.

### Local Installation

- **Install PostgreSQL** (version 13+ recommended).
- Create a database and user that match the values in `.env`:

```bash
sudo -u postgres createuser -P tuteur_ia        # set password: tuteur_ia
sudo -u postgres createdb -O tuteur_ia tuteur_ia
```

Update your local `.env` as needed.

### Django Database Configuration

- The database is configured in `TuteurIA/settings.py` via environment variables:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "tuteur_ia"),
        "USER": os.getenv("POSTGRES_USER", "tuteur_ia"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "tuteur_ia"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
```

## Schema Overview

High‑level groups:

- **accounts**: `User`, `Student`
- **education**: `Grade`, `Subject`, `Chapter`, `Lesson`, `LessonContent`
- **exercises**: `Difficulty`, `ExerciseType`, `Exercise`, `Question`, `Answer`, `UserAnswer`
- **ai**: `ErrorAnalysis`
- **progress**: `Progress`
- **revision**: `RevisionSession`
- **notifications**: `Achievement`, `Notification`
- **offline**: `OfflineContent`

See each app `README.md` for model‑level descriptions and relations.

## Migrations Strategy

- Migrations are stored under each app’s `migrations/` folder.
- Standard workflow:

```bash
python manage.py makemigrations
python manage.py migrate
```

- Never edit existing, applied migrations in production. Instead, create new migrations for schema changes.
- For CI/CD, always run `python manage.py migrate --noinput` on deploy.

## Indexing Strategy

- Commonly queried fields have explicit indexes, for example:
  - `accounts.User.email` (unique + db_index)
  - `accounts.Student` name composite index
  - `education.Grade.level`
  - `exercises.UserAnswer.student, submission_date`
  - `progress.Progress.student, last_activity`
  - `offline.OfflineContent.student, content_type`

Additional indexes can be added in migrations if new query patterns appear.

## Backups & Restore

### Backup

```bash
pg_dump -U tuteur_ia -h localhost -Fc tuteur_ia > backup.dump
```

### Restore

```bash
pg_restore -U tuteur_ia -h localhost -d tuteur_ia --clean backup.dump
```

Integrate these commands into your infrastructure (cron, CI/CD, or managed backups).

## Environment Configuration

Sensitive configuration is stored in `.env` and loaded via `python-dotenv`.

Key variables:

- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`

Ensure `.env` is **not committed** to version control. Use `.env.example` as reference.

