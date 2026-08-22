"""Configuracion de las pruebas del servicio de monitoreo y clima.

Las pruebas corren contra SQLite en memoria para que el pipeline no dependa de
PostgreSQL ni de una conexion real con el proveedor meteorologico.
"""

import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.base_datos import Base, obtener_sesion  # noqa: E402
from app.main import app  # noqa: E402

motor_pruebas = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SesionPrueba = sessionmaker(bind=motor_pruebas)


@pytest.fixture
def cliente():
    Base.metadata.create_all(bind=motor_pruebas)

    def sesion_de_prueba():
        sesion = SesionPrueba()
        try:
            yield sesion
        finally:
            sesion.close()

    app.dependency_overrides[obtener_sesion] = sesion_de_prueba
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=motor_pruebas)
