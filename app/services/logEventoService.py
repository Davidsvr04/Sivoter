from sqlalchemy.orm import Session
from app.models.logEvento import LogEvento


def save_log_evento(db: Session, evento: str, descripcion: str, usuario_id: int = None) -> LogEvento:
    """
    Guardar un evento de log en la base de datos.
    
    Args:
        db: Sesión de base de datos
        evento: Nombre del evento (ej: MESA_CREADA, CANDIDATO_ACTUALIZADO)
        descripcion: Descripción detallada del evento
        usuario_id: ID del usuario que realizó la acción (opcional)
    
    Returns:
        LogEvento: El registro creado
    """
    log = LogEvento(
        evento=evento,
        descripcion=descripcion,
        usuario_id=usuario_id
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_logs_eventos(db: Session, skip: int = 0, limit: int = 100):
    """Listar todos los logs de eventos con paginación."""
    return db.query(LogEvento).offset(skip).limit(limit).all()


def get_logs_by_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    """Obtener logs de un usuario específico."""
    return db.query(LogEvento).filter(LogEvento.usuario_id == usuario_id).offset(skip).limit(limit).all()


def get_logs_by_evento(db: Session, evento: str, skip: int = 0, limit: int = 100):
    """Obtener logs de un tipo de evento específico."""
    return db.query(LogEvento).filter(LogEvento.evento == evento).offset(skip).limit(limit).all()
