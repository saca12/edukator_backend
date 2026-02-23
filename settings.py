import dj_database_url
import os

INSTALLED_APPS = [
    # ...
    'corsheaders',
    'rest_framework', # Si vous utilisez DRF
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # DOIT être tout en haut
    'django.middleware.common.CommonMiddleware',
    # ...
]

CSRF_TRUSTED_ORIGINS = [
    "https://edukatorproj-pzxuqzfx6-saca12s-projects.vercel.app",
    "https://*.railway.app" # Optionnel mais recommandé
]
# Remplacez par l'URL réelle de votre projet Vercel
CORS_ALLOWED_ORIGINS = [
    "https://edukatorproj-pzxuqzfx6-saca12s-projects.vercel.app",
]

# Si vous voulez tester rapidement sans restriction (moins sécurisé)
# CORS_ALLOW_ALL_ORIGINS = True

# Railway injecte DATABASE_URL automatiquement
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}