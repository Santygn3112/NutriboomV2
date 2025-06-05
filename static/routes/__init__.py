# HOME

from .home import home  


# AUTENTIFICACIÓN
from .login import login
from .register import register
from .logout import logout  


# ESTADISTICAS
from .estadisticas.estadistica_general import estadistica_general
from .estadisticas.estadistica_calorias import estadistica_calorias
from  .estadisticas.estadistica_mostrar import mostrar_estadistica


# DATOS PERSONALES
from .datos_personales import datos_personales


# PLATOS

from  .platos import *
from  .platos.add_plato import add_plato
from  .platos.delete_plato import delete_plato
from  .platos.delete_platos import delete_platos
from  .platos.update_plato import update_plato
from  .platos.platos import platos


# INGREDIENTES
from  .ingredientes.add_ingrediente import add_ingrediente
from  .ingredientes.delete_ingrediente import delete_ingrediente
from  .ingredientes.delete_ingredientes import delete_ingredientes
from  .ingredientes.update_ingrediente import update_ingrediente
from  .ingredientes.ingredientes import ingredientes


# INFO_DIARIA

from .info_diaria.add_info_diaria import add_info_diaria
from .info_diaria.delete_info_diaria import delete_info_diaria
from .info_diaria.delete_info_diarias import delete_info_diarias
from .info_diaria.update_info_diaria import update_info_diaria
from .info_diaria.info_diaria import info_diaria


# USER
from .user.update_usuario import update_usuario
from .user.cuenta import cuenta
from .user.olvidado_contraseña import olvidado_contraseña
from .user.restablecer_contraseña import restablecer_contraseña
from .user.update_contraseña import update_contraseña
from .id_usuario import ver_id_usuario

#Calendario Dieta
from .CalendarioDieta import calendario_dieta
from .CalendarioDieta import seleccionar_plato
