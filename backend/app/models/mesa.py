from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    pareja1_id = Column(Integer, ForeignKey("parejas.id"))
    pareja2_id = Column(Integer, ForeignKey("parejas.id"))
    
    pareja1 = relationship("Pareja", foreign_keys=[pareja1_id])
    pareja2 = relationship("Pareja", foreign_keys=[pareja2_id])
