import base64
import io
import re
from bson import ObjectId
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash
import qrcode
from administrador import Administrador
import db as database
from usuario import Usuario
import crud
# Instanciar la Conexión a la BD
db = database.conexionBD()

app = Flask(__name__)
app.secret_key = 'PalabraSecreta'


@app.route('/')
def index():
    if session:
        redirect(url_for('añadirusuario'))
    return render_template('index.html')

@app.route('/iniciar')
def iniciar():
    return render_template('iniciar.html')


@app.route('/administracion')
def administracion():
    usuarios = crud.UsuarioCRUD(db).obtener_usuarios()
    return render_template('administracion.html', usuarios=usuarios)

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return render_template('index.html')


@app.route('/añadirusuario')
def añadirusuario():
    return render_template('añadirusuario.html')


@app.route('/registroadmin')
def registroadmin():
    return render_template('registroadmin.html')



def generar_qr(data):
    # Codificación de los datos en un código QR
    img = qrcode.make(data)

    # Guardado del código QR como archivo de imagen en memoria
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_byte = buffer.read()

    # Codificar la imagen en base64
    img_base64 = base64.b64encode(img_byte)

    # Retornar el código QR codificado en base64
    return img_base64.decode("utf-8")


@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        correo = request.form['correo']
        if nombre.strip() and contrasena.strip() and correo.strip():
            admin = Administrador.obtener_por_credenciales(nombre, contrasena, correo)
            if admin:
                session['nombre'] = admin['nombre']
                session['correo'] = admin['correo']
                session['contrasena'] = admin['contrasena']
                session['nip'] = admin['nip']

                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('añadirusuario'))
            else:
                flash("Credenciales incorrectas. Por favor, inténtalo de nuevo.", "error")
                return redirect(url_for('iniciar'))
        else:
            flash("Por favor, ingresa la información correcta", "error")
            return redirect(url_for('iniciar'))


        

@app.route('/agregarUsuario', methods=['POST'])
def agregarUsuario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        matricula = request.form.get('matricula')
        contrasena = request.form.get('contrasena')
        usuario = request.form.get('usuario')

        # Verificar si se proporcionaron todos los campos requeridos
        if nombre and matricula and contrasena and usuario:
            # Verificar la longitud de la contraseña
            if 6 <= len(contrasena) <= 10:
                # Verificar la longitud del nombre y usuario
                if 5 <= len(nombre) <= 15 and 5 <= len(usuario) <= 15:
                    # Verificar si la matrícula tiene exactamente 8 caracteres y son todos números
                    if len(matricula) == 8 and matricula.isdigit():
                        print("Datos del formulario:", nombre, matricula, contrasena, usuario)
                        
                        # Consultar la base de datos para obtener todos los registros de usuarios
                        usuarios_registrados = list(db.usuarios.find({}, {'matricula': 1}))
                        print("Usuarios registrados:", usuarios_registrados)
                        
                        # Verificar si la matrícula ya existe en algún registro de usuarios
                        matriculas_registradas = [usuario['matricula'] for usuario in usuarios_registrados]
                        print("Matrículas registradas:", matriculas_registradas)
                        
                        if int(matricula) in matriculas_registradas:
                            flash("La matrícula ya está registrada", "error")
                            print("La matrícula ya está registrada en la base de datos.")
                        else:
                            print("La matrícula no está registrada, procediendo con la inserción")

                            # Generar el código QR utilizando la matrícula del usuario
                            qr = generar_qr(matricula)

                            # Obtener la información de sesión del administrador
                            sesion_nombre = session.get('nombre')
                            sesion_correo = session.get('correo')
                            sesion_contrasena = session.get('contrasena')
                            sesion_nip = session.get('nip')

                            # Crear un objeto Administrador para el usuario actual
                            admin = Administrador(sesion_nombre, sesion_correo, sesion_contrasena, sesion_nip)

                            # Crear un nuevo objeto Usuario con los datos proporcionados
                            nuevo_usuario = Usuario(nombre, matricula, contrasena, usuario, qr, admin.aLaColeccion())

                            # Convertir el objeto Usuario en un diccionario para insertarlo en la base de datos
                            datos_usuario = nuevo_usuario.aLaColeccion()

                            # Insertar el nuevo usuario en la base de datos
                            db.usuarios.insert_one(datos_usuario)

                            # Mostrar un mensaje de éxito
                            flash("Usuario agregado correctamente", "success")
                            print("Usuario agregado correctamente")
                    else:
                        flash("La matrícula debe tener exactamente 8 caracteres y ser numérica", "error")
                        print("La matrícula debe tener exactamente 8 caracteres y ser numérica")
                else:
                    flash("La longitud del nombre y usuario debe estar entre 5 y 15 caracteres", "error")
                    print("La longitud del nombre y usuario debe estar entre 5 y 15 caracteres")
            else:
                flash("La contraseña debe tener entre 6 y 10 caracteres", "error")
                print("La contraseña debe tener entre 6 y 10 caracteres")
        else:
            # Mostrar un mensaje de error si falta información en el formulario
            flash("Falta información en el formulario", "error")
            print("Falta información en el formulario")

    # Redireccionar al formulario de añadir usuario
    return redirect(url_for('añadirusuario'))
        

