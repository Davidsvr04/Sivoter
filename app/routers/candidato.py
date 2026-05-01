from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.candidatoSchema import CandidatoCreate, CandidatoUpdate, CandidatoResponse
from app.services.candidatoService import (
    create_candidato,
    list_candidatos,
    get_candidato,
    update_candidato,
    delete_candidato,
)

router = APIRouter(prefix="/candidatos", tags=["Candidatos"])


@router.post("", response_model=CandidatoResponse, status_code=status.HTTP_201_CREATED)
def create(payload: CandidatoCreate, usuario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    return create_candidato(db, payload, usuario_id)


@router.get("", response_model=List[CandidatoResponse])
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_candidatos(db, skip=skip, limit=limit)


@router.get("/{candidato_id}", response_model=CandidatoResponse)
def get_one(candidato_id: int, db: Session = Depends(get_db)):
    return get_candidato(db, candidato_id)


@router.put("/{candidato_id}", response_model=CandidatoResponse)
def update(candidato_id: int, payload: CandidatoUpdate, usuario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    return update_candidato(db, candidato_id, payload, usuario_id)


@router.delete("/{candidato_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(candidato_id: int, usuario_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    delete_candidato(db, candidato_id, usuario_id)
    return None