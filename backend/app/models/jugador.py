from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Pareja(Base):
    __tablename__ = "parejas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    club = Column(String, nullable=True)  # Añadimos esta línea
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    activa = Column(Boolean, default=True)
    campeonato = relationship("Campeonato", back_populates="parejas")
    campeonato = relationship("Campeonato", back_populates="parejas")
    jugadores = relationship("Jugador", back_populates="pareja")

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    pareja_id = Column(Integer, ForeignKey("parejas.id"))
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"), nullable=False)

    pareja = relationship("Pareja", back_populates="jugadores")
    campeonato = relationship("Campeonato", back_populates="jugadores")

    __table_args__ = (
        UniqueConstraint('nombre', 'apellido', name='uq_jugador'),
    )
