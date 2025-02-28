from crypt import methods

from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import Tarea
import db
from db import get_db
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route("/registro", methods=["POST"])
def registro():
    db_session = next(get_db())
    nombre = request.form["nombre"]
    email = request.form["email"]
    contrasenia = request.form["contrasenia"]

@app.route("/")
def home():
    db_session = next(get_db())  # Obtener sesión local
    todas_tareas = db_session.query(Tarea).all()
    db_session.close()  # Cerrar sesión después de usarla
    return render_template("index.html", lista_tareas=todas_tareas)


@app.route("/crear-tarea", methods=["POST"])
def crear():
    db_session = next(get_db())
    tarea = Tarea(
        contenido=request.form["contenido_tarea"],
        tipo_objetivo=request.form["tipo_objetivo"],
        enfoque=request.form["enfoque"],
        hecha=False
    )
    db_session.add(tarea)
    db_session.commit()
    db_session.close()
    return redirect(url_for("home"))


@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    db_session = next(get_db())  # Obtener sesión correctamente
    tareas = db_session.query(Tarea).all()
    db_session.close()  # Cerrar la sesión después de la consulta
    return jsonify([{"id": t.id, "contenido": t.contenido, "hecha": t.hecha} for t in tareas])


@app.route("/tarea-hecha/<id>")
def hecha(id):
    db_session = next(get_db())
    tarea = db_session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not tarea.hecha
    db_session.commit()
    db_session.close()
    return redirect(url_for("home"))


@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    db_session = next(get_db())
    db_session.query(Tarea).filter_by(id=int(id)).delete()
    db_session.commit()
    db_session.close()
    return redirect(url_for("home"))


@app.route('/editar-tarea/<int:id>')
def editar_tarea(id):
    db_session = next(get_db())
    tarea = db_session.query(Tarea).filter_by(id=id).first()
    db_session.close()
    if not tarea:
        return redirect(url_for("home"))
    return render_template("edit.html", tarea=tarea)


@app.route("/actualizar-tarea/<id>", methods=["POST"])
def actualizar_tarea(id):
    db_session = next(get_db())
    tarea = db_session.query(Tarea).filter_by(id=int(id)).first()
    tarea.contenido = request.form["contenido_tarea"]
    tarea.tipo_objetivo = request.form["tipo_objetivo"]
    tarea.enfoque = request.form["enfoque"]
    db_session.commit()
    db_session.close()
    return redirect(url_for("home"))


if __name__ == "__main__":
    from db import Base, engine
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)


