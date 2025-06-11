from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import datetime
import json

class Aliment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    categorie: str
    calories: int
    allergenes: str = Field(default="[]")  # Stocké comme JSON string
    image_url: Optional[str] = None

class Utilisateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    allergies: str = Field(default="[]")  # Stocké comme JSON string
    is_active: bool = True
    is_superuser: bool = False
    plans_repas: List["PlanRepas"] = Relationship(back_populates="utilisateur")

class PlanRepas(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    semaine: datetime.date
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