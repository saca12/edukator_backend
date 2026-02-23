#!/usr/bin/env bash
set -o errexit

# Installation propre
pip install -r requirements.txt

# Préparation des fichiers pour la prod
python manage.py collectstatic --no-input

# Migration vers la base de données configurée dans DATABASE_URL
python manage.py migrate --no-input