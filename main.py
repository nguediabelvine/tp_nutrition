from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel
from database import engine, create_db_and_tables
from routers import aliments, utilisateurs, plans_repas, buffets
from utils import load_initial_data
from security import create_access_token
from datetime import timedelta
import os

# Créer l'application FastAPI
app = FastAPI(
    title="API Nutritionnelle - Université de Yaoundé I",
    description="API RESTful pour la gestion de buffets et recommandation alimentaire",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Inclure les routeurs
app.include_router(aliments.router)
app.include_router(utilisateurs.router)
app.include_router(plans_repas.router)
app.include_router(buffets.router)

@app.on_event("startup")
async def on_startup():
    """Initialisation de l'application au démarrage"""
    # Créer les tables
    create_db_and_tables()
    
    # Charger les données initiales si configuré
    if os.getenv("LOAD_INITIAL_DATA", "false").lower() == "true":
        from sqlmodel import Session
        with Session(engine) as session:
            load_initial_data(session)
            print("✅ Données initiales chargées avec succès")

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "API Nutritionnelle - Université de Yaoundé I",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Point de contrôle de santé de l'API"""
    return {"status": "healthy", "message": "API opérationnelle"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 