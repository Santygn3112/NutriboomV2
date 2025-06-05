from flask import render_template, redirect, request, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Datos_personales import Datos_personales
from backend.Modelos.platos import Platos
from backend.Modelos.IngredientePlato import IngredientePlato
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.IngredientePlatoUsuario import IngredientePlatoUsuario

def calcular_porcentajes_comidas(user_id, dia):
    registros = (
        db.session.query(
            IngredientePlatoUsuario.cantidad,
            Ingredientes,
            Platos.tipo,
        )
        .join(Ingredientes, IngredientePlatoUsuario.id_ingrediente == Ingredientes.id_ingrediente)
        .join(Platos, IngredientePlatoUsuario.id_plato == Platos.id_plato)
        .filter(IngredientePlatoUsuario.id_usuario == user_id, IngredientePlatoUsuario.dia == dia)
        .all()
    )

    totales = {"calorias": 0.0, "proteina": 0.0, "carbs": 0.0, "grasas": 0.0}
    por_comida = {}

    for cantidad, ingrediente, tipo in registros:
        cantidad = float(cantidad)
        prote = float(ingrediente.proteina) * cantidad / 100
        carbs = float(ingrediente.carbohidratos) * cantidad / 100
        grasas = (float(ingrediente.grasas_Saturadas) + float(ingrediente.grasas_NO_Saturadas)) * cantidad / 100
        calorias = prote * 4 + carbs * 4 + grasas * 9

        datos = por_comida.setdefault(tipo, {"calorias": 0.0, "proteina": 0.0, "carbs": 0.0, "grasas": 0.0})
        datos["calorias"] += calorias
        datos["proteina"] += prote
        datos["carbs"] += carbs
        datos["grasas"] += grasas

        totales["calorias"] += calorias
        totales["proteina"] += prote
        totales["carbs"] += carbs
        totales["grasas"] += grasas

    porcentajes = {}
    for tipo, valores in por_comida.items():
        porcentajes[tipo] = {}
        for clave in ["calorias", "proteina", "carbs", "grasas"]:
            total_val = totales[clave]
            if total_val > 0:
                porcentajes[tipo][clave] = round(valores[clave] * 100 / total_val, 2)
            else:
                porcentajes[tipo][clave] = 0.0

    total_porcentajes = {k: 0 for k in totales.keys()}
    for datos in porcentajes.values():
        for k in total_porcentajes:
            total_porcentajes[k] += datos[k]
    for k in total_porcentajes:
        total_porcentajes[k] = round(total_porcentajes[k], 2)

    return porcentajes, round(totales["calorias"], 2), total_porcentajes
# genera una lista de platos, segun su tipo
def generarListPlatosPorTipo(tipo):
    platos = Platos.query.filter(Platos.tipo == tipo).all()
    return platos
# genera los ingredientes del plato en cuestion
def obtenerIngredientesPlato(id_platos):
    ingredientes = []
    ingredientesPlato = IngredientePlato.query.filter(IngredientePlato.id_plato ==id_platos).all()
    for ing in ingredientesPlato:
        ingrediente = Ingredientes.query.filter(Ingredientes.id_ingrediente == ing.id_ingrediente).first()
        ingredientes.append(ingrediente)
    return ingredientes
