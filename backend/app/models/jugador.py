from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Pareja(Base):
    __tablename__ = "parejas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    club = Column(String, nullable=True)  # Permitir que sea nulo
    activa = Column(Boolean, default=True)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))

    jugadores = relationship("Jugador", back_populates="pareja")
    campeonato = relationship("Campeonato", back_populates="parejas")

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    pareja_id = Column(Integer, ForeignKey("parejas.id"))
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))

    pareja = relationship("Pareja", back_populates="jugadores")
    campeonato = relationship("Campeonato", back_populates="jugadores")

    __table_args__ = (
        UniqueConstraint('nombre', 'apellido', 'campeonato_id', name='uq_jugador_campeonato'),
    )
