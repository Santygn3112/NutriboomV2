from backend.Modelos.database import db 

class IngredientePlatoUsuario(db.Model):
    __tablename__ = 'ingredienteplatousuario'
    id_plato = db.Column(db.Integer, primary_key=True)
    id_ingrediente = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.Enum('Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo'),primary_key=True)
    cantidad = db.Column(db.Numeric(6, 2), nullable=False)