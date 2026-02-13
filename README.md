# Wikimedia-dashboard

Consumidor de la API de Wikimedia que registra en tiempo real datos obtenidos de:

https://stream.wikimedia.org/v2/stream/recentchange

Los eventos son almacenados en **MongoDB** y expuestos mediante un servidor HTTP (Flask) para ser consumidos por un dashboard en tiempo real.

---

# Requisitos

- Python 3.9+
- MongoDB instalado localmente
- pip

---

# Instalar MongoDB localmente

En Linux (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install mongodb

Verificar que esté corriendo:

sudo systemctl status mongod


Si no está activo:

sudo systemctl start mongodb

Entrar al shell de MongoDB:

mongosh


Crear/seleccionar base:

use prueba_db

```
# Crear colección (opcional, se crea sola al insertar datos):

db.eventos.insertOne({ init: true })


Verificar bases existentes:

show dbs


# Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate
```

 
En Windows:

``` bash
venv\Scripts\activate
``` 

# instalar dependencias
```bash 

pip install -r requirements.txt
``` 

# Ejecutar el servidor HTTP
```bash 

python3 src/app.py
```
Estara corriendo en el puerto 5000 
