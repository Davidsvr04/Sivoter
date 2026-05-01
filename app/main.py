from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import settings
from app.database.connection import engine
from app.routers import candidato, mesaVotacion, logEvento
from app.services.kafkaConsumer import kafka_consumer


app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Corriendo API Sivoter",
    }

app.include_router(candidato.router)
app.include_router(mesaVotacion.router)
app.include_router(logEvento.router)

@app.on_event("startup")
def startup_event():
    """Ejecutar al iniciar la aplicación."""
    # Test de conexión a BD
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Conexión exitosa a PostgreSQL")
    except Exception as e:
        print("Error de conexión:", e)
    
    # Iniciar consumer de Kafka
    try:
        kafka_consumer.start()
        print("Kafka Consumer iniciado")
    except Exception as e:
        print(f"Error iniciando Kafka Consumer: {e}")

@app.on_event("shutdown")
def shutdown_event():
    """Ejecutar al cerrar la aplicación."""
    try:
        kafka_consumer.close()
        print("Kafka Consumer cerrado")
    except Exception as e:
        print(f"Error cerrando Kafka Consumer: {e}")