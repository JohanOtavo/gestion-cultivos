"""Conexion con PostgreSQL mediante SQLAlchemy.

Cada microservicio accede unicamente a las entidades de su propio dominio
funcional, tal como lo define el SRS para la arquitectura de microservicios.

El motor se construye de forma perezosa: solo se crea la primera vez que
alguien lo pide. Asi las pruebas pueden sustituir la sesion sin necesidad
de tener instalado el driver de PostgreSQL ni una base de datos levantada.
"""

import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos del servicio."""


def construir_url() -> str:
    """Arma la cadena de conexion a partir de las variables de entorno (RF111)."""
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
    """Crea el motor una sola vez por proceso."""
    return create_engine(construir_url(), pool_pre_ping=True)


@lru_cache
def obtener_fabrica_sesiones():
    return sessionmaker(autocommit=False, autoflush=False, bind=obtener_motor())


def obtener_sesion():
    """Entrega una sesion por solicitud y la cierra al terminar."""
    sesion = obtener_fabrica_sesiones()()
    try:
        yield sesion
    finally:
        sesion.close()


def crear_tablas() -> None:
    """Crea las tablas del dominio al arrancar el servicio."""
    Base.metadata.create_all(bind=obtener_motor())
