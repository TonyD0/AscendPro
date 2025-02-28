import db
import re
import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

def validar_email(email):
    #Verifica que el email tenga un formato correcto
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Expresión regular para validar emails
    return re.match(patron, email) is not None

class Usuario(db.Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50),nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasenia = Column(String(200), nullable=False)
    tareas = relationship("Tarea", back_populates="usuario")

    def __init__(self, nombre, email, contrasenia):
        if not validar_email(email):
            raise ValueError("El email no es válido")
        self.nombre = nombre
        self.email = email
        self.contrasenia = self.hash_password(contrasenia)

    def hash_password(self, plain_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed_password

    def verificar_contrasenia(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.contrasenia)


class Tarea(db.Base):
    __tablename__ = "tarea"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    hecha = Column(Boolean)
    tipo_objetivo = Column(String(50), nullable=False)
    enfoque = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Relación con Usuario
    usuario = relationship("Usuario", back_populates="tareas")

    def __init__(self, contenido, hecha, tipo_objetivo, enfoque, usuario_id):
        self.contenido = contenido
        self.hecha = hecha
        self.tipo_objetivo = tipo_objetivo
        self.enfoque = enfoque
        self.usuario_id = usuario_id


def __str__ (self):
    return f"Tarea {self.id}: {self.contenido},{self.hecha},{self.tipo_objetivo}, {self.enfoque}"