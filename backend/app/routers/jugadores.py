import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.models.jugador import Jugador, Pareja
from app.schemas.jugador import ParejaCreate, ParejaSchema, JugadorSchema, ParejaUpdate  # Añadimos JugadorSchema aquí
from typing import List

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parejas/", response_model=ParejaSchema)
def crear_pareja_con_jugadores(pareja: ParejaCreate, db: Session = Depends(get_db)):
    # Crear el nombre de la pareja
    nombre_pareja = f"{pareja.jugador1.nombre} {pareja.jugador1.apellido} y {pareja.jugador2.nombre} {pareja.jugador2.apellido}"
    
    # Crear la pareja
    db_pareja = Pareja(nombre=nombre_pareja, club=pareja.club, campeonato_id=pareja.campeonato_id)
    db.add(db_pareja)
    db.flush()

    # Crear los jugadores asociados a la pareja
    jugador1 = Jugador(**pareja.jugador1.dict(), pareja_id=db_pareja.id)
    jugador2 = Jugador(**pareja.jugador2.dict(), pareja_id=db_pareja.id)
    
    db.add(jugador1)
    db.add(jugador2)

    db.commit()
    db.refresh(db_pareja)
    return db_pareja

@router.get("/parejas/", response_model=List[ParejaSchema])
def obtener_parejas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        parejas = db.query(Pareja).options(joinedload(Pareja.jugadores)).offset(skip).limit(limit).all()
        return parejas
    except Exception as e:
        logger.exception(f"Error detallado al obtener parejas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/jugadores/", response_model=List[JugadorSchema])
def listar_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        jugadores = db.query(Jugador).offset(skip).limit(limit).all()
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
        
        db_pareja.activa = pareja.activa
        db_pareja.club = pareja.club

        db.add(db_pareja)
        db.commit()
        db.refresh(db_pareja)
        return db_pareja
    except Exception as e:
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

# Añade más rutas según sea necesario
