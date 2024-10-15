from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import resultados as crud_resultado
from app.schemas.resultado import ResultadoCreate, Resultado

router = APIRouter()

@router.post("/resultados", response_model=dict[str, Resultado])
def create_resultado(resultado: ResultadoCreate, db: Session = Depends(get_db)):
    try:
        return crud_resultado.create_resultado(db, resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
def test_connection():
    return {"message": "Conexión exitosa"}

@router.get("/mesa-tiene-resultados/{mesa_id}/{partida}")
def check_mesa_tiene_resultados(mesa_id: int, partida: int, db: Session = Depends(get_db)):
    return {"tiene_resultados": crud_resultado.mesa_tiene_resultados(db, mesa_id, partida)}

@router.get("/resultados/{mesa_id}/{partida}", response_model=dict[str, Resultado])
def get_resultados(mesa_id: int, partida: int, db: Session = Depends(get_db)):
    try:
        return crud_resultado.get_resultados(db, mesa_id, partida)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/resultados/{mesa_id}/{partida}", response_model=dict[str, Resultado])
def update_resultados(mesa_id: int, partida: int, resultado: ResultadoCreate, db: Session = Depends(get_db)):
    try:
        return crud_resultado.update_resultados(db, mesa_id, partida, resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Añade más rutas según sea necesario