@app.route('/verificarMatricula', methods=['POST'])
def verificar_matricula():
    data = request.json
    matricula = data.get('matricula')
    
    # Consultar la base de datos para verificar si la matrícula existe
    matricula_existe = db.usuarios.find_one({'matricula': matricula}) is not None
    
    return jsonify({"existe": matricula_existe})


db, administrador_collection = database.conexionBD()

@app.route('/administrador', methods=['POST'])
def agregarAdministrador():
    if request.method == 'POST':
        nombre = request.form['username']
        correo = request.form['email']
        contrasena = request.form['password']
        nip = request.form['nip']

        # Expresiones regulares para validar los campos
        regex_usuario = re.compile(r'^[a-zA-Z]{5,15}$')
        regex_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        regex_contrasena = re.compile(r'^\d{6,10}$')
        regex_nip = re.compile(r'^\d{5}$')

        # Verificar si los campos están completos y cumplen con las reglas
        if nombre and correo and contrasena and nip:
            if regex_usuario.match(nombre) and regex_correo.match(correo) and regex_contrasena.match(contrasena) and regex_nip.match(nip):
                nuevo_administrador = Administrador(nombre, correo, contrasena, nip)
                db.administrador.insert_one(nuevo_administrador.aLaColeccion())
                print("Datos insertados correctamente", "success")
                return redirect(url_for('iniciar'))
            else:
                print("Los datos no cumplen con los criterios de validación", "error")
                return redirect(url_for('registroadmin'))
        else:
            print("Falta información en el formulario", "error")
            return redirect(url_for('registroadmin'))
        
        
@app.route('/eliminar_usuario/<id>', methods=['POST'])
def eliminar_usuario(id):
    if request.method == 'POST':
        # Crear una instancia de UsuarioCRUD
        usuario_crud = crud.UsuarioCRUD(db)
        
        # Llamar al método eliminar_usuario de la instancia usuario_crud
        usuario_crud.eliminar_usuario(id)
        
        flash('Usuario eliminado correctamente', 'success')
        return redirect(url_for('administracion'))

    
@app.route('/editar_usuario/<id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'GET':
        # Lógica para obtener el usuario con el ID proporcionado
        usuario = crud.UsuarioCRUD.obtener_usuario_por_id(id)
        # Renderizar la plantilla de edición y pasar el usuario como contexto
        return render_template('editar_usuario.html', usuario=usuario)
    elif request.method == 'POST':
        # Lógica para actualizar el usuario con los datos enviados en el formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        crud.UsuarioCRUD.actualizar_usuario(id, nombre, correo)
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('administracion'))
    

    
coleccion_notificaciones = db['notificaciones']  # Nombre de la colección de notificaciones

@app.route('/notificaciones')
def mostrar_notificaciones():
    notificaciones = coleccion_notificaciones.find().sort([("fecha_hora", -1)])  
    notificaciones_formateadas = [
        {
            "id": str(notificacion['_id']),  # Convertir ObjectId a str
            "mensaje": f"Acceso concedido al usuario: {notificacion['nombre']}, la fecha de: {notificacion['fecha_hora'].strftime('%Y-%m-%d')}, a las: {notificacion['fecha_hora'].strftime('%H:%M:%S')}"
        } for notificacion in notificaciones
    ]
    return render_template('notificaciones.html', notificaciones=notificaciones_formateadas)

@app.route('/borrar_notificaciones', methods=['POST'])
def borrar_notificaciones():
    try:
        coleccion_notificaciones.delete_many({})  
        flash("Notificaciones borradas correctamente.")
    except Exception as e:
        flash("Error al borrar notificaciones: " + str(e))
    return redirect(url_for('mostrar_notificaciones'))

@app.route('/eliminar_notificacion/<string:notificacion_id>', methods=['POST'])
def eliminar_notificacion(notificacion_id):
    try:
        result = coleccion_notificaciones.delete_one({"_id": ObjectId(notificacion_id)})
        if result.deleted_count == 1:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Notificación no encontrada'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/estadisticas')
def estadisticas():
    # Suponiendo que 'db' es tu variable de conexión a la base de datos.
    try:
        accesos = db['accesos'].aggregate([
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$fecha_hora"}},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}  # Asegúrate de que los resultados estén ordenados
        ])
        accesos = list(accesos)  # Convertir el cursor a una lista

        # Verificar y depurar los datos recibidos
        print(accesos)

        fechas = [acceso['_id'] for acceso in accesos]
        conteos = [acceso['count'] for acceso in accesos]

        # Más impresiones de depuración si es necesario
        print(fechas)
        print(conteos)

        return render_template('estadisticas.html', fechas=fechas, conteos=conteos)
    except Exception as e:
        print("Error al obtener estadísticas:", e)
        return render_template('error.html')  # Una página de error genérica
    
@app.route('/eliminar_accesos', methods=['POST'])
def eliminar_accesos():
    try:
        # Aquí elimina todos los registros de la colección 'accesos'
        db['accesos'].delete_many({})
        # No necesitas devolver el mensaje {"success": true}
        return redirect(url_for('estadisticas'))  # Redirecciona a la página de estadísticas
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
