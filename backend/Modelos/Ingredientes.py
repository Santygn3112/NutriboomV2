from backend.Modelos.database import db 
from sqlalchemy.orm import relationship

class Ingredientes(db.Model):
    __tablename__ = 'ingredientes'
    id_ingrediente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    grasas_Saturadas = db.Column(db.Numeric(5, 2), nullable=False)
    grasas_NO_Saturadas = db.Column(db.Numeric(5, 2), nullable=False)
    carbohidratos = db.Column(db.Numeric(5, 2), nullable=False)
    azucar = db.Column(db.Numeric(5, 2), nullable=False)
    proteina = db.Column(db.Numeric(5, 2), nullable=False)

    platos = relationship('Platos', secondary='ingredienteplato', back_populates='ingredientes')