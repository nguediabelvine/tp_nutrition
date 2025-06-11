from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from database import get_session
from schemas import PlanRepasCreate, PlanRepasRead
from services import generate_plan_repas, get_plan_repas_by_id, get_plans_repas_utilisateur
from security import get_current_active_user
import datetime

router = APIRouter(prefix="/plans_repas", tags=["plans_repas"])

@router.post("/", response_model=PlanRepasRead)
def generate_plan_repas_route(plan: PlanRepasCreate, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    """Générer un plan de repas hebdomadaire pour un utilisateur"""
    try:
        plan_repas = generate_plan_repas(session, plan.utilisateur_id, plan.semaine)
        return plan_repas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du plan de repas")

@router.get("/{plan_id}", response_model=PlanRepasRead)
def get_plan_repas_route(plan_id: int, session: Session = Depends(get_session)):
    """Récupérer un plan de repas par son ID"""
    plan_repas = get_plan_repas_by_id(session, plan_id)
    if not plan_repas:
        raise HTTPException(status_code=404, detail="Plan de repas non trouvé")
    return plan_repas

@router.get("/utilisateur/{utilisateur_id}", response_model=List[PlanRepasRead])
def get_plans_repas_utilisateur_route(utilisateur_id: int, session: Session = Depends(get_session)):
    """Récupérer tous les plans de repas d'un utilisateur"""
    plans = get_plans_repas_utilisateur(session, utilisateur_id)
    return plans

@router.post("/generer-auto/{utilisateur_id}")
def generer_plan_repas_auto_route(utilisateur_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_active_user)):
    """Générer automatiquement un plan de repas pour la semaine en cours"""
    semaine_courante = datetime.date.today()
    # Ajuster au début de la semaine (lundi)
    jours_jusquau_lundi = semaine_courante.weekday()
    debut_semaine = semaine_courante - datetime.timedelta(days=jours_jusquau_lundi)
    
    try:
        plan_repas = generate_plan_repas(session, utilisateur_id, debut_semaine)
        return {"message": "Plan de repas généré avec succès", "plan_id": plan_repas.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du plan de repas") 