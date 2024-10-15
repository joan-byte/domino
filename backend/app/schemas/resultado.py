from pydantic import BaseModel
from typing import Optional

class ResultadoBase(BaseModel):
    P: int
    M: int
    id_pareja: int
    RP: int
    PG: int
    PP: int
    GB: str = "A"

class ResultadoCreate(BaseModel):
    pareja1: ResultadoBase
    pareja2: Optional[ResultadoBase] = None

class ResultadoUpdate(BaseModel):
    pareja1: ResultadoBase
    pareja2: ResultadoBase

class Resultado(ResultadoBase):
    id: int

    class Config:
        from_attributes = True
