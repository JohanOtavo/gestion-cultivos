# Flujo de trabajo con control de versiones

Este documento deja registrado cómo trabaja el equipo sobre el repositorio y
cómo se ve el historial resultante. Las reglas están en
[CONTRIBUTING.md](../CONTRIBUTING.md); aquí se muestra su aplicación real.

## 1. Ramas creadas

Cada rama corresponde a un requerimiento del SRS y sigue la convención
`feature/RFx-descripcion`.

| Rama | Requerimientos | Qué contiene | Estado |
|---|---|---|---|
| `main` | — | Rama principal protegida. Solo recibe cambios por Pull Request. | Activa |
| `feature/RF1-gestion-fincas` | RF1 a RF4 | Modelo de finca y lote, esquemas, CRUD completo y pruebas. | Fusionada |
| `feature/RF33-diagnostico-fitosanitario` | RF33, RF35, RF36 | Envoltura del modelo de visión artificial, carga de imagen, historial y pruebas. | Fusionada |
| `feature/RF39-datos-meteorologicos` | RF39 | Cliente de OpenWeather con reintentos. | En desarrollo |
| `docs/flujo-de-trabajo` | — | Documentación de este flujo. | En revisión |

## 2. Ciclo que sigue cada cambio

```
1. git checkout main && git pull
2. git checkout -b feature/RFx-descripcion
3. (trabajo) → commits pequeños con el código del RF en el mensaje
4. black . && flake8 . && pytest      ← antes de subir
5. git push -u origin feature/RFx-descripcion
6. Pull Request hacia main
7. Revisión de pares: otro integrante aprueba
8. Merge con --no-ff para conservar visible la rama
```

El paso 4 también lo repite GitHub Actions en el servidor, de modo que si
alguien lo olvida el pipeline lo detiene antes del merge.

## 3. Historial resultante

Salida real de `git log --graph --oneline --all`:

```
* c7211c9 feat(clima): agrega el cliente de OpenWeather con reintentos - RF39
*   7f50677 Merge de feature/RF33-diagnostico-fitosanitario hacia main
|\
| * 3e275c2 test(diagnostico): verifica el resultado, el rechazo y el historial - RF33, RF36
| * 94b0f73 feat(diagnostico): recibe la imagen del cultivo y entrega el diagnostico - RF33, RF36
| * 043026f feat(diagnostico): agrega la envoltura del modelo de vision artificial - RF33
|/
*   be3c1e9 Merge de feature/RF1-gestion-fincas hacia main
|\
| * 5f65891 refactor(fincas): crea el motor de forma perezosa para probar sin PostgreSQL - RF1
| * 1a229e1 test(fincas): cubre el CRUD de fincas con siete pruebas automaticas - RF1 a RF4
| * fab0612 feat(fincas): implementa los endpoints CRUD - RF1 a RF4
| * d47fa33 feat(fincas): agrega el modelo de finca y lote con su esquema - RF1
|/
* 3a92510 chore(proyecto): estructura inicial de microservicios con Docker
```

Se usó `--no-ff` a propósito: con *fast-forward* los commits quedarían en una
sola línea recta y se perdería la información de qué rama trajo cada cambio.
Con el merge commit, el gráfico muestra la bifurcación y permite responder
"¿qué entró con el RF33?" mirando una sola rama.

## 4. Por qué el mensaje de commit lleva el código del RF

Porque la sección 4 del SRS exige una matriz de trazabilidad entre
requerimientos y verificación. Al escribir el RF en cada mensaje, esa matriz
se puede reconstruir desde el historial:

```bash
git log --oneline --grep="RF33"
```

## 5. Cómo ver el historial

```bash
git log --graph --oneline --all      # el gráfico completo de ramas
git log --oneline --grep="RF1"       # todo lo hecho para un requerimiento
git blame services/fincas-cultivos/app/rutas/fincas.py   # autor de cada línea
git branch -a                        # ramas locales y remotas
```
