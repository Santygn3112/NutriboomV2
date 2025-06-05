from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.platos import Platos
from math import ceil
import os
from werkzeug.utils import secure_filename

TIPOS_PLATO = ["Desayuno", "Almuerzo", "Merienda", "Cena"]

def update_plato(id_plato):
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    plato_a_editar = Platos.query.get(id_plato)
    if not plato_a_editar:
        return redirect(url_for('platos'))

    if request.method == 'POST':
        # Actualizar campos básicos
        plato_a_editar.nombre = request.form['nombre']
        plato_a_editar.tipo = request.form['tipo']
        nuevos_ingredientes = request.form.getlist('ingredientes')

        # Guardar nueva imagen si se subió
        imagen = request.files.get('imagen')
        if imagen and imagen.filename:
            filename = secure_filename(imagen.filename)
            ruta_carpeta = 'static/img/platos'
            os.makedirs(ruta_carpeta, exist_ok=True)
            imagen.save(os.path.join(ruta_carpeta, filename))
            plato_a_editar.imagen_plato = f'img/platos/{filename}'

        # Actualizar ingredientes
        db.session.query(IngredientePlato).filter_by(id_plato=id_plato).delete()
        db.session.bulk_insert_mappings(
            IngredientePlato,
            [{"id_plato": id_plato, "id_ingrediente": int(i)} for i in nuevos_ingredientes]
        )

        db.session.commit()
        return redirect(url_for('platos'))

    # GET: Mostrar formulario de edición
    ingredientes = Ingredientes.query.all()
    ingredientes_ids = [ingrediente.id_ingrediente for ingrediente in plato_a_editar.ingredientes]

    pagina = request.args.get('page', 1, type=int)
    per_page = 10
    platos_paginated = Platos.query.paginate(page=pagina, per_page=per_page)

    return render_template(
        'platos/platos.html',
        ingredientes=ingredientes,
        platos=platos_paginated.items,
        tipos_plato=TIPOS_PLATO,
        current_page=pagina,
        total_pages=ceil(Platos.query.count() / per_page),
        plato_a_editar=plato_a_editar,
        ingredientes_ids=ingredientes_ids
    )
