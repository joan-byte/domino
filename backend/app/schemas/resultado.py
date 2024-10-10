from pydantic import BaseModel

class ResultadoBase(BaseModel):
    P: int
    M: int
    id_pareja: int
    RP: int
    GB: str = "A"  # Añadimos esta línea con el valor por defecto

class ResultadoCreate(ResultadoBase):
    pass

class ResultadoUpdate(BaseModel):
    RP: int

class Resultado(ResultadoBase):
    id: int
    PG: int
    PP: int

    class Config:
        from_attributes = True
