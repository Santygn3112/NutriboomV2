from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pymysql
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Creamos la instancia de la base de datos
db = SQLAlchemy()

# Datos del servidor MySQL (se pueden sobrescribir mediante variables de entorno)
USER = os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "")
HOST = os.getenv("MYSQL_HOST", "localhost")
PORT = os.getenv("MYSQL_PORT", "3306")
DATABASE = os.getenv("MYSQL_DATABASE", "nutriboom")


def _create_database_if_not_exists():
    """Crea la base de datos si todavía no existe."""
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=int(PORT))
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE}`")
        connection.commit()
    finally:
        connection.close()


def _seed_database():
    """Inserta datos iniciales si las tablas están vacías."""
    from .platos import Platos
    from .Ingredientes import Ingredientes
    from .IngredientePlato import IngredientePlato

    if Platos.query.first() is not None:
        return

    sql_platos = text("""
INSERT INTO platos (id_plato, nombre, tipo, imagen_plato) VALUES
    (1, 'Tortitas de avena caseras', 'Desayuno', 'img/platos/Tortitas_de_avena_caseras.jpg'),
    (2, 'Huevos revueltos con pan', 'Desayuno', 'img/platos/Huevos_revueltos_con_pan.jpg'),
    (3, 'Yogur griego con cereales y frutos rojos', 'Desayuno', 'img/platos/Yogur_griego_con_cereales_y_frutos_rojos.jpg'),
    (4, 'Huevos fritos con bacon y pan y zumo de naranja', 'Desayuno', 'img/platos/Huevos_fritos_con_bacon_y_pan_y_zumo_de_naranja.jpg'),
    (5, 'Tostadas con mermelada y mantequilla', 'Desayuno', 'img/platos/Tostadas_con_mermelada_y_mantequilla.jpg'),
    (6, 'Sandwich de jamón y queso', 'Merienda', 'img/platos/Sandwich_de_jamon_y_queso.jpg'),
    (7, 'Pa amb oli', 'Merienda', 'img/platos/Pa_amb_oli.jpg'),
    (8, 'Manzana', 'Merienda', 'img/platos/Manzana.jpg'),
    (9, 'Tostada con aguacate y queso fresco', 'Merienda', 'img/platos/Tostada_con_aguacate_y_queso_fresco.jpg'),
    (10, 'Donas rellenas de chocolate', 'Merienda', 'img/platos/Donas_rellenas_de_chocolate.jpg'),
    (11, 'Arroz con pollo', 'Comida', 'img/platos/Arroz_con_pollo.jpg'),
    (12, 'Spaghetti boloñesa', 'Comida', 'img/platos/Spaghetti_bolonesa.jpg'),
    (13, 'Bistec con patatas, ensalada y setas', 'Comida', 'img/platos/Bistec_con_patatas_ensalada_y_setas.jpg'),
    (14, 'Salmón al horno con espárragos y patata hervida', 'Comida', 'img/platos/Salmon_al_horno_con_esparragos_y_patata_hervida.jpg'),
    (15, 'Ensalada de quinoa con frutos secos y verduras', 'Comida', 'img/platos/Ensalada_de_quinoa_con_frutos_secos_y_verduras.jpg'),
    (16, 'Ensalada mixta con atún y huevo hervido', 'Cena', 'img/platos/Ensalada_mixta_con_atun_y_huevo_hervido.jpg'),
    (17, 'Pollo al horno con arroz y ensalada rusa', 'Cena', 'img/platos/Pollo_al_horno_con_arroz_y_ensalada_rusa.jpg'),
    (18, 'Quesadillas a la española', 'Cena', 'img/platos/Quesadillas_a_la_espanola.jpg'),
    (19, 'Tortilla de patata', 'Cena', 'img/platos/Tortilla_de_patata.jpg'),
    (20, 'Croquetas de pollo', 'Cena', 'img/platos/Croquetas_de_pollo.jpg'),
    (22, 'Natalia', 'Desayuno', 'img/platos/Natalia.jpg');
""")

    sql_ingredientes = text("""
INSERT INTO ingredientes (id_ingrediente, nombre, grasas_Saturadas, grasas_NO_Saturadas, carbohidratos, azucar, proteina) VALUES
    (1, 'Huevo', 3.30, 7.70, 1.00, 1.00, 13.00),
    (2, 'Avena', 1.50, 5.50, 60.00, 1.00, 13.50),
    (3, 'Leche', 1.10, 0.50, 4.80, 4.80, 3.20),
    (4, 'Plátano', 0.10, 0.20, 23.00, 12.00, 1.30),
    (5, 'Pan blanco', 0.82, 2.62, 49.20, 5.30, 9.40),
    (6, 'Yogur griego natural', 6.60, 3.10, 3.60, 3.60, 5.50),
    (7, 'Cereales/Granola', 1.00, 6.00, 60.00, 20.00, 10.00),
    (8, 'Frutos rojos', 0.00, 0.30, 7.00, 5.00, 1.00),
    (9, 'Bacon', 14.00, 24.00, 1.00, 0.00, 37.00),
    (10, 'Naranja', 0.00, 0.10, 11.80, 9.20, 0.90),
    (11, 'Pan de tostada', 0.82, 2.62, 49.20, 5.30, 9.40),
    (12, 'Mermelada', 0.00, 0.00, 60.00, 60.00, 0.20),
    (13, 'Mantequilla', 51.00, 30.00, 0.10, 0.10, 0.80),
    (14, 'Queso mozzarella', 14.00, 8.00, 1.00, 0.50, 22.00),
    (15, 'Pan rústico', 0.82, 2.62, 49.20, 5.30, 9.40),
    (16, 'Aceite de oliva', 14.00, 86.00, 0.00, 0.00, 0.00),
    (17, 'Tomate', 0.00, 0.20, 4.00, 3.00, 1.00),
    (18, 'Manzana', 0.00, 0.20, 14.00, 10.00, 0.30),
    (19, 'Aguacate', 2.10, 12.90, 9.00, 0.70, 2.00),
    (20, 'Queso fresco', 5.50, 2.50, 3.00, 3.00, 11.00),
    (21, 'Dona rellena de chocolate', 9.00, 11.00, 47.00, 22.00, 6.00),
    (22, 'Arroz blanco crudo', 0.10, 0.50, 75.00, 0.00, 7.50),
    (23, 'Spaghetti', 0.20, 0.90, 31.00, 0.60, 5.00),
    (24, 'Carne picada de ternera', 6.00, 9.00, 0.00, 0.00, 20.00),
    (25, 'Salsa de tomate casera', 0.20, 0.80, 6.00, 4.00, 1.50),
    (26, 'Bistec de ternera', 2.50, 3.50, 0.00, 0.00, 22.00),
    (27, 'Lechuga', 0.00, 0.10, 3.00, 1.30, 1.30),
    (28, 'Cebolla', 0.00, 0.10, 9.00, 4.20, 1.10),
    (29, 'Patata', 0.00, 0.10, 17.00, 0.80, 2.00),
    (30, 'Setas', 0.00, 0.20, 3.30, 0.50, 2.50),
    (31, 'Salmón', 2.50, 9.00, 0.00, 0.00, 20.00),
    (32, 'Espárrago', 0.00, 0.10, 3.90, 1.80, 2.20),
    (33, 'Quinoa', 0.20, 1.70, 21.30, 0.90, 4.10),
    (34, 'Almendra', 3.70, 44.30, 22.00, 3.90, 21.00),
    (35, 'Nueces', 6.10, 58.90, 14.00, 2.60, 15.00),
    (36, 'Pepino', 0.00, 0.10, 3.60, 1.70, 0.80),
    (37, 'Zanahoria', 0.00, 0.10, 9.60, 4.70, 0.90),
    (38, 'Atún en lata', 1.50, 8.80, 0.00, 0.00, 23.50),
    (39, 'Pollo crudo', 1.00, 3.00, 0.00, 0.00, 22.50),
    (40, 'Guisantes', 0.10, 0.30, 14.00, 5.00, 5.00),
    (41, 'Mayonesa', 10.00, 62.00, 5.00, 1.80, 1.10),
    (42, 'Tortita de trigo', 0.60, 2.90, 50.00, 0.60, 8.00),
    (43, 'Queso manchego', 19.00, 10.00, 0.50, 0.50, 25.00),
    (44, 'Jamón serrano', 4.90, 9.10, 0.00, 0.00, 28.00),
    (45, 'Jamón york', 1.50, 3.50, 1.50, 1.50, 15.00),
    (46, 'Pimiento', 0.00, 0.20, 6.30, 4.20, 1.00),
    (47, 'Orégano', 1.50, 8.50, 69.00, 4.50, 9.00),
    (48, 'Harina de trigo', 0.20, 0.30, 73.30, 0.30, 10.00),
    (49, 'Pimienta negra', 0.50, 2.80, 53.00, 0.00, 10.00),
    (50, 'Pan rallado', 0.60, 2.90, 50.00, 0.60, 8.00);
""")

    sql_relaciones = text("""
INSERT INTO ingredienteplato (id_plato, id_ingrediente) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 1),
    (2, 5),
    (3, 6),
    (3, 7),
    (3, 8),
    (4, 1),
    (4, 5),
    (4, 9),
    (4, 10),
    (5, 11),
    (5, 12),
    (5, 13),
    (6, 11),
    (6, 14),
    (6, 45),
    (7, 15),
    (7, 16),
    (7, 17),
    (8, 18),
    (9, 11),
    (9, 19),
    (9, 20),
    (10, 21),
    (11, 16),
    (11, 22),
    (11, 39),
    (12, 16),
    (12, 23),
    (12, 24),
    (12, 25),
    (13, 16),
    (13, 17),
    (13, 26),
    (13, 27),
    (13, 28),
    (13, 29),
    (13, 30),
    (14, 16),
    (14, 29),
    (14, 31),
    (14, 32),
    (15, 16),
    (15, 17),
    (15, 27),
    (15, 33),
    (15, 34),
    (15, 35),
    (15, 36),
    (15, 37),
    (16, 1),
    (16, 16),
    (16, 17),
    (16, 27),
    (16, 28),
    (16, 36),
    (16, 38),
    (17, 16),
    (17, 22),
    (17, 29),
    (17, 37),
    (17, 39),
    (17, 40),
    (17, 41),
    (18, 1),
    (18, 16),
    (18, 42),
    (18, 43),
    (18, 44),
    (18, 45),
    (18, 46),
    (18, 47),
    (19, 1),
    (19, 16),
    (19, 28),
    (19, 29),
    (20, 1),
    (20, 3),
    (20, 13),
    (20, 16),
    (20, 39),
    (20, 48),
    (20, 49),
    (20, 50);
""")

    db.session.execute(sql_platos)
    db.session.execute(sql_ingredientes)
    db.session.execute(sql_relaciones)
    db.session.commit()


def init_db(app):
    """Configura la aplicación y prepara la base de datos."""
    _create_database_if_not_exists()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        from .Usuario import Usuario
        from .Datos_personales import Datos_personales
        from .Info_diaria import Info_diaria
        from .IngredientePlatoUsuario import IngredientePlatoUsuario
        from .platos import Platos
        from .Ingredientes import Ingredientes
        from .IngredientePlato import IngredientePlato

        db.create_all()
        _seed_database()
