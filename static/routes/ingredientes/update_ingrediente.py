from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.platos import Platos
from math import ceil

def update_ingrediente(id_ingrediente):
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    # Recuperamos el ingrediente a editar
    ingrediente_a_editar = Ingredientes.query.get(id_ingrediente)
    if not ingrediente_a_editar:
        return redirect(url_for('ingredientes'))

    if request.method == 'POST':
        # Actualizamos los atributos del ingrediente
        ingrediente_a_editar.nombre = request.form['nombre']
        ingrediente_a_editar.grasas_Saturadas = request.form['grasas_Saturadas']
        ingrediente_a_editar.grasas_NO_Saturadas = request.form['grasas_NO_Saturadas']
        ingrediente_a_editar.carbohidratos = request.form['carbohidratos']
        ingrediente_a_editar.azucar = request.form['azucar']
        ingrediente_a_editar.proteina = request.form['proteina']
        
        db.session.commit()  # Guardamos los cambios
        return redirect(url_for('ingredientes'))  # Redirigimos a la lista de ingredientes

    return render_template('ingredientes/edit_ingrediente.html', ingrediente=ingrediente_a_editar)
