from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime

app = FastAPI(title="Dashaalia Dashboard API")

# Connexion MongoDB 
client = MongoClient("mongodb://localhost:27017/")
db = client["ma_db"]
collection = db["ma_collection"]

# --- Vue d'ensemble ---
@app.get("/api/stats/overview")
def stats_overview():
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_duration": {"$avg": "$duree_minutes"},
            "avg_note": {"$avg": "$note_praticien"},
            "avg_quality": {"$avg": "$qualite_score"},
            "total_sessions": {"$sum": 1}
        }}
    ]
    result = list(collection.aggregate(pipeline))[0]
    return result

# --- Top langues ---
@app.get("/api/stats/top-languages")
def top_languages(limit: int = 5):
    pipeline = [
        {"$group": {"_id": "$langue", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))

# --- Sessions par jour (dates formatées) ---
@app.get("/api/stats/daily")
def stats_daily():
    pipeline = [
        {"$group": {"_id": "$date", "sessions_count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = []
    for d in collection.aggregate(pipeline):
        try:
            # Conversion en datetime puis format ISO
            date_obj = datetime.strptime(d["_id"], "%Y-%m-%d")
            results.append({
                "date": date_obj.strftime("%Y-%m-%d"),
                "sessions_count": d["sessions_count"]
            })
        except Exception:
            # Si la valeur n'est pas une date valide, on la renvoie telle quelle
            results.append({
                "date": d["_id"],
                "sessions_count": d["sessions_count"]
            })
    return results

# --- Répartition par service ---
@app.get("/api/stats/by-service")
def stats_by_service():
    pipeline = [
        {"$group": {"_id": "$service", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    return list(collection.aggregate(pipeline))

# --- Interactions ---
@app.get("/api/stats/interactions")
def stats_interactions():
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_patient": {"$avg": "$interactions_patient"},
            "avg_praticien": {"$avg": "$interactions_praticien"},
            "avg_total": {"$avg": "$interactions_totales"}
        }}
    ]
    return list(collection.aggregate(pipeline))[0]

# --- Notes praticiens ---
@app.get("/api/stats/notes")
def stats_notes():
    pipeline = [
        {"$group": {"_id": "$note_praticien", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))

# --- Liste des sessions (dates formatées) ---
@app.get("/api/sessions")
def list_sessions(limit: int = 10):
    docs = collection.find().limit(limit)
    results = []
    for doc in docs:
        # Formatage de la date si elle existe
        if "date" in doc:
            try:
                date_obj = datetime.strptime(doc["date"], "%Y-%m-%d")
                doc["date"] = date_obj.strftime("%Y-%m-%d")
            except Exception:
                pass
        results.append(doc)
    return results
