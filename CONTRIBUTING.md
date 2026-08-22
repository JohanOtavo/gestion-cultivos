# Guía de contribución

Estas son las reglas que acordó el equipo para trabajar sobre el repositorio.
Se aplican a todos los integrantes sin excepción.

## 1. Ramas

`main` es la rama principal y está protegida: nadie hace commit directo sobre ella.
Todo cambio entra por una rama propia y se fusiona mediante Pull Request.

Cada rama corresponde a **un requerimiento del SRS** y se nombra así:

```
feature/RFx-descripcion-corta
```

Ejemplos reales del proyecto:

```
feature/RF1-gestion-fincas
feature/RF33-diagnostico-fitosanitario
feature/RF39-datos-meteorologicos
```

Otros prefijos permitidos:

| Prefijo | Cuándo se usa |
|---|---|
| `feature/` | Implementa un requerimiento funcional nuevo |
| `fix/` | Corrige un defecto encontrado en `main` |
| `docs/` | Cambios solo de documentación |

## 2. Commits

Se usa la convención *Conventional Commits* y **el mensaje termina con el código del
requerimiento**, para poder reconstruir la matriz de verificación del SRS desde el
historial.

```
tipo(alcance): descripción en presente - RFx
```

Ejemplos:

```
feat(fincas): registra una finca con nombre unico y ubicacion - RF1
test(fincas): valida que no se acepten fincas con nombre repetido - RF1
fix(clima): reintenta la consulta cuando OpenWeather responde 429 - RF39
```

Tipos aceptados: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`.

Reglas prácticas:

- Un commit por idea completa. Nada de un solo commit gigante al final del día.
- El mensaje explica **qué cambia y por qué**, no "cambios varios" ni "avance".
- El código debe quedar funcionando en cada commit.

## 3. Pull Request y revisión de pares

1. Se sube la rama con `git push -u origin feature/RFx-descripcion`.
2. Se abre el Pull Request hacia `main`. La plantilla se llena sola con las
   preguntas que debe responder el autor.
3. **Otro integrante** revisa el cambio. El autor no aprueba su propio PR.
4. Con la aprobación se fusiona usando *merge commit* (`--no-ff`), para que el
   historial conserve visible la rama de dónde vino el cambio.

### Qué mira el revisor

No se trata de leer el código por encima y aprobar. El revisor responde cuatro
preguntas concretas, que son las de la plantilla:

| Pregunta | Qué significa aprobar |
|---|---|
| ¿Cumple el requerimiento? | Se abre el SRS y se compara contra lo que dice el RF |
| ¿Respeta el estándar? | `black` y `flake8` pasan y los nombres siguen la convención |
| ¿Tiene pruebas? | Cubren el camino principal y al menos un caso de error |
| ¿Se entiende? | Los nombres y comentarios se entienden sin preguntarle al autor |

Si algo no cumple, se comenta en la línea concreta del Pull Request y se
devuelve al autor. Pedir cambios no es un reproche: es más barato corregir en
la revisión que después de que el código entró a `main`.

### Rotación de revisores

Revisa quien **no** escribió el cambio. El archivo `.github/CODEOWNERS` hace que
GitHub proponga revisor automáticamente al abrir el Pull Request.

## 3.1. Verificaciones automáticas antes del commit

Para no descubrir en el servidor algo que se podía ver en la máquina propia,
cada integrante instala los hooks una sola vez:

```bash
pip install pre-commit
pre-commit install
```

A partir de ahí, cada `git commit` corre el formato, el análisis de estilo, la
detección de llaves privadas y el bloqueo de commits directos a `main`.

## 4. Estándar de codificación

| Parte del sistema | Herramientas | Convención |
|---|---|---|
| Microservicios (Python / FastAPI) | Black, Flake8 | PEP 8, `snake_case` |
| Aplicación web (React) | ESLint, Prettier | `camelCase`, componentes en `PascalCase` |

Antes de subir cambios:

```bash
black services/ gateway/
flake8 services/ gateway/
cd services/<el-servicio-que-tocaste> && pytest
```

Las pruebas se ejecutan **dentro de cada servicio**, no desde la raíz: los nueve
tienen un paquete llamado `app` y Python no puede importar dos con el mismo nombre
en la misma sesión. El pipeline hace lo mismo, servicio por servicio.

## 5. Qué nunca se sube

El archivo `.env` con credenciales reales, claves de AWS u OpenWeather, modelos
entrenados y carpetas `venv/` o `node_modules/`. Todo eso está en `.gitignore`.
