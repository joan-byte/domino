from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.campeonato import Campeonato
from app.schemas.campeonato import CampeonatoCreate, CampeonatoSchema, CampeonatoUpdate
from typing import List
from app.models.jugador import Jugador, Pareja
from app.schemas.jugador import ParejaCreate, ParejaSchema, ParejaUpdate
from app.crud.pareja import update_pareja
from sqlalchemy.sql import func
from app.models import Resultado
from sqlalchemy.orm import joinedload
import logging
from sqlalchemy import func, case

router = APIRouter()

@router.post("/", response_model=CampeonatoSchema)
def crear_campeonato(campeonato: CampeonatoCreate, db: Session = Depends(get_db)):
    db_campeonato = Campeonato(**campeonato.dict())
    db.add(db_campeonato)
    db.commit()
    db.refresh(db_campeonato)
    return db_campeonato

@router.get("/", response_model=List[CampeonatoSchema])
def listar_campeonatos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campeonatos = db.query(Campeonato).offset(skip).limit(limit).all()
    return campeonatos

@router.get("/{campeonato_id}", response_model=CampeonatoSchema)
def obtener_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if campeonato is None:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    return campeonato

@router.put("/{campeonato_id}", response_model=CampeonatoSchema)
def actualizar_campeonato(campeonato_id: int, campeonato: CampeonatoUpdate, db: Session = Depends(get_db)):
    db_campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if db_campeonato is None:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    for key, value in campeonato.dict(exclude_unset=True).items():
        setattr(db_campeonato, key, value)
    db.commit()
    db.refresh(db_campeonato)
    return db_campeonato

@router.delete("/{campeonato_id}")
def eliminar_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if campeonato is None:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    db.delete(campeonato)
    db.commit()
    return {"message": "Campeonato eliminado con éxito"}

@router.get("/{campeonato_id}/parejas", response_model=List[ParejaSchema])
def obtener_parejas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    parejas = db.query(Pareja).options(joinedload(Pareja.jugadores)).filter(Pareja.campeonato_id == campeonato_id).all()
    return parejas

@router.post("/{campeonato_id}/parejas", response_model=ParejaSchema)
def crear_pareja_campeonato(campeonato_id: int, pareja: ParejaCreate, db: Session = Depends(get_db)):
    # Verificar si el campeonato existe
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    # Crear la pareja
    nombre_pareja = f"{pareja.jugador1.nombre} {pareja.jugador1.apellido} y {pareja.jugador2.nombre} {pareja.jugador2.apellido}"
    db_pareja = Pareja(nombre=nombre_pareja, club=pareja.club, campeonato_id=campeonato_id)
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

@router.get("/{campeonato_id}/ultima-partida")
def get_ultima_partida(campeonato_id: int, db: Session = Depends(get_db)):
    ultima_partida = db.query(func.max(Resultado.P)).filter(Resultado.campeonato_id == campeonato_id).scalar()
    return {"ultima_partida": ultima_partida or 0}

@router.get("/{campeonato_id}/ranking")
def get_ranking(campeonato_id: int, db: Session = Depends(get_db)):
    subquery = (
        db.query(
            Resultado.id_pareja,
            func.max(Resultado.P).label("ultima_partida"),
            case(
                (func.max(case((Resultado.GB == "B", 1), else_=0)) > 0, "B"),
                else_="A"
            ).label("GB"),
            func.sum(Resultado.PG).label("PG_total"),
            func.sum(Resultado.PP).label("PP_total")
        )
        .filter(Resultado.campeonato_id == campeonato_id)
        .group_by(Resultado.id_pareja)
        .subquery()
    )

    ranking = (
        db.query(
            subquery.c.ultima_partida,
            subquery.c.GB,
            subquery.c.PG_total,
            subquery.c.PP_total,
            Pareja.id.label("pareja_id"),
            Pareja.nombre.label("nombre_pareja"),
            Pareja.club
        )
        .outerjoin(subquery, Pareja.id == subquery.c.id_pareja)
        .filter(Pareja.campeonato_id == campeonato_id, Pareja.activa == True)
        .order_by(
            subquery.c.GB.asc(),
            subquery.c.PG_total.desc(),
            subquery.c.PP_total.desc()
        )
        .all()
    )

    return [
        {
            "partida": r.ultima_partida or 0,
            "GB": r.GB or "A",
            "PG": r.PG_total or 0,
            "PP": r.PP_total or 0,
            "pareja_id": r.pareja_id,
            "nombre_pareja": r.nombre_pareja,
            "club": r.club
        }
        for r in ranking
    ]

@router.post("/{campeonato_id}/actualizar-ranking")
def actualizar_ranking(campeonato_id: int, db: Session = Depends(get_db)):
    # Aquí iría la lógica para actualizar el ranking
    # Por ahora, simplemente devolveremos un mensaje de éxito
    return {"message": "Ranking actualizado correctamente"}
