import db  # Asegúrate de importar el módulo db adecuadamente

class Administrador:
    def __init__(self, nombre, correo, contrasena, nip):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.nip = nip
    
    def aLaColeccion(self):
        return {
            'nombre': self.nombre,
            'correo': self.correo,
            'contrasena': self.contrasena,
            'nip': self.nip
        }

    @staticmethod
    def aLaColeccionSesion(admin_data):
        return {
            'nombre': admin_data['nombre'],
            'correo': admin_data['correo'],
            'contrasena': admin_data['contrasena'],
            'nip': admin_data.get('nip')
        }

    @staticmethod
    def obtener_por_credenciales(nombre, contrasena, correo):
        _, administrador_collection = db.conexionBD()
        admin_data = administrador_collection.find_one({"nombre": nombre, "contrasena": contrasena, "correo": correo})
        if admin_data:
            admin_data['_id'] = str(admin_data['_id'])  # Agregar el campo '_id' como 'id'
            return Administrador.aLaColeccionSesion(admin_data)
        else:
            return None
