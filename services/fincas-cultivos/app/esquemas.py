"""Esquemas de entrada y salida del servicio de fincas."""

from pydantic import BaseModel, ConfigDict, Field


class FincaBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=120)
    ubicacion: str = Field(min_length=3, max_length=200)
    area_total: float = Field(gt=0, description="Area total expresada en la unidad elegida")
    unidad_area: str = Field(default="hectarea")


class FincaCrear(FincaBase):
    """Datos que envia el usuario para registrar una finca (RF1)."""

    id_propietario: int


class FincaActualizar(FincaBase):
    """Datos que se pueden modificar de una finca existente (RF3)."""


class FincaRespuesta(FincaBase):
    """Representacion de la finca que devuelve la API (RF2)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    id_propietario: int
    activa: bool
