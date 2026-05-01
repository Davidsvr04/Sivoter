from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import settings
from app.database.connection import engine
from app.routers import candidato, mesaVotacion


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

@app.on_event("startup")
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Conexión exitosa a PostgreSQL")
    except Exception as e:
        print("Error de conexión:", e)