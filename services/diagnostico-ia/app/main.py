"""Microservicio diagnostico ia.

Diagnostico fitosanitario con inteligencia artificial (RF33-RF38)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - diagnostico ia",
    description="Diagnostico fitosanitario con inteligencia artificial (RF33-RF38)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "diagnostico-ia", "estado": "operativo"}
