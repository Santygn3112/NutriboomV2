from flask import jsonify, session
from backend.Modelos.database import db
from sqlalchemy import text

def ver_id_usuario():
    if "user" not in session:
        return jsonify({"mensaje": "Usuario no autenticado"}), 403

    user_id = session["user"]
    
    return jsonify({"id_usuario": user_id})
