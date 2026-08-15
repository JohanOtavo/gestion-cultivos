"""Conexion con PostgreSQL mediante SQLAlchemy.

Cada microservicio accede unicamente a las entidades de su propio dominio
funcional, tal como lo define el SRS para la arquitectura de microservicios.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

URL_BASE_DATOS = os.getenv(
    "URL_BASE_DATOS",
    "postgresql+psycopg2://{usuario}:{clave}@{host}:{puerto}/{base}".format(
        usuario=os.getenv("POSTGRES_USER", "postgres"),
        clave=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "db"),
        puerto=os.getenv("POSTGRES_PORT", "5432"),
        base=os.getenv("POSTGRES_DB", "gestion_cultivos"),
    ),
)

motor = create_engine(URL_BASE_DATOS, pool_pre_ping=True)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos del servicio."""


def obtener_sesion():
    """Entrega una sesion por solicitud y la cierra al terminar."""
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
