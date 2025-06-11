from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List, Optional
from database import get_session
from schemas import UtilisateurCreate, UtilisateurRead
from services import create_utilisateur, get_utilisateur_by_id, get_utilisateur_by_email, authenticate_user
from security import get_current_active_user, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])

@router.post("/", response_model=UtilisateurRead)
def create_utilisateur_route(user: UtilisateurCreate, session: Session = Depends(get_session)):
    """Créer un nouvel utilisateur"""
    # Vérifier si l'email existe déjà
    existing_user = get_utilisateur_by_email(session, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Un utilisateur avec cet email existe déjà")
    
    try:
        user_data = user.dict()
        return create_utilisateur(session, user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'utilisateur")

@router.get("/{user_id}", response_model=UtilisateurRead)
def get_utilisateur_route(user_id: int, session: Session = Depends(get_session)):
    """Récupérer un utilisateur par son ID"""
    utilisateur = get_utilisateur_by_id(session, user_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.get("/", response_model=UtilisateurRead)
def get_utilisateur_by_email_route(email: str = Query(...), session: Session = Depends(get_session)):
    """Récupérer un utilisateur par son email"""
    utilisateur = get_utilisateur_by_email(session, email)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.post("/auth/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Authentifier un utilisateur et retourner un token d'accès"""
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
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