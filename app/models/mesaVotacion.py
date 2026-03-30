from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.database.base import Base


class MesaVotacion(Base):
    __tablename__ = "lugares_votacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(200), nullable=True)
    municipio_id = Column(Integer, ForeignKey("municipios.id", ondelete="SET NULL"), nullable=True)
    barrio_id = Column(Integer, ForeignKey("barrios.id", ondelete="SET NULL"), nullable=True)
    numero_mesa = Column(Integer, nullable=True)
