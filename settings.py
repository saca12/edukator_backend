import dj_database_url
import os

# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps tierces
    'corsheaders',
    'rest_framework', # Si vous utilisez Django Rest Framework
    
    # Vos applications locales (selon votre DATABASE.md)
    'accounts',
    'education',
    'exercises',
    'ai',
    'progress',
    'revision',
    'notifications',
    'offline',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Doit être en premier
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Pour les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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