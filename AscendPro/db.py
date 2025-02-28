from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Crear la conexión a la base de datos
engine = create_engine('sqlite:///database/tareas.db', connect_args={"check_same_thread": False})

# Crear SessionLocal para manejar sesiones individuales
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Crear Base para los modelos
Base = declarative_base()

# Función para obtener una sesión en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
