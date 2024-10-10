from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    P = Column(Integer)  # Número de partida
    M = Column(Integer, ForeignKey("mesas.id"))  # ID de la mesa
    id_pareja = Column(Integer, ForeignKey("parejas.id"))  # ID de la pareja
    GB = Column(String, default="A")  # Por defecto A
    PG = Column(Integer)  # 1 si ganó, 0 si perdió
    PP = Column(Integer)  # Diferencia de puntos
    RP = Column(Integer)  # Resultado de la pareja
