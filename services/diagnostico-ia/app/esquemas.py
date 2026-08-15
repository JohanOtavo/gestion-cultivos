"""Esquemas del servicio de diagnostico fitosanitario."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiagnosticoRespuesta(BaseModel):
    """Resultado que la interfaz muestra al usuario (RF33).

    El SRS exige devolver tres cosas junto a la imagen: que se detecto,
    con cuanta confianza y que se recomienda hacer.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    id_cultivo: int
    categoria: str = Field(description="plaga, enfermedad, maleza o deficiencia nutricional")
    resultado: str
    confianza: float = Field(ge=0, le=1, description="Probabilidad entregada por el modelo")
    recomendacion: str
    url_imagen: str
    fecha: datetime
