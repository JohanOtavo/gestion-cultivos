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
2. Se abre el Pull Request hacia `main` describiendo qué RF implementa.
3. **Otro integrante** revisa el cambio. El autor no aprueba su propio PR.
4. El revisor verifica: que cumpla el requerimiento del SRS, que respete el estándar
   de codificación y que incluya pruebas.
5. Con la aprobación se fusiona usando *merge commit* (`--no-ff`), para que el
   historial conserve visible la rama de dónde vino el cambio.

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
