from faker import Faker
from sqlalchemy.orm import Session
from app.models.jugador import Pareja, Jugador
from app.models.campeonato import Campeonato
from app.db.session import SessionLocal

fake = Faker('es_ES')  # Utilizamos nombres en español

def crear_parejas_prueba(db: Session):
    # Obtener el campeonato existente o crear uno nuevo si no existe
    campeonato = db.query(Campeonato).first()
    if not campeonato:
        campeonato = Campeonato(nombre="Campeonato de Prueba")
        db.add(campeonato)
        db.commit()
        db.refresh(campeonato)

    parejas = []
    for _ in range(21):
        # Generar nombres y apellidos para dos jugadores
        nombre1, apellido1 = fake.first_name(), fake.last_name()
        nombre2, apellido2 = fake.first_name(), fake.last_name()

        # Formar el nombre de la pareja
        nombre_pareja = f"{nombre1} {apellido1} y {nombre2} {apellido2}"

        # Crear la pareja
        pareja = Pareja(
            nombre=nombre_pareja,
            campeonato_id=campeonato.id,
            activa=True  # Todas las parejas son activas
        )
        db.add(pareja)
        db.flush()  # Para obtener el ID de la pareja

        # Crear los jugadores asociados a la pareja
        jugador1 = Jugador(nombre=nombre1, apellido=apellido1, pareja_id=pareja.id)
        jugador2 = Jugador(nombre=nombre2, apellido=apellido2, pareja_id=pareja.id)
        
        db.add(jugador1)
        db.add(jugador2)

        parejas.append(pareja)
    
    db.commit()

    print(f"Se han creado {len(parejas)} parejas de prueba con sus respectivos jugadores.")

if __name__ == "__main__":
    db = SessionLocal()
    crear_parejas_prueba(db)
    db.close()
