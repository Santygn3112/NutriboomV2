from flask import jsonify
from backend.Modelos.database import db
from sqlalchemy import text
from flask import session
from backend.Modelos.Info_diaria import Info_diaria

# Esta función genera estadísticas generales para un usuario específico
def estadistica_general(id_usuario):
    # Consultamos los registros diarios del usuario en la base de datos
    registros = Info_diaria.query.filter(Info_diaria.id_usuario == id_usuario).all()
    
    # Si no hay registros, devolvemos un mensaje indicando que no hay datos
    if not registros:
        return jsonify({"mensaje": "No hay datos registrados para este usuario"})

    datos = []  # Lista para almacenar los datos procesados
    for reg in registros:
        # Calculamos la masa muscular usando el peso y el porcentaje de grasa corporal
        masa_muscular = float(reg.peso) * (1 - float(reg.grasa_corporal) / 100)
        
        # Agregamos los datos procesados a la lista
        datos.append({
            "dia": reg.fecha.strftime("%A"),  # Día de la semana
            "peso": float(reg.peso),  # Peso del usuario
            "grasa_corporal": float(reg.grasa_corporal),  # Porcentaje de grasa corporal
            "masa_muscular": round(masa_muscular, 2),  # Masa muscular redondeada a 2 decimales
            "imc": float(reg.imc) if reg.imc is not None else None
        })
    
    # Devolvemos los datos en formato JSON
    return jsonify(datos)
