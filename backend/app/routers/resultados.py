from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import resultados as crud_resultado
from app.schemas.resultado import ResultadoSchema, ResultadoCreate, Resultado, ResultadoResponse
from sqlalchemy import func
from sqlalchemy.sql import func

router = APIRouter()

@router.post("/create", response_model=ResultadoResponse)
def create_resultado(resultado: ResultadoCreate, db: Session = Depends(get_db)):
    return crud_resultado.create_resultado(db=db, resultado=resultado)

@router.get("/test")
def test_connection():
    return {"message": "Conexión exitosa"}

@router.get("/mesa-tiene-resultados/{mesa_id}/{partida}")
def check_mesa_tiene_resultados(mesa_id: int, partida: int, db: Session = Depends(get_db)):
    tiene_resultados = crud_resultado.mesa_tiene_resultados(db, mesa_id, partida)
    return {"tiene_resultados": tiene_resultados}

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
