"""Microservicio fincas cultivos.

Fincas, lotes y cultivos (RF1-RF13)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - fincas cultivos",
    description="Fincas, lotes y cultivos (RF1-RF13)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "fincas-cultivos", "estado": "operativo"}
