from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Info_diaria import Info_diaria

def delete_info_diarias():
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    # Obtener los IDs de las informaciones diarias seleccionadas
    ids = request.form.getlist('ids')

    # Eliminar las informaciones diarias del usuario seleccionadas
    Info_diaria.query.filter(Info_diaria.id_info_diaria.in_(ids)).delete()

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Redirigir a la lista de info diaria
    return redirect(url_for('info_diaria'))
