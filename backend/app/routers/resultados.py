from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import resultados as crud_resultado
from app.schemas.resultado import ResultadoSchema, ResultadoCreate, Resultado, ResultadoResponse
from app.models.resultado import Resultado
from app.models.campeonato import Campeonato
from sqlalchemy import func
from sqlalchemy.sql import func
from typing import Dict

router = APIRouter()

@router.post("/create", response_model=ResultadoResponse)
def create_resultado(resultado: ResultadoCreate, db: Session = Depends(get_db)):
    return crud_resultado.create_resultado(db=db, resultado=resultado)

@router.get("/test")
def test_connection():
    return {"message": "Conexión exitosa"}

@router.get("/mesa-tiene-resultados/{mesa_id}/{partida}")
def check_mesa_tiene_resultados(
    mesa_id: int, 
    partida: int, 
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    tiene_resultados = crud_resultado.mesa_tiene_resultados(
        db=db, 
        mesa_id=mesa_id, 
        partida=partida,
        campeonato_id=campeonato_id
    )
    return {"tiene_resultados": tiene_resultados}

@router.get("/{mesa_id}/{partida}")
def get_resultados(
    mesa_id: int, 
    partida: int, 
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    return crud_resultado.get_resultados(db, mesa_id, partida, campeonato_id)

@router.post("/update/{mesa_id}/{partida}")
def update_resultados(mesa_id: int, partida: int, resultado: ResultadoCreate, db: Session = Depends(get_db)):
    return crud_resultado.update_resultados(db, mesa_id, partida, resultado)

@router.put("/resultados/{mesa_id}/{partida}")
def update_resultados(mesa_id: int, partida: int, resultado: ResultadoCreate, db: Session = Depends(get_db)):
    try:
        return crud_resultado.update_resultados(db, mesa_id, partida, resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mesa/{mesa_id}/partida/{partida}")
def obtener_resultados_mesa(
    mesa_id: int, 
    partida: int, 
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    try:
        return crud_resultado.get_resultados(db, mesa_id, partida, campeonato_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mesa/{mesa_id}/partida/{partida}/tiene-resultados")
def verificar_resultados_mesa(
    mesa_id: int, 
    partida: int, 
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    return {
        "tiene_resultados": crud_resultado.mesa_tiene_resultados(
            db, 
            mesa_id, 
            partida, 
            campeonato_id
        )
    }

@router.post("/inicializar-gb")
def inicializar_gb(datos: dict, db: Session = Depends(get_db)):
    try:
        # Actualizar TODOS los resultados futuros de la pareja
        db.query(Resultado).filter(
            Resultado.campeonato_id == datos["campeonato_id"],
            Resultado.id_pareja == datos["pareja_id"],
            Resultado.P > datos["partida_actual"]  # Solo partidas futuras
        ).update({"GB": datos["gb"]})
        
        # Crear plantillas para todas las partidas futuras si no existen
        partida_actual = datos["partida_actual"]
        campeonato = db.query(Campeonato).filter(
            Campeonato.id == datos["campeonato_id"]
        ).first()
        
        if campeonato:
            for partida in range(partida_actual + 1, campeonato.numero_partidas + 1):
                # Verificar si ya existe un resultado para esta partida
                resultado_existente = db.query(Resultado).filter(
                    Resultado.campeonato_id == datos["campeonato_id"],
                    Resultado.id_pareja == datos["pareja_id"],
                    Resultado.P == partida
                ).first()
                
                # Si no existe, crear uno nuevo
                if not resultado_existente:
                    nuevo_resultado = Resultado(
                        campeonato_id=datos["campeonato_id"],
                        id_pareja=datos["pareja_id"],
                        GB=datos["gb"],
                        P=partida
                    )
                    db.add(nuevo_resultado)
        
        db.commit()
        return {"message": "GB inicializado correctamente para todas las partidas futuras"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al inicializar GB: {str(e)}"
        )

@router.post("/ajustar-pg")
def ajustar_pg(datos: dict, db: Session = Depends(get_db)):
    try:
        # Actualizar el PG de la pareja en la última partida registrada
        resultado = db.query(Resultado).filter(
            Resultado.campeonato_id == datos["campeonato_id"],
            Resultado.id_pareja == datos["pareja_id"]
        ).order_by(Resultado.P.desc()).first()
        
        if resultado:
            resultado.PG = datos["nuevo_pg"]
            db.commit()
            return {"message": "PG actualizado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="No se encontró el resultado para ajustar")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))





