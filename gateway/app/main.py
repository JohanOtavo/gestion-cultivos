"""API Gateway del sistema Gestion de Cultivos (RF106).

Unico punto de entrada de la aplicacion web. Enruta cada solicitud hacia el
microservicio del dominio correspondiente por la red interna de Docker, de modo
que los servicios no quedan expuestos hacia el exterior (RF110).
"""

import os

import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI(title="Gestion de Cultivos - API Gateway", version="0.1.0")

# Cada prefijo publico apunta al nombre del contenedor dentro de la red interna.
RUTAS = {
    "auth": os.getenv("URL_AUTH", "http://auth-usuarios:8001"),
    "fincas": os.getenv("URL_FINCAS", "http://fincas-cultivos:8002"),
    "agricola": os.getenv("URL_AGRICOLA", "http://gestion-agricola:8003"),
    "tareas": os.getenv("URL_TAREAS", "http://tareas-labores:8004"),
    "monitoreo": os.getenv("URL_MONITOREO", "http://monitoreo-clima:8005"),
    "diagnostico": os.getenv("URL_DIAGNOSTICO", "http://diagnostico-ia:8006"),
    "reportes": os.getenv("URL_REPORTES", "http://reportes-analitica:8007"),
    "alertas": os.getenv("URL_ALERTAS", "http://alertas-notificaciones:8008"),
    "archivos": os.getenv("URL_ARCHIVOS", "http://archivos-imagenes:8009"),
}


@app.get("/salud", tags=["salud"])
def verificar_estado():
    return {"servicio": "api-gateway", "estado": "operativo"}


@app.api_route("/api/{dominio}/{ruta:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def redirigir(dominio: str, ruta: str, request: Request):
    """Reenvia la solicitud al microservicio dueno del dominio funcional."""
    destino = RUTAS.get(dominio)
    if destino is None:
        return Response(content=f"Dominio no registrado: {dominio}", status_code=404)

    async with httpx.AsyncClient(timeout=30) as cliente:
        respuesta = await cliente.request(
            method=request.method,
            url=f"{destino}/{ruta}",
            content=await request.body(),
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            params=request.query_params,
        )

    return Response(
        content=respuesta.content,
        status_code=respuesta.status_code,
        media_type=respuesta.headers.get("content-type"),
    )
