import certifi
import urllib
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://crixgarx:" + urllib.parse.quote('crixgarx123') + "@clustercrixgarx.deconmm.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCrixGarx"
ca = certifi.where()

def conexionBD():
    try:
        cliente = MongoClient(MONGO_URI, tlsCAFile=ca)
        print("Conexión a la base de datos exitosa")
        return cliente["integradora"], cliente["integradora"]["administrador"]  # Devuelve la referencia a la base de datos y la colección administrador
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

