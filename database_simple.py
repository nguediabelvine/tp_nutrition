from sqlmodel import SQLModel, create_engine, Session
import os

# Configuration de la base de données SQLite pour les tests
DATABASE_URL = "sqlite:///./nutrition_test.db"

# Créer le moteur de base de données
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

# Fonction utilitaire pour obtenir une session
def get_session():
    with Session(engine) as session:
        yield session

# Fonction pour créer toutes les tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 