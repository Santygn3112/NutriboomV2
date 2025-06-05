from flask import render_template, request, redirect, url_for, session
from backend.Modelos.database import db
from backend.Modelos.Info_diaria import Info_diaria  

# Esta función se encarga de eliminar un registro de información diaria basado en su ID.
def delete_info_diaria(id_info_diaria):
    # Verifica si el usuario tiene permisos de administrador. Si no, redirige al inicio de sesión.
    if 'is_admin' not in session:
        return redirect(url_for('login'))

    # Busca el registro de información diaria en la base de datos usando el ID proporcionado.
    info = Info_diaria.query.get(id_info_diaria)
    
    # Si el registro existe, lo elimina de la base de datos.
    if info:
        db.session.delete(info)
        db.session.commit()

    # Redirige a la página de información diaria después de completar la operación.
    return redirect(url_for('info_diaria'))
