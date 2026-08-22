"""Microservicio de monitoreo y datos meteorologicos.

Guarda los seguimientos de campo y el registro diario de variables
meteorologicas obtenidas del proveedor externo (RF20-RF24, RF39-RF42).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.base_datos import crear_tablas
from app.rutas import clima


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    """Prepara las tablas al arrancar el contenedor, no al importar el modulo."""
    crear_tablas()
    yield


app = FastAPI(
    title="Gestion de Cultivos - monitoreo clima",
    description="Monitoreo, analisis edafologico y datos meteorologicos (RF20-RF24, RF39-RF42)",
    version="0.2.0",
    lifespan=ciclo_de_vida,
)

app.include_router(clima.router)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "monitoreo-clima", "estado": "operativo"}
