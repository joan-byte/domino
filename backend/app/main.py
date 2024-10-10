from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine, get_db
from app.routers import jugadores, campeonatos, partidas, resultados
from typing import List
from app.models.jugador import Pareja
from app.schemas.jugador import ParejaSchema
from sqlalchemy.orm import Session

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(jugadores.router, prefix="/api", tags=["jugadores"])
app.include_router(campeonatos.router, prefix="/api/campeonatos", tags=["campeonatos"])
app.include_router(partidas.router, prefix="/api")
app.include_router(resultados.router, prefix="/api", tags=["resultados"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Campeonato de Dominó"}
