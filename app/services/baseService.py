from __future__ import annotations
from typing import TypeVar, overload
from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseService[T]:
    
    def __init__(self, model_class: type[T], fk_map: dict[str, str] | None = None):
        self.model_class = model_class
        self.fk_map = fk_map or {}
    
    def _exists(self, db: Session, table: str, value_id: int) -> bool:
        query = text(f"SELECT 1 FROM {table} WHERE id = :id LIMIT 1")
        row = db.execute(query, {"id": value_id}).first()
        return row is not None
    
    def _validate_foreign_keys(self, db: Session, data: dict[str, int | None]) -> None:
        for field, table in self.fk_map.items():
            value = data.get(field)
            if value is not None and not self._exists(db, table, value):
                raise HTTPException(
                    status_code=400,
                    detail=f"El valor {value} de '{field}' no existe en '{table}'."
                )
    
    def list_all[U: T](self, db: Session, skip: int = 0, limit: int = 100) -> Sequence[U]:
        return db.query(self.model_class).offset(skip).limit(limit).all()
    
    def get_by_id[U: T](self, db: Session, entity_id: int) -> U:
        entity = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if not entity:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model_class.__name__} con ID {entity_id} no encontrado."
            )
        return entity
    
    def delete[U: T](self, db: Session, entity_id: int) -> U:
        entity = self.get_by_id(db, entity_id)
        db.delete(entity)
        db.commit()
        return entity