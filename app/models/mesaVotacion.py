from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.base import Base


class MesaVotacion(Base):
    __tablename__ = "mesas_votacion"

    id = Column(Integer, primary_key=True, index=True)
    departamento = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    barrio = Column(String(100), nullable=False)
    nombre_lugar = Column(String(150), nullable=False)
    numero_mesa = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
