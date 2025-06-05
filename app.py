from datetime import datetime
import locale
import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from backend.Modelos.database import db, init_db

from routes import *


load_dotenv()  


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))
CORS(app)

init_db(app)




app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# HOME
app.add_url_rule('/', 'home', home)  

# AUTENTIFICACION
app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])
app.add_url_rule('/register', 'register', register, methods=["GET", "POST"])
app.add_url_rule('/cerrar_sesion', 'logout', logout)
app.add_url_rule('/olvidado_contraseña', 'olvidado_contraseña', olvidado_contraseña, methods=["GET", "POST"])
app.add_url_rule('/update_usuario', 'update_usuario', update_usuario, methods=['POST']) 


# USUARIO
app.add_url_rule('/ver_id_usuario', 'ver_id_usuario', ver_id_usuario)
app.add_url_rule('/cuenta', 'cuenta', cuenta)
app.add_url_rule('/cambiar_contraseña', 'cambiar_contraseña', update_contraseña, methods=["GET", "POST"])
app.add_url_rule('/restablecer_contraseña/<token>', 'restablecer_contraseña', restablecer_contraseña, methods=["GET", "POST"])


# ESTADISTICA
app.add_url_rule('/estadistica_general/<int:id_usuario>', 'estadistica_general', estadistica_general)
app.add_url_rule('/estadistica_calorias/<int:id_usuario>', 'estadistica_calorias', estadistica_calorias)
app.add_url_rule('/estadistica/<tipo_estadistica>', '/estadistica/<tipo_estadistica>', mostrar_estadistica, methods=["GET"])  


# DATOS PERSONALES
app.add_url_rule('/datos_personales', 'datos_personales', datos_personales, methods=["GET", "POST"])


# PLATOS
app.add_url_rule('/platos', 'platos', platos, methods=["GET", "POST"]) 
app.add_url_rule('/plato/add', 'add_plato', add_plato, methods=["POST"])  
app.add_url_rule('/plato/delete/<int:id_plato>', 'delete_plato', delete_plato, methods=["POST"])  
app.add_url_rule('/plato/update/<int:id_plato>', 'update_plato', update_plato, methods=["GET", "POST"])  
app.add_url_rule('/delete_platos' , 'delete_platos' , delete_platos ,  methods = ['POST'])

# INGREDIENTES
app.add_url_rule('/ingredientes', 'ingredientes', ingredientes, methods=["GET", "POST"]) 
app.add_url_rule('/ingrediente/add', 'add_ingrediente', add_ingrediente, methods=["POST"]) 
app.add_url_rule('/ingrediente/update/<int:id_ingrediente>', 'update_ingrediente', update_ingrediente, methods=["GET", "POST"])  
app.add_url_rule('/ingrediente/delete/<int:id_ingrediente>', 'delete_ingrediente', delete_ingrediente, methods=["POST"])  
app.add_url_rule('/delete_ingredientes' , 'delete_ingredientes' , delete_ingredientes ,  methods = ['POST'])


# INFO_DIARIA
app.add_url_rule('/info_diaria', 'info_diaria', info_diaria, methods=["GET", "POST"]) 
app.add_url_rule('/info_diaria/add', 'add_info_diaria', add_info_diaria, methods=["POST"]) 
app.add_url_rule('/info_diaria/update/<int:id_info_diaria>', 'update_info_diaria', update_info_diaria, methods=["GET", "POST"])  
app.add_url_rule('/info_diaria/delete/<int:id_info_diaria>', 'delete_info_diaria', delete_info_diaria, methods=["POST"])  
app.add_url_rule('/delete_info_diarias' , 'delete_info_diarias' , delete_info_diarias ,  methods = ['POST'])

#CALENDARIO DIETA
app.add_url_rule('/calendario_dieta/<dia>', 'calendario_dieta', calendario_dieta, methods=["GET", "POST"])
app.add_url_rule('/calendario_dieta/seleccionar_plato/<int:id_plato>/<dia>', 'seleccionar_plato', seleccionar_plato, methods=["GET", "POST"] )
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
