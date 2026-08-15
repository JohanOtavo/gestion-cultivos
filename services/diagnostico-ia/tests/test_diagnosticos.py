"""Pruebas del endpoint de diagnostico fitosanitario (RF33 y RF36)."""

import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app  # noqa: E402

IMAGEN = ("hoja.jpg", b"contenido-de-prueba", "image/jpeg")


@pytest.fixture
def cliente():
    return TestClient(app)


def test_diagnostico_devuelve_resultado_confianza_y_recomendacion(cliente):
    respuesta = cliente.post("/diagnosticos", params={"id_cultivo": 1}, files={"imagen": IMAGEN})

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["categoria"] in (
        "plaga",
        "enfermedad",
        "maleza",
        "deficiencia nutricional",
    )
    assert 0 <= cuerpo["confianza"] <= 1
    assert cuerpo["recomendacion"]


def test_rechaza_archivos_que_no_son_imagen(cliente):
    respuesta = cliente.post(
        "/diagnosticos",
        params={"id_cultivo": 1},
        files={"imagen": ("reporte.pdf", b"%PDF-1.4", "application/pdf")},
    )

    assert respuesta.status_code == 415


def test_el_historial_solo_trae_los_del_cultivo_consultado(cliente):
    cliente.post("/diagnosticos", params={"id_cultivo": 7}, files={"imagen": IMAGEN})
    cliente.post("/diagnosticos", params={"id_cultivo": 8}, files={"imagen": IMAGEN})

    respuesta = cliente.get("/diagnosticos", params={"id_cultivo": 7})

    assert respuesta.status_code == 200
    assert all(d["id_cultivo"] == 7 for d in respuesta.json())
