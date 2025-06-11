# API Nutritionnelle - Projet Universitaire

Une API RESTful complète pour des recommandations nutritionnelles, développée avec FastAPI, SQLModel et SQLite.

## 🚀 Fonctionnalités

- **Gestion des aliments** : CRUD complet pour les aliments avec informations nutritionnelles
- **Gestion des utilisateurs** : Inscription, authentification et profils utilisateurs
- **Recommandations nutritionnelles** : Algorithmes de recommandation basés sur les préférences
- **API RESTful** : Interface complète avec documentation automatique
- **Base de données SQLite** : Solution simple et portable

## 📋 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## 🛠️ Installation

### 1. Cloner le repository
```bash
git clone <votre-repo-url>
cd tp_nutrition
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
./start.sh
```

Ou manuellement :
```bash
# Créer la base de données
python3 -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"

# Charger les données initiales
python3 -c "from app.utils.data_loader import load_initial_data; load_initial_data()"

# Démarrer l'API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Accès à l'API

- **Interface Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health

## 📁 Structure du Projet

```
tp_nutrition/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée de l'application
│   ├── database.py             # Configuration de la base de données
│   ├── models.py               # Modèles SQLModel
│   ├── schemas.py              # Schémas Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Routes d'authentification
│   │   ├── foods.py            # Routes des aliments
│   │   ├── recommendations.py  # Routes des recommandations
│   │   └── users.py            # Routes des utilisateurs
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Logique d'authentification
│   │   ├── food_service.py     # Logique des aliments
│   │   └── recommendation_service.py # Logique des recommandations
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py      # Chargement des données initiales
│       └── security.py         # Utilitaires de sécurité
├── data/
│   └── initial_data.json       # Données initiales
├── requirements.txt            # Dépendances Python
├── start.sh                    # Script de démarrage
└── README.md                   # Documentation
```

## 🔧 Configuration

L'application utilise SQLite par défaut. La base de données sera créée automatiquement dans le fichier `nutrition.db`.

## 📊 Endpoints Principaux

### Authentification
- `POST /auth/register` - Inscription d'un utilisateur
- `POST /auth/login` - Connexion
- `POST /auth/logout` - Déconnexion

### Aliments
- `GET /foods/` - Liste des aliments
- `POST /foods/` - Créer un aliment
- `GET /foods/{food_id}` - Détails d'un aliment
- `PUT /foods/{food_id}` - Modifier un aliment
- `DELETE /foods/{food_id}` - Supprimer un aliment

### Recommandations
- `GET /recommendations/` - Obtenir des recommandations
- `POST /recommendations/` - Créer une recommandation personnalisée

### Utilisateurs
- `GET /users/me` - Profil utilisateur actuel
- `PUT /users/me` - Modifier le profil

## 🧪 Tests

Pour tester l'API, vous pouvez utiliser :

1. **L'interface Swagger** : http://localhost:8000/docs
2. **curl** :
```bash
# Test de santé
curl http://localhost:8000/health

# Liste des aliments
curl http://localhost:8000/foods/

# Créer un aliment
curl -X POST "http://localhost:8000/foods/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pomme",
    "calories": 52,
    "proteins": 0.3,
    "carbohydrates": 14,
    "fats": 0.2,
    "fiber": 2.4,
    "category": "Fruits"
  }'
```

## 📝 Exemple d'Utilisation

### Créer un nouvel aliment via Swagger UI

1. Ouvrez http://localhost:8000/docs
2. Trouvez l'endpoint `POST /foods/`
3. Cliquez sur "Try it out"
4. Remplissez le formulaire avec les données de l'aliment
5. Cliquez sur "Execute"

### Exemple de données pour un aliment :
```json
{
  "name": "Banane",
  "calories": 89,
  "proteins": 1.1,
  "carbohydrates": 23,
  "fats": 0.3,
  "fiber": 2.6,
  "category": "Fruits",
  "vitamins": "[\"B6\", \"C\"]",
  "minerals": "[\"Potassium\", \"Magnesium\"]"
}
```

## 🚀 Déploiement

Cette version utilise SQLite, ce qui la rend portable et facile à déployer. Pour un environnement de production, considérez :

1. Utiliser PostgreSQL ou MySQL
2. Ajouter des variables d'environnement pour la configuration
3. Implémenter une authentification plus robuste
4. Ajouter des tests automatisés

## 📞 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur GitHub.

## 📄 Licence

Ce projet est développé dans le cadre d'un projet universitaire. 