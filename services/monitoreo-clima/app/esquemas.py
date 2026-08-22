"""Esquemas de entrada y salida del servicio de monitoreo y clima."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RegistroBase(BaseModel):
    temperatura: float | None = Field(default=None, description="Grados centigrados")
    presion_atmosferica: float | None = Field(default=None, description="hPa")
    humedad: float | None = Field(default=None, ge=0, le=100, description="Porcentaje")
    precipitacion: float = Field(default=0.0, ge=0, description="Milimetros")
    indice_ultravioleta: float | None = Field(default=None, ge=0)
    horas_sol: float | None = Field(default=None, ge=0, le=24)


class RegistroCrear(RegistroBase):
    """Datos que se guardan al consultar el proveedor o al cargarlos a mano."""

    id_lote: int
    fecha: date


class RegistroRespuesta(RegistroBase):
    """Registro tal como lo devuelve la API (RF40)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    id_lote: int
    fecha: date
