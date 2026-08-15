"""Microservicio monitoreo clima.

Monitoreo, analisis edafologico y datos meteorologicos (RF20-RF24, RF39-RF42)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - monitoreo clima",
    description="Monitoreo, analisis edafologico y datos meteorologicos (RF20-RF24, RF39-RF42)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "monitoreo-clima", "estado": "operativo"}
