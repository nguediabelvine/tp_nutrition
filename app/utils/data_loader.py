import json
from sqlmodel import Session, text
from app.database import engine
from app.models import Food

def load_initial_data():
    """Charger les données initiales dans la base de données"""
    with Session(engine) as session:
        # Vérifier si des données existent déjà
        result = session.exec(text("SELECT COUNT(*) FROM food")).first()
        existing_foods = result[0] if result else 0
        if existing_foods > 0:
            print("Données déjà chargées, skip...")
            return
        
        try:
            # Charger les données depuis le fichier JSON
            with open("data/foods_data.json", "r", encoding="utf-8") as f:
                foods_data = json.load(f)
        except FileNotFoundError:
            print("Fichier data/foods_data.json non trouvé, génération des données...")
            # Générer les données si le fichier n'existe pas
            from scripts.generate_foods import generate_food_data
            foods_data = generate_food_data()
            
            # Sauvegarder les données générées
            import os
            os.makedirs("data", exist_ok=True)
            with open("data/foods_data.json", "w", encoding="utf-8") as f:
                json.dump(foods_data, f, ensure_ascii=False, indent=2)
        
        # Ajouter les aliments à la base de données
        for food_data in foods_data:
            food = Food(**food_data)
            session.add(food)
        
        session.commit()
        print(f"✅ {len(foods_data)} aliments chargés avec succès!") 