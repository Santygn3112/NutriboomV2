from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.platos import Platos
from math import ceil

def delete_ingrediente(id_ingrediente):
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    ingrediente = Ingredientes.query.get(id_ingrediente)
    
    if ingrediente:
        # Eliminar todas las relaciones de IngredientePlato para este ingrediente
        db.session.query(IngredientePlato).filter_by(id_ingrediente=id_ingrediente).delete()
        
        # Ahora, revisar si el ingrediente está asociado a algún plato
        relaciones_ingrediente = db.session.query(IngredientePlato).filter_by(id_ingrediente=id_ingrediente).all()

        # Si no hay relaciones con otros platos, eliminamos el ingrediente
        if not relaciones_ingrediente:
            db.session.delete(ingrediente)
        
        db.session.commit()

    return redirect(url_for('ingredientes'))
