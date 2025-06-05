import os
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from backend.Modelos.database import db
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.platos import Platos
from math import ceil

TIPOS_PLATO = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
CARPETA_IMAGENES = 'static/img/platos'  # Carpeta donde se guardarán las imágenes

def add_plato():
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre_plato = request.form['nombre']
        tipo_plato = request.form['tipo']
        lista_ingredientes = request.form.getlist('ingredientes')

        # Procesamos la imagen enviada por el usuario
        archivo_imagen = request.files['imagen']
        ruta_imagen = None

        if archivo_imagen:
            nombre_original = archivo_imagen.filename
            extension = nombre_original.split('.')[-1]  # Obtenemos la extensión del archivo
            nombre_archivo = secure_filename(nombre_plato + '.' + extension)
            ruta_completa = os.path.join(CARPETA_IMAGENES, nombre_archivo)

            # Creamos la carpeta si no existe
            if not os.path.exists(CARPETA_IMAGENES):
                os.makedirs(CARPETA_IMAGENES)

            # Guardamos la imagen en la carpeta correspondiente
            archivo_imagen.save(ruta_completa)
            ruta_imagen = 'img/platos/' + nombre_archivo  # Ruta relativa para usar en el HTML

        # Creamos el nuevo plato con sus datos
        nuevo_plato = Platos(nombre=nombre_plato, tipo=tipo_plato, imagen_plato=ruta_imagen)
        db.session.add(nuevo_plato)
        db.session.commit()

        # El método de SQLAlchemy permite insertar múltiples registros de manera eficiente.
        # Para cada id_ingrediente en la lista lista_ingredientes:
        #   - Asociamos el id_plato con el id_ingrediente
        #   - Creamos un diccionario con ambos valores y lo preparamos para la inserción en la tabla IngredientePlato
        # La función bulk_insert_mappings insertará todas estas relaciones en la base de datos de una sola vez.
        # A diferencia del add permite al mismo tiempo insertarlos
        relaciones = []
        for id_ingrediente in lista_ingredientes:
            relaciones.append({
                "id_plato": nuevo_plato.id_plato,
                "id_ingrediente": int(id_ingrediente)
            })

        db.session.bulk_insert_mappings(IngredientePlato, relaciones)
        db.session.commit()

        return redirect(url_for('platos'))

    ingredientes_disponibles = Ingredientes.query.all()
    return render_template('add_plato.html', ingredientes=ingredientes_disponibles, tipos_plato=TIPOS_PLATO)
