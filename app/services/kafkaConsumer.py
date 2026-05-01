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
                value_deserializer=self._safe_deserialize,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                auto_commit_interval_ms=5000
            )
            logger.info(f"KafkaConsumer conectado a topics: {self.topics}")
            return True
        except Exception as e:
            logger.error(f"Error conectando KafkaConsumer: {e}")
            return False
    
    @staticmethod
    def _safe_deserialize(data):
        """Deserializar JSON de forma segura."""
        if not data:
            return None
        try:
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, AttributeError, UnicodeDecodeError) as e:
            logger.warning(f"Error deserializando mensaje: {e}, data: {data[:100]}")
            return None
    
    def process_message(self, message: dict) -> None:
        """
        Procesar un mensaje de Kafka y guardarlo en BD.
        
        Args:
            message: Diccionario con los datos del evento
        """
        if not message:
            logger.warning("Mensaje vacío o inválido recibido")
            return
        
        try:
            db = SessionLocal()
            
            evento = message.get('evento')
            descripcion = message.get('descripcion')
            usuario_id = message.get('usuario_id')
            
            if not evento or not descripcion:
                logger.warning(f"Mensaje incompleto (falta evento o descripción): {message}")
                db.close()
                return
            
            # Guardar en BD
            log = save_log_evento(db, evento, descripcion, usuario_id)
            logger.info(f"Log guardado: ID={log.id}, Evento={evento}, Usuario={usuario_id}")
            
            db.close()
        except Exception as e:
            logger.error(f"Error procesando mensaje de Kafka: {e}", exc_info=True)
            if 'db' in locals():
                db.close()
    
    def start(self) -> None:
        """Iniciar el consumer en un thread separado."""
        if not self.connect():
            logger.error("No se pudo conectar a Kafka")
            return
        
        def run():
            try:
                logger.info("Iniciando consumo de eventos Kafka...")
                for message in self.consumer:
                    try:
                        if message.value:
                            self.process_message(message.value)
                    except Exception as e:
                        logger.error(f"Error procesando mensaje individual: {e}")
                        continue
            except KeyboardInterrupt:
                logger.info("Consumer detenido manualmente")
            except Exception as e:
                logger.error(f"Error en consumer loop: {e}", exc_info=True)
            finally:
                try:
                    self.consumer.close()
                except:
                    pass
        
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
