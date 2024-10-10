from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud import mesa as crud_mesa
from app.crud import pareja as crud_pareja
from app.schemas.mesa import MesaConParejas, Mesa
# Importa los modelos y esquemas necesarios

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
    
    mesas = crud_mesa.crear_mesas(db, parejas_activas)
    return {"mesas": mesas, "partida_actual": 1}

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


