from backend.Modelos.database import db 


class IngredientePlato(db.Model):
    __tablename__ = 'ingredienteplato'
    id_plato = db.Column(db.Integer,  db.ForeignKey('platos.id_plato'),primary_key=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingredientes.id_ingrediente') , primary_key=True)
