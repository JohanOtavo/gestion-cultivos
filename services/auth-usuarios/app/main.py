"""Microservicio auth usuarios.

Autenticacion, usuarios, roles y permisos (RF62-RF69, RF82-RF91)
"""

from fastapi import FastAPI

app = FastAPI(
    title="Gestion de Cultivos - auth usuarios",
    description="Autenticacion, usuarios, roles y permisos (RF62-RF69, RF82-RF91)",
    version="0.1.0",
)


@app.get("/salud", tags=["salud"])
def verificar_estado():
    """Health check que usa Docker Compose antes de aceptar trafico (RF112)."""
    return {"servicio": "auth-usuarios", "estado": "operativo"}
