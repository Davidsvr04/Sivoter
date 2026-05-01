from __future__ import annotations
from collections.abc import Sequence
from sqlalchemy.orm import Session

from app.models.mesaVotacion import MesaVotacion
from app.schemas.mesaVotacionSchema import MesaVotacionCreate, MesaVotacionUpdate
from app.services.kafkaService import kafka_producer
from app.services.baseService import BaseService

FK_MAP = {"barrio_id": "barrios"}
base_service = BaseService(MesaVotacion, FK_MAP)


def create_mesa_votacion(db: Session, payload: MesaVotacionCreate, usuario_id: int = None) -> MesaVotacion:
    """Crear una nueva mesa de votación."""
    data = payload.model_dump()
    base_service._validate_foreign_keys(db, data)

    mesa = MesaVotacion(**data)
    db.add(mesa)
    db.commit()
    db.refresh(mesa)
    
    kafka_producer.send_mesa_created(mesa.id, mesa.nombre, usuario_id)
    return mesa


def list_mesas_votacion(db: Session, skip: int = 0, limit: int = 100) -> Sequence[MesaVotacion]:
    """Listar todas las mesas de votación."""
    return base_service.list_all(db, skip, limit)


def get_mesa_votacion(db: Session, mesa_id: int) -> MesaVotacion:
    """Obtener una mesa de votación por ID."""
    return base_service.get_by_id(db, mesa_id)


def update_mesa_votacion(db: Session, mesa_id: int, payload: MesaVotacionUpdate, usuario_id: int = None) -> MesaVotacion:
    """Actualizar una mesa de votación."""
    mesa = base_service.get_by_id(db, mesa_id)
    data = payload.model_dump(exclude_unset=True)
    base_service._validate_foreign_keys(db, data)
    
    for field, value in data.items():
        setattr(mesa, field, value)
    
    db.commit()
    db.refresh(mesa)
    kafka_producer.send_mesa_updated(mesa.id, mesa.nombre, usuario_id)
    return mesa


def delete_mesa_votacion(db: Session, mesa_id: int, usuario_id: int = None) -> None:
    """Eliminar una mesa de votación."""
    mesa = base_service.delete(db, mesa_id)
    kafka_producer.send_mesa_deleted(mesa.id, mesa.nombre, usuario_id)