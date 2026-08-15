"""Microservicio alertas notificaciones.

Alertas y notificaciones del sistema (RF70-RF73)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - alertas notificaciones",
    description="Alertas y notificaciones del sistema (RF70-RF73)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "alertas-notificaciones", "estado": "operativo"}
