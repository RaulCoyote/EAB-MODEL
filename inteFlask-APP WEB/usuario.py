class Usuario:
   
    def __init__(self,nombre,matricula,contrasena,usuario,qr,admin):
        self.nombre = nombre
        self.matricula = matricula
        self.contrasena = contrasena
        self.usuario = usuario
        self.qr = qr
        self.admin = admin
    def aLaColeccion(self):
        return{
            'nombre': str(self.nombre),
            'matricula':int(self.matricula),
            'contrasena': str(self.contrasena),
            'usuario':str(self.usuario),
            'qr': str(self.qr),
            'admin': self.admin
        }
        
        