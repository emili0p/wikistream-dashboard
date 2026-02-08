import threading
import time
import json
import requests

from pymongo import MongoClient
from routes import app
from config import (
    MONGO_URI,
    APP_DB,
    APP_COLLECTION,
    STREAM_URL,
    BATCH_SIZE,
)

# conexion
cliente = MongoClient(MONGO_URI)
db = cliente[APP_DB]
coleccion = db[APP_COLLECTION]


# loop principal
def consume_events():
    # headers para mandar la peticicion curl a la api
    headers = {
        "Accept": "text/event-stream",
        "User-Agent": "LiveData-Test/1.0 (emilio@example.com)",
    }

    # print("[DEBUG] Conectando al stream...")

    try:
        with requests.get(STREAM_URL, headers=headers, stream=True) as resp:
            if resp.status_code != 200:
                # si hay error 200 es por que se rechazo la conexion
                # print(f"[DEBUG] Error al conectar: {resp.status_code}")
                return

            print("[DEBUG] Conexión establecida, escuchando eventos...")
            # guardarmos en listas los datos obtenidos y el tiempo desde la ultima insercion
            buffer = []
            last_flush = time.time()

            for line in resp.iter_lines():
                if not line:
                    continue

                decoded = line.decode("utf-8")

                if decoded.startswith("data: "):
                    try:
                        evento = json.loads(decoded[6:])
                        buffer.append(evento)

                        # print(
                        #     f"[DEBUG] Evento recibido: {evento.get('title', 'sin título')}"
                        # )

                        # Flush por tamaño
                        if len(buffer) >= BATCH_SIZE:
                            coleccion.insert_many(buffer)
                            # print(f"[DB] Insertados {len(buffer)} eventos (batch)")
                            buffer.clear()
                            last_flush = time.time()

                        # Flush por tiempo
                        elif time.time() - last_flush >= 1:
                            if buffer:
                                coleccion.insert_many(buffer)
                                print(f"[DB] Insertados {len(buffer)} eventos (time)")
                                buffer.clear()
                                last_flush = time.time()

                    except json.JSONDecodeError as e:
                        print("[DEBUG] JSON invalido:", e)

    except requests.exceptions.RequestException as e:
        print("[DEBUG] Error en la conexion:", e)


thread = threading.Thread(target=consume_events, daemon=True)
thread.start()
# hilo para correr la ingesta de datos

# levantar servidor en flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
