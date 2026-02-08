from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from config import MONGO_URI, APP_DB, APP_COLLECTION
import time

app = Flask(__name__, template_folder="templates")

client = MongoClient(MONGO_URI)
db = client[APP_DB]
coleccion = db[APP_COLLECTION]


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
