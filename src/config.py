# all these are local keys so just do whenever you want lol

# MongoDB
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_URI = "mongodb://admin:localhost@127.0.0.1:27017/?authSource=admin"

APP_DB = "prueba_db"
APP_COLLECTION = "events"


# app !!
APP_NAME = "events"

# consumo !!
STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"

# ingesta !!
BATCH_SIZE = 1000  # documentos por inserción
FLUSH_EVERY_SEC = 0.01  # cada cuánto se escriben a la BD

# retencion !! (para limpiar)
MAX_DOCS = None  # ej. 5_000_000 de inserciones o none para ilimitado inserciones
