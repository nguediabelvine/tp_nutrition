from sqlmodel import Session, select
from typing import List, Optional
from app.models import Food, FoodCreate, FoodRead
from app.schemas import FoodCreate as FoodCreateSchema, FoodRead as FoodReadSchema

class FoodService:
    def __init__(self, session: Session):
        self.session = session

    def create_food(self, food_data: FoodCreateSchema) -> FoodReadSchema:
        food = Food(**food_data.dict())
        self.session.add(food)
        self.session.commit()
        self.session.refresh(food)
        
        # Convertir en schéma de réponse
        return FoodReadSchema(
            id=food.id,
            name=food.name,
            calories=food.calories,
            proteins=food.proteins,
            carbohydrates=food.carbohydrates,
            fats=food.fats,
            fiber=food.fiber,
            category=food.category,
            vitamins=food.vitamins,
            minerals=food.minerals,
            created_at=food.created_at
        )

    def get_foods(self, skip: int = 0, limit: int = 100) -> List[FoodReadSchema]:
        statement = select(Food).offset(skip).limit(limit)
        foods = self.session.exec(statement).all()
        
        return [
            FoodReadSchema(
                id=food.id,
                name=food.name,
                calories=food.calories,
                proteins=food.proteins,
                carbohydrates=food.carbohydrates,
                fats=food.fats,
                fiber=food.fiber,
                category=food.category,
                vitamins=food.vitamins,
                minerals=food.minerals,
                created_at=food.created_at
            )
            for food in foods
        ]

    def get_food(self, food_id: int) -> Optional[FoodReadSchema]:
        food = self.session.get(Food, food_id)
        if not food:
            return None
            
        return FoodReadSchema(
            id=food.id,
            name=food.name,
            calories=food.calories,
            proteins=food.proteins,
            carbohydrates=food.carbohydrates,
            fats=food.fats,
            fiber=food.fiber,
            category=food.category,
            vitamins=food.vitamins,
            minerals=food.minerals,
            created_at=food.created_at
        )

    def update_food(self, food_id: int, food_data: dict) -> Optional[FoodReadSchema]:
        food = self.session.get(Food, food_id)
        if not food:
            return None
        
        # Mettre à jour les champs fournis
        for field, value in food_data.items():
            if value is not None:
                setattr(food, field, value)
        
        self.session.add(food)
        self.session.commit()
        self.session.refresh(food)
        
        return FoodReadSchema(
            id=food.id,
            name=food.name,
            calories=food.calories,
            proteins=food.proteins,
            carbohydrates=food.carbohydrates,
            fats=food.fats,
            fiber=food.fiber,
            category=food.category,
            vitamins=food.vitamins,
            minerals=food.minerals,
            created_at=food.created_at
        )

    def delete_food(self, food_id: int) -> bool:
        food = self.session.get(Food, food_id)
        if not food:
            return False
        
        self.session.delete(food)
        self.session.commit()
        return True 