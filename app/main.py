from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.database import create_db_and_tables
from app.routers import foods
from app.schemas import HealthCheck

# Créer l'application FastAPI
app = FastAPI(
    title="API Nutritionnelle",
    description="API RESTful pour la gestion d'aliments et recommandations nutritionnelles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(foods.router, prefix="/api/v1")

# Endpoint de santé
@app.get("/health", response_model=HealthCheck, tags=["health"])
def health_check():
    """Vérifier l'état de l'API"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow()
    )

# Endpoint racine
@app.get("/", tags=["root"])
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API Nutritionnelle",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }

# Événement de démarrage
@app.on_event("startup")
def startup_event():
    """Créer les tables de la base de données au démarrage"""
    create_db_and_tables()
    print("✅ Base de données initialisée avec succès!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 