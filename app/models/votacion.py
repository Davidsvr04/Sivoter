from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from app.database.base import Base
from datetime import datetime
import enum


class EstadoEnum(str, enum.Enum):
    activa = "activa"
    cerrada = "cerrada"


class Votacion(Base):
    __tablename__ = "votaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    tipo_cargo_id = Column(Integer, ForeignKey("tipo_cargo.id", ondelete="SET NULL"), nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(Enum(EstadoEnum), nullable=False)