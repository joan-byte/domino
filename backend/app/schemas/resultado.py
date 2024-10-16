from pydantic import BaseModel
from typing import Optional

class ResultadoBase(BaseModel):
    id: int
    campeonato_id: int
    P: int
    M: int
    id_pareja: int
    RP: int
    PG: int
    PP: int
    GB: str

class ResultadoPareja(BaseModel):
    P: int
    M: int
    id_pareja: int
    RP: int
    PG: int
    PP: int
    GB: str

class ResultadoCreate(BaseModel):
    campeonato_id: int
    pareja1: ResultadoPareja
    pareja2: Optional[ResultadoPareja] = None

class ResultadoUpdate(ResultadoCreate):
    pass

class Resultado(ResultadoCreate):
    id: int

    class Config:
        from_attributes = True

class ResultadoSchema(BaseModel):
    id: int
    campeonato_id: int
    P: int
    M: int
    id_pareja: int
    RP: int
    PG: int
    PP: int
    GB: str

    class Config:
        from_attributes = True

class ResultadoResponse(BaseModel):
    pareja1: ResultadoBase
    pareja2: Optional[ResultadoBase]

    class Config:
        from_attributes = True
