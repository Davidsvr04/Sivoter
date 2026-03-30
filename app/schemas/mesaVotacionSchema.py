from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class MesaVotacionBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=200)
    municipio_id: int
    barrio_id: Optional[int] = None
    numero_mesa: Optional[int] = Field(default=None, gt=0)


class MesaVotacionCreate(MesaVotacionBase):
    pass


class MesaVotacionUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=200)
    municipio_id: Optional[int] = None
    barrio_id: Optional[int] = None
    numero_mesa: Optional[int] = Field(default=None, gt=0)


class MesaVotacionResponse(MesaVotacionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
