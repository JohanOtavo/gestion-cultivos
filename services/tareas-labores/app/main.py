"""Microservicio tareas labores.

Tareas y labores culturales del cultivo (RF25-RF32, RF43-RF46)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - tareas labores",
    description="Tareas y labores culturales del cultivo (RF25-RF32, RF43-RF46)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "tareas-labores", "estado": "operativo"}
