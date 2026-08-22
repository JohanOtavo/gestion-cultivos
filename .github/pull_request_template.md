## Qué hace este cambio

<!-- Una o dos frases. Qué resuelve, no cómo. -->

## Requerimiento del SRS

<!-- Ejemplo: RF39 - Registro diario de datos meteorológicos -->

RF:

## Cómo probarlo

```bash
cd services/<servicio>
pytest -q
```

## Lista de verificación del autor

- [ ] La rama sigue la convención `feature/RFx-descripcion`
- [ ] Los mensajes de commit terminan con el código del requerimiento
- [ ] `black` y `flake8` pasan sin hallazgos
- [ ] Las pruebas del servicio pasan en local
- [ ] No se subieron credenciales ni archivos `.env`

## Para el revisor

- [ ] El cambio cumple lo que dice el requerimiento del SRS
- [ ] El código respeta el estándar de codificación del equipo
- [ ] Hay pruebas que cubren el camino principal y al menos un caso de error
- [ ] Los nombres y comentarios se entienden sin preguntar al autor
