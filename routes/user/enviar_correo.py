from flask_mail import Mail, Message

# Instancia de Flask-Mail global
mail = Mail()

def enviar_correo(app, asunto, destinatario, cuerpo, archivos=None):
    """
    Envía un correo electrónico usando Flask-Mail.
    
    :param app: instancia de Flask app
    :param asunto: asunto del correo
    :param destinatario: email del destinatario
    :param cuerpo: cuerpo del mensaje
    :param archivos: lista de rutas de archivos a adjuntar (opcional)
    """
    mail.init_app(app)

    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo

    # Si hay archivos, los adjuntamos
    if archivos:
        for archivo in archivos:
            with app.open_resource(archivo) as adjunto:
                filename = archivo.split("/")[-1]  # Nombre del archivo
                msg.attach(filename, "application/octet-stream", adjunto.read())

    mail.send(msg)
