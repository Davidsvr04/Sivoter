from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.candidatos import Candidato
from app.schemas.candidatoSchema import CandidatoCreate, CandidatoUpdate
from app.services.kafkaService import kafka_producer


FK_MAP = {
    "partido_id": "partidos",
    "votacion_id": "votaciones",
    "tipo_cargo_id": "tipo_cargo",
    "departamento_id": "departamentos",
    "municipio_id": "municipios",
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


def create_candidato(db: Session, payload: CandidatoCreate, usuario_id: int = None) -> Candidato:
    data = payload.model_dump()
    _validate_foreign_keys(db, data)

    candidato = Candidato(**data)
    db.add(candidato)
    db.commit()
    db.refresh(candidato)
    
    # Registrar en Kafka
    kafka_producer.send_candidato_created(candidato.id, candidato.nombre, usuario_id)
    
    return candidato


def list_candidatos(db: Session, skip: int = 0, limit: int = 100) -> List[Candidato]:
    return db.query(Candidato).offset(skip).limit(limit).all()


def get_candidato(db: Session, candidato_id: int) -> Candidato:
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado.")
    return candidato


def update_candidato(db: Session, candidato_id: int, payload: CandidatoUpdate, usuario_id: int = None) -> Candidato:
    candidato = get_candidato(db, candidato_id)
    update_data = payload.model_dump(exclude_unset=True)

    _validate_foreign_keys(db, update_data)

    for field, value in update_data.items():
        setattr(candidato, field, value)

    db.commit()
    db.refresh(candidato)
    
    # Registrar en Kafka
    kafka_producer.send_candidato_updated(candidato.id, candidato.nombre, usuario_id)
    
    return candidato


def delete_candidato(db: Session, candidato_id: int, usuario_id: int = None) -> None:
    candidato = get_candidato(db, candidato_id)
    candidato_nombre = candidato.nombre
    
    db.delete(candidato)
    db.commit()
    
    # Registrar en Kafka
    kafka_producer.send_candidato_deleted(candidato_id, candidato_nombre, usuario_id)