import dj_database_url
import os

# Sécurité
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*'] # À affiner plus tard avec ton URL Render

# Base de données (Utilise la variable d'env DATABASE_URL de Render)
DATABASES = {
    'default': dj_database_url.config(
        # Cette ligne récupère la variable DATABASE_URL de Render
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Fichiers statiques (indispensable pour WhiteNoise)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
