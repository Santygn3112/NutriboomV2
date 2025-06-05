from backend.Modelos.database import db 

class Datos_personales(db.Model):
    __tablename__ = 'datos_personales'
    id_usuario = db.Column(db.Integer, primary_key=True)
    altura = db.Column(db.Numeric(5, 2), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.Enum("Masculino","Femenino","Otros"))
    nivel_actividad = db.Column(db.Integer, nullable=False)
    tipo_dieta = db.Column(db.Enum("Subir","Bajar","Mantenerse"))
    calorias_base = db.Column(db.Numeric(8, 2), nullable=False)
    calorias_permitidas = db.Column(db.Numeric(8, 2), nullable=False)
    numero_Comidas = db.Column(db.Integer, nullable=False)