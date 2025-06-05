from flask import render_template, request, redirect, session, url_for
from backend.Modelos.Info_diaria import Info_diaria
from backend.Modelos.Datos_personales import Datos_personales
from backend.Modelos.database import db
from datetime import datetime, date

def add_info_diaria():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        peso = request.form['peso']
        grasa_corporal = request.form['grasa_corporal']
        fecha = request.form['fecha']  # Obtener la fecha desde el formulario

        # Convertir la fecha en formato YYYY-MM-DD a tipo date
        fecha_formato = datetime.strptime(fecha, '%Y-%m-%d').date()

        datos_personales = Datos_personales.query.filter_by(id_usuario=session['user']).first()
        altura = float(datos_personales.altura) if datos_personales else None
        imc = float(peso) / (altura ** 2) if altura else None

        # Verificar si ya existe una entrada para el usuario en la fecha dada
        info_diaria_existente = Info_diaria.query.filter_by(
            id_usuario=session['user']
        ).filter(Info_diaria.fecha == fecha_formato).first()

        if info_diaria_existente:
            # Si ya existe, actualizamos la entrada
            info_diaria_existente.peso = float(peso)
            info_diaria_existente.grasa_corporal = float(grasa_corporal)
            info_diaria_existente.imc = imc
        else:
            # Si no existe, la creamos
            nueva_info_diaria = Info_diaria(
                id_usuario=int(session['user']),
                fecha=fecha_formato,  # Solo la fecha (sin la parte de la hora)
                peso=float(peso),
                grasa_corporal=float(grasa_corporal),
                imc=imc
            )
            db.session.add(nueva_info_diaria)

        db.session.commit()
        return redirect(url_for('info_diaria'))

    return render_template('add_info_diaria.html')
