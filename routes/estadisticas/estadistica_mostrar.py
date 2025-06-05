from flask import redirect, render_template, session, url_for
from backend.Modelos.Datos_personales import Datos_personales

# Lista de tipos de estadísticas válidos que se pueden mostrar
TIPOS_VALIDOS = ['masa_muscular', 'peso', 'grasa_corporal', 'imc', 'calorias']

def mostrar_estadistica(tipo_estadistica):
    if "user" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user"]
    datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

    if not datos:
        return redirect(url_for("datos_personales"))

    # Verifica si el tipo de estadística solicitado está en la lista de tipos válidos
    if tipo_estadistica in TIPOS_VALIDOS:
        # Si es válido, renderiza la plantilla HTML y pasa el tipo de estadística como contexto
        return render_template('estadisticas.html', tipo=tipo_estadistica)
    else:
        # Si no es válido, devuelve un mensaje de error con un código de estado 404
        return render_template('error.html', mensaje="Tipo de estadística no encontrada"), 404