# funcion que genera modales segun el numero de comidas
def generarModales(numComidas, dia, user_id):
    html_modals = ""
    comidas = ["Comida","Cena","Desayuno","Merienda","Almuerzo"]
    # segun el numero de comidas
    for num in range(numComidas):
       tipo = comidas[num]
       platos = generarListPlatosPorTipo(tipo)
       html_modals = html_modals + f"""
      <div id="modalplatos{tipo}" class="modal fade modal-dialog-scrollable" data-bs-backdrop="static" tabindex="-1" aria-labelledby="modalplatostitulo{tipo}" data-bs-keyboard="false">
    
    <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="modalplatostitulo{tipo}">Platos: {tipo}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
"""        
       for plato in platos:
          ingredientePlato = obtenerIngredientesPlato(plato.id_plato)
          valores_usuario = {ipu.id_ingrediente: ipu.cantidad for ipu in IngredientePlatoUsuario.query.filter_by(id_usuario=user_id, dia=dia, id_plato=plato.id_plato).all()}
          html_modals = html_modals + f"""
           <div class="d-flex align-items-start">
           <form method="POST" action="{ url_for('seleccionar_plato',id_plato=plato.id_plato, dia=dia  ) }">
              <img src="{ url_for('static', filename=plato.imagen_plato) }" class="rounded me-3" alt="Imagen" style="width: 80px; height: 80px;">
              <div>
                <h5 class="mb-2">{plato.nombre}</h5>
              <div class="row row-cols-2 g-2 mb-3">
"""         
          # allow the user to enter how much of each ingredient they ate
          for ingrediente in ingredientePlato:
            valor_existente = valores_usuario.get(ingrediente.id_ingrediente, "")
            html_modals = html_modals + f"""
            <div class="col">
              <label class="form-label">{ingrediente.nombre}</label>
              <input type="number" step="0.01" min="0" name="cantidad_{ingrediente.id_ingrediente}" class="form-control" value="{valor_existente}" required>
            </div>
"""
          html_modals = html_modals + f"""
                 </div>
                  <button class="btn btn-sm btn-success">Seleccionar</button>
                  </form>
                </div>
              </div>
"""
       html_modals = html_modals + """      
       </div>
    </div>
  </div>
    </div>
    """
    return html_modals
# genera el arcodeon y sus "tarjetas" segun el numero de comidas
def generarTajetasPlatos(numComidas, dia, user_id):
    comidas = ["Comida","Cena","Desayuno","Merienda","Almuerzo"]
    modales = generarModales(numComidas, dia, user_id)
    html_code = """<div class="accordion" id="accordionPanelsStayOpenExampletipo">"""
    #segun el numero de comidas
    for num in range(numComidas):
      tipo = comidas[num]
      plato = (
      Platos.query.join(IngredientePlatoUsuario, IngredientePlatoUsuario.id_plato == Platos.id_plato)
      .filter(IngredientePlatoUsuario.dia==dia, Platos.tipo == tipo)
      .group_by(Platos.id_plato).first()
      )
      if plato:
          IpuLista = IngredientePlatoUsuario.query.filter(IngredientePlatoUsuario.id_usuario == user_id, IngredientePlatoUsuario.dia == dia,IngredientePlatoUsuario.id_plato == plato.id_plato ).all()
          html_code = html_code +  f"""
          
                  <div class="accordion-item{tipo}">
                    <h2 class="accordion-header" id="panelsStayOpen-heading{tipo}">
                      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{tipo}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{tipo}">
                        {tipo}
                      </button>
                    </h2>
                    <div id="panelsStayOpen-collapse{tipo}" class="accordion-collapse collapse show" aria-labelledby="panelsStayOpen-heading{tipo}">
                      <div class="accordion-body">
                      <div class="d-flex align-items-start">
                      <img src="{ url_for('static', filename=plato.imagen_plato) }" class="rounded me-3" alt="Imagen" style="width: 80px; height: 80px;">
                        <div>
                        <h5 class="mb-2">{plato.nombre}</h5>
                        <div class="row row-cols-2 g-2 mb-3">
                        """
          # por cada ingredientePlatoUsario
          for ipu in IpuLista:
                        ingrediente = Ingredientes.query.filter(Ingredientes.id_ingrediente == ipu.id_ingrediente).first()
                        html_code = html_code +  f""" 
                        <div class="col"><span class="badge bg-secondary w-100">{ingrediente.nombre}: {ipu.cantidad}g</span></div>
                        """
          html_code = html_code +  f""" 
                        </div>
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalplatos{tipo}">
                          Editar {tipo}
                        </button>
                      </div>
                    </div>
                  </div>
                  </div>
                """
      else:
          html_code = html_code +  f"""
          <div class="accordion" id="accordionPanelsStayOpenExampletipo">
                  <div class="accordion-item{tipo}">
                    <h2 class="accordion-header" id="panelsStayOpen-heading{tipo}">
                      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{tipo}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{tipo}">
                        {tipo}
                      </button>
                    </h2>
                    <div id="panelsStayOpen-collapse{tipo}" class="accordion-collapse collapse show" aria-labelledby="panelsStayOpen-heading{tipo}">
                      <div class="accordion-body">
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalplatos{tipo}">
                          Seleccionar {tipo}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                """ 
    return html_code, modales   
