from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class MesaVotacionBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=200)
    barrio_id: int


class MesaVotacionCreate(MesaVotacionBase):
    pass


class MesaVotacionUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=200)
    barrio_id: Optional[int] = None


class MesaVotacionResponse(MesaVotacionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


