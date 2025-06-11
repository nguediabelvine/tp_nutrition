from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("config.env")

# Configuration de la base de données PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nutrition_user:nutrition_password@localhost:5432/nutrition_db")

# Créer le moteur de base de données
engine = create_engine(
    DATABASE_URL,
    echo=True  # Afficher les requêtes SQL (à désactiver en production)
)

# Fonction pour créer toutes les tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Fonction pour obtenir une session de base de données
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session 