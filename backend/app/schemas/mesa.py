from pydantic import BaseModel
from typing import Optional
from .jugador import ParejaSchema

class MesaBase(BaseModel):
    pareja1_id: int
    pareja2_id: Optional[int] = None

class Mesa(MesaBase):
    id: int

    class Config:
        orm_mode = True

class ParejaSimple(BaseModel):
    id: int
    nombre: str

class MesaConParejas(BaseModel):
    id: int
    pareja1_id: Optional[int] = None
    pareja2_id: Optional[int] = None

    class Config:
        orm_mode = True

class ParejaConMesa(BaseModel):
    id: int
    nombre: str
    mesa_id: Optional[int] = None

    class Config:
        from_attributes = True

