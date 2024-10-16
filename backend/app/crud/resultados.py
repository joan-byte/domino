from sqlalchemy.orm import Session
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoCreate, ResultadoUpdate
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def create_resultado(db: Session, resultado: ResultadoCreate):
    db_resultado1 = Resultado(
        campeonato_id=resultado.campeonato_id,
        P=resultado.pareja1.P,
        M=resultado.pareja1.M,
        id_pareja=resultado.pareja1.id_pareja,
        RP=resultado.pareja1.RP,
        PG=resultado.pareja1.PG,
        PP=resultado.pareja1.PP,
        GB=resultado.pareja1.GB
    )
    db.add(db_resultado1)
    
    db_resultado2 = None
    if resultado.pareja2:
        db_resultado2 = Resultado(
            campeonato_id=resultado.campeonato_id,
            P=resultado.pareja2.P,
            M=resultado.pareja2.M,
            id_pareja=resultado.pareja2.id_pareja,
            RP=resultado.pareja2.RP,
            PG=resultado.pareja2.PG,
            PP=resultado.pareja2.PP,
            GB=resultado.pareja2.GB
        )
        db.add(db_resultado2)
    
    db.commit()
    db.refresh(db_resultado1)
    if db_resultado2:
        db.refresh(db_resultado2)
    
    return {
        "pareja1": db_resultado1.to_dict(),
        "pareja2": db_resultado2.to_dict() if db_resultado2 else None
    }

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
    if len(resultados) == 1:
        # Si solo hay una pareja, asignar automáticamente los valores
        resultados[0].PG = 1
        resultados[0].PP = 150
    elif len(resultados) == 2:
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

def get_resultados(db: Session, mesa_id: int, partida: int):
    resultados = db.query(Resultado).filter(Resultado.M == mesa_id, Resultado.P == partida).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="Resultados no encontrados")
    
    response = {}
    for resultado in resultados:
        key = f"pareja{1 if resultado.id_pareja == resultados[0].id_pareja else 2}"
        response[key] = resultado
    
    return response

def update_resultados(db: Session, mesa_id: int, partida: int, resultado: ResultadoCreate):
    existing_resultados = db.query(Resultado).filter(Resultado.M == mesa_id, Resultado.P == partida).all()
    if not existing_resultados:
        raise HTTPException(status_code=404, detail="Resultados no encontrados")
    
    for existing_resultado in existing_resultados:
        if existing_resultado.id_pareja == resultado.pareja1.id_pareja:
            for key, value in resultado.pareja1.dict().items():
                setattr(existing_resultado, key, value)
        elif resultado.pareja2 and existing_resultado.id_pareja == resultado.pareja2.id_pareja:
            for key, value in resultado.pareja2.dict().items():
                setattr(existing_resultado, key, value)
    
    db.commit()
    return get_resultados(db, mesa_id, partida)

def get_resultado_by_mesa_and_partida(db: Session, mesa_id: int, partida: int):
    return db.query(Resultado).filter(Resultado.M == mesa_id, Resultado.P == partida).first()
