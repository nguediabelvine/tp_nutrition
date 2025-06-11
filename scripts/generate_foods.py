#!/usr/bin/env python3
"""
Script pour générer 200 aliments avec des données nutritionnelles réalistes
"""

import json
import random
from typing import List, Dict

# Données de base pour générer les aliments
FRUITS = [
    "Pomme", "Banane", "Orange", "Fraise", "Raisin", "Mangue", "Ananas", "Kiwi", 
    "Pêche", "Poire", "Prune", "Cerise", "Myrtille", "Framboise", "Mûre", "Citron",
    "Lime", "Pamplemousse", "Mandarine", "Clémentine", "Abricot", "Nectarine",
    "Figue", "Grenade", "Papaye", "Goyave", "Litchi", "Ramboutan", "Longane",
    "Mangoustan", "Durian", "Jackfruit", "Breadfruit", "Sapodilla", "Soursop"
]

LEGUMES = [
    "Brocoli", "Épinards", "Carotte", "Tomate", "Concombre", "Poivron", "Oignon",
    "Ail", "Chou", "Chou-fleur", "Chou de Bruxelles", "Asperge", "Haricot vert",
    "Pois", "Maïs", "Courgette", "Aubergine", "Patate douce", "Pomme de terre",
    "Betterave", "Radis", "Navet", "Rutabaga", "Céleri", "Fenouil", "Artichaut",
    "Poireau", "Échalote", "Ciboulette", "Persil", "Basilic", "Thym", "Romarin",
    "Sauge", "Menthe", "Coriandre", "Aneth", "Estragon", "Marjolaine", "Origan"
]

VIANDES = [
    "Poulet", "Dinde", "Bœuf", "Porc", "Agneau", "Veau", "Canard", "Oie",
    "Lapin", "Chevreuil", "Sanglier", "Bison", "Autruche", "Émeu", "Kangourou",
    "Chèvre", "Mouton", "Cochon d'Inde", "Pintade", "Caille", "Faisan", "Perdrix"
]

POISSONS = [
    "Saumon", "Thon", "Morue", "Cabillaud", "Haddock", "Aiglefin", "Lieu",
    "Merlu", "Bar", "Dorade", "Sole", "Turbot", "Saint-Pierre", "Rouget",
    "Sardine", "Anchois", "Maquereau", "Hareng", "Truite", "Perche", "Brochet",
    "Sandre", "Carpe", "Anguille", "Congre", "Raie", "Lotte", "Baudroie"
]

CEREALES = [
    "Riz", "Blé", "Avoine", "Orge", "Seigle", "Millet", "Sorgho", "Quinoa",
    "Amarante", "Sarrasin", "Épeautre", "Kamut", "Triticale", "Teff", "Fonio"
]

NOIX_GRAINES = [
    "Amande", "Noix", "Noisette", "Pistache", "Cajou", "Macadamia", "Pécan",
    "Noix du Brésil", "Noix de cajou", "Pignon", "Châtaigne", "Marron",
    "Graines de tournesol", "Graines de citrouille", "Graines de sésame",
    "Graines de lin", "Graines de chia", "Graines de chanvre", "Graines de pavot"
]

LAITAGES = [
    "Lait", "Yaourt", "Fromage", "Beurre", "Crème", "Crème fraîche", "Kéfir",
    "Lait de chèvre", "Lait de brebis", "Lait d'amande", "Lait de soja",
    "Lait de riz", "Lait de coco", "Lait d'avoine", "Lait de noisette"
]

# Vitamines et minéraux
VITAMINES = ["A", "B1", "B2", "B3", "B5", "B6", "B7", "B9", "B12", "C", "D", "E", "K"]
MINERAUX = ["Calcium", "Fer", "Magnesium", "Phosphore", "Potassium", "Sodium", "Zinc", "Cuivre", "Manganèse", "Sélénium", "Iode", "Chrome", "Molybdène"]

