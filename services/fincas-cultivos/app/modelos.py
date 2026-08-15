"""Modelos del dominio de fincas, lotes y cultivos."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos import Base


class Finca(Base):
    """Unidad productiva registrada por un usuario (RF1).

    El nombre es unico porque el requerimiento exige que no se creen fincas
    duplicadas para el mismo propietario.
    """

    __tablename__ = "fincas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(200), nullable=False)
    area_total: Mapped[float] = mapped_column(Float, nullable=False)
    unidad_area: Mapped[str] = mapped_column(String(20), default="hectarea")
    id_propietario: Mapped[int] = mapped_column(nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    lotes: Mapped[list["Lote"]] = relationship(back_populates="finca")


class Lote(Base):
    """Subdivision de una finca sobre la que se siembra un cultivo (RF5)."""

    __tablename__ = "lotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    area: Mapped[float] = mapped_column(Float, nullable=False)
    unidad_area: Mapped[str] = mapped_column(String(20), default="hectarea")
    latitud: Mapped[float] = mapped_column(Float, nullable=True)
    longitud: Mapped[float] = mapped_column(Float, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    id_finca: Mapped[int] = mapped_column(ForeignKey("fincas.id"), nullable=False)

    finca: Mapped["Finca"] = relationship(back_populates="lotes")
