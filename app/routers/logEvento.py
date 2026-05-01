from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.logEvento import LogEvento
from app.services.logEventoService import (
    list_logs_eventos,
    get_logs_by_usuario,
    get_logs_by_evento,
)

router = APIRouter(prefix="/logs-eventos", tags=["Logs de Eventos"])


@router.get("", response_model=List[dict])
def get_all_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los logs de eventos."""
    logs = list_logs_eventos(db, skip=skip, limit=limit)
    return [
        {
            "id": log.id,
            "evento": log.evento,
            "descripcion": log.descripcion,
            "usuario_id": log.usuario_id,
            "fecha": log.fecha
        }
        for log in logs
    ]


@router.get("/usuario/{usuario_id}", response_model=List[dict])
def get_logs_user(usuario_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener logs de un usuario específico."""
    logs = get_logs_by_usuario(db, usuario_id, skip=skip, limit=limit)
    return [
        {
            "id": log.id,
            "evento": log.evento,
            "descripcion": log.descripcion,
            "usuario_id": log.usuario_id,
            "fecha": log.fecha
        }
        for log in logs
    ]


@router.get("/evento/{evento}", response_model=List[dict])
def get_logs_event(evento: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener logs de un tipo de evento específico."""
    logs = get_logs_by_evento(db, evento, skip=skip, limit=limit)
    return [
        {
            "id": log.id,
            "evento": log.evento,
            "descripcion": log.descripcion,
            "usuario_id": log.usuario_id,
            "fecha": log.fecha
        }
        for log in logs
    ]
