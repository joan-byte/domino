from pydantic import BaseModel
from datetime import date
from typing import Optional

class CampeonatoBase(BaseModel):
    nombre: str
    fecha_inicio: date
    dias_duracion: int
    numero_partidas: int
    grupo_b: Optional[bool] = False

class CampeonatoCreate(CampeonatoBase):
    pass

class CampeonatoSchema(CampeonatoBase):
    id: int
    partida_actual: int

    class Config:
        from_attributes = True

class CampeonatoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    dias_duracion: Optional[int] = None
    numero_partidas: Optional[int] = None
    partida_actual: Optional[int] = None
