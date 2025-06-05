from flask import render_template, request, redirect, session, url_for
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.database import db

def add_ingrediente():
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        grasas_saturadas = request.form['grasas_saturadas']
        grasas_no_saturadas = request.form['grasas_no_saturadas']
        carbohidratos = request.form['carbohidratos']
        azucar = request.form['azucar']
        proteina = request.form['proteina']

        # Validar que los valores numéricos sean correctos
        grasas_saturadas = float(grasas_saturadas)
        grasas_no_saturadas = float(grasas_no_saturadas)
        carbohidratos = float(carbohidratos)
        azucar = float(azucar)
        proteina = float(proteina)

        # Crear un nuevo ingrediente con los datos del formulario
        nuevo_ingrediente = Ingredientes(
            nombre=nombre,
            grasas_Saturadas=grasas_saturadas,
            grasas_NO_Saturadas=grasas_no_saturadas,
            carbohidratos=carbohidratos,
            azucar=azucar,
            proteina=proteina
        )

        # Agregar el nuevo ingrediente a la base de datos
        db.session.add(nuevo_ingrediente)
        db.session.commit()

        return redirect(url_for('ingredientes'))

    return render_template('add_ingrediente.html')  # Mostrar el formulario para añadir ingredientes
