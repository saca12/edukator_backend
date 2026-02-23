import dj_database_url
import os

# On ne définit PLUS les HOST, USER, etc. manuellement ici.
# On laisse dj-database-url tout extraire de la variable Railway.
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

print(f"DEBUG: DATABASE_URL is {os.environ.get('DATABASE_URL')}")