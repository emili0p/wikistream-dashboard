import pymongo
from config import MONGO_URI, APP_DB, APP_COLLECTION
import datetime

# Conexión a MongoDB
myclient = pymongo.MongoClient(MONGO_URI)
mydb = myclient[APP_DB]
mycol = mydb[APP_COLLECTION]


def insert_event(event: dict):
    if "id" not in event:
        print("[WARN] Evento sin 'id':", event)
        return

    try:
        event_copy = event.copy()
        event_copy["event_id"] = event_copy.pop("id")
        mycol.insert_one(event_copy)
        print("[DB] Evento insertado:", event_copy["event_id"])
    except pymongo.errors.DuplicateKeyError:
        print("[DB] Evento ya existente:", event["id"])
    except Exception as e:
        print("[DB] Error al insertar:", e)


def leer_todos_eventos():
    return list(mycol.find({}))


def contar_eventos():
    return mycol.count_documents({})


def eventos_por_minuto():
    now = int(datetime.utcnow().timestamp())
    one_hour_ago = now - 3600

    pipeline = [
        {"$match": {"timestamp": {"$gte": one_hour_ago}}},
        {"$project": {"minute": {"$floor": {"$divide": ["$timestamp", 60]}}}},
        {"$group": {"_id": "$minute", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]

    result = list(mycol.aggregate(pipeline))

    labels = []
    values = []

    for r in result:
        ts = r["_id"] * 60
        labels.append(datetime.utcfromtimestamp(ts).strftime("%H:%M"))
        values.append(r["count"])

    return {"labels": labels, "values": values}
