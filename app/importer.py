import pandas as pd
from pymongo import MongoClient
import time

MONGO_URI = "mongodb://mongo:27017/"
DB_NAME = "ma_db"
COLLECTION_NAME = "ma_collection"
CSV_FILE = "data/data.csv"

# Attendre que MongoDB soit prêt
for _ in range(10):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        break
    except:
        print("MongoDB non prêt, attente 2s...")
        time.sleep(2)
else:
    print("Impossible de se connecter à MongoDB.")
    exit(1)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

if collection.count_documents({}) == 0:
    print(f"Collection '{COLLECTION_NAME}' vide. Importation du CSV...")
    df = pd.read_csv(CSV_FILE)
    if not df.empty:
        collection.insert_many(df.to_dict("records"))
        print(f"{len(df)} documents insérés !")
else:
    print(f"Collection '{COLLECTION_NAME}' contient déjà {collection.count_documents({})} documents.")

# Afficher 5 documents
for doc in collection.find().limit(5):
    print(doc)
