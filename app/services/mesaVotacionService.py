from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.mesaVotacion import MesaVotacion
from app.schemas.mesaVotacionSchema import MesaVotacionCreate, MesaVotacionUpdate


FK_MAP = {
    "municipio_id": "municipios",
    "barrio_id": "barrios",
}


def _exists(db: Session, table: str, value_id: int) -> bool:
    query = text(f"SELECT 1 FROM {table} WHERE id = :id LIMIT 1")
    row = db.execute(query, {"id": value_id}).first()
    return row is not None


def _validate_foreign_keys(db: Session, data: dict) -> None:
    for field, table in FK_MAP.items():
        value = data.get(field)
        if value is not None and not _exists(db, table, value):
            raise HTTPException(
                status_code=400,
                detail=f"El valor {value} de '{field}' no existe en '{table}'."
            )


def create_mesa_votacion(db: Session, payload: MesaVotacionCreate) -> MesaVotacion:
    """Crear una nueva mesa de votación (lugar de votación)."""
    data = payload.model_dump()
    _validate_foreign_keys(db, data)

    mesa = MesaVotacion(**data)
    db.add(mesa)
    db.commit()
    db.refresh(mesa)
    return mesa


def list_mesas_votacion(db: Session, skip: int = 0, limit: int = 100) -> List[MesaVotacion]:
    """Listar todas las mesas de votación con paginación."""
    return db.query(MesaVotacion).offset(skip).limit(limit).all()


def get_mesa_votacion(db: Session, mesa_id: int) -> MesaVotacion:
    """Obtener una mesa de votación por ID."""
    mesa = db.query(MesaVotacion).filter(MesaVotacion.id == mesa_id).first()
    if not mesa:
        raise HTTPException(
            status_code=404,
            detail=f"Mesa de votación con ID {mesa_id} no encontrada."
        )
    return mesa


def update_mesa_votacion(db: Session, mesa_id: int, payload: MesaVotacionUpdate) -> MesaVotacion:
    """Actualizar una mesa de votación."""
    mesa = get_mesa_votacion(db, mesa_id)
    
    data = payload.model_dump(exclude_unset=True)
    _validate_foreign_keys(db, data)
    
    for field, value in data.items():
        setattr(mesa, field, value)
    
    db.commit()
    db.refresh(mesa)
    return mesa


def delete_mesa_votacion(db: Session, mesa_id: int) -> None:
    """Eliminar una mesa de votación."""
    mesa = get_mesa_votacion(db, mesa_id)
    db.delete(mesa)
    db.commit()
