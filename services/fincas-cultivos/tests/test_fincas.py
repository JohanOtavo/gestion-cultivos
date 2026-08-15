"""Pruebas de los endpoints de gestion de fincas (RF1 a RF4)."""

FINCA = {
    "nombre": "La Esperanza",
    "ubicacion": "Campoalegre, Huila",
    "area_total": 12.5,
    "unidad_area": "hectarea",
    "id_propietario": 1,
}


def test_crear_finca_devuelve_201(cliente):
    respuesta = cliente.post("/fincas", json=FINCA)

    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "La Esperanza"
    assert respuesta.json()["activa"] is True


def test_no_permite_dos_fincas_con_el_mismo_nombre(cliente):
    cliente.post("/fincas", json=FINCA)

    respuesta = cliente.post("/fincas", json=FINCA)

    assert respuesta.status_code == 409


def test_rechaza_area_negativa(cliente):
    respuesta = cliente.post("/fincas", json={**FINCA, "area_total": -3})

    assert respuesta.status_code == 422


def test_consultar_solo_devuelve_las_fincas_del_propietario(cliente):
    cliente.post("/fincas", json=FINCA)
    cliente.post("/fincas", json={**FINCA, "nombre": "El Progreso", "id_propietario": 2})

    respuesta = cliente.get("/fincas", params={"id_propietario": 1})

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["nombre"] == "La Esperanza"


def test_modificar_finca_actualiza_la_ubicacion(cliente):
    id_finca = cliente.post("/fincas", json=FINCA).json()["id"]

    respuesta = cliente.put(
        f"/fincas/{id_finca}",
        json={
            "nombre": "La Esperanza",
            "ubicacion": "Rivera, Huila",
            "area_total": 12.5,
            "unidad_area": "hectarea",
        },
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["ubicacion"] == "Rivera, Huila"


def test_eliminar_finca_la_deja_inactiva(cliente):
    id_finca = cliente.post("/fincas", json=FINCA).json()["id"]

    assert cliente.delete(f"/fincas/{id_finca}").status_code == 204
    assert cliente.get(f"/fincas/{id_finca}").status_code == 404


def test_consultar_finca_inexistente_devuelve_404(cliente):
    assert cliente.get("/fincas/999").status_code == 404
