# Démonstration de l'API Nutritionnelle - Version Simplifiée

## 🎯 Objectif du Projet

Cette API de recommandation nutritionnelle a été développée dans le cadre d'un projet universitaire utilisant :
- **FastAPI** pour l'API REST
- **SQLModel** pour les modèles de données
- **SQLite** pour la base de données
- **JWT** pour l'authentification

## 🚀 Comment Démarrer le Projet

### Option 1 : Script automatique (Recommandé)
```bash
./start_simple.sh
```

### Option 2 : Manuel
```bash
# Installer les dépendances
pip install -r requirements_simple.txt

# Démarrer l'API
python main_simple.py
```

## 📚 Interface de Test

Une fois l'API démarrée, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🧪 Tests Recommandés pour la Démonstration

### 1. Test de Santé
```bash
curl http://localhost:8000/health
```

### 2. Créer un Utilisateur
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof@universite.com",
    "password": "password123",
    "nom": "Professeur Test"
  }'
```

### 3. Se Connecter
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "prof@universite.com",
    "password": "password123"
  }'
```

### 4. Consulter les Aliments (avec token)
```bash
curl -X GET "http://localhost:8000/aliments/" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

### 5. Créer un Aliment
```bash
curl -X POST "http://localhost:8000/aliments/" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Banane",
    "calories": 89,
    "proteines": 1.1,
    "glucides": 23,
    "lipides": 0.3,
    "fibres": 2.6,
    "categorie": "Fruits"
  }'
```

### 6. Créer un Plan de Repas
```bash
curl -X POST "http://localhost:8000/plans/" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Petit-déjeuner équilibré",
    "description": "Un petit-déjeuner riche en fibres et protéines",
    "aliments": ["1", "2", "3"]
  }'
```

## 📊 Fonctionnalités Implémentées

### ✅ Authentification
- Inscription utilisateur
- Connexion avec JWT
- Protection des routes

### ✅ Gestion des Aliments
- CRUD complet (Create, Read, Update, Delete)
- Données nutritionnelles complètes
- Catégorisation

### ✅ Plans de Repas
- Création de plans personnalisés
- Association d'aliments
- Gestion des utilisateurs

### ✅ Buffets
- Création de buffets
- Sélection d'aliments multiples

### ✅ Données Initiales
- Chargement automatique des repas canadiens
- Base de données pré-remplie

## 🔧 Architecture Technique

### Modèles de Données
- **Aliment** : nom, calories, protéines, glucides, lipides, fibres, catégorie
- **User** : email, nom, mot de passe hashé
- **PlanRepas** : nom, description, aliments (JSON)
- **Buffet** : nom, description, aliments (JSON)

### Sécurité
- Authentification JWT
- Hachage des mots de passe avec bcrypt
- Validation des données avec Pydantic

### Base de Données
- SQLite pour la simplicité
- Schéma automatiquement créé
- Données initiales chargées au démarrage

## 📁 Structure des Fichiers

```
tp_nutrition/
├── main_simple.py          # Point d'entrée principal
├── models.py               # Modèles SQLModel
├── schemas.py              # Schémas Pydantic
├── database_simple.py      # Configuration SQLite
├── security_simple.py      # Authentification JWT
├── utils_simple.py         # Utilitaires et chargement de données
├── requirements_simple.txt # Dépendances Python
├── start_simple.sh         # Script de démarrage
├── app/                    # Structure modulaire
│   ├── routers/           # Routes API
│   ├── services/          # Logique métier
│   └── utils/             # Utilitaires
├── data/                  # Données initiales
├── tests/                 # Tests unitaires
└── scripts/               # Scripts utilitaires
```

## 🎓 Points d'Évaluation

### Code
- ✅ Architecture propre et modulaire
- ✅ Séparation des responsabilités
- ✅ Gestion d'erreurs appropriée
- ✅ Documentation du code

### API
- ✅ Endpoints RESTful
- ✅ Authentification sécurisée
- ✅ Validation des données
- ✅ Documentation automatique (Swagger)

### Base de Données
- ✅ Modèles bien définis
- ✅ Relations appropriées
- ✅ Données initiales
- ✅ Migrations automatiques

### Tests
- ✅ Tests unitaires inclus
- ✅ Couverture des fonctionnalités principales

## 🚀 Améliorations Futures

Cette version simplifiée peut être étendue avec :
- PostgreSQL et pgvector pour la recherche sémantique
- Algorithmes de recommandation avancés
- Interface utilisateur web
- Tests d'intégration complets
- Déploiement Docker

## 📞 Support

Pour toute question ou problème lors de la démonstration, les logs de l'API fournissent des informations détaillées sur les erreurs éventuelles. 