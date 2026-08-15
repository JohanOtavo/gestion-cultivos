"""Envoltura del modelo de vision artificial del diagnostico (RF33).

El modelo de TensorFlow se carga una sola vez por proceso y no en cada
solicitud, porque cargarlo es lo mas costoso de la operacion. Mientras el
modelo entrenado no este disponible, la clase responde con una prediccion
neutra para no bloquear al resto del equipo.
"""

import os
from functools import lru_cache

RUTA_MODELO = os.getenv("RUTA_MODELO", "modelos/diagnostico_arroz.keras")

CATEGORIAS = ("plaga", "enfermedad", "maleza", "deficiencia nutricional")

RECOMENDACIONES = {
    "plaga": "Programar monitoreo dirigido y evaluar control segun el umbral de dano.",
    "enfermedad": "Revisar humedad y ventilacion del lote antes de aplicar el control quimico.",
    "maleza": "Programar control mecanico o quimico segun la etapa fenologica del cultivo.",
    "deficiencia nutricional": "Contrastar con el ultimo analisis edafologico antes de fertilizar.",
}


class ModeloDiagnostico:
    """Clasifica una imagen del cultivo en una de las cuatro categorias."""

    def __init__(self, ruta: str = RUTA_MODELO):
        self.ruta = ruta
        self._modelo = None

    @property
    def disponible(self) -> bool:
        return os.path.exists(self.ruta)

    def predecir(self, contenido: bytes) -> tuple[str, str, float]:
        """Devuelve la categoria, el hallazgo y la confianza.

        Mientras no exista el archivo del modelo entrenado, se responde con
        una confianza de cero para que la interfaz muestre el aviso de
        diagnostico no concluyente en lugar de un resultado inventado.
        """
        if not self.disponible:
            return "enfermedad", "Modelo no disponible: diagnostico no concluyente", 0.0

        raise NotImplementedError(
            "Pendiente conectar el modelo entrenado de TensorFlow (tarea del sprint 3)."
        )

    @staticmethod
    def recomendacion_para(categoria: str) -> str:
        """Entrega la recomendacion tecnica asociada a la categoria (RF35)."""
        return RECOMENDACIONES.get(categoria, "Consultar al agronomo responsable del cultivo.")


@lru_cache
def obtener_modelo() -> ModeloDiagnostico:
    return ModeloDiagnostico()
