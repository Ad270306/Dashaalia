from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware # Important pour le frontend

app = FastAPI(title="Dashaalia Dashboard API")

# Configuration CORS pour autoriser Streamlit ou React à parler à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion MongoDB 
# Si tu n'as pas MongoDB installé localement, l'API plantera plus tard.
# Assure-toi que MongoDB tourne ou gère l'erreur ici.
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client["ma_db"]
    collection = db["ma_collection"]
    # Test rapide de connexion
    client.server_info()
except Exception:
    print("ATTENTION: Impossible de se connecter à MongoDB.")
    print("Vérifie que MongoDB est lancé ou utilise Docker.")

# --- Vue d'ensemble ---
@app.get("/api/stats/overview")
def stats_overview():
    try:
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_duration": {"$avg": "$duree_minutes"},
                "avg_note": {"$avg": "$note_praticien"},
                "avg_quality": {"$avg": "$qualite_score"},
                "total_sessions": {"$sum": 1}
            }}
        ]
        result = list(collection.aggregate(pipeline))
        return result[0] if result else {}
    except Exception as e:
        return {"error": str(e)}

# --- Top langues ---
@app.get("/api/stats/top-languages")
def top_languages(limit: int = 5):
    try:
        pipeline = [
            {"$group": {"_id": "$langue", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        return list(collection.aggregate(pipeline))
    except Exception:
        return []

# --- Sessions par jour ---
@app.get("/api/stats/daily")
def stats_daily():
    try:
        pipeline = [
            {"$group": {"_id": "$date", "sessions_count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        results = []
        for d in collection.aggregate(pipeline):
            try:
                date_obj = datetime.strptime(d["_id"], "%Y-%m-%d")
                results.append({
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "sessions_count": d["sessions_count"]
                })
            except Exception:
                results.append({
                    "date": d["_id"],
                    "sessions_count": d["sessions_count"]
                })
        return results
    except Exception:
        return []

# --- Répartition par service ---
@app.get("/api/stats/by-service")
def stats_by_service():
    try:
        pipeline = [
            {"$group": {"_id": "$service", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(collection.aggregate(pipeline))
    except Exception:
        return []

# --- Interactions ---
@app.get("/api/stats/interactions")
def stats_interactions():
    try:
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_patient": {"$avg": "$interactions_patient"},
                "avg_praticien": {"$avg": "$interactions_praticien"},
                "avg_total": {"$avg": "$interactions_totales"}
            }}
        ]
        res = list(collection.aggregate(pipeline))
        return res[0] if res else {}
    except Exception:
        return {}

# --- Liste des sessions ---
@app.get("/api/sessions")
def list_sessions(limit: int = 10):
    try:
        docs = collection.find().limit(limit)
        results = []
        for doc in docs:
            doc["_id"] = str(doc["_id"]) # Convertir ObjectId en string pour le JSON
            results.append(doc)
        return results
    except Exception:
        return []