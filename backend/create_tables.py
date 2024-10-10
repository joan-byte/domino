import os
import sys

# Añade el directorio actual y el directorio padre al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from backend.app.db.session import engine
from backend.app.models import campeonato, jugador

def create_tables():
    campeonato.Base.metadata.create_all(bind=engine)
    jugador.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tablas creadas exitosamente.")
