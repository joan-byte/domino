from fastapi import APIRouter, Depends, HTTPException, Body
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
from app.models.mesa import Mesa
from app.schemas.mesa import MesaAsignacion
from app.models.ranking_final import RankingFinal
from sqlalchemy import text
from app.models.campeonato import Campeonato
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from app.models.jugador import Pareja

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
def update_campeonato(
    campeonato_id: int,
    campeonato_in: CampeonatoUpdate,
    db: Session = Depends(get_db)
):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    for field, value in campeonato_in.dict(exclude_unset=True).items():
        setattr(campeonato, field, value)
    
    try:
        db.commit()
        db.refresh(campeonato)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return campeonato

@router.delete("/{campeonato_id}")
def eliminar_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Primero verificamos si el campeonato existe
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if campeonato is None:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Eliminamos en orden para mantener la integridad referencial
        
        # 1. Eliminar ranking final si existe
        db.query(RankingFinal).filter(RankingFinal.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 2. Eliminar resultados
        db.query(Resultado).filter(Resultado.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 3. Eliminar mesas
        db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 4. Eliminar jugadores asociados a las parejas del campeonato
        parejas = db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).all()
        for pareja in parejas:
            db.query(Jugador).filter(Jugador.pareja_id == pareja.id).delete(synchronize_session=False)
        
        # 5. Eliminar parejas
        db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 6. Finalmente eliminamos el campeonato
        db.delete(campeonato)
        
        # Confirmar todos los cambios
        db.commit()
        
        return {"message": "Campeonato y todos sus datos asociados eliminados con éxito"}
        
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el campeonato: {str(e)}")  # Para debugging
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar el campeonato: {str(e)}"
        )

@router.get("/{campeonato_id}/parejas", response_model=List[ParejaSchema])
def obtener_parejas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    # Verificar si el campeonato existe primero
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
    parejas = db.query(Pareja).options(joinedload(Pareja.jugadores)).filter(Pareja.campeonato_id == campeonato_id).all()
    # Ya no lanzamos excepción si no hay parejas
    return parejas  # Retornamos lista vacía si no hay parejas

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
        db_pareja.club = pareja.club  # Asegúrate de que esta línea esté presente
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
            func.coalesce(func.sum(Resultado.PG), 0).label("PG_total"),
            func.coalesce(func.sum(Resultado.PP), 0).label("PP_total")
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

    # Procesar el ranking para asignar posiciones independientes por grupo
    resultado_final = []
    posicion_grupo_a = 1
    posicion_grupo_b = 1

    for r in ranking:
        es_grupo_b = r.GB == "B"
        posicion = posicion_grupo_b if es_grupo_b else posicion_grupo_a

        resultado_final.append({
            "partida": r.ultima_partida or 0,
            "GB": r.GB or "A",
            "PG": r.PG_total or 0,
            "PP": r.PP_total or 0,
            "pareja_id": r.pareja_id,
            "nombre_pareja": r.nombre_pareja,
            "club": r.club,
            "posicion": posicion
        })

        if es_grupo_b:
            posicion_grupo_b += 1
        else:
            posicion_grupo_a += 1

    return resultado_final

@router.post("/{campeonato_id}/actualizar-ranking")
def actualizar_ranking(campeonato_id: int, db: Session = Depends(get_db)):
    # Aquí iría la lógica para actualizar el ranking
    # Por ahora, simplemente devolveremos un mensaje de éxito
    return {"message": "Ranking actualizado correctamente"}

@router.put("/{campeonato_id}/partida_actual", response_model=CampeonatoSchema)
def actualizar_partida_actual(campeonato_id: int, partida_actual: int = Body(..., embed=True), db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    campeonato.partida_actual = partida_actual
    db.commit()
    db.refresh(campeonato)
    return campeonato

@router.post("/{campeonato_id}/asignar-mesas")
def asignar_mesas(campeonato_id: int, asignaciones: List[MesaAsignacion], db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    # Eliminar todas las mesas de la partida actual
    db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id, Mesa.partida == campeonato.partida_actual).delete()

    # Crear nuevas asignaciones
    for asignacion in asignaciones:
        nueva_mesa = Mesa(
            campeonato_id=campeonato_id,
            partida=campeonato.partida_actual,
            numero=asignacion.mesa,
            pareja1_id=asignacion.pareja1_id,
            pareja2_id=asignacion.pareja2_id
        )
        db.add(nueva_mesa)

    db.commit()
    return {"message": "Mesas asignadas correctamente para la partida actual"}

@router.get("/{campeonato_id}/parejas-mesas")
def obtener_parejas_mesas(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    # Obtener el ranking actual
    ranking = get_ranking(campeonato_id, db)

    # Asignar mesas basadas en la posición del ranking
    parejas_mesas = []
    for i, pareja in enumerate(ranking):
        mesa_numero = (i // 2) + 1  # Dividir por 2 y redondear hacia arriba
        parejas_mesas.append({
            "pareja_id": pareja["pareja_id"],
            "nombre_pareja": pareja["nombre_pareja"],
            "mesa_asignada": mesa_numero
        })

    return parejas_mesas

@router.get("/{campeonato_id}/mesas-partida-actual")
def obtener_mesas_partida_actual(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")

    mesas = db.query(Mesa).filter(
        Mesa.campeonato_id == campeonato_id,
        Mesa.partida == campeonato.partida_actual
    ).order_by(Mesa.numero).all()

    return [
        {
            "id": mesa.id,
            "pareja1_id": mesa.pareja1_id,
            "pareja2_id": mesa.pareja2_id,
            "numero": mesa.numero
        }
        for mesa in mesas
    ]

@router.get("/{campeonato_id}/ranking-final")
def get_ranking_final(campeonato_id: int, db: Session = Depends(get_db)):
    # Primero verificamos si el campeonato está cerrado
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    # Verificar si existe un ranking final guardado
    ranking_final = db.query(RankingFinal).filter(
        RankingFinal.campeonato_id == campeonato_id
    ).order_by(RankingFinal.posicion).all()
    
    if ranking_final:
        return [
            {
                "pareja_id": r.pareja_id,
                "nombre_pareja": r.nombre_pareja,
                "PG": r.PG,
                "PP": r.PP,
                "posicion": r.posicion
            }
            for r in ranking_final
        ]
    
    return []

@router.post("/{campeonato_id}/cerrar-campeonato")
def cerrar_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    # Obtener el ranking actual usando la función get_ranking que ya funciona
    ranking = get_ranking(campeonato_id, db)
    
    # Primero, eliminar cualquier ranking final existente para este campeonato
    db.query(RankingFinal).filter(RankingFinal.campeonato_id == campeonato_id).delete()
    
    # Guardar el ranking final
    for posicion, pareja in enumerate(ranking, 1):
        ranking_final = RankingFinal(
            campeonato_id=campeonato_id,
            pareja_id=pareja["pareja_id"],
            nombre_pareja=pareja["nombre_pareja"],
            PG=pareja["PG"] or 0,
            PP=pareja["PP"] or 0,
            posicion=posicion
        )
        print(f"Guardando ranking final para pareja {pareja['nombre_pareja']}: PG={pareja['PG']}, PP={pareja['PP']}")
        db.add(ranking_final)
    
    # Marcar el campeonato como cerrado
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    campeonato.estado = "CERRADO"
    
    try:
        db.commit()
        return {"message": "Campeonato cerrado exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al cerrar el campeonato: {str(e)}")
