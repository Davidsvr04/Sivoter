from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    sigla = Column(String(20), nullable=True)