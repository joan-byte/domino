import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.models.jugador import Jugador, Pareja
from app.schemas.jugador import ParejaCreate, ParejaSchema, JugadorSchema, ParejaUpdate, ParejaConMesa
from typing import List, Optional
from app.crud import pareja as crud_pareja
from sqlalchemy.exc import IntegrityError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parejas/", response_model=ParejaSchema)
def crear_pareja_con_jugadores(pareja: ParejaCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si los jugadores ya existen en este campeonato
        jugador1 = db.query(Jugador).filter_by(
            nombre=pareja.jugador1.nombre,
            apellido=pareja.jugador1.apellido,
            campeonato_id=pareja.campeonato_id
        ).first()
        jugador2 = db.query(Jugador).filter_by(
            nombre=pareja.jugador2.nombre,
            apellido=pareja.jugador2.apellido,
            campeonato_id=pareja.campeonato_id
        ).first()

        if jugador1 and jugador1.pareja_id:
            raise HTTPException(status_code=400, detail=f"El jugador {jugador1.nombre} {jugador1.apellido} ya está asignado a otra pareja en este campeonato")
        if jugador2 and jugador2.pareja_id:
            raise HTTPException(status_code=400, detail=f"El jugador {jugador2.nombre} {jugador2.apellido} ya está asignado a otra pareja en este campeonato")

        # Crear la pareja
        nueva_pareja = Pareja(club=pareja.club, activa=pareja.activa, campeonato_id=pareja.campeonato_id)
        db.add(nueva_pareja)
        db.flush()

        # Crear o actualizar jugadores
        if jugador1:
            jugador1.pareja_id = nueva_pareja.id
        else:
            jugador1 = Jugador(**pareja.jugador1.dict(), pareja_id=nueva_pareja.id, campeonato_id=pareja.campeonato_id)
            db.add(jugador1)

        if jugador2:
            jugador2.pareja_id = nueva_pareja.id
        else:
            jugador2 = Jugador(**pareja.jugador2.dict(), pareja_id=nueva_pareja.id, campeonato_id=pareja.campeonato_id)
            db.add(jugador2)

        # Generar el nombre de la pareja con nombre y apellido de ambos jugadores
        nueva_pareja.nombre = f"{jugador1.nombre} {jugador1.apellido} y {jugador2.nombre} {jugador2.apellido}"

        db.commit()
        db.refresh(nueva_pareja)
        return nueva_pareja
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error de integridad en la base de datos: {str(e)}")
    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/parejas/", response_model=List[ParejaSchema])
def obtener_parejas(db: Session = Depends(get_db)):
    try:
        parejas = db.query(Pareja).options(joinedload(Pareja.jugadores)).all()
        return parejas
    except Exception as e:
        logger.exception(f"Error detallado al obtener parejas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/jugadores/", response_model=List[JugadorSchema])
def listar_jugadores(campeonato_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Jugador)
        if campeonato_id:
            query = query.filter(Jugador.campeonato_id == campeonato_id)
        jugadores = query.all()
        logger.info(f"Obtenidos {len(jugadores)} jugadores")
        return jugadores
    except Exception as e:
        logger.error(f"Error al obtener jugadores: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/parejas/{pareja_id}", response_model=ParejaSchema)
def obtener_pareja(pareja_id: int, db: Session = Depends(get_db)):
    pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if pareja is None:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return pareja

@router.get("/jugadores/{jugador_id}", response_model=JugadorSchema)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.put("/parejas/{pareja_id}", response_model=ParejaSchema)
def actualizar_pareja(pareja_id: int, pareja: ParejaUpdate, db: Session = Depends(get_db)):
    logger.info(f"Intentando actualizar pareja {pareja_id} con datos: {pareja.dict()}")
    try:
        db_pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
        if not db_pareja:
            raise HTTPException(status_code=404, detail="Pareja no encontrada")
        
        # Actualizar los campos de la pareja
        db_pareja.activa = pareja.activa
        db_pareja.club = pareja.club
        db_pareja.campeonato_id = pareja.campeonato_id

        # Actualizar los jugadores
        jugadores = db.query(Jugador).filter(Jugador.pareja_id == pareja_id).all()
        if len(jugadores) != 2:
            raise HTTPException(status_code=400, detail="La pareja debe tener exactamente dos jugadores")

        for i, jugador_data in enumerate([pareja.jugador1, pareja.jugador2]):
            jugador = jugadores[i]
            jugador.nombre = jugador_data.nombre
            jugador.apellido = jugador_data.apellido
            jugador.campeonato_id = pareja.campeonato_id

        db.add(db_pareja)
        db.add_all(jugadores)
        db.commit()
        db.refresh(db_pareja)
        return db_pareja
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar pareja: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Error al procesar la solicitud: {str(e)}")

@router.delete("/parejas/{pareja_id}")
def eliminar_pareja(pareja_id: int, db: Session = Depends(get_db)):
    pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if pareja is None:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    db.delete(pareja)
    db.commit()
    return {"message": "Pareja eliminada con éxito"}

@router.patch("/parejas/{pareja_id}", response_model=ParejaSchema)
def actualizar_estado_pareja(pareja_id: int, pareja_update: dict, db: Session = Depends(get_db)):
    db_pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if not db_pareja:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    
    if 'activa' in pareja_update:
        db_pareja.activa = pareja_update['activa']
    
    db.commit()
    db.refresh(db_pareja)
    return db_pareja

@router.get("/parejas-mesas/{campeonato_id}", response_model=List[ParejaConMesa])
def obtener_parejas_mesas_por_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        return crud_pareja.get_parejas_con_mesas_por_campeonato(db, campeonato_id)
    except Exception as e:
        logger.exception(f"Error al obtener parejas y mesas para el campeonato {campeonato_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/campeonatos/{campeonato_id}/parejas", response_model=List[ParejaSchema])
def obtener_parejas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    parejas = db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).all()
    if not parejas:
        raise HTTPException(status_code=404, detail="No se encontraron parejas para este campeonato")
    
    # Asegúrate de que todas las parejas tengan un nombre válido
    parejas_validas = [pareja for pareja in parejas if pareja.nombre is not None]
    
    return parejas_validas

# Añade más rutas según sea necesario

