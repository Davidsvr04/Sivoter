from typing import List
from fastapi import APIRouter, Depends, status
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
def create(payload: CandidatoCreate, db: Session = Depends(get_db)):
    return create_candidato(db, payload)


@router.get("", response_model=List[CandidatoResponse])
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_candidatos(db, skip=skip, limit=limit)


@router.get("/{candidato_id}", response_model=CandidatoResponse)
def get_one(candidato_id: int, db: Session = Depends(get_db)):
    return get_candidato(db, candidato_id)


@router.put("/{candidato_id}", response_model=CandidatoResponse)
def update(candidato_id: int, payload: CandidatoUpdate, db: Session = Depends(get_db)):
    return update_candidato(db, candidato_id, payload)


@router.delete("/{candidato_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(candidato_id: int, db: Session = Depends(get_db)):
    delete_candidato(db, candidato_id)
    return None