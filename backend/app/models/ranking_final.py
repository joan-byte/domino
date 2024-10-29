from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class RankingFinal(Base):
    __tablename__ = "rankings_finales"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    pareja_id = Column(Integer, ForeignKey("parejas.id"))
    nombre_pareja = Column(String)
    puntos_ganados = Column(Integer)
    puntos_perdidos = Column(Integer)
    posicion = Column(Integer) 