def generate_food_data():
    """Génère 200 aliments avec des données nutritionnelles réalistes"""
    foods = []
    
    # Générer des fruits
    for fruit in FRUITS:
        foods.append({
            "name": fruit,
            "calories": random.randint(30, 120),
            "proteins": round(random.uniform(0.5, 2.0), 1),
            "carbohydrates": round(random.uniform(8, 25), 1),
            "fats": round(random.uniform(0.1, 0.5), 1),
            "fiber": round(random.uniform(1.5, 5.0), 1),
            "category": "Fruits",
            "vitamins": random.sample(VITAMINES, random.randint(1, 4)),
            "minerals": random.sample(MINERAUX, random.randint(1, 3))
        })
    
    # Générer des légumes
    for legume in LEGUMES:
        foods.append({
            "name": legume,
            "calories": random.randint(15, 100),
            "proteins": round(random.uniform(1.0, 4.0), 1),
            "carbohydrates": round(random.uniform(3, 20), 1),
            "fats": round(random.uniform(0.1, 0.8), 1),
            "fiber": round(random.uniform(1.5, 6.0), 1),
            "category": "Légumes",
            "vitamins": random.sample(VITAMINES, random.randint(2, 5)),
            "minerals": random.sample(MINERAUX, random.randint(2, 4))
        })
    
    # Générer des viandes
    for viande in VIANDES:
        foods.append({
            "name": f"{viande} grillé(e)",
            "calories": random.randint(120, 300),
            "proteins": round(random.uniform(20, 35), 1),
            "carbohydrates": 0,
            "fats": round(random.uniform(2, 15), 1),
            "fiber": 0,
            "category": "Viandes",
            "vitamins": random.sample(["B1", "B2", "B3", "B6", "B12"], random.randint(2, 4)),
            "minerals": random.sample(["Fer", "Zinc", "Phosphore", "Potassium"], random.randint(2, 4))
        })
    
    # Générer des poissons
    for poisson in POISSONS:
        foods.append({
            "name": f"{poisson} cuit",
            "calories": random.randint(100, 250),
            "proteins": round(random.uniform(18, 30), 1),
            "carbohydrates": 0,
            "fats": round(random.uniform(1, 12), 1),
            "fiber": 0,
            "category": "Poissons",
            "vitamins": random.sample(["D", "B12", "B6", "A"], random.randint(2, 4)),
            "minerals": random.sample(["Sélénium", "Phosphore", "Potassium", "Magnesium"], random.randint(2, 4))
        })
    
    # Générer des céréales
    for cereale in CEREALES:
        foods.append({
            "name": f"{cereale} cuit",
            "calories": random.randint(80, 150),
            "proteins": round(random.uniform(2, 6), 1),
            "carbohydrates": round(random.uniform(15, 30), 1),
            "fats": round(random.uniform(0.5, 2.0), 1),
            "fiber": round(random.uniform(1.5, 4.0), 1),
            "category": "Céréales",
            "vitamins": random.sample(["B1", "B2", "B3", "B6"], random.randint(2, 4)),
            "minerals": random.sample(["Magnesium", "Phosphore", "Potassium", "Fer"], random.randint(2, 4))
        })
    
    # Générer des noix et graines
    for noix in NOIX_GRAINES:
        foods.append({
            "name": noix,
            "calories": random.randint(150, 650),
            "proteins": round(random.uniform(5, 25), 1),
            "carbohydrates": round(random.uniform(5, 20), 1),
            "fats": round(random.uniform(10, 60), 1),
            "fiber": round(random.uniform(2, 12), 1),
            "category": "Noix et Graines",
            "vitamins": random.sample(["E", "B1", "B6"], random.randint(1, 3)),
            "minerals": random.sample(["Magnesium", "Phosphore", "Potassium", "Zinc"], random.randint(2, 4))
        })
    
    # Générer des produits laitiers
    for laitier in LAITAGES:
        foods.append({
            "name": laitier,
            "calories": random.randint(40, 400),
            "proteins": round(random.uniform(3, 25), 1),
            "carbohydrates": round(random.uniform(0, 15), 1),
            "fats": round(random.uniform(0, 35), 1),
            "fiber": 0,
            "category": "Produits Laitiers",
            "vitamins": random.sample(["A", "D", "B2", "B12"], random.randint(2, 4)),
            "minerals": random.sample(["Calcium", "Phosphore", "Potassium"], random.randint(2, 3))
        })
    
    # Ajouter quelques aliments supplémentaires pour atteindre 200
    extra_foods = [
        {"name": "Œuf", "calories": 155, "proteins": 13, "carbohydrates": 1.1, "fats": 11, "fiber": 0, "category": "Œufs", "vitamins": ["A", "D", "B12"], "minerals": ["Fer", "Sélénium"]},
        {"name": "Tofu", "calories": 76, "proteins": 8, "carbohydrates": 1.9, "fats": 4.8, "fiber": 0.3, "category": "Protéines Végétales", "vitamins": ["B1", "B6"], "minerals": ["Calcium", "Fer"]},
        {"name": "Lentilles", "calories": 116, "proteins": 9, "carbohydrates": 20, "fats": 0.4, "fiber": 8, "category": "Légumineuses", "vitamins": ["B1", "B6", "B9"], "minerals": ["Fer", "Magnesium"]},
        {"name": "Pois chiches", "calories": 164, "proteins": 9, "carbohydrates": 27, "fats": 2.6, "fiber": 8, "category": "Légumineuses", "vitamins": ["B6", "B9"], "minerals": ["Fer", "Magnesium"]},
        {"name": "Haricots noirs", "calories": 132, "proteins": 9, "carbohydrates": 24, "fats": 0.5, "fiber": 8, "category": "Légumineuses", "vitamins": ["B1", "B6"], "minerals": ["Fer", "Magnesium"]}
    ]
    
    foods.extend(extra_foods)
    
    # Mélanger la liste pour plus de variété
    random.shuffle(foods)
    
    return foods[:200]  # Retourner exactement 200 aliments

if __name__ == "__main__":
    # Générer les données
    foods_data = generate_food_data()
    
    # Sauvegarder dans un fichier JSON
    with open("data/foods_data.json", "w", encoding="utf-8") as f:
        json.dump(foods_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(foods_data)} aliments générés et sauvegardés dans data/foods_data.json") 