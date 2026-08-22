"""Endpoints de datos meteorologicos (RF39, RF40 y RF42)."""

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import esquemas, modelos
from app.base_datos import obtener_sesion
from app.clientes.openweather import ClienteOpenWeather, ErrorOpenWeather

router = APIRouter(prefix="/clima", tags=["datos meteorologicos"])

# El SRS exige conservar el historico por al menos cinco anios (RF42).
ANIOS_DE_RETENCION = 5


@router.post(
    "/lotes/{id_lote}/sincronizar",
    response_model=esquemas.RegistroRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def sincronizar(
    id_lote: int,
    latitud: float,
    longitud: float,
    sesion: Session = Depends(obtener_sesion),
):
    """Consulta el proveedor y guarda el dato del dia para el lote (RF39).

    Si el dia ya tiene registro se actualiza en lugar de crear otro, porque la
    tarea programada puede repetirse tras un reintento.
    """
    try:
        datos = ClienteOpenWeather().consultar(latitud, longitud)
    except ErrorOpenWeather as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    hoy = date.today()
    registro = (
        sesion.query(modelos.RegistroMeteorologico).filter_by(id_lote=id_lote, fecha=hoy).first()
    )
    if registro is None:
        registro = modelos.RegistroMeteorologico(id_lote=id_lote, fecha=hoy)
        sesion.add(registro)

    for campo, valor in datos.items():
        setattr(registro, campo, valor)

    sesion.commit()
    sesion.refresh(registro)
    return registro


@router.get("/lotes/{id_lote}", response_model=list[esquemas.RegistroRespuesta])
def consultar_historico(
    id_lote: int,
    desde: date | None = None,
    hasta: date | None = None,
    sesion: Session = Depends(obtener_sesion),
):
    """Entrega el historico meteorologico de un lote (RF40).

    Sin fechas devuelve la ventana completa de retencion, para que la interfaz
    pueda graficar el comportamiento a lo largo del ciclo del cultivo.
    """
    limite = date.today() - timedelta(days=365 * ANIOS_DE_RETENCION)
    consulta = sesion.query(modelos.RegistroMeteorologico).filter(
        modelos.RegistroMeteorologico.id_lote == id_lote,
        modelos.RegistroMeteorologico.fecha >= (desde or limite),
    )
    if hasta is not None:
        consulta = consulta.filter(modelos.RegistroMeteorologico.fecha <= hasta)

    return consulta.order_by(modelos.RegistroMeteorologico.fecha.desc()).all()


@router.post("", response_model=esquemas.RegistroRespuesta, status_code=201)
def registrar_manual(datos: esquemas.RegistroCrear, sesion: Session = Depends(obtener_sesion)):
    """Permite cargar un dato a mano cuando el proveedor no estuvo disponible."""
    repetido = (
        sesion.query(modelos.RegistroMeteorologico)
        .filter_by(id_lote=datos.id_lote, fecha=datos.fecha)
        .first()
    )
    if repetido is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El lote {datos.id_lote} ya tiene un registro para {datos.fecha}",
        )

    registro = modelos.RegistroMeteorologico(**datos.model_dump())
    sesion.add(registro)
    sesion.commit()
    sesion.refresh(registro)
    return registro
