import json
import os
from sqlmodel import Session
from models import Aliment

def load_initial_data(session: Session, data_path: str = "data/repas_canadiens.json"):
    if not os.path.exists(data_path):
        print(f"Fichier {data_path} introuvable.")
        return
    with open(data_path, "r", encoding="utf-8") as f:
        aliments = json.load(f)
    for aliment in aliments:
        if not session.exec(
            Aliment.select().where(Aliment.nom == aliment["nom"])  # éviter les doublons
        ).first():
            session.add(Aliment(
                nom=aliment["nom"],
                categorie=aliment["categorie"],
                calories=aliment["calories"],
                allergenes=aliment["allergenes"],
                image_url=aliment["image_url"]
            ))
    session.commit() 