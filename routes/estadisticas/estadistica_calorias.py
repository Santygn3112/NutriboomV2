from flask import jsonify
from backend.Modelos.IngredientePlatoUsuario import IngredientePlatoUsuario
from backend.Modelos.Ingredientes import Ingredientes
from backend.Modelos.database import db


def estadistica_calorias(id_usuario):
    dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    resultados = []

    # Verificar si existen registros para el usuario
    existe = db.session.query(IngredientePlatoUsuario).filter_by(id_usuario=id_usuario).first()
    if not existe:
        return jsonify({"mensaje": "No hay datos registrados para este usuario"})

    for dia in dias_semana:
        registros = (
            db.session.query(
                IngredientePlatoUsuario.cantidad,
                Ingredientes.grasas_Saturadas,
                Ingredientes.grasas_NO_Saturadas,
                Ingredientes.carbohidratos,
                Ingredientes.proteina,
            )
            .join(Ingredientes, IngredientePlatoUsuario.id_ingrediente == Ingredientes.id_ingrediente)
            .filter(
                IngredientePlatoUsuario.id_usuario == id_usuario,
                IngredientePlatoUsuario.dia == dia,
            )
            .all()
        )

        total_dia = 0.0
        for cantidad, g_sat, g_no_sat, carbs, prote in registros:
            cantidad = float(cantidad)
            grasas = (float(g_sat) + float(g_no_sat)) * cantidad / 100
            proteina = float(prote) * cantidad / 100
            carbohidratos = float(carbs) * cantidad / 100
            calorias = proteina * 4 + carbohidratos * 4 + grasas * 9
            total_dia += calorias

        resultados.append({"dia": dia, "calorias": round(total_dia, 2)})

    return jsonify(resultados)
