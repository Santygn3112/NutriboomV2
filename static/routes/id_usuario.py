from flask import jsonify, session

def ver_id_usuario():
    if "user" not in session:
        return jsonify({"mensaje": "Usuario no autenticado"}), 403

    user_id = session["user"]
    
    return jsonify({"id_usuario": user_id})
