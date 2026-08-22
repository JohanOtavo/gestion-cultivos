"""Pruebas del cliente de OpenWeather (RF39)."""

import os
import sys

import httpx
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.clientes.openweather import ClienteOpenWeather, ErrorOpenWeather  # noqa: E402

RESPUESTA = {
    "main": {"temp": 26.5, "pressure": 1010, "humidity": 74},
    "rain": {"1h": 2.5},
    "sys": {"sunrise": 1_700_000_000, "sunset": 1_700_043_200},
}


def test_normaliza_las_variables_del_requerimiento():
    datos = ClienteOpenWeather._normalizar(RESPUESTA)

    assert datos["temperatura"] == 26.5
    assert datos["humedad"] == 74
    assert datos["precipitacion"] == 2.5
    assert datos["horas_sol"] == 12.0


def test_sin_lluvia_la_precipitacion_es_cero():
    datos = ClienteOpenWeather._normalizar({"main": {"temp": 20}})

    assert datos["precipitacion"] == 0.0
    assert datos["horas_sol"] is None


def test_reintenta_y_avisa_cuando_el_proveedor_falla(monkeypatch):
    intentos = {"n": 0}

    def fallar(*args, **kwargs):
        intentos["n"] += 1
        raise httpx.ConnectError("sin conexion")

    monkeypatch.setattr(httpx, "get", fallar)

    with pytest.raises(ErrorOpenWeather):
        ClienteOpenWeather(clave="prueba").consultar(2.9, -75.3)

    assert intentos["n"] == 3
