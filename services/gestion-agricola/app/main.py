"""Microservicio gestion agricola.

Catalogos: variedades, insumos, maquinaria y etapas (RF74-RF81)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - gestion agricola",
    description="Catalogos: variedades, insumos, maquinaria y etapas (RF74-RF81)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "gestion-agricola", "estado": "operativo"}
