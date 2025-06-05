from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.platos import Platos
from math import ceil


def delete_platos():
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    ids = request.form.getlist('ids')
    Platos.query.filter(Platos.id_plato.in_(ids)).delete()
    db.session.commit()

    return redirect(url_for('platos'))
