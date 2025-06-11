from typing import List, Optional
from sqlmodel import Session, select
from models import Aliment, Utilisateur, PlanRepas, Buffet, RepasJour, AlimentRepasJour, BuffetAliment
from embedding import embedding_service
from security import get_password_hash
import random
import datetime

# CRUD Aliment

def create_aliment(session: Session, aliment_data: dict) -> Aliment:
    """Créer un nouvel aliment avec embedding"""
    embedding = embedding_service.embed(aliment_data["nom"])
    aliment = Aliment(**aliment_data, embedding=embedding)
    session.add(aliment)
    session.commit()
    session.refresh(aliment)
    return aliment

def get_aliment(session: Session, aliment_id: int) -> Optional[Aliment]:
    """Récupérer un aliment par son ID"""
    return session.get(Aliment, aliment_id)

def search_aliments(session: Session, query: str, allergies: Optional[List[str]] = None, top_k: int = 10) -> List[Aliment]:
    """Recherche sémantique d'aliments avec filtrage par allergies"""
    query_embedding = embedding_service.embed(query)
    
    # Recherche par similarité cosinus avec pgvector
    sql = f"""
        SELECT *, (embedding <#> '[{','.join(map(str, query_embedding))}]') AS distance
        FROM aliment
        ORDER BY distance ASC
        LIMIT {top_k}
    """
    results = session.exec(sql)
    aliments = []
    for row in results:
        aliment_dict = dict(row)
        aliment = Aliment(**aliment_dict)
        aliments.append(aliment)
    
    # Filtrer par allergies si spécifiées
    if allergies:
        aliments = [a for a in aliments if not set(a.allergenes) & set(allergies)]
    
    return aliments

def get_all_aliments(session: Session) -> List[Aliment]:
    """Récupérer tous les aliments"""
    return session.exec(select(Aliment)).all()

# CRUD Utilisateur

def create_utilisateur(session: Session, user_data: dict) -> Utilisateur:
    """Créer un nouvel utilisateur avec mot de passe hashé"""
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    user = Utilisateur(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_utilisateur_by_id(session: Session, user_id: int) -> Optional[Utilisateur]:
    """Récupérer un utilisateur par son ID"""
    return session.get(Utilisateur, user_id)

def get_utilisateur_by_email(session: Session, email: str) -> Optional[Utilisateur]:
    """Récupérer un utilisateur par son email"""
    return session.exec(select(Utilisateur).where(Utilisateur.email == email)).first()

def authenticate_user(session: Session, email: str, password: str) -> Optional[Utilisateur]:
    """Authentifier un utilisateur"""
    from security import verify_password
    user = get_utilisateur_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# CRUD Buffet

def create_buffet(session: Session, buffet_data: dict) -> Buffet:
    """Créer un nouveau buffet"""
    buffet = Buffet(**buffet_data)
    session.add(buffet)
    session.commit()
    session.refresh(buffet)
    return buffet

def get_buffet_by_id(session: Session, buffet_id: int) -> Optional[Buffet]:
    """Récupérer un buffet par son ID"""
    return session.get(Buffet, buffet_id)

def add_aliments_to_buffet(session: Session, buffet_id: int, aliment_ids: List[int]) -> Buffet:
    """Ajouter des aliments à un buffet"""
    buffet = get_buffet_by_id(session, buffet_id)
    if not buffet:
        raise ValueError("Buffet non trouvé")
    
    for aliment_id in aliment_ids:
        aliment = get_aliment(session, aliment_id)
        if aliment:
            buffet_aliment = BuffetAliment(buffet_id=buffet_id, aliment_id=aliment_id)
            session.add(buffet_aliment)
    
    session.commit()
    session.refresh(buffet)
    return buffet

def get_buffet_aliments(session: Session, buffet_id: int) -> List[Aliment]:
    """Récupérer tous les aliments d'un buffet"""
    buffet = get_buffet_by_id(session, buffet_id)
    if not buffet:
        return []
    
    aliments = []
    for buffet_aliment in buffet.aliments:
        aliment = get_aliment(session, buffet_aliment.aliment_id)
        if aliment:
            aliments.append(aliment)
    
    return aliments

# CRUD Plan de Repas

def generate_plan_repas(session: Session, utilisateur_id: int, semaine: datetime.date) -> PlanRepas:
    """Générer un plan de repas hebdomadaire pour un utilisateur"""
    utilisateur = get_utilisateur_by_id(session, utilisateur_id)
    if not utilisateur:
        raise ValueError("Utilisateur non trouvé")
    
    # Créer le plan de repas
    plan_repas = PlanRepas(utilisateur_id=utilisateur_id, semaine=semaine)
    session.add(plan_repas)
    session.commit()
    session.refresh(plan_repas)
    
    # Jours de la semaine
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    # Récupérer tous les aliments disponibles
    aliments_disponibles = get_all_aliments(session)
    
    # Filtrer par allergies de l'utilisateur
    if utilisateur.allergies:
        aliments_disponibles = [
            a for a in aliments_disponibles 
            if not set(a.allergenes) & set(utilisateur.allergies)
        ]
    
    # Générer les repas pour chaque jour
    for jour in jours:
        repas_jour = RepasJour(plan_repas_id=plan_repas.id, jour=jour)
        session.add(repas_jour)
        session.commit()
        session.refresh(repas_jour)
        
        # Sélectionner 2-3 aliments par jour (entrée + plat + dessert)
        nb_aliments = random.randint(2, 3)
        aliments_selectionnes = random.sample(aliments_disponibles, min(nb_aliments, len(aliments_disponibles)))
        
        for aliment in aliments_selectionnes:
            aliment_repas = AlimentRepasJour(
                repas_jour_id=repas_jour.id,
                aliment_id=aliment.id
            )
            session.add(aliment_repas)
    
    session.commit()
    session.refresh(plan_repas)
    return plan_repas

def get_plan_repas_by_id(session: Session, plan_id: int) -> Optional[PlanRepas]:
    """Récupérer un plan de repas par son ID"""
    return session.get(PlanRepas, plan_id)

def get_plans_repas_utilisateur(session: Session, utilisateur_id: int) -> List[PlanRepas]:
    """Récupérer tous les plans de repas d'un utilisateur"""
    return session.exec(
        select(PlanRepas).where(PlanRepas.utilisateur_id == utilisateur_id)
    ).all()

# Services de recommandation

def recommend_aliments(session: Session, query: str, allergies: List[str] = None, max_calories: int = 800) -> List[Aliment]:
    """Recommandation d'aliments basée sur une requête et des contraintes"""
    aliments = search_aliments(session, query, allergies, top_k=20)
    
    # Filtrer par calories si spécifié
    if max_calories:
        aliments = [a for a in aliments if a.calories <= max_calories]
    
    return aliments[:10]  # Retourner les 10 meilleurs

def get_aliments_by_categorie(session: Session, categorie: str) -> List[Aliment]:
    """Récupérer tous les aliments d'une catégorie"""
    return session.exec(
        select(Aliment).where(Aliment.categorie == categorie)
    ).all()

def get_aliments_low_calories(session: Session, max_calories: int = 300) -> List[Aliment]:
    """Récupérer les aliments faibles en calories"""
    return session.exec(
        select(Aliment).where(Aliment.calories <= max_calories)
    ).all() 