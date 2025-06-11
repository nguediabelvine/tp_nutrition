from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.services.food_service import FoodService
from app.schemas import FoodCreate, FoodRead, FoodUpdate

router = APIRouter(prefix="/foods", tags=["foods"])

@router.post("/", response_model=FoodRead, status_code=status.HTTP_201_CREATED)
def create_food(food: FoodCreate, session: Session = Depends(get_session)):
    """Créer un nouvel aliment"""
    food_service = FoodService(session)
    return food_service.create_food(food)

@router.get("/", response_model=List[FoodRead])
def get_foods(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Récupérer la liste des aliments"""
    food_service = FoodService(session)
    return food_service.get_foods(skip=skip, limit=limit)

@router.get("/{food_id}", response_model=FoodRead)
def get_food(food_id: int, session: Session = Depends(get_session)):
    """Récupérer un aliment par son ID"""
    food_service = FoodService(session)
    food = food_service.get_food(food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aliment non trouvé"
        )
    return food

@router.put("/{food_id}", response_model=FoodRead)
def update_food(food_id: int, food_update: FoodUpdate, session: Session = Depends(get_session)):
    """Mettre à jour un aliment"""
    food_service = FoodService(session)
    food = food_service.update_food(food_id, food_update.dict(exclude_unset=True))
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aliment non trouvé"
        )
    return food

@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food(food_id: int, session: Session = Depends(get_session)):
    """Supprimer un aliment"""
    food_service = FoodService(session)
    success = food_service.delete_food(food_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aliment non trouvé"
        ) 