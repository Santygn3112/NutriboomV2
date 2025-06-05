from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from math import ceil

def ingredientes():
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    # Obtener parámetros de búsqueda y paginación
    pagina = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 10

    # Construir la consulta con filtro opcional por nombre
    query = Ingredientes.query
    if search:
        query = query.filter(Ingredientes.nombre.ilike(f"%{search}%"))

    ingredientes_paginated = query.order_by(Ingredientes.id_ingrediente.desc()).paginate(page=pagina, per_page=per_page)

    return render_template(
        'ingredientes/ingredientes.html',
        ingredientes=ingredientes_paginated.items,
        current_page=pagina,
        total_pages=ceil(query.count() / per_page),
        search_query=search
    )
