from pydantic import BaseModel, validator
from typing import Optional, List

class JugadorBase(BaseModel):
    nombre: str
    apellido: str

class JugadorCreate(JugadorBase):
    pass

class JugadorInDBBase(JugadorBase):
    id: int
    pareja_id: int

    class Config:
        orm_mode = True

class JugadorSchema(JugadorInDBBase):
    pass

class ParejaBase(BaseModel):
    nombre: str
    campeonato_id: int
    club: Optional[str] = None  # Añadimos esta línea
    activa: bool = True

class ParejaCreate(BaseModel):
    jugador1: JugadorCreate
    jugador2: JugadorCreate
    club: str
    campeonato_id: int
    activa: bool

class ParejaInDBBase(ParejaBase):
    id: int

    class Config:
        orm_mode = True

class ParejaSchema(ParejaInDBBase):
    pass

class ParejaUpdate(BaseModel):
    jugador1: JugadorCreate
    jugador2: JugadorCreate
    club: str
    activa: bool
    campeonato_id: int