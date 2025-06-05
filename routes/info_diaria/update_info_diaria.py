from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Info_diaria import Info_diaria
from backend.Modelos.Datos_personales import Datos_personales
from datetime import datetime

def update_info_diaria(id_info_diaria):
    if 'user' not in session:
        return redirect(url_for('login'))

    # Obtener la entrada de info diaria a editar
    info_a_editar = Info_diaria.query.get(id_info_diaria)
    if not info_a_editar:
        return redirect(url_for('info_diaria'))

    # Verifica que el usuario solo edite su propia info diaria
    if info_a_editar.id_usuario != int(session['user']):
        return redirect(url_for('info_diaria'))

    if request.method == 'POST':
        # Actualizar los atributos
        info_a_editar.peso = float(request.form['peso'])
        info_a_editar.grasa_corporal = float(request.form['grasa_corporal'])

        datos_personales = Datos_personales.query.filter_by(id_usuario=session['user']).first()
        altura = float(datos_personales.altura) if datos_personales else None
        info_a_editar.imc = float(info_a_editar.peso) / (altura ** 2) if altura else None
        info_a_editar.fecha = datetime.now()  # Si quieres actualizar la fecha a "ahora"

        db.session.commit()
        return redirect(url_for('info_diaria'))

    return render_template('info_diaria/edit_info_diaria.html', info=info_a_editar)
