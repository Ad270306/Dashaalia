FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers Python dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir pandas pymongo

# Commande par défaut
CMD ["python", "importer.py"]
