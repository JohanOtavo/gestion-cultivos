"""Microservicio archivos imagenes.

Gestion de imagenes en Amazon S3 (soporte a RF33)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - archivos imagenes",
    description="Gestion de imagenes en Amazon S3 (soporte a RF33)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "archivos-imagenes", "estado": "operativo"}
