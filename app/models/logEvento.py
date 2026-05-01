from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database.base import Base


class LogEvento(Base):
    __tablename__ = "logs_eventos"

    id = Column(Integer, primary_key=True, index=True)
    evento = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    usuario_id = Column(Integer, nullable=True)
    fecha = Column(DateTime, server_default=func.now())
