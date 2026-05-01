from kafka import KafkaConsumer
import json
import logging
from threading import Thread
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database.connection import engine
from app.services.logEventoService import save_log_evento

logger = logging.getLogger(__name__)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class KafkaEventConsumer:
    """Consumer de Kafka que escucha eventos y los guarda en BD."""
    
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        """
        Inicializar el consumer de Kafka.
        
        Args:
            bootstrap_servers: Dirección del servidor Kafka
        """
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.topics = ['quickstart-events']
        
    def connect(self) -> bool:
        """Conectar a Kafka."""
        try:
            self.consumer = KafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id='sivoter-logs-group',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            logger.info(f"KafkaConsumer conectado a topics: {self.topics}")
            return True
        except Exception as e:
            logger.error(f"Error conectando KafkaConsumer: {e}")
            return False
    
    def process_message(self, message: dict) -> None:
        """
        Procesar un mensaje de Kafka y guardarlo en BD.
        
        Args:
            message: Diccionario con los datos del evento
        """
        try:
            db = SessionLocal()
            
            evento = message.get('evento')
            descripcion = message.get('descripcion')
            usuario_id = message.get('usuario_id')
            
            if not evento or not descripcion:
                logger.warning(f"Mensaje inválido: {message}")
                return
            
            # Guardar en BD
            log = save_log_evento(db, evento, descripcion, usuario_id)
            logger.info(f"Log guardado: ID={log.id}, Evento={evento}, Usuario={usuario_id}")
            
            db.close()
        except Exception as e:
            logger.error(f"Error procesando mensaje de Kafka: {e}")
    
    def start(self) -> None:
        """Iniciar el consumer en un thread separado."""
        if not self.connect():
            logger.error("No se pudo conectar a Kafka")
            return
        
        def run():
            try:
                logger.info("Iniciando consumo de eventos Kafka...")
                for message in self.consumer:
                    if message.value:
                        self.process_message(message.value)
            except Exception as e:
                logger.error(f"Error en consumer loop: {e}")
            finally:
                self.consumer.close()
        
        # Ejecutar en un thread daemon
        thread = Thread(target=run, daemon=True)
        thread.start()
        logger.info("Consumer thread iniciado en background")
    
    def close(self) -> None:
        """Cerrar la conexión con Kafka."""
        if self.consumer:
            try:
                self.consumer.close()
                logger.info("KafkaConsumer cerrado")
            except Exception as e:
                logger.error(f"Error cerrando KafkaConsumer: {e}")


# Instancia global del consumer
kafka_consumer = KafkaEventConsumer()
