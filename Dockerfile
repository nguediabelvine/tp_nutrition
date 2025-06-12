# choix de mon image 
FROM python:3.11-slim

#  je defini répertoire de travail
WORKDIR /app

# installation les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances
COPY requirements_simple.txt .

# installation les dépendances
RUN pip install --no-cache-dir -r requirements_simple.txt

# Copier le reste du projet
COPY . .

# Exposer le port de l’API
EXPOSE 8000

# Lancer FastAPI avec Uvicorn
CMD ["uvicorn", "main_simple:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
