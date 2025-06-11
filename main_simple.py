from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel
from database_simple import engine, create_db_and_tables, get_session
from routers.aliments_simple import router as aliments_router
from routers.utilisateurs_simple import router as utilisateurs_router
from utils_simple import load_initial_data
from security_simple import create_access_token
from datetime import timedelta
import os

# Créer l'application FastAPI
app = FastAPI(
    title="API Nutritionnelle - Université de Yaoundé I (Version Simple)",
    description="API RESTful pour la gestion de buffets et recommandation alimentaire",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Inclure les routeurs simplifiés
app.include_router(aliments_router)
app.include_router(utilisateurs_router)

@app.on_event("startup")
async def on_startup():
    """Initialisation de l'application au démarrage"""
    # Créer les tables
    create_db_and_tables()
    
    # Charger les données initiales si configuré
    if os.getenv("LOAD_INITIAL_DATA", "true").lower() == "true":
        from sqlmodel import Session
        with Session(engine) as session:
            load_initial_data(session)
            print("✅ Données initiales chargées avec succès")

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "API Nutritionnelle - Université de Yaoundé I (Version Simple)",
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