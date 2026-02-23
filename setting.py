import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Définit BASE_DIR proprement
BASE_DIR = Path(__file__).resolve().parent

# Charge le .env SEULEMENT s'il existe (donc en local)
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# ... reste de ton code DATABASES ...
# Sécurité
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*'] # À affiner plus tard avec ton URL Render

# Base de données (Utilise la variable d'env DATABASE_URL de Render)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}
# TEST DE DÉBOGAGE (à supprimer après)
if os.environ.get('RENDER'):
    print("--- DEBUG RENDER ---")
    print(f"DATABASE_URL trouvée : {os.environ.get('DATABASE_URL') is not None}")
    print(f"HOST utilisé : {DATABASES['default'].get('HOST')}")
    print("--------------------")
# Sécurité supplémentaire : si DATABASE_URL est vide (erreur de config), 
# on remet l'ancienne config pour ne pas casser ton local
if not DATABASES['default']:
    DATABASES['default'] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "tuteur_ia"),
        "USER": os.getenv("POSTGRES_USER", "tuteur_ia"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "tuteur_ia"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
# Fichiers statiques (indispensable pour WhiteNoise)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
