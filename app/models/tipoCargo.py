from sqlalchemy import Column, Integer, String, Enum
from app.database.base import Base
import enum


class NivelEnum(str, enum.Enum):
    nacional = "nacional"
    departamental = "departamental"
    municipal = "municipal"


class TipoCargo(Base):
    __tablename__ = "tipo_cargo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    nivel = Column(Enum(NivelEnum), nullable=False)