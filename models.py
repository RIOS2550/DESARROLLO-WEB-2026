from database import db
from datetime import datetime

class EquipoComputo(db.Model):
    # Evita conflictos de duplicados en la memoria de SQLAlchemy
    __table_args__ = {'extend_existing': True}
    
    # Campos de la tabla de la constructora
    id = db.Column(db.Integer, primary_key=True)
    codigo_activo = db.Column(db.String(50), unique=True, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    puesto = db.Column(db.String(50), nullable=False)
    politica_firmada = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)