"""Endpoints del diagnostico fitosanitario (RF33 y RF36)."""

from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.esquemas import DiagnosticoRespuesta
from app.modelo_vision import obtener_modelo

router = APIRouter(prefix="/diagnosticos", tags=["diagnostico fitosanitario"])

FORMATOS_ACEPTADOS = {"image/jpeg", "image/png"}
TAMANO_MAXIMO_MB = 8

# Almacen temporal en memoria hasta conectar el microservicio de archivos.
_historial: list[dict] = []


@router.post("", response_model=DiagnosticoRespuesta, status_code=status.HTTP_201_CREATED)
async def diagnosticar(id_cultivo: int, imagen: UploadFile = File(...)):
    """Recibe una imagen del cultivo y devuelve el diagnostico (RF33).

    La imagen puede venir de un archivo del dispositivo o de la camara; el
    servicio no distingue entre las dos, solo valida formato y tamano.
    """
    if imagen.content_type not in FORMATOS_ACEPTADOS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Solo se aceptan imagenes en formato JPEG o PNG",
        )

    contenido = await imagen.read()
    if len(contenido) > TAMANO_MAXIMO_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"La imagen supera el limite de {TAMANO_MAXIMO_MB} MB",
        )

    modelo = obtener_modelo()
    categoria, resultado, confianza = modelo.predecir(contenido)

    diagnostico = {
        "id": len(_historial) + 1,
        "id_cultivo": id_cultivo,
        "categoria": categoria,
        "resultado": resultado,
        "confianza": confianza,
        "recomendacion": modelo.recomendacion_para(categoria),
        "url_imagen": f"s3://diagnosticos/{imagen.filename}",
        "fecha": datetime.now(timezone.utc),
    }
    _historial.append(diagnostico)
    return diagnostico


@router.get("", response_model=list[DiagnosticoRespuesta])
def consultar_historial(id_cultivo: int):
    """Lista los diagnosticos realizados sobre un cultivo (RF36)."""
    return [d for d in _historial if d["id_cultivo"] == id_cultivo]
