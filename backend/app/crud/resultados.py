from sqlalchemy.orm import Session
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoCreate, ResultadoUpdate
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy import func, case
from app.models.jugador import Pareja

def create_resultado(db: Session, resultado: ResultadoCreate):
    # Verificar si estamos en la mitad del campeonato y es grupo B
    def should_be_gb_b(mesa_id: int, campeonato_id: int) -> bool:
        try:
            # Obtener el total de mesas para esta partida
            total_mesas = db.query(func.count(Resultado.M.distinct())).filter(
                Resultado.campeonato_id == campeonato_id,
                Resultado.P == resultado.pareja1.P
            ).scalar() or 0

            # Calcular la mitad de las mesas (redondeando hacia abajo)
            mitad_mesas = total_mesas // 2

            # La mesa está en la segunda mitad si su número es mayor que la mitad
            return mesa_id > mitad_mesas
        except Exception as e:
            print(f"Error al verificar GB para mesa {mesa_id}: {str(e)}")
            return False

    def get_gb_for_pareja(pareja_id: int, mesa_id: int) -> str:
        # Primero verificar si la pareja ya tiene algún GB='B'
        gb_anterior = db.query(
            func.max(case(
                (Resultado.GB == 'B', 'B'),
                else_='A'
            ))
        ).filter(
            Resultado.campeonato_id == resultado.campeonato_id,
            Resultado.id_pareja == pareja_id
        ).scalar()

        if gb_anterior == 'B':
            return 'B'

        # Si no tiene GB='B' previo, verificar si debería tenerlo por su posición en la mesa
        es_grupo_b = should_be_gb_b(mesa_id, resultado.campeonato_id)
        return 'B' if es_grupo_b else 'A'

    # Crear resultado para pareja 1
    gb_pareja1 = get_gb_for_pareja(resultado.pareja1.id_pareja, resultado.pareja1.M)
    db_resultado1 = Resultado(
        campeonato_id=resultado.campeonato_id,
        P=resultado.pareja1.P,
        M=resultado.pareja1.M,
        id_pareja=resultado.pareja1.id_pareja,
        RP=resultado.pareja1.RP,
        PG=resultado.pareja1.PG,
        PP=resultado.pareja1.PP,
        GB=gb_pareja1
    )
    db.add(db_resultado1)
    
    db_resultado2 = None
    if resultado.pareja2:
        gb_pareja2 = get_gb_for_pareja(resultado.pareja2.id_pareja, resultado.pareja2.M)
        db_resultado2 = Resultado(
            campeonato_id=resultado.campeonato_id,
            P=resultado.pareja2.P,
            M=resultado.pareja2.M,
            id_pareja=resultado.pareja2.id_pareja,
            RP=resultado.pareja2.RP,
            PG=resultado.pareja2.PG,
            PP=resultado.pareja2.PP,
            GB=gb_pareja2
        )
        db.add(db_resultado2)
    
    try:
        db.commit()
        db.refresh(db_resultado1)
        if db_resultado2:
            db.refresh(db_resultado2)
        
        return {
            "pareja1": db_resultado1.to_dict(),
            "pareja2": db_resultado2.to_dict() if db_resultado2 else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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

def mesa_tiene_resultados(db: Session, mesa_id: int, partida: int, campeonato_id: int):
    resultados = db.query(Resultado).filter(
        Resultado.M == mesa_id, 
        Resultado.P == partida,
        Resultado.campeonato_id == campeonato_id
    ).all()
    return len(resultados) > 0

def get_resultados(db: Session, mesa_id: int, partida: int, campeonato_id: int):
    print(f"Buscando resultados para mesa_id: {mesa_id}, partida: {partida}, campeonato_id: {campeonato_id}")
    resultados = db.query(Resultado).filter(
        Resultado.M == mesa_id, 
        Resultado.P == partida,
        Resultado.campeonato_id == campeonato_id
    ).all()
    print(f"Resultados encontrados: {resultados}")
    
    if not resultados:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron resultados para la mesa {mesa_id}, partida {partida} y campeonato {campeonato_id}"
        )
    
    response = {}
    for i, resultado in enumerate(resultados, start=1):
        response[f"pareja{i}"] = {
            "id": resultado.id,
            "campeonato_id": resultado.campeonato_id,
            "P": resultado.P,
            "M": resultado.M,
            "id_pareja": resultado.id_pareja,
            "GB": resultado.GB,
            "PG": resultado.PG,
            "PP": resultado.PP,
            "RP": resultado.RP
        }
    
    # Si solo hay una pareja, asegurarse de que pareja2 esté presente pero vacía
    if len(resultados) == 1:
        response["pareja2"] = None
    
    print(f"Respuesta final: {response}")
    return response

def update_resultados(db: Session, mesa_id: int, partida: int, resultado: ResultadoCreate):
    # Buscar los resultados existentes
    resultados_existentes = db.query(Resultado).filter(Resultado.M == mesa_id, Resultado.P == partida).all()
    
    if not resultados_existentes:
        raise HTTPException(status_code=404, detail="Resultados no encontrados")

    # Actualizar los resultados existentes
    for resultado_existente in resultados_existentes:
        if resultado_existente.id_pareja == resultado.pareja1.id_pareja:
            update_data = resultado.pareja1.dict(exclude_unset=True)
        elif resultado_existente.id_pareja == resultado.pareja2.id_pareja:
            update_data = resultado.pareja2.dict(exclude_unset=True)
        else:
            continue

        for key, value in update_data.items():
            setattr(resultado_existente, key, value)

    try:
        db.commit()
        db.refresh(resultado_existente)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar los resultados: {str(e)}")
    
    return {"message": "Resultados actualizados exitosamente"}

def get_resultado_by_mesa_and_partida(db: Session, mesa_id: int, partida: int):
    return db.query(Resultado).filter(Resultado.M == mesa_id, Resultado.P == partida).first()

def get_ranking(db: Session, campeonato_id: int):
    # Primero obtenemos todos los resultados para cada pareja
    resultados = db.query(
        Resultado.id_pareja,
        func.sum(Resultado.PG).label('total_PG'),
        func.sum(Resultado.PP).label('total_PP'),
        # Usamos una subquery para determinar si algún resultado tiene GB='B'
        func.max(case(
            (Resultado.GB == 'B', 'B'),
            else_='A'
        )).label('GB')
    ).filter(
        Resultado.campeonato_id == campeonato_id
    ).group_by(
        Resultado.id_pareja
    ).all()

    # Procesamos los resultados
    ranking = []
    for resultado in resultados:
        pareja = db.query(Pareja).filter(Pareja.id == resultado.id_pareja).first()
        if pareja:
            ranking.append({
                'pareja_id': resultado.id_pareja,
                'nombre_pareja': pareja.nombre,
                'club': pareja.club,
                'PG': resultado.total_PG,
                'PP': resultado.total_PP,
                'GB': resultado.GB
            })

    # Ordenar el ranking
    ranking.sort(key=lambda x: (-x['PG'], x['PP']))
    return ranking
