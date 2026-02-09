from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from config import MONGO_URI, APP_DB, APP_COLLECTION
import time

app = Flask(__name__, template_folder="templates")

client = MongoClient(MONGO_URI)
db = client[APP_DB]
coleccion = db[APP_COLLECTION]
# consultas a mongo
pipeline_top_users = [
    {
        "$group": {
            "_id": "$user",
            "total_changes": {"$sum": 1},
            "bot_changes": {"$sum": {"$cond": [{"$eq": ["$bot", True]}, 1, 0]}},
            "human_changes": {"$sum": {"$cond": [{"$eq": ["$bot", False]}, 1, 0]}},
        }
    },
    {"$sort": {"total_changes": -1}},
    {"$limit": 10},
]

pipeline_by_type = [
    {"$group": {"_id": "$type", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
]


@app.route("/")
def index():
    eventos = list(coleccion.find().sort("_id", -1).limit(50))
    return render_template("index.html", eventos=eventos)


@app.route("/api/total")
def api_total():
    total = coleccion.count_documents({})
    return jsonify({"total": total})


@app.route("/api/events_last")
def events_last():
    now = int(time.time())
    window = 10  # últimos 10 segundos

    count = coleccion.count_documents({"timestamp": {"$gte": now - window}})

    return jsonify({"timestamp": now, "count": count})


# LISTA LOS ULTIMOS EVENTOS
@app.route("/api/latest_events")
def latest_events():
    eventos = list(
        coleccion.find(
            {},
            {
                "_id": 0,
                "title": 1,
                "user": 1,
                "wiki": 1,
                "timestamp": 1,
                "bot": 1,
            },
        )
        .sort("_id", -1)
        .limit(10)
    )
    return jsonify(eventos)


@app.route("/api/bd_metrics")
def bd_metrics():
    stats = db.command("collstats", coleccion.name)

    return jsonify({"size_kb": round(stats["storageSize"] / 1024, 2)})


@app.route("/api/bd_metrics")
def kb_sec():
    stats = db.command("collstats", coleccion.name)

    return jsonify({"size_kb": round(stats["storageSize"] / 1024, 2)})


@app.route("/api/top_usuarios")
def top_usuarios():
    start = time.time()
    data = list(coleccion.aggregate(pipeline_top_users))
    elapsed = round(time.time() - start, 4)

    return jsonify({"source": "mongodb", "query_time_sec": elapsed, "data": data})


@app.route("/api/type_edit")
def edit_types():
    start = time.time()
    data = list(coleccion.aggregate(pipeline_by_type))
    elapsed = round(time.time() - start, 4)

    return jsonify({"source": "mongodb", "query_time_sec": elapsed, "data": data})
