from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Campeonato(Base):
    __tablename__ = "campeonatos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    fecha_inicio = Column(Date)
    dias_duracion = Column(Integer)
    numero_partidas = Column(Integer)
    grupo_b = Column(Boolean, default=False)
    parejas = relationship("Pareja", back_populates="campeonato")
    jugadores = relationship("Jugador", back_populates="campeonato")
    resultados = relationship("Resultado", back_populates="campeonato")
