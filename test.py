from pymongo import MongoClient

# Connexion au MongoDB Docker exposé sur localhost:27018

MONGO_URI = "mongodb://localhost:27018/"
DB_NAME = "ma_db"
COLLECTION_NAME = "ma_collection"

# Connexion

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Vérifier le nombre de documents

count = collection.count_documents({})
print(f"Nombre de documents dans la collection '{COLLECTION_NAME}': {count}")

# Afficher les 5 premiers documents

print("Exemples de documents :")
for doc in collection.find().limit(5):
    print(doc)
