import pandas as pd
from pymongo import MongoClient
import json

# 1. Configuration (Mets ici le nom exact de ton fichier CSV)

CSV_FILE = "../data/data.csv"

# 2. Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ma_db"]
collection = db["ma_collection"]

def import_csv_to_mongo():
    try:
        # Lecture du CSV
        print(f"📂 Lecture du fichier {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE)
        
        # Nettoyage : On s'assure que les dates sont au bon format (String YYYY-MM-DD)
        # Si ta colonne date s'appelle autrement, change "date" ci-dessous
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        # Conversion en liste de dictionnaires (format JSON pour Mongo)
        data = df.to_dict(orient="records")
        
        # Vider la collection avant d'importer (pour éviter les doublons si tu relances)
        collection.delete_many({})
        print("🗑️ Anciennes données effacées.")

        # Insertion
        if data:
            collection.insert_many(data)
            print(f"✅ Succès ! {len(data)} sessions ont été importées dans MongoDB.")
        else:
            print("⚠️ Le fichier CSV semble vide.")

    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{CSV_FILE}' est introuvable. Vérifie le nom.")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    import_csv_to_mongo()