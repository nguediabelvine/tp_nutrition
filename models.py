from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime , date
import json
from sqlalchemy import Column, JSON

class Aliment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    categorie: str
    calories: int
    allergenes: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    image_url: Optional[str] = None

class Utilisateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    allergies: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    is_active: bool = True
    is_superuser: bool = False
    plans_repas: List["PlanRepas"] = Relationship(back_populates="utilisateur")

class PlanRepas(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    semaine: date
    repas: List["RepasJour"] = Relationship(back_populates="plan_repas")
    utilisateur: Optional[Utilisateur] = Relationship(back_populates="plans_repas")

class RepasJour(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plan_repas_id: int = Field(foreign_key="planrepas.id")
    jour: str
    aliments: List["AlimentRepasJour"] = Relationship(back_populates="repas_jour")
    plan_repas: Optional[PlanRepas] = Relationship(back_populates="repas")

class AlimentRepasJour(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repas_jour_id: int = Field(foreign_key="repasjour.id")
    aliment_id: int = Field(foreign_key="aliment.id")
    repas_jour: Optional[RepasJour] = Relationship(back_populates="aliments")
    aliment: Optional[Aliment] = Relationship()

class Buffet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    description: Optional[str] = None
    aliments: List["BuffetAliment"] = Relationship(back_populates="buffet")

class BuffetAliment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    buffet_id: int = Field(foreign_key="buffet.id")
    aliment_id: int = Field(foreign_key="aliment.id")
    buffet: Optional[Buffet] = Relationship(back_populates="aliments")
    aliment: Optional[Aliment] = Relationship()

class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    allergies: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    recommendations: List["Recommendation"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class FoodBase(SQLModel):
    name: str = Field(index=True)
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    fiber: float
    category: str = Field(index=True)
    vitamins: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    minerals: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))

class Food(FoodBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    recommendations: List["Recommendation"] = Relationship(back_populates="food")

class FoodCreate(FoodBase):
    pass

class FoodRead(FoodBase):
    id: int
    created_at: datetime

class RecommendationBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    food_id: int = Field(foreign_key="food.id")
    reason: str
    score: float

class Recommendation(RecommendationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="recommendations")
    food: Food = Relationship(back_populates="recommendations")

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationRead(RecommendationBase):
    id: int
    created_at: datetime 