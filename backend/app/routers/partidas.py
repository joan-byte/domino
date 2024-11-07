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



@router.post("/{campeonato_id}/sorteo-inicial")
def realizar_sorteo_inicial(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Verificar que el campeonato existe
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Obtener todas las parejas activas del campeonato
        parejas_activas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        if not parejas_activas:
            raise HTTPException(
                status_code=400,
                detail="No hay parejas activas para realizar el sorteo"
            )

        # Actualizar la partida actual del campeonato a 1
        campeonato.partida_actual = 1
        db.commit()

        # Crear las mesas con las parejas
        mesas = crud_mesa.crear_mesas(db, parejas_activas, campeonato_id, partida=1)

        return [
            {
                "id": mesa.id,
                "numero": mesa.numero,
                "pareja1_id": mesa.pareja1_id,
                "pareja2_id": mesa.pareja2_id
            }
            for mesa in mesas
        ]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{campeonato_id}/sorteo-inicial")
def eliminar_sorteo_inicial(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Verificar que el campeonato existe
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Eliminar todas las mesas del campeonato
        db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).delete()
        
        # Resetear la partida actual del campeonato
        campeonato.partida_actual = 0
        
        db.commit()
        return {"message": "Sorteo eliminado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mesas", response_model=List[MesaConParejas])
def obtener_mesas(db: Session = Depends(get_db)):
    return crud_mesa.obtener_mesas_con_parejas(db)

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
    
    # Ordenar la lista por ID de pareja
    parejas_info.sort(key=lambda x: x["id"])
    
    return parejas_info
