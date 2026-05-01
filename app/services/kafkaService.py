from kafka import KafkaProducer
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class KafkaEventProducer:
    """Servicio para enviar eventos a Kafka."""
    
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        """
        Inicializar el productor de Kafka.
        
        Args:
            bootstrap_servers: Dirección del servidor Kafka (default: localhost:9092)
        """
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("KafkaProducer inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando KafkaProducer: {e}")
            self.producer = None

    def send_event(self, topic: str, event: Dict[str, Any]) -> None:
        """
        Enviar un evento a Kafka.
        
        Args:
            topic: Nombre del topic de Kafka
            event: Diccionario con los datos del evento
        """
        if not self.producer:
            logger.warning(f"KafkaProducer no disponible, evento no enviado: {event}")
            return
        
        try:
            self.producer.send(topic, event)
            self.producer.flush()
            logger.info(f"Evento enviado a {topic}: {event}")
        except Exception as e:
            logger.error(f"Error enviando evento a Kafka: {e}")

    def send_generic_event(
        self,
        operacion: str,
        entidad_tipo: str,
        entidad_id: int,
        entidad_nombre: str,
        usuario_id: int = None,
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Enviar un evento genérico para cualquier entidad y operación.
        
        Args:
            operacion: Tipo de operación (CREADA, ACTUALIZADA, ELIMINADA, VOTÓ, etc.)
            entidad_tipo: Tipo de entidad (MESA, CANDIDATO, VOTACION, PARTIDO, BARRIO, etc.)
            entidad_id: ID de la entidad
            entidad_nombre: Nombre de la entidad
            usuario_id: ID del usuario que realizó la acción (opcional)
            metadata: Diccionario adicional con información extra (opcional)
        """
        evento = {
            "evento": f"{entidad_tipo}_{operacion}",
            "descripcion": f"{entidad_tipo.capitalize().replace('_', ' ')} '{entidad_nombre}' (ID: {entidad_id}) {operacion.lower()}",
            f"{entidad_tipo.lower()}_id": entidad_id,
            "usuario_id": usuario_id,
            "timestamp": str(__import__('datetime').datetime.now())
        }
        
        # Agregar metadata si se proporciona
        if metadata:
            evento.update(metadata)
        
        self.send_event('quickstart-events', evento)

    # Métodos específicos mantenidos por compatibilidad (pero ahora usan el método genérico)
    
    def send_mesa_created(self, mesa_id: int, mesa_nombre: str, usuario_id: int = None) -> None:
        """Registrar creación de mesa de votación."""
        self.send_generic_event("CREADA", "MESA", mesa_id, mesa_nombre, usuario_id)

    def send_mesa_updated(self, mesa_id: int, mesa_nombre: str, usuario_id: int = None) -> None:
        """Registrar actualización de mesa de votación."""
        self.send_generic_event("ACTUALIZADA", "MESA", mesa_id, mesa_nombre, usuario_id)

    def send_mesa_deleted(self, mesa_id: int, mesa_nombre: str, usuario_id: int = None) -> None:
        """Registrar eliminación de mesa de votación."""
        self.send_generic_event("ELIMINADA", "MESA", mesa_id, mesa_nombre, usuario_id)

    def send_candidato_created(self, candidato_id: int, candidato_nombre: str, usuario_id: int = None) -> None:
        """Registrar creación de candidato."""
        self.send_generic_event("CREADO", "CANDIDATO", candidato_id, candidato_nombre, usuario_id)

    def send_candidato_updated(self, candidato_id: int, candidato_nombre: str, usuario_id: int = None) -> None:
        """Registrar actualización de candidato."""
        self.send_generic_event("ACTUALIZADO", "CANDIDATO", candidato_id, candidato_nombre, usuario_id)

    def send_candidato_deleted(self, candidato_id: int, candidato_nombre: str, usuario_id: int = None) -> None:
        """Registrar eliminación de candidato."""
        self.send_generic_event("ELIMINADO", "CANDIDATO", candidato_id, candidato_nombre, usuario_id)

    def close(self) -> None:
        """Cerrar la conexión con Kafka."""
        if self.producer:
            try:
                self.producer.close()
                logger.info("KafkaProducer cerrado correctamente")
            except Exception as e:
                logger.error(f"Error cerrando KafkaProducer: {e}")


# Instancia global del productor
kafka_producer = KafkaEventProducer()
