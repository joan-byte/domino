from sqlalchemy.orm import Session
from app.models.jugador import Pareja, Jugador
from app.models.mesa import Mesa
from app.schemas import jugador as jugador_schema
from fastapi import HTTPException
from typing import List
from sqlalchemy.exc import IntegrityError
from app.schemas.jugador import ParejaConMesa  # Importamos el esquema aquí

def get_pareja(db: Session, pareja_id: int) -> Pareja:
    pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if pareja is None:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return pareja

def get_parejas(db: Session) -> List[Pareja]:
    return db.query(Pareja).all()

def create_pareja(db: Session, pareja: jugador_schema.ParejaCreate) -> Pareja:
    db_pareja = Pareja(**pareja.dict())
    db.add(db_pareja)
    db.commit()
    db.refresh(db_pareja)
    return db_pareja

def update_pareja(db: Session, pareja_id: int, pareja_data: dict):
    pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if not pareja:
        return None

    try:
        # Actualizar datos de la pareja
        for key, value in pareja_data.items():
            if key not in ['jugador1', 'jugador2']:
                setattr(pareja, key, value)

        # Actualizar jugadores
        for i in [1, 2]:
            jugador = getattr(pareja, f'jugador{i}')
            jugador_data = pareja_data[f'jugador{i}']
            
            # Verificar si ya existe un jugador con el mismo nombre y apellido
            existing_jugador = db.query(Jugador).filter(
                Jugador.nombre == jugador_data['nombre'],
                Jugador.apellido == jugador_data['apellido']
            ).first()

            if existing_jugador and existing_jugador.id != jugador.id:
                raise ValueError(f"Ya existe un jugador con el nombre {jugador_data['nombre']} {jugador_data['apellido']}")

            # Actualizar datos del jugador
            for key, value in jugador_data.items():
                setattr(jugador, key, value)

        db.commit()
        return pareja
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos") from e
    except Exception as e:
        db.rollback()
        raise e

def delete_pareja(db: Session, pareja_id: int) -> Pareja:
    db_pareja = get_pareja(db, pareja_id)
    db.delete(db_pareja)
    db.commit()
    return db_pareja

def get_active_parejas(db: Session, skip: int = 0, limit: int = 100) -> List[Pareja]:
    return db.query(Pareja).filter(Pareja.activa == True).offset(skip).limit(limit).all()

def deactivate_pareja(db: Session, pareja_id: int) -> Pareja:
    db_pareja = get_pareja(db, pareja_id)
    db_pareja.activa = False
    db.add(db_pareja)
    db.commit()
    db.refresh(db_pareja)
    return db_pareja

def activate_pareja(db: Session, pareja_id: int) -> Pareja:
    db_pareja = get_pareja(db, pareja_id)
    db_pareja.activa = True
    db.add(db_pareja)
    db.commit()
    db.refresh(db_pareja)
    return db_pareja

def get_parejas_activas(db: Session) -> List[Pareja]:
    return db.query(Pareja).filter(Pareja.activa == True).all()

def get_parejas_con_mesas_por_campeonato(db: Session, campeonato_id: int) -> List[ParejaConMesa]:
    parejas = db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).all()
    mesas = db.query(Mesa).all()
    
    parejas_con_mesas = []
    for pareja in parejas:
        mesa_asignada = next((mesa for mesa in mesas if mesa.pareja1_id == pareja.id or mesa.pareja2_id == pareja.id), None)
        parejas_con_mesas.append(ParejaConMesa(
            id=pareja.id,
            nombre=pareja.nombre,
            mesa_asignada=mesa_asignada.id if mesa_asignada else None
        ))
    
    return parejas_con_mesas
