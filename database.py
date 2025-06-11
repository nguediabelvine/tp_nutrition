from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("config.env")

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nutrition_user:nutrition_password@localhost:5432/nutrition_db")

# Créer le moteur de base de données
engine = create_engine(DATABASE_URL, echo=True)

# Fonction utilitaire pour obtenir une session
def get_session():
    with Session(engine) as session:
        yield session

# Fonction pour créer toutes les tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 