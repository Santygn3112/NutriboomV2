from flask import render_template, request, redirect, url_for, session
from backend.Modelos.Datos_personales import Datos_personales
from backend.Modelos.database import db
from backend.Modelos.Info_diaria import Info_diaria
from math import ceil

def info_diaria():
    if 'user' not in session:
        return redirect(url_for('login'))
    

    user_id = int(session["user"])  # Obtener el ID del usuario desde la sesión

    
    datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

    if not datos:
        return redirect(url_for("datos_personales"))

    # Obtener la página actual, con un valor por defecto de 1
    pagina = request.args.get('page', 1, type=int)
    per_page = 10

    # Paginación de la info diaria del usuario
    info_diaria_paginated = Info_diaria.query.filter_by(id_usuario=user_id).paginate(page=pagina, per_page=per_page)

    return render_template(
        'info_diaria/info_diaria.html', 
        info_diaria=info_diaria_paginated.items,  # Pasar la información diaria paginada
        current_page=pagina,
        total_pages=ceil(Info_diaria.query.filter_by(id_usuario=user_id).count() / per_page),  # Calcular el total de páginas
    )
