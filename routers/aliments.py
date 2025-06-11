from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from database import get_session
from schemas import AlimentCreate, AlimentRead
from services import create_aliment, get_aliment, search_aliments, get_all_aliments, get_aliments_by_categorie, get_aliments_low_calories, recommend_aliments
from security import get_current_active_user

router = APIRouter(prefix="/aliments", tags=["aliments"])

@router.post("/", response_model=AlimentRead)
def create_aliment_route(aliment: AlimentCreate, session: Session = Depends(get_session), user=Depends(get_current_active_user)):
    """Créer un nouvel aliment"""
    try:
        return create_aliment(session, aliment.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'aliment")

@router.get("/{aliment_id}", response_model=AlimentRead)
def get_aliment_route(aliment_id: int, session: Session = Depends(get_session)):
    """Récupérer un aliment par son ID"""
    aliment = get_aliment(session, aliment_id)
    if not aliment:
        raise HTTPException(status_code=404, detail="Aliment non trouvé")
    return aliment

@router.get("/", response_model=List[AlimentRead])
def search_aliments_route(q: str = Query("", description="Recherche sémantique"), allergies: Optional[str] = Query(None), session: Session = Depends(get_session)):
    """Rechercher des aliments par requête sémantique"""
    allergies_list = allergies.split(",") if allergies else []
    return search_aliments(session, q, allergies_list)

@router.get("/tous/", response_model=List[AlimentRead])
def get_all_aliments_route(session: Session = Depends(get_session)):
    """Récupérer tous les aliments"""
    return get_all_aliments(session)

@router.get("/categorie/{categorie}", response_model=List[AlimentRead])
def get_aliments_by_categorie_route(categorie: str, session: Session = Depends(get_session)):
    """Récupérer les aliments par catégorie"""
    return get_aliments_by_categorie(session, categorie)

@router.get("/faibles-calories/", response_model=List[AlimentRead])
def get_aliments_low_calories_route(max_calories: int = Query(300, description="Calories maximum"), session: Session = Depends(get_session)):
    """Récupérer les aliments faibles en calories"""
    return get_aliments_low_calories(session, max_calories)

@router.get("/recommandations/", response_model=List[AlimentRead])
def get_recommendations_route(
    query: str = Query(..., description="Requête pour les recommandations"),
    allergies: Optional[str] = Query(None, description="Allergies séparées par des virgules"),
    max_calories: int = Query(800, description="Calories maximum"),
    session: Session = Depends(get_session)
):
    """Obtenir des recommandations d'aliments personnalisées"""
    allergies_list = allergies.split(",") if allergies else []
    return recommend_aliments(session, query, allergies_list, max_calories) 