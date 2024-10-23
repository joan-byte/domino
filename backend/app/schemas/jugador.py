from pydantic import BaseModel, validator, Field
from typing import Optional, List

class JugadorBase(BaseModel):
    nombre: str
    apellido: str

class JugadorCreate(JugadorBase):
    pass

class JugadorSchema(JugadorBase):
    id: int
    pareja_id: Optional[int] = None
    campeonato_id: int

    class Config:
        from_attributes = True

class ParejaBase(BaseModel):
    club: Optional[str] = None  # Hacer el campo opcional
    activa: bool
    campeonato_id: int

class ParejaCreate(ParejaBase):
    jugador1: JugadorCreate
    jugador2: JugadorCreate

class ParejaSchema(ParejaBase):
    id: int
    nombre: str = Field(..., description="Nombre de la pareja")
    jugadores: List[JugadorSchema]

    class Config:
        from_attributes = True

class JugadorUpdateForPairing(BaseModel):
    nombre: str
    apellido: str

class ParejaUpdate(BaseModel):
    jugador1: JugadorUpdateForPairing
    jugador2: JugadorUpdateForPairing
    club: Optional[str] = None
    activa: bool
    campeonato_id: int

class ParejaConMesa(BaseModel):
    id: int
    nombre: str
    mesa_asignada: Optional[int] = None

    class Config:
        from_attributes = True  # Cambiamos 'orm_mode' a 'from_attributes'

# Importación circular al final del archivo
from app.schemas.jugador import JugadorSchema
ParejaSchema.model_rebuild()
