"""Modelos del dominio de monitoreo y datos meteorologicos."""

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.base_datos import Base


class RegistroMeteorologico(Base):
    """Dato meteorologico diario de un lote (RF39).

    Se guarda un registro por lote y por dia. La restriccion de unicidad evita
    duplicados cuando la tarea programada se ejecuta dos veces el mismo dia,
    por ejemplo tras un reintento por falla del proveedor.
    """

    __tablename__ = "registros_meteorologicos"
    __table_args__ = (UniqueConstraint("id_lote", "fecha", name="uq_lote_fecha"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    id_lote: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    temperatura: Mapped[float] = mapped_column(Float, nullable=True)
    presion_atmosferica: Mapped[float] = mapped_column(Float, nullable=True)
    humedad: Mapped[float] = mapped_column(Float, nullable=True)
    precipitacion: Mapped[float] = mapped_column(Float, default=0.0)
    indice_ultravioleta: Mapped[float] = mapped_column(Float, nullable=True)
    horas_sol: Mapped[float] = mapped_column(Float, nullable=True)

    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
