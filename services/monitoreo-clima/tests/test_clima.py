"""Pruebas del registro y consulta de datos meteorologicos (RF39, RF40, RF42)."""

from datetime import date, timedelta

REGISTRO = {
    "id_lote": 1,
    "fecha": "2026-08-10",
    "temperatura": 27.4,
    "presion_atmosferica": 1012,
    "humedad": 78,
    "precipitacion": 3.2,
    "indice_ultravioleta": 8.1,
    "horas_sol": 11.5,
}


def test_registrar_dato_manual(cliente):
    respuesta = cliente.post("/clima", json=REGISTRO)

    assert respuesta.status_code == 201
    assert respuesta.json()["temperatura"] == 27.4
    assert respuesta.json()["horas_sol"] == 11.5


def test_no_permite_dos_registros_del_mismo_dia_y_lote(cliente):
    cliente.post("/clima", json=REGISTRO)

    respuesta = cliente.post("/clima", json=REGISTRO)

    assert respuesta.status_code == 409


def test_rechaza_humedad_fuera_de_rango(cliente):
    respuesta = cliente.post("/clima", json={**REGISTRO, "humedad": 140})

    assert respuesta.status_code == 422


def test_rechaza_precipitacion_negativa(cliente):
    respuesta = cliente.post("/clima", json={**REGISTRO, "precipitacion": -5})

    assert respuesta.status_code == 422


def test_historico_solo_devuelve_el_lote_consultado(cliente):
    cliente.post("/clima", json=REGISTRO)
    cliente.post("/clima", json={**REGISTRO, "id_lote": 2})

    respuesta = cliente.get("/clima/lotes/1")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["id_lote"] == 1


def test_historico_respeta_el_rango_de_fechas(cliente):
    hoy = date.today()
    for dias in (0, 10, 40):
        cliente.post(
            "/clima",
            json={**REGISTRO, "fecha": (hoy - timedelta(days=dias)).isoformat()},
        )

    respuesta = cliente.get(
        "/clima/lotes/1",
        params={"desde": (hoy - timedelta(days=15)).isoformat()},
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 2


def test_historico_vacio_devuelve_lista_vacia(cliente):
    assert cliente.get("/clima/lotes/99").json() == []
