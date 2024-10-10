import os
import sys

# Añade el directorio 'backend' al PYTHONPATH
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from app.db.session import engine
from app.models import campeonato, jugador

def create_tables():
    campeonato.Base.metadata.create_all(bind=engine)
    jugador.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tablas creadas exitosamente.")
