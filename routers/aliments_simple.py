from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from database_simple import get_session
from schemas import AlimentCreate, AlimentRead
from models import Aliment
from security_simple import get_current_active_user
import json

router = APIRouter(prefix="/aliments", tags=["aliments"])

@router.post("/", response_model=AlimentRead)
def create_aliment_route(aliment: AlimentCreate, session: Session = Depends(get_session), user=Depends(get_current_active_user)):
    """Créer un nouvel aliment"""
    try:
        aliment_data = aliment.dict()
        # Convertir les allergènes en JSON string
        aliment_data["allergenes"] = json.dumps(aliment_data["allergenes"])
        aliment_obj = Aliment(**aliment_data)
        session.add(aliment_obj)
        session.commit()
        session.refresh(aliment_obj)
        return aliment_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'aliment")

@router.get("/{aliment_id}", response_model=AlimentRead)
def get_aliment_route(aliment_id: int, session: Session = Depends(get_session)):
    """Récupérer un aliment par son ID"""
    aliment = session.get(Aliment, aliment_id)
    if not aliment:
        raise HTTPException(status_code=404, detail="Aliment non trouvé")
    return aliment

@router.get("/", response_model=List[AlimentRead])
def search_aliments_route(q: str = Query("", description="Recherche par nom"), allergies: Optional[str] = Query(None), session: Session = Depends(get_session)):
    """Rechercher des aliments par nom (version simplifiée)"""
    query = select(Aliment)
    if q:
        query = query.where(Aliment.nom.contains(q))
    
    aliments = session.exec(query).all()
    
    # Filtrer par allergies si spécifiées
    if allergies:
        allergies_list = allergies.split(",")
        filtered_aliments = []
        for aliment in aliments:
            aliment_allergenes = json.loads(aliment.allergenes)
            if not set(aliment_allergenes) & set(allergies_list):
                filtered_aliments.append(aliment)
        aliments = filtered_aliments
    
    return aliments

@router.get("/tous/", response_model=List[AlimentRead])
def get_all_aliments_route(session: Session = Depends(get_session)):
    """Récupérer tous les aliments"""
    aliments = session.exec(select(Aliment)).all()
    # Convertir les allergènes JSON en listes pour la réponse
    for aliment in aliments:
        if isinstance(aliment.allergenes, str):
            try:
                aliment.allergenes = json.loads(aliment.allergenes)
            except:
                aliment.allergenes = []
    return aliments

@router.get("/categorie/{categorie}", response_model=List[AlimentRead])
def get_aliments_by_categorie_route(categorie: str, session: Session = Depends(get_session)):
    """Récupérer les aliments par catégorie"""
    aliments = session.exec(select(Aliment).where(Aliment.categorie == categorie)).all()
    # Convertir les allergènes JSON en listes pour la réponse
    for aliment in aliments:
        if isinstance(aliment.allergenes, str):
            try:
                aliment.allergenes = json.loads(aliment.allergenes)
            except:
                aliment.allergenes = []
    return aliments

@router.get("/faibles-calories/", response_model=List[AlimentRead])
def get_aliments_low_calories_route(max_calories: int = Query(300, description="Calories maximum"), session: Session = Depends(get_session)):
    """Récupérer les aliments faibles en calories"""
    aliments = session.exec(select(Aliment).where(Aliment.calories <= max_calories)).all()
    # Convertir les allergènes JSON en listes pour la réponse
    for aliment in aliments:
        if isinstance(aliment.allergenes, str):
            try:
                aliment.allergenes = json.loads(aliment.allergenes)
            except:
                aliment.allergenes = []
    return aliments 