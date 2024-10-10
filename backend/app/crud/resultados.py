from sqlalchemy.orm import Session
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoCreate, ResultadoUpdate

def create_resultado(db: Session, resultado: ResultadoCreate):
    db_resultado = Resultado(**resultado.dict())
    db.add(db_resultado)
    db.commit()
    db.refresh(db_resultado)
    return db_resultado

def get_resultado(db: Session, resultado_id: int):
    return db.query(Resultado).filter(Resultado.id == resultado_id).first()

def update_resultado(db: Session, resultado_id: int, resultado: ResultadoUpdate):
    db_resultado = db.query(Resultado).filter(Resultado.id == resultado_id).first()
    if db_resultado:
        for key, value in resultado.dict().items():
            setattr(db_resultado, key, value)
        db.commit()
        db.refresh(db_resultado)
    return db_resultado

def calculate_and_update_results(db: Session, mesa_id: int):
    resultados = db.query(Resultado).filter(Resultado.M == mesa_id).all()
    if len(resultados) == 2:
        if resultados[0].RP > resultados[1].RP:
            resultados[0].PG, resultados[1].PG = 1, 0
            resultados[0].PP = resultados[0].RP - resultados[1].RP
            resultados[1].PP = resultados[1].RP - resultados[0].RP
        elif resultados[0].RP < resultados[1].RP:
            resultados[0].PG, resultados[1].PG = 0, 1
            resultados[0].PP = resultados[0].RP - resultados[1].RP
            resultados[1].PP = resultados[1].RP - resultados[0].RP
        else:
            resultados[0].PG, resultados[1].PG = 0, 0
            resultados[0].PP, resultados[1].PP = 0, 0
        db.commit()
