#!/bin/bash

echo "🚀 Démarrage de l'API Nutritionnelle (Version SQLite)"

# Vérifier si Python 3.10+ est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez installer Python 3.10+ d'abord."
    exit 1
fi

# Vérifier la version de Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version détecté. Python 3.10+ est requis."
    exit 1
fi

echo "✅ Python $python_version détecté"

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip3 install fastapi uvicorn sqlmodel pydantic email-validator

# Créer le fichier de base de données SQLite s'il n'existe pas
if [ ! -f "nutrition.db" ]; then
    echo "🗄️ Création de la base de données SQLite..."
    python3 -c "
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print('Base de données créée avec succès!')
"
fi

# Charger les données initiales
echo "📊 Chargement des données initiales..."
python3 -c "
from app.utils.data_loader import load_initial_data
load_initial_data()
print('Données initiales chargées avec succès!')
"

echo "🚀 Démarrage de l'API..."
echo "🌐 Interface Swagger: http://localhost:8000/docs"
echo "📖 Documentation ReDoc: http://localhost:8000/redoc"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "📝 Pour arrêter l'API: Ctrl+C"

# Démarrer l'API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 