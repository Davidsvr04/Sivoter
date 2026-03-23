from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CandidatoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    partido_id: Optional[int] = None
    votacion_id: Optional[int] = None
    tipo_cargo_id: Optional[int] = None
    departamento_id: Optional[int] = None
    municipio_id: Optional[int] = None


class CandidatoCreate(CandidatoBase):
    pass


class CandidatoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    partido_id: Optional[int] = None
    votacion_id: Optional[int] = None
    tipo_cargo_id: Optional[int] = None
    departamento_id: Optional[int] = None
    municipio_id: Optional[int] = None
    votos: Optional[int] = Field(default=None, ge=0)


class CandidatoResponse(CandidatoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    votos: int