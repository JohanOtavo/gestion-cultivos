"""Microservicio de fincas, lotes y cultivos.

Administra la estructura productiva del sistema: finca, lote y cultivo
(RF1 a RF13). Es la raiz de la que dependen los demas modulos, porque sin
finca no hay lote y sin lote no hay cultivo.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.base_datos import crear_tablas
from app.rutas import fincas


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    """Prepara las tablas al arrancar el contenedor, no al importar el modulo."""
    crear_tablas()
    yield


app = FastAPI(
    title="Gestion de Cultivos - fincas cultivos",
    description="Fincas, lotes y cultivos (RF1-RF13)",
    version="0.2.0",
    lifespan=ciclo_de_vida,
)

app.include_router(fincas.router)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "fincas-cultivos", "estado": "operativo"}
