"""Cliente del servicio meteorologico OpenWeather (RF39).

El SRS registra que el plan gratuito permite hasta 60 llamadas por minuto,
por lo que el sistema consulta una vez al dia por lote y guarda el
resultado, en lugar de pedir el dato cada vez que alguien abre la pantalla.
"""

import os

import httpx

URL_BASE = "https://api.openweathermap.org/data/2.5/weather"
INTENTOS = 3


class ErrorOpenWeather(RuntimeError):
    """Se lanza cuando el proveedor no responde despues de los reintentos."""


class ClienteOpenWeather:
    def __init__(self, clave: str | None = None, tiempo_espera: int = 10):
        self.clave = clave or os.getenv("OPENWEATHER_API_KEY", "")
        self.tiempo_espera = tiempo_espera

    def consultar(self, latitud: float, longitud: float) -> dict:
        """Trae el dato meteorologico de un punto geografico.

        Reintenta hasta tres veces porque el plan contratado solo garantiza
        un 95 por ciento de disponibilidad; una falla puntual no debe dejar
        el dia sin registro.
        """
        parametros = {
            "lat": latitud,
            "lon": longitud,
            "appid": self.clave,
            "units": "metric",
            "lang": "es",
        }

        ultimo_error: Exception | None = None
        for _ in range(INTENTOS):
            try:
                respuesta = httpx.get(URL_BASE, params=parametros, timeout=self.tiempo_espera)
                respuesta.raise_for_status()
                return self._normalizar(respuesta.json())
            except httpx.HTTPError as error:
                ultimo_error = error

        raise ErrorOpenWeather(
            f"OpenWeather no respondio despues de {INTENTOS} intentos"
        ) from ultimo_error

    @staticmethod
    def _normalizar(datos: dict) -> dict:
        """Deja solo las variables que pide el RF39.

        Las horas de sol se calculan como la diferencia entre el amanecer y el
        atardecer que reporta el proveedor. El indice ultravioleta solo viene
        en el plan que incluye One Call, asi que puede llegar vacio.
        """
        principal = datos.get("main", {})
        sistema = datos.get("sys", {})

        horas_sol = None
        amanecer, atardecer = sistema.get("sunrise"), sistema.get("sunset")
        if amanecer and atardecer and atardecer > amanecer:
            horas_sol = round((atardecer - amanecer) / 3600, 2)

        return {
            "temperatura": principal.get("temp"),
            "presion_atmosferica": principal.get("pressure"),
            "humedad": principal.get("humidity"),
            "precipitacion": datos.get("rain", {}).get("1h", 0.0),
            "indice_ultravioleta": datos.get("uvi"),
            "horas_sol": horas_sol,
        }
