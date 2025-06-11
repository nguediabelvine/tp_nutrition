import json
import os
from sqlmodel import Session, select
from models import Aliment

def load_initial_data(session: Session, data_path: str = "data/repas_canadiens.json"):
    if not os.path.exists(data_path):
        print(f"Fichier {data_path} introuvable.")
        return
    with open(data_path, "r", encoding="utf-8") as f:
        aliments = json.load(f)
    for aliment in aliments:
        # Vérifier si l'aliment existe déjà
        existing = session.exec(select(Aliment).where(Aliment.nom == aliment["nom"])).first()
        if not existing:
            session.add(Aliment(
                nom=aliment["nom"],
                categorie=aliment["categorie"],
                calories=aliment["calories"],
                allergenes=json.dumps(aliment["allergenes"]),  # Convertir en JSON string
                image_url=aliment["image_url"]
            ))
    session.commit()
    print(f"✅ {len(aliments)} aliments chargés dans la base de données") 