from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.mesa import Mesa
from app.crud import mesa as crud_mesa

router = APIRouter(
    prefix="/api/mesas",
    tags=["mesas"]
)

@router.get("/{mesa_id}")
def obtener_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail=f"Mesa {mesa_id} no encontrada")
    
    total_mesas = db.query(Mesa).filter(
        Mesa.campeonato_id == mesa.campeonato_id,
        Mesa.partida == mesa.partida
    ).count()
    
    mitad_mesas = total_mesas // 2
    grupo = 'B' if mesa.numero > mitad_mesas else 'A'
    
    return {
        "id": mesa.id,
        "numero": mesa.numero,
        "pareja1_id": mesa.pareja1_id,
        "pareja2_id": mesa.pareja2_id,
        "campeonato_id": mesa.campeonato_id,
        "partida": mesa.partida,
        "grupo": grupo
    }