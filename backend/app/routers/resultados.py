from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import resultados as crud_resultado
from app.schemas.resultado import ResultadoCreate, ResultadoUpdate, Resultado

router = APIRouter()

@router.get("/resultados/")
@router.post("/resultados", response_model=Resultado)
def create_resultado(resultado: ResultadoCreate, db: Session = Depends(get_db)):
    db_resultado = crud_resultado.create_resultado(db, resultado)
    crud_resultado.calculate_and_update_results(db, resultado.M)
    return db_resultado

@router.put("/resultados/{resultado_id}", response_model=Resultado)
def update_resultado(resultado_id: int, resultado: ResultadoUpdate, db: Session = Depends(get_db)):
    db_resultado = crud_resultado.update_resultado(db, resultado_id, resultado)
    if db_resultado is None:
        raise HTTPException(status_code=404, detail="Resultado not found")
    crud_resultado.calculate_and_update_results(db, db_resultado.M)
    return db_resultado

@router.get("/resultados/{resultado_id}", response_model=Resultado)
def read_resultado(resultado_id: int, db: Session = Depends(get_db)):
    db_resultado = crud_resultado.get_resultado(db, resultado_id)
    if db_resultado is None:
        raise HTTPException(status_code=404, detail="Resultado not found")
    return db_resultado

# Añade más rutas según sea necesario
