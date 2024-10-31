from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.resultado import Resultado
from app.models.campeonato import Campeonato

router = APIRouter()

@router.post("/{campeonato_id}/actualizar-gb")
def actualizar_gb(
    campeonato_id: int,
    datos: dict,
    db: Session = Depends(get_db)
):
    try:
        # Actualizar el GB en los resultados actuales y futuros de la pareja
        db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == datos["pareja_id"],
            Resultado.P >= datos["partida_actual"]  # Incluye la partida actual
        ).update({"GB": datos["gb"]})
        
        # También actualizar los resultados existentes de la partida actual
        db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == datos["pareja_id"],
            Resultado.P == datos["partida_actual"]
        ).update({"GB": datos["gb"]})
        
        db.commit()
        return {"message": "GB actualizado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar GB: {str(e)}"
        ) 