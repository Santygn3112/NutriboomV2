from flask import render_template, request, redirect, session, url_for
from backend.Modelos.database import db
from backend.Modelos.Usuario import Usuario
from backend.Modelos.Datos_personales import Datos_personales
import bcrypt

def login():
    # Si ya hay un usuario en la sesión, redirigir al home
    if "user" in session:
        return redirect(url_for("home"))

    # Si es un POST request, es decir, el formulario de login fue enviado
    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        # Buscar el usuario por su email
        usuario_encontrado = Usuario.query.filter_by(email=email).first()

        # Verificar que el usuario existe y que la contraseña es correcta
        if usuario_encontrado and bcrypt.checkpw(contrasena.encode("utf-8"), usuario_encontrado.contrasena.encode("utf-8")):
            # Si las credenciales son correctas, guardamos el id del usuario en la sesión
            session["user"] = usuario_encontrado.id_usuario
            session["is_admin"] = usuario_encontrado.is_admin  # Guardamos el estado de admin en la sesión

            # Recuperamos los datos personales del usuario
            user_id = session["user"]
            datos = Datos_personales.query.filter_by(id_usuario=user_id).first()

            # Si el usuario no es admin y no tiene datos personales, lo redirigimos a la página de datos personales
            if not usuario_encontrado.is_admin and not datos:
                return redirect(url_for("datos_personales"))

            # Si el login fue exitoso y el usuario tiene datos personales (o es admin), lo redirigimos al home
            return redirect(url_for("home"))

        # Si las credenciales no son correctas, mostramos un mensaje de error
        return render_template("login.html", error="Credenciales incorrectas")

    # Si es un GET request, simplemente mostramos la página de login
    return render_template("login.html")
