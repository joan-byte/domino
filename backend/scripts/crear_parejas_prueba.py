import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.jugador import Pareja, Jugador
from app.models.campeonato import Campeonato

# Listas de nombres y apellidos reales españoles
nombres = [
    "Antonio", "Manuel", "José", "Francisco", "David", "Juan", "Miguel", "Javier",
    "Daniel", "Carlos", "Jesús", "Alejandro", "Rafael", "Pedro", "Pablo", "Ángel",
    "Sergio", "Fernando", "Jorge", "Luis", "Alberto", "Álvaro", "Diego", "Adrián",
    "María", "Carmen", "Ana", "Isabel", "Laura", "Elena", "Cristina", "Marta",
    "Rosa", "Sara", "Paula", "Lucía", "Raquel", "Andrea", "Patricia", "Beatriz"
]

apellidos = [
    "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez",
    "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno",
    "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres",
    "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Suárez",
    "Molina", "Morales", "Ortega", "Delgado", "Castro", "Ortiz", "Rubio", "Marín"
]

def crear_parejas_prueba():
    db = SessionLocal()
    try:
        # Solicitar ID del campeonato
        while True:
            campeonato_id = input("Ingrese el ID del campeonato: ")
            try:
                campeonato_id = int(campeonato_id)
                # Verificar si el campeonato existe
                campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
                if campeonato:
                    break
                else:
                    print(f"No existe un campeonato con ID {campeonato_id}")
            except ValueError:
                print("Por favor, ingrese un número válido")

        # Solicitar número de parejas
        while True:
            num_parejas = input("¿Cuántas parejas desea crear? ")
            try:
                num_parejas = int(num_parejas)
                if num_parejas > 0:
                    break
                else:
                    print("Por favor, ingrese un número mayor que 0")
            except ValueError:
                print("Por favor, ingrese un número válido")

        # Crear parejas
        for i in range(num_parejas):
            # Generar datos aleatorios para los jugadores
            jugador1_nombre = random.choice(nombres)
            jugador1_apellido = random.choice(apellidos)
            jugador2_nombre = random.choice(nombres)
            jugador2_apellido = random.choice(apellidos)
            
            # Crear el nombre de la pareja según el formato especificado
            nombre_pareja = f"{jugador1_nombre} {jugador1_apellido} y {jugador2_nombre} {jugador2_apellido}"
            club = f"Club {i+1}"
            
            nueva_pareja = Pareja(
                nombre=nombre_pareja,
                club=club,
                campeonato_id=campeonato_id,
                activa=True
            )
            db.add(nueva_pareja)
            db.flush()  # Para obtener el ID de la pareja

            # Crear jugadores de la pareja con los nombres generados
            jugador1 = Jugador(
                nombre=jugador1_nombre,
                apellido=jugador1_apellido,
                pareja_id=nueva_pareja.id,
                campeonato_id=campeonato_id
            )

            jugador2 = Jugador(
                nombre=jugador2_nombre,
                apellido=jugador2_apellido,
                pareja_id=nueva_pareja.id,
                campeonato_id=campeonato_id
            )

            db.add(jugador1)
            db.add(jugador2)

            print(f"Creada pareja {i+1}/{num_parejas}: {nombre_pareja}")

        db.commit()
        print(f"\nSe han creado {num_parejas} parejas exitosamente en el campeonato {campeonato_id}")

    except Exception as e:
        db.rollback()
        print(f"Error al crear las parejas: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Creación de Parejas de Prueba ===")
    crear_parejas_prueba()
