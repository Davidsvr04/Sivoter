from sqlalchemy import Column, Integer, String, ForeignKey, text
from app.database.base import Base


class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    partido_id = Column(Integer, ForeignKey("partidos.id", ondelete="SET NULL"), nullable=True)
    votacion_id = Column(Integer, ForeignKey("votaciones.id", ondelete="CASCADE"), nullable=True)
    tipo_cargo_id = Column(Integer, ForeignKey("tipo_cargo.id", ondelete="SET NULL"), nullable=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id", ondelete="SET NULL"), nullable=True)
    municipio_id = Column(Integer, ForeignKey("municipios.id", ondelete="SET NULL"), nullable=True)

    votos = Column(Integer, nullable=False, default=0, server_default=text("0"))