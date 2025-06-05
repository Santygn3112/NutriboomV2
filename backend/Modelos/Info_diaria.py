from backend.Modelos.database import db 

class Info_diaria(db.Model):
    __tablename__ = 'info_diaria'
    id_info_diaria = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    peso = db.Column(db.Numeric(5, 2), nullable=False)
    grasa_corporal = db.Column(db.Numeric(5, 2), nullable=False)
    imc = db.Column(db.Numeric(5, 2))
