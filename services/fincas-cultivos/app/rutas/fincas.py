"""Endpoints de gestion de fincas (RF1 a RF4)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import esquemas, modelos
from app.base_datos import obtener_sesion

router = APIRouter(prefix="/fincas", tags=["fincas"])


@router.post("", response_model=esquemas.FincaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_finca(datos: esquemas.FincaCrear, sesion: Session = Depends(obtener_sesion)):
    """Registra una finca nueva (RF1)."""
    repetida = sesion.query(modelos.Finca).filter_by(nombre=datos.nombre).first()
    if repetida is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una finca registrada con el nombre {datos.nombre}",
        )

    finca = modelos.Finca(**datos.model_dump())
    sesion.add(finca)
    sesion.commit()
    sesion.refresh(finca)
    return finca


@router.get("", response_model=list[esquemas.FincaRespuesta])
def consultar_fincas(id_propietario: int, sesion: Session = Depends(obtener_sesion)):
    """Lista las fincas activas del usuario autenticado (RF2)."""
    return (
        sesion.query(modelos.Finca)
        .filter_by(id_propietario=id_propietario, activa=True)
        .order_by(modelos.Finca.nombre)
        .all()
    )


@router.get("/{id_finca}", response_model=esquemas.FincaRespuesta)
def consultar_finca(id_finca: int, sesion: Session = Depends(obtener_sesion)):
    """Entrega el detalle de una finca (RF2)."""
    return _buscar_finca(id_finca, sesion)


@router.put("/{id_finca}", response_model=esquemas.FincaRespuesta)
def modificar_finca(
    id_finca: int,
    datos: esquemas.FincaActualizar,
    sesion: Session = Depends(obtener_sesion),
):
    """Modifica los datos de una finca existente (RF3)."""
    finca = _buscar_finca(id_finca, sesion)

    for campo, valor in datos.model_dump().items():
        setattr(finca, campo, valor)

    sesion.commit()
    sesion.refresh(finca)
    return finca


@router.delete("/{id_finca}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_finca(id_finca: int, sesion: Session = Depends(obtener_sesion)):
    """Elimina una finca (RF4).

    La eliminacion es logica: la finca se marca como inactiva en lugar de
    borrarse, para conservar el historico de lotes y cultivos asociados.
    """
    finca = _buscar_finca(id_finca, sesion)
    finca.activa = False
    sesion.commit()


def _buscar_finca(id_finca: int, sesion: Session) -> modelos.Finca:
    """Devuelve la finca activa o corta la solicitud con un 404."""
    finca = sesion.query(modelos.Finca).filter_by(id=id_finca, activa=True).first()
    if finca is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe una finca activa con el identificador {id_finca}",
        )
    return finca
