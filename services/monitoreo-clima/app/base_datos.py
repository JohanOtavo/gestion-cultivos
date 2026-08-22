"""Conexion con PostgreSQL para el dominio de monitoreo y clima.

El motor se construye de forma perezosa para que las pruebas puedan sustituir
la sesion sin necesidad del driver de PostgreSQL ni de una base levantada.
"""

import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Clase base de la que heredan los modelos del servicio."""


def construir_url() -> str:
    """Arma la cadena de conexion desde las variables de entorno (RF111)."""
    url_directa = os.getenv("URL_BASE_DATOS")
    if url_directa:
        return url_directa

    return "postgresql+psycopg2://{usuario}:{clave}@{host}:{puerto}/{base}".format(
        usuario=os.getenv("POSTGRES_USER", "postgres"),
        clave=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "db"),
        puerto=os.getenv("POSTGRES_PORT", "5432"),
        base=os.getenv("POSTGRES_DB", "gestion_cultivos"),
    )


@lru_cache
def obtener_motor():
    return create_engine(construir_url(), pool_pre_ping=True)


@lru_cache
def obtener_fabrica_sesiones():
    return sessionmaker(autocommit=False, autoflush=False, bind=obtener_motor())


def obtener_sesion():
    sesion = obtener_fabrica_sesiones()()
    try:
        yield sesion
    finally:
        sesion.close()


def crear_tablas() -> None:
    Base.metadata.create_all(bind=obtener_motor())
