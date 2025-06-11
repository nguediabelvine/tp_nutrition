from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Schémas pour l'authentification
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Schémas pour les utilisateurs
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    allergies: List[str] = []

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    allergies: List[str]
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    allergies: Optional[List[str]] = None

# Schémas pour les aliments
class FoodCreate(BaseModel):
    name: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    fiber: float
    category: str
    vitamins: List[str] = []
    minerals: List[str] = []

class FoodRead(BaseModel):
    id: int
    name: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    fiber: float
    category: str
    vitamins: List[str]
    minerals: List[str]
    created_at: datetime

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    category: Optional[str] = None
    vitamins: Optional[List[str]] = None
    minerals: Optional[List[str]] = None

# Schémas pour les recommandations
class RecommendationCreate(BaseModel):
    user_id: int
    food_id: int
    reason: str
    score: float

class RecommendationRead(BaseModel):
    id: int
    user_id: int
    food_id: int
    reason: str
    score: float
    created_at: datetime

# Schémas pour les réponses API
class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0" 