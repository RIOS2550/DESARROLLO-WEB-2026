import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
import crud

app = Flask(__name__, template_folder=os.path.abspath(os.path.dirname(__file__)))

# Clave secreta necesaria para poder mostrar mensajes de éxito (Flash)
app.secret_key = 'clave_secreta_constructora'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///constructora_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        responsable = request.form.get('responsable')
        puesto = request.form.get('puesto')
        firmado = 'firmado' in request.form
        obs = request.form.get('observaciones')
        
        crud.registrar_equipo(codigo, responsable, puesto, firmado, obs)
        flash('¡Equipo registrado con éxito en el sistema!', 'exito')
        return redirect(url_for('inicio'))
        
    equipos = crud.obtener_todos_equipos()
    total = len(equipos)
    firmados = sum(1 for e in equipos if e.politica_firmada)
    pendientes = total - firmados

    return render_template('index.html', equipos=equipos, total=total, firmados=firmados, pendientes=pendientes)

# --- OPERACIÓN: LEER (Consulta individual para ver la ficha técnica) ---
@app.route('/equipo/<int:id>')
def leer_individual(id):
    # Reutilizamos la lógica del modelo para buscar un solo equipo
    from models import EquipoComputo
    equipo = EquipoComputo.query.get_or_create
    equipo = EquipoComputo.query.get(id)
    if not equipo:
        flash('El equipo no existe.', 'error')
        return redirect(url_for('inicio'))
    return render_template('detalle.html', equipo=equipo)

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    codigo = request.form.get('codigo')
    responsable = request.form.get('responsable')
    puesto = request.form.get('puesto')
    firmado = 'firmado' in request.form
    obs = request.form.get('observaciones')
    
    crud.actualizar_equipo(id, codigo, responsable, puesto, firmado, obs)
    flash('¡Los datos del equipo se actualizaron correctamente!', 'info')
    return redirect(url_for('inicio'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    crud.eliminar_equipo(id)
    flash('El equipo fue eliminado del padrón general.', 'alerta')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)