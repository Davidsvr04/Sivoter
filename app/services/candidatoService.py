from __future__ import annotations
from collections.abc import Sequence
from sqlalchemy.orm import Session

from app.models.candidatos import Candidato
from app.schemas.candidatoSchema import CandidatoCreate, CandidatoUpdate
from app.services.kafkaService import kafka_producer
from app.services.baseService import BaseService

FK_MAP = {
    "partido_id": "partidos",
    "votacion_id": "votaciones",
    "tipo_cargo_id": "tipo_cargo",
    "departamento_id": "departamentos",
    "municipio_id": "municipios",
}
base_service = BaseService(Candidato, FK_MAP)


def create_candidato(db: Session, payload: CandidatoCreate, usuario_id: int = None) -> Candidato:
    """Crear un nuevo candidato."""
    data = payload.model_dump()
    base_service._validate_foreign_keys(db, data)

    candidato = Candidato(**data)
    db.add(candidato)
    db.commit()
    db.refresh(candidato)
    
    kafka_producer.send_candidato_created(candidato.id, candidato.nombre, usuario_id)
    return candidato


def list_candidatos(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Candidato]:
    """Listar candidatos."""
    return base_service.list_all(db, skip, limit)


def get_candidato(db: Session, candidato_id: int) -> Candidato:
    """Obtener candidato por ID."""
    return base_service.get_by_id(db, candidato_id)


def update_candidato(db: Session, candidato_id: int, payload: CandidatoUpdate, usuario_id: int = None) -> Candidato:
    """Actualizar candidato."""
    candidato = base_service.get_by_id(db, candidato_id)
    data = payload.model_dump(exclude_unset=True)
    base_service._validate_foreign_keys(db, data)
    
    for field, value in data.items():
        setattr(candidato, field, value)
    
    db.commit()
    db.refresh(candidato)
    kafka_producer.send_candidato_updated(candidato.id, candidato.nombre, usuario_id)
    return candidato


def delete_candidato(db: Session, candidato_id: int, usuario_id: int = None) -> None:
    """Eliminar candidato."""
    candidato = base_service.delete(db, candidato_id)
    kafka_producer.send_candidato_deleted(candidato.id, candidato.nombre, usuario_id)