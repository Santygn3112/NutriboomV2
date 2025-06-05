from flask import render_template, request, redirect, url_for
from backend.Modelos.database import db
from backend.Modelos.Usuario import Usuario
import bcrypt

def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido1 = request.form.get("apellido1", "")
        apellido2 = request.form.get("apellido2", "")
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        confirmar_contrasena = request.form["confirmar_contrasena"]

        if contrasena != confirmar_contrasena:
            return render_template("register.html", error="Las contraseñas no coinciden.")

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template("register.html", error="Correo electrónico ya registrado.")

        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            email=email,
            contrasena=contrasena_encriptada,
            is_admin=False
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")
