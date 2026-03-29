from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class MesaVotacionBase(BaseModel):
    departamento: str = Field(..., min_length=1, max_length=100)
    municipio: str = Field(..., min_length=1, max_length=100)
    barrio: str = Field(..., min_length=1, max_length=100)
    nombre_lugar: str = Field(..., min_length=1, max_length=150)
    numero_mesa: int = Field(..., gt=0)


class MesaVotacionCreate(MesaVotacionBase):
    pass


class MesaVotacionUpdate(BaseModel):
    departamento: Optional[str] = Field(default=None, min_length=1, max_length=100)
    municipio: Optional[str] = Field(default=None, min_length=1, max_length=100)
    barrio: Optional[str] = Field(default=None, min_length=1, max_length=100)
    nombre_lugar: Optional[str] = Field(default=None, min_length=1, max_length=150)
    numero_mesa: Optional[int] = Field(default=None, gt=0)


class MesaVotacionResponse(MesaVotacionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
