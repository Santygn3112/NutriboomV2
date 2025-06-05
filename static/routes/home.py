from flask import render_template, redirect, url_for, session
from backend.Modelos.Datos_personales import Datos_personales

def home():
    # Verificar si el usuario ha iniciado sesión
    if "user" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user"]
    is_admin = session.get("is_admin", False)

    # Recuperar los datos personales del usuario
    datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

    # Si no es admin y no tiene datos personales, pedir que los complete
    if not is_admin and not datos:
        return redirect(url_for("datos_personales"))

    # Si no es admin y sí tiene datos personales, mostrar seguimiento
    if not is_admin and datos:
        return render_template(
            "SeguimientoNutricional.html",
            datos=datos
        )

    # Si es admin, ir a la página de gestión de platos
    return redirect(url_for("platos"))
