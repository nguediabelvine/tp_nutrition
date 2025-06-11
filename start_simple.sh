#!/bin/bash

# Script de démarrage pour l'API Nutritionnelle - Version Simplifiée
echo "🚀 Démarrage de l'API de Recommandation Nutritionnelle - Version Simplifiée"
echo "================================================================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si les dépendances sont installées
echo "📦 Vérification des dépendances..."
if ! python3 -c "import fastapi, sqlmodel, uvicorn" &> /dev/null; then
    echo "📥 Installation des dépendances..."
    pip install -r requirements_simple.txt
fi

# Créer la base de données si elle n'existe pas
echo "🗄️  Initialisation de la base de données..."
python3 -c "
from database_simple import engine
from models import Base
Base.metadata.create_all(bind=engine)
print('✅ Base de données initialisée')
"

# Charger les données initiales
echo "📊 Chargement des données initiales..."
python3 -c "
from utils_simple import load_initial_data
load_initial_data()
print('✅ Données initiales chargées')
"

echo ""
echo "🌐 Démarrage du serveur..."
echo "📍 API accessible sur: http://localhost:8000"
echo "📚 Documentation Swagger: http://localhost:8000/docs"
echo "📖 Documentation ReDoc: http://localhost:8000/redoc"
echo ""
echo "🛑 Pour arrêter le serveur, appuyez sur Ctrl+C"
echo "================================================================"

# Démarrer l'API
python3 main_simple.py 