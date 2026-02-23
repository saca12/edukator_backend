import dj_database_url
import os

# Sécurité
SECRET_KEY = os.environ.get('SECRET_KEY', '16269758h')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['.railway.app', 'votre-domaine.com'] # Accepte le domaine Railway

# Base de données
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# Middlewares (ajoutez WhiteNoise juste après SecurityMiddleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

# Fichiers Statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'