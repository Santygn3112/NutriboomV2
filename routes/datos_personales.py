from flask import render_template, request, redirect, url_for, session
from backend.Modelos.Datos_personales import Datos_personales
from backend.Modelos.database import db
#Funcion que permite calvular las calorias minimas para que el usuario se mantenga
def calcular_calorias_base(edad, genero, altura, nivel_actividad):
    altura_cm = altura * 100 

    if genero == "Masculino":
        bmr = 88.362 + (13.397 * altura_cm) - (5.677 * edad)
    else:
        bmr = 447.593 + (9.247 * altura_cm) - (4.330 * edad)
    
    if nivel_actividad == 1:
        bmr *= 1.2
    elif nivel_actividad == 2:
        bmr *= 1.375
    elif nivel_actividad == 3:
        bmr *= 1.55
    elif nivel_actividad == 4:
        bmr *= 1.725
    elif nivel_actividad == 5:
        bmr *= 1.9
    return bmr
# Funcion que abre la ventana de datos personales y actualiza los valores al darle a guardar
def datos_personales():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = int(session["user"])

    if request.method == "POST":
        altura = float(request.form.get("altura", 0))
        edad = int(request.form.get("edad", 0))
        genero = request.form.get("genero", "Masculino")
        nivel_actividad = int(request.form.get("nivel_actividad", 1))
        tipo_dieta = request.form.get("tipo_dieta", "Mantenerse")
        calorias_base = calcular_calorias_base(edad, genero, altura, nivel_actividad)
        # Daba error con 0  por lo tanto he tenido que poner 0.0
        calorias_permitidas = float(request.form.get("calorias_permitidas") or 0.0)
        numero_Comidas = int(request.form.get("numero_Comidas", 1))

        datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

        if not datos:
            nuevo_dato = Datos_personales(
                id_usuario=user_id,
                altura=altura,
                edad=edad,
                genero=genero,
                nivel_actividad=nivel_actividad,
                tipo_dieta=tipo_dieta,
                calorias_base=calorias_base,
                calorias_permitidas=calorias_permitidas,
                numero_Comidas=numero_Comidas
            )
            db.session.add(nuevo_dato)
        else:
            datos.altura = altura
            datos.edad = edad
            datos.genero = genero
            datos.nivel_actividad = nivel_actividad
            datos.tipo_dieta = tipo_dieta
            datos.calorias_base = calorias_base
            datos.calorias_permitidas = calorias_permitidas
            datos.numero_Comidas = numero_Comidas

        db.session.commit()

        return redirect(url_for("home"))

    datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

    if datos:
        return render_template("datos_personales.html", datos=datos)

    return render_template("datos_personales.html", mensaje="No tienes datos registrados.")
