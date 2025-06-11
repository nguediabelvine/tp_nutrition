from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from database import get_session
from schemas import BuffetCreate, BuffetRead
from services import create_buffet, add_aliments_to_buffet, get_buffet_by_id, get_buffet_aliments
from security import get_current_active_user

router = APIRouter(prefix="/buffets", tags=["buffets"])

@router.post("/", response_model=BuffetRead)
def create_buffet_route(buffet: BuffetCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    """Créer un nouveau buffet"""
    try:
        buffet_obj = create_buffet(session, buffet.dict())
        return buffet_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du buffet")

@router.put("/{buffet_id}/aliments/")
def add_aliments_to_buffet_route(buffet_id: int, aliment_ids: List[int], session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    """Ajouter des aliments à un buffet"""
    try:
        buffet = add_aliments_to_buffet(session, buffet_id, aliment_ids)
        return {"message": f"{len(aliment_ids)} aliments ajoutés au buffet", "buffet_id": buffet.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout des aliments")

@router.get("/{buffet_id}", response_model=BuffetRead)
def get_buffet_route(buffet_id: int, session: Session = Depends(get_session)):
    """Récupérer un buffet par son ID"""
    buffet = get_buffet_by_id(session, buffet_id)
    if not buffet:
        raise HTTPException(status_code=404, detail="Buffet non trouvé")
    return buffet

@router.get("/{buffet_id}/aliments/")
def get_buffet_aliments_route(buffet_id: int, session: Session = Depends(get_session)):
    """Récupérer tous les aliments d'un buffet"""
    aliments = get_buffet_aliments(session, buffet_id)
    return {"buffet_id": buffet_id, "aliments": aliments} 