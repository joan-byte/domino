from faker import Faker
from sqlalchemy.orm import Session
from app.models.jugador import Pareja, Jugador
from app.models.campeonato import Campeonato
from app.db.session import SessionLocal

fake = Faker('es_ES')  # Utilizamos nombres en español

def crear_parejas_prueba(db: Session, campeonato_id: int, num_parejas: int):
    # Obtener el campeonato existente
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        print(f"No se encontró un campeonato con id {campeonato_id}")
        return

    # Obtener el número más alto de pareja existente para este campeonato
    ultima_pareja = db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).order_by(Pareja.numero.desc()).first()
    numero_inicial = 1 if not ultima_pareja else ultima_pareja.numero + 1

    parejas = []
    for i in range(num_parejas):
        # Generar nombres y apellidos para dos jugadores
        nombre1, apellido1 = fake.first_name(), fake.last_name()
        nombre2, apellido2 = fake.first_name(), fake.last_name()

        # Formar el nombre de la pareja
        nombre_pareja = f"{nombre1} {apellido1} y {nombre2} {apellido2}"

        # Crear la pareja
        pareja = Pareja(
            nombre=nombre_pareja,
            campeonato_id=campeonato.id,
            activa=True,
            numero=numero_inicial + i  # Asignar número secuencial
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

    print(f"Se han creado {len(parejas)} parejas de prueba para el campeonato '{campeonato.nombre}' (ID: {campeonato.id}).")
    print(f"Los números de las parejas van desde {numero_inicial} hasta {numero_inicial + num_parejas - 1}.")

if __name__ == "__main__":
    db = SessionLocal()
    crear_parejas_prueba(db, campeonato_id=3, num_parejas=70)
    db.close()
