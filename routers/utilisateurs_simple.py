from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List, Optional
from database_simple import get_session
from schemas import UtilisateurCreate, UtilisateurRead
from models import Utilisateur
from security_simple import get_current_active_user, create_access_token, get_password_hash, verify_password
from datetime import timedelta
import json

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])

@router.post("/", response_model=UtilisateurRead)
def create_utilisateur_route(user: UtilisateurCreate, session: Session = Depends(get_session)):
    """Créer un nouvel utilisateur"""
    # Vérifier si l'email existe déjà
    existing_user = session.exec(select(Utilisateur).where(Utilisateur.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Un utilisateur avec cet email existe déjà")
    
    try:
        user_data = user.dict()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        # Convertir les allergies en JSON string
        user_data["allergies"] = json.dumps(user_data["allergies"])
        user_obj = Utilisateur(**user_data)
        session.add(user_obj)
        session.commit()
        session.refresh(user_obj)
        return user_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'utilisateur")

@router.get("/{user_id}", response_model=UtilisateurRead)
def get_utilisateur_route(user_id: int, session: Session = Depends(get_session)):
    """Récupérer un utilisateur par son ID"""
    utilisateur = session.get(Utilisateur, user_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.get("/", response_model=UtilisateurRead)
def get_utilisateur_by_email_route(email: str = Query(...), session: Session = Depends(get_session)):
    """Récupérer un utilisateur par son email"""
    utilisateur = session.exec(select(Utilisateur).where(Utilisateur.email == email)).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.post("/auth/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Authentifier un utilisateur et retourner un token d'accès"""
    user = session.exec(select(Utilisateur).where(Utilisateur.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }

@router.get("/me/", response_model=UtilisateurRead)
def read_users_me(current_user=Depends(get_current_active_user)):
    """Récupérer les informations de l'utilisateur connecté"""
    return current_user 