# funcion central de calendario dieta
def calendario_dieta(dia="Lunes"): 
    
    if "user" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user"]
    datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

    if not datos:
        return redirect(url_for("datos_personales"))
    

    datos_Usuario = Datos_personales.query.filter_by(id_usuario=user_id).first()

    html, modales = generarTajetasPlatos(int(datos_Usuario.numero_Comidas), dia, user_id)
    porcentajes, total_calorias, total_porcentajes = calcular_porcentajes_comidas(user_id, dia)

    calorias_objetivo = float(datos_Usuario.calorias_permitidas)
    diferencia_calorias = calorias_objetivo - total_calorias

    return render_template(
        "CalendarioDieta.html",
        day=dia,
        html=html,
        modales=modales,
        porcentajes=porcentajes,
        total_porcentajes=total_porcentajes,
        total_calorias=total_calorias,
        calorias_objetivo=calorias_objetivo,
        diferencia_calorias=diferencia_calorias,
    )

#Funcion que coje el plato y lo asigna al dia y al usuario
def seleccionar_plato(id_plato, dia):
    if "user" not in session:
      return redirect(url_for("login"))
    if request.method == 'POST':
      user_id = int(session["user"])
      plato_nuevo = Platos.query.get(id_plato)
      if plato_nuevo:
        platos_mismo_tipo = db.session.query(Platos.id_plato).filter(Platos.tipo == plato_nuevo.tipo).subquery()
        db.session.query(IngredientePlatoUsuario).filter(
            IngredientePlatoUsuario.id_usuario==user_id,
            IngredientePlatoUsuario.dia==dia,
            IngredientePlatoUsuario.id_plato.in_(platos_mismo_tipo)
        ).delete(synchronize_session=False)

      Ingredientes = obtenerIngredientesPlato(id_plato)

      # read the amount the user entered for each ingredient
      for ing in Ingredientes:
        cantidad = request.form.get(f"cantidad_{ing.id_ingrediente}", 0)
        try:
          cantidad = float(cantidad)
        except (TypeError, ValueError):
          cantidad = 0.0

        nuevo_ing_user_plato = IngredientePlatoUsuario(
          id_plato=id_plato,
          id_ingrediente=ing.id_ingrediente,
          id_usuario= int(session["user"]),
          cantidad = cantidad,
          dia= dia
        )
        db.session.add(nuevo_ing_user_plato)

      db.session.commit()

    return redirect(url_for("calendario_dieta", dia=dia))


# funcion que nos da los porcentajes segun el tipo de dieta 
#Ahora mismo no esta en funcionamiento
def obtenerPorcentajes(tipo_dieta):
    porcentaje = {}
    match tipo_dieta:
        case "Subir":
            porcentaje = {"proteina": float(0.35), "carbs": float(0.45), "grasas": float(0.20)}
        case "Bajar":
            porcentaje = {"proteina": float(0.45), "carbs": float(0.35), "grasas": float(0.20)}
        case "Mantenerse":
            porcentaje = {"proteina": float(0.30), "carbs": float(0.50), "grasas": float(0.20)}     
    return porcentaje     