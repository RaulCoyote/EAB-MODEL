from bson import ObjectId
from flask import session

class UsuarioCRUD:
    def __init__(self, db):
        self.db = db

    def verificar_existencia_usuario(self, matricula):
        # Realizar la consulta para verificar la existencia del usuario
        usuario = self.db.usuarios.find_one({'matricula': matricula})

        # Si usuario es None, significa que no se encontró ningún usuario con la matrícula dada
        if usuario is None:
            return False
        else:
            return True

    def agregar_usuario(self, nombre, matricula, contrasena, usuario, qr, admin_object):
        self.db.usuarios.insert_one({
            'nombre': nombre,
            'matricula': matricula,
            'contrasena': contrasena,
            'usuario': usuario,
            'qr': qr,
            'admin': admin_object
        })

    def obtener_usuarios(self):
        nombre_admin = session.get('nombre')
        correo_admin = session.get('correo')
        usuarios = self.db.usuarios.find({'admin.nombre': nombre_admin, 'admin.correo': correo_admin})
        return list(usuarios)  # Convertir el cursor a una lista de diccionarios

    def obtener_usuario_por_id(self, id):
        return self.db.usuarios.find_one({'_id': ObjectId(id)})

    def actualizar_usuario(self, id, nombre, usuario, matricula):
        self.db.usuarios.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': nombre, 'usuario': usuario, 'matricula': matricula}})

    def eliminar_usuario(self, id):
        self.db.usuarios.delete_one({'_id': ObjectId(id)})
