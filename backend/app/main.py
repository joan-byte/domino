from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import jugadores, campeonatos, partidas, resultados, mesas

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir los routers
app.include_router(jugadores.router, prefix="/api", tags=["jugadores"])
app.include_router(campeonatos.router, prefix="/api/campeonatos", tags=["campeonatos"])
app.include_router(partidas.router, prefix="/api/partidas", tags=["partidas"])
app.include_router(resultados.router, prefix="/api/resultados", tags=["resultados"])
app.include_router(mesas.router, prefix="/api/mesas", tags=["mesas"])

@app.get("/")
def read_root():
    return {"Hello": "World"}




