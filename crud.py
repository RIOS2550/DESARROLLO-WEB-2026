from database import db
from models import EquipoComputo

def obtener_todos_equipos():
    return EquipoComputo.query.all()

def registrar_equipo(codigo, responsable, puesto, firmado, obs):
    nuevo_equipo = EquipoComputo(
        codigo_activo=codigo,
        responsable=responsable,
        puesto=puesto,
        politica_firmada=firmado,
        observaciones=obs
    )
    db.session.add(nuevo_equipo)
    db.session.commit()

def actualizar_equipo(id_equipo, codigo, responsable, puesto, firmado, obs):
    equipo = EquipoComputo.query.get(id_equipo)
    if equipo:
        equipo.codigo_activo = codigo
        equipo.responsable = responsable
        equipo.puesto = puesto
        equipo.politica_firmada = firmado
        equipo.observaciones = obs
        db.session.commit()

def eliminar_equipo(id_equipo):
    equipo = EquipoComputo.query.get(id_equipo)
    if equipo:
        db.session.delete(equipo)
        db.session.commit()