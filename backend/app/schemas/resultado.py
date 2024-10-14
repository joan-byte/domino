from pydantic import BaseModel

class ResultadoBase(BaseModel):
    P: int
    M: int
    id_pareja: int
    RP: int
    GB: str = "A"

class ResultadoCreate(BaseModel):
    pareja1: ResultadoBase
    pareja2: ResultadoBase

class ResultadoUpdate(BaseModel):
    pareja1: ResultadoBase
    pareja2: ResultadoBase

class Resultado(ResultadoBase):
    id: int
    PG: int
    PP: int

    class Config:
        from_attributes = True