"""Microservicio reportes analitica.

Reportes, presupuesto y recomendaciones (RF19, RF47-RF61)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - reportes analitica",
    description="Reportes, presupuesto y recomendaciones (RF19, RF47-RF61)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "reportes-analitica", "estado": "operativo"}
