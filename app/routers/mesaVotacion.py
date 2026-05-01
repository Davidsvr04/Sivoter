from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.mesaVotacionSchema import MesaVotacionCreate, MesaVotacionUpdate, MesaVotacionResponse
from app.services.mesaVotacionService import (
    create_mesa_votacion,
    list_mesas_votacion,
    get_mesa_votacion,
    update_mesa_votacion,
    delete_mesa_votacion,
)

router = APIRouter(prefix="/mesas-votacion", tags=["Mesas de Votación"])


@router.post("", response_model=MesaVotacionResponse, status_code=status.HTTP_201_CREATED)
def create(payload: MesaVotacionCreate, usuario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Crear una nueva mesa de votación."""
    return create_mesa_votacion(db, payload, usuario_id)


@router.get("", response_model=List[MesaVotacionResponse])
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas las mesas de votación."""
    return list_mesas_votacion(db, skip=skip, limit=limit)


@router.get("/{mesa_id}", response_model=MesaVotacionResponse)
def get_one(mesa_id: int, db: Session = Depends(get_db)):
    """Obtener una mesa de votación por ID."""
    return get_mesa_votacion(db, mesa_id)


@router.put("/{mesa_id}", response_model=MesaVotacionResponse)
def update(mesa_id: int, payload: MesaVotacionUpdate, usuario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Actualizar una mesa de votación."""
    return update_mesa_votacion(db, mesa_id, payload, usuario_id)


@router.delete("/{mesa_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(mesa_id: int, usuario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Eliminar una mesa de votación."""
    delete_mesa_votacion(db, mesa_id, usuario_id)
    return None
