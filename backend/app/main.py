from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine, get_db
from app.routers import jugadores, campeonatos, partidas, resultados
from typing import List
from app.models.jugador import Pareja
from app.schemas.jugador import ParejaSchema
from sqlalchemy.orm import Session, registry
import logging

mapper_registry = registry()
mapper_registry.configure()

app = FastAPI()

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
app.include_router(resultados.router, prefix="/api/resultados", tags=["resultados"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Campeonato de Dominó"}

@app.middleware("http")
async def log_requests(request, call_next):
    logging.info(f"Solicitud recibida: {request.method} {request.url}")
    response = await call_next(request)
    return response


