from flask import render_template, session, redirect, url_for
from backend.Modelos.Datos_personales import Datos_personales
from backend.Modelos.Usuario import Usuario

def cuenta():
    # Verifica si el usuario está en sesión
    user_id = session.get("user")
    if not user_id:
        return redirect(url_for("login"))

    # Verifica si el usuario tiene datos personales
    datos = Datos_personales.query.filter_by(id_usuario=user_id).first()
    if not datos:
        return redirect(url_for("datos_personales"))

    # Obtiene el objeto Usuario
    usuario = Usuario.query.filter_by(id_usuario=user_id).first()
    if not usuario:
        return "Usuario no encontrado", 404

    # Renderiza la plantilla con los datos del usuario
    return render_template('usuario_configuracion/cuenta.html', usuario=usuario)
