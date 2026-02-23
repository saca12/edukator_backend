import dj_database_url
import os

# settings.py

INSTALLED_APPS = [
    ...,
    'corsheaders',  #
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # DOIT ÊTRE EN PREMIER
    'django.middleware.common.CommonMiddleware',
    ...
]

# Autorisez votre domaine Vercel spécifique
CORS_ALLOWED_ORIGINS = [
    "https://edukator-student.vercel.app",
]

# Si vous voulez aussi autoriser le mode développement local
CORS_ALLOWED_ORIGIN_WHITELIST = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# Railway injecte DATABASE_URL automatiquement
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}