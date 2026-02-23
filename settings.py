import dj_database_url
import os

# ...

DATABASES = {
    'default': dj_database_url.config(
        # On récupère la variable DATABASE_URL de Railway
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Sécurité supplémentaire : si DATABASE_URL est vide, 
# dj-database-url pourrait causer une erreur. 
# Assurez-vous que la variable est BIEN nommée DATABASE_URL sur Railway.