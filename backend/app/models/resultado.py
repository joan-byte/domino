from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    P = Column(Integer)
    M = Column(Integer)
    id_pareja = Column(Integer, ForeignKey("parejas.id"))
    RP = Column(Integer)
    PG = Column(Integer)
    PP = Column(Integer)
    GB = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "campeonato_id": self.campeonato_id,
            "P": self.P,
            "M": self.M,
            "id_pareja": self.id_pareja,
            "RP": self.RP,
            "PG": self.PG,
            "PP": self.PP,
            "GB": self.GB
        }
