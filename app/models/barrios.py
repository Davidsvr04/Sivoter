from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base


class Barrio(Base):
    __tablename__ = "barrios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    municipio_id = Column(Integer, ForeignKey("municipios.id", ondelete="CASCADE"), nullable=True)