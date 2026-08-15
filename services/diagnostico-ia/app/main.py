"""Microservicio de diagnostico fitosanitario.

Procesa las imagenes cargadas desde archivo o camara y devuelve el
resultado, el porcentaje de confianza y la recomendacion tecnica
(RF33 a RF38).
"""

from fastapi import FastAPI

from app.rutas import diagnosticos

app = FastAPI(
    title="Gestion de Cultivos - diagnostico ia",
    description="Diagnostico fitosanitario con inteligencia artificial (RF33-RF38)",
    version="0.2.0",
)

app.include_router(diagnosticos.router)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "diagnostico-ia", "estado": "operativo"}
