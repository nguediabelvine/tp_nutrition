from typing import List, Optional
from pydantic import BaseModel, EmailStr
import datetime

class AlimentBase(BaseModel):
    nom: str
    categorie: str
    calories: int
    allergenes: List[str] = []
    image_url: Optional[str] = None

class AlimentCreate(AlimentBase):
    pass

class AlimentRead(AlimentBase):
    id: int
    class Config:
        from_attributes = True

class UtilisateurBase(BaseModel):
    nom: str
    email: EmailStr
    allergies: List[str] = []

class UtilisateurCreate(UtilisateurBase):
    password: str

class UtilisateurRead(UtilisateurBase):
    id: int
    is_active: bool
    is_superuser: bool
    class Config:
        from_attributes = True

class PlanRepasCreate(BaseModel):
    utilisateur_id: int
    semaine: datetime.date

class PlanRepasRead(BaseModel):
    id: int
    utilisateur_id: int
    semaine: datetime.date
    class Config:
        from_attributes = True

class BuffetCreate(BaseModel):
    nom: str
    description: Optional[str] = None

class BuffetRead(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    class Config:
        from_attributes = True 