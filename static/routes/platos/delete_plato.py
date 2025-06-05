from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.platos import Platos
from math import ceil



def delete_plato(id_plato):
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    plato = Platos.query.get(id_plato)
    if plato:
        # Se elimina el Ingrediente plato
        db.session.query(IngredientePlato).filter_by(id_plato=id_plato).delete()
        # Se elimina el plato
        db.session.delete(plato)
        db.session.commit()

    return redirect(url_for('platos'))
