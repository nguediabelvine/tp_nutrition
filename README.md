# API de Recommandation Nutritionnelle - Version Simplifiée

## Description

Cette API de recommandation nutritionnelle est une version simplifiée utilisant FastAPI, SQLModel et SQLite. Elle permet de gérer des aliments, utilisateurs, plans de repas et buffets avec authentification par token.

## Fonctionnalités

- **Gestion des aliments** : CRUD complet pour les aliments avec données nutritionnelles
- **Gestion des utilisateurs** : Inscription, connexion et authentification par token
- **Plans de repas** : Création et gestion de plans de repas personnalisés
- **Buffets** : Gestion de buffets avec sélection d'aliments
- **Données initiales** : Chargement automatique des données de repas canadiens
- **API REST** : Interface Swagger/OpenAPI complète

## Structure du Projet

```
tp_nutrition/
├── app/                    # Modules de l'application
│   ├── routers/           # Routes API
│   │   ├── auth.py        # Authentification
│   │   ├── aliments.py    # Gestion des aliments
│   │   ├── users.py       # Gestion des utilisateurs
│   │   ├── plans.py       # Plans de repas
│   │   └── buffets.py     # Gestion des buffets
├── data/                  # Données initiales
│   └── repas_canadiens.json
├── tests/                 # Tests unitaires
├── scripts/               # Scripts utilitaires
├── models.py              # Modèles SQLModel
├── schemas.py             # Schémas Pydantic
├── database_simple.py     # Configuration base de données SQLite
├── security_simple.py     # Authentification et sécurité
├── utils_simple.py        # Utilitaires
├── main_simple.py         # Point d'entrée principal
├── requirements_simple.txt # Dépendances
└── README.md              # Documentation
```

## Installation et Démarrage

### Prérequis

- Python 3.8+
- pip
- docker
- docker-compose

### Installation

1. **Cloner le projet**
```bash
git clone <votre-repo-github>
cd tp_nutrition
```

2. **Installer les dépendances**
```bash
pip install -r requirements_simple.txt
```

3.1 **Démarrer l'API**
```bash
docker-compose up 
```

3.2 **Démarrer version simple de l'API**
```bash
python main_simple.py
```

L'API sera accessible sur `http://localhost:8000`

### Interface Swagger

Accédez à la documentation interactive de l'API :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Utilisation de l'API

### 1. Créer un utilisateur

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "nom": "John Doe"
  }'
```

### 2. Se connecter

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "password123"
  }'
```

### 3. Créer un aliment

```bash
curl -X POST "http://localhost:8000/aliments/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Pomme",
    "calories": 52,
    "proteines": 0.3,
    "glucides": 14,
    "lipides": 0.2,
    "fibres": 2.4,
    "categorie": "Fruits"
  }'
```

### 4. Consulter les aliments

```bash
curl -X GET "http://localhost:8000/aliments/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Endpoints Principaux

### Authentification
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion

### Aliments
- `GET /aliments/` - Liste des aliments
- `POST /aliments/` - Créer un aliment
- `GET /aliments/{id}` - Détails d'un aliment
- `PUT /aliments/{id}` - Modifier un aliment
- `DELETE /aliments/{id}` - Supprimer un aliment

### Utilisateurs
- `GET /users/me` - Profil utilisateur
- `PUT /users/me` - Modifier le profil

### Plans de Repas
- `GET /plans/` - Liste des plans
- `POST /plans/` - Créer un plan
- `GET /plans/{id}` - Détails d'un plan

### Buffets
- `GET /buffets/` - Liste des buffets
- `POST /buffets/` - Créer un buffet
- `GET /buffets/{id}` - Détails d'un buffet

## Tests

Exécuter les tests unitaires :

```bash
python -m pytest tests/
```

## Données Initiales

L'API charge automatiquement les données de repas canadiens au démarrage. Ces données sont stockées dans `data/repas_canadiens.json`.

## Version Simplifiée

Cette version utilise :
- **SQLite** au lieu de PostgreSQL
- **Pas de pgvector** ni d'embeddings
- **Authentification simple** avec JWT
- **Structure simplifiée** pour faciliter le développement

## Développement

### Structure des Modèles

- **Aliment** : nom, calories, protéines, glucides, lipides, fibres, catégorie
- **User** : email, nom, mot de passe hashé
- **PlanRepas** : nom, description, aliments (JSON)
- **Buffet** : nom, description, aliments (JSON)

### Sécurité

- Authentification par token JWT
- Mots de passe hashés avec bcrypt
- Validation des données avec Pydantic

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est destiné à des fins éducatives.

## Contact

Pour toute question concernant ce projet, contactez votre professeur.  
