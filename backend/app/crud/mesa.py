from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models.mesa import Mesa
from app.models.jugador import Pareja
from app.schemas.mesa import MesaConParejas, ParejaSimple
import random
from sqlalchemy import text

def crear_mesas(db: Session, parejas_activas: List[Pareja]) -> List[Mesa]:
    # Mezclar las parejas aleatoriamente
    random.shuffle(parejas_activas)
    
    mesas = []
    for i in range(0, len(parejas_activas), 2):
        if i + 1 < len(parejas_activas):
            mesa = Mesa(pareja1_id=parejas_activas[i].id, pareja2_id=parejas_activas[i+1].id)
        else:
            # Si hay un número impar de parejas, la última mesa tendrá solo una pareja
            mesa = Mesa(pareja1_id=parejas_activas[i].id)
        db.add(mesa)
        mesas.append(mesa)
    
    db.commit()
    return mesas

def obtener_mesas(db: Session) -> List[Mesa]:
    return db.query(Mesa).all()

def eliminar_todas_mesas(db: Session):
    db.query(Mesa).delete()
    db.execute(text("ALTER SEQUENCE mesas_id_seq RESTART WITH 1"))
    db.commit()

def obtener_mesas_con_parejas(db: Session) -> List[Mesa]:
    return db.query(Mesa).options(
        joinedload(Mesa.pareja1),
        joinedload(Mesa.pareja2)
    ).all()

def obtener_parejas_con_mesas(db: Session) -> List[dict]:
    parejas = db.query(Pareja).all()
    mesas = db.query(Mesa).options(
        joinedload(Mesa.pareja1),
        joinedload(Mesa.pareja2)
    ).all()
    
    parejas_con_mesas = []
    for pareja in parejas:
        mesa_asignada = next((mesa for mesa in mesas if mesa.pareja1_id == pareja.id or mesa.pareja2_id == pareja.id), None)
        parejas_con_mesas.append({
            "id": pareja.id,
            "nombre": pareja.nombre,
            "mesa_asignada": mesa_asignada.id if mesa_asignada else None
        })
    
    return parejas_con_mesas

def obtener_mesas_para_registro(db: Session) -> List[MesaConParejas]:
    mesas = db.query(Mesa).all()
    return [MesaConParejas(
        id=mesa.id,
        pareja1_id=mesa.pareja1_id,
        pareja2_id=mesa.pareja2_id
    ) for mesa in mesas]
