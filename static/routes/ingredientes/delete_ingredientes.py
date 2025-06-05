from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato

def delete_ingredientes():
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    # Obtener los IDs de los ingredientes seleccionados
    ids = request.form.getlist('ids')

    # Eliminar las relaciones en la tabla intermedia IngredientePlato
    IngredientePlato.query.filter(IngredientePlato.id_ingrediente.in_(ids)).delete()

    # Eliminar los ingredientes seleccionados
    Ingredientes.query.filter(Ingredientes.id_ingrediente.in_(ids)).delete()

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Redirigir a la lista de ingredientes
    return redirect(url_for('ingredientes'))
