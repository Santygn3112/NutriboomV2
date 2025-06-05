from backend.Modelos.database import db 
from sqlalchemy.orm import relationship

class Platos(db.Model):
    __tablename__ = 'platos'
    id_plato = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum("Desayuno","Almuerzo" , "Comida","Merienda", "Cena"))
    imagen_plato = db.Column(db.String(255)) 
    ingredientes = relationship('Ingredientes', secondary='ingredienteplato', back_populates='platos')