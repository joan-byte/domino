from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud import mesa as crud_mesa
from app.crud import pareja as crud_pareja
from app.schemas.mesa import MesaConParejas, Mesa
from app.models.campeonato import Campeonato
from app.models.mesa import Mesa as MesaModel
from app.models.jugador import Pareja

router = APIRouter()

@router.get("/partidas/")
def read_partidas(db: Session = Depends(get_db)):
    # Lógica para leer partidas
    return {"message": "Lectura de partidas"}

@router.get("/partidas/test")
def test_partidas():
    return {"message": "Test de partidas exitoso"}

# Añade más rutas según sea necesario



@router.post("/sorteo-inicial", response_model=List[Mesa])
def realizar_sorteo_inicial(db: Session = Depends(get_db)):
    parejas_activas = crud_pareja.get_parejas_activas(db)
    if len(parejas_activas) < 2:
        raise HTTPException(status_code=400, detail="No hay suficientes parejas activas para realizar el sorteo")
    
    # Eliminar mesas existentes antes de crear nuevas
    crud_mesa.eliminar_todas_mesas(db)
    
    campeonato_id = parejas_activas[0].campeonato_id  # Asumimos que todas las parejas son del mismo campeonato
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    campeonato.partida_actual = 1
    db.commit()
    
    mesas = crud_mesa.crear_mesas(db, parejas_activas, campeonato_id, campeonato.partida_actual)
    return mesas

@router.get("/mesas", response_model=List[MesaConParejas])
def obtener_mesas(db: Session = Depends(get_db)):
    return crud_mesa.obtener_mesas_con_parejas(db)

@router.delete("/sorteo-inicial")
def eliminar_sorteo_inicial(db: Session = Depends(get_db)):
    crud_mesa.eliminar_todas_mesas(db)
    return {"message": "Sorteo eliminado"}

@router.get("/parejas-mesas")
def obtener_parejas_mesas(db: Session = Depends(get_db)):
    return crud_mesa.obtener_parejas_con_mesas(db)

@router.get("/mesas-registro", response_model=List[MesaConParejas])
def obtener_mesas_registro(db: Session = Depends(get_db)):
    return crud_mesa.obtener_mesas_para_registro(db)

@router.get("/mesas-asignadas/{campeonato_id}")
def obtener_mesas_asignadas(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    mesas = db.query(MesaModel).filter(
        MesaModel.campeonato_id == campeonato_id,
        MesaModel.partida == campeonato.partida_actual
    ).all()
    
    parejas_info = []
    for mesa in mesas:
        for pareja_id in [mesa.pareja1_id, mesa.pareja2_id]:
            if pareja_id:
                pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
                if pareja:
                    parejas_info.append({
                        "id": pareja.id,
                        "nombre": pareja.nombre,
                        "club": pareja.club,
                        "mesa": mesa.numero
                    })
    
    return parejas_info
