from sqlalchemy.orm import Session
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoCreate, ResultadoUpdate
from sqlalchemy.exc import SQLAlchemyError

def create_resultado(db: Session, resultado: ResultadoCreate):
    try:
        db_resultado1 = Resultado(**resultado.pareja1.dict())
        db_resultado2 = Resultado(**resultado.pareja2.dict())
        db.add(db_resultado1)
        db.add(db_resultado2)
        db.commit()
        db.refresh(db_resultado1)
        db.refresh(db_resultado2)
        return {"resultado1": db_resultado1, "resultado2": db_resultado2}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos: {str(e)}")
        raise
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise

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

def mesa_tiene_resultados(db: Session, mesa_id: int, partida: int):
    resultado = db.query(Resultado).filter(Resultado.M == mesa_id, Resultado.P == partida).first()
    return resultado is not None
