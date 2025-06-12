from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

from sqlalchemy import Column, JSON

class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    allergies: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relations
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
    
    # Relations
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
    
    # Relations
    user: User = Relationship(back_populates="recommendations")
    food: Food = Relationship(back_populates="recommendations")

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationRead(RecommendationBase):
    id: int
    created_at: datetime 