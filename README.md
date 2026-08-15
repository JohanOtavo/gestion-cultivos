# Gestión de Cultivos

Aplicación web en la nube para la gestión del ciclo completo de producción agrícola:
planificación del cultivo, registro y trazabilidad de labores y costos, diagnóstico
fitosanitario con inteligencia artificial, datos meteorológicos, recomendaciones e
informes de rentabilidad.

Proyecto formativo — Análisis y Desarrollo de Software
Centro de la Industria, la Empresa y los Servicios (CIES) — SENA

## Equipo

| Integrante | Rol en el repositorio |
|---|---|
| Jannier Johan Otavo Artunduaga | Mantenedor, revisor de Pull Requests |
| Iván Andrés Cortez Olaya | Desarrollador, revisor de Pull Requests |
| Jeison Camilo Dueñas Lozano | Desarrollador, revisor de Pull Requests |

## Arquitectura

Backend organizado en nueve microservicios independientes (RF105), cada uno con su
propio Dockerfile (RF108), coordinados por una API Gateway que es el único punto de
entrada (RF106).

| Servicio | Puerto | Dominio funcional | Requerimientos |
|---|---|---|---|
| `api-gateway` | 8000 | Enrutamiento de solicitudes | RF106, RF110 |
| `auth-usuarios` | 8001 | Autenticación, roles y permisos | RF62–RF69, RF82–RF91 |
| `fincas-cultivos` | 8002 | Fincas, lotes y cultivos | RF1–RF13 |
| `gestion-agricola` | 8003 | Catálogos y ciclo vegetativo | RF14–RF18, RF74–RF81 |
| `tareas-labores` | 8004 | Labores, mecanización y tareas | RF25–RF32, RF43–RF46 |
| `monitoreo-clima` | 8005 | Suelo, monitoreo y clima | RF20–RF24, RF39–RF42 |
| `diagnostico-ia` | 8006 | Diagnóstico fitosanitario | RF33–RF38 |
| `reportes-analitica` | 8007 | Presupuesto, reportes y recomendaciones | RF19, RF47–RF61 |
| `alertas-notificaciones` | 8008 | Alertas y notificaciones | RF70–RF73 |
| `archivos-imagenes` | 8009 | Imágenes en Amazon S3 | Soporta RF33 |

## Requisitos

- Docker 24.x o superior y Docker Compose 2.x o superior
- Python 3.11 (solo si se ejecuta un servicio fuera de contenedor)

## Cómo levantar el proyecto

```bash
cp .env.example .env
docker compose up --build
```

La API Gateway queda en `http://localhost:8000` y la documentación automática de
cada servicio en `/docs`. Ningún microservicio se expone directamente al exterior:
todos se comunican por la red interna de Docker (RF110).

Para verificar que todo está arriba:

```bash
curl http://localhost:8000/salud
```

## Flujo de trabajo

El equipo trabaja con una rama por requerimiento y fusiona a `main` mediante Pull
Request con revisión de pares. Las convenciones están en
[CONTRIBUTING.md](CONTRIBUTING.md) y el historial documentado en
[docs/flujo-de-trabajo.md](docs/flujo-de-trabajo.md).

## Documento base

SRS Gestión de Cultivos v1.0 — 112 requerimientos funcionales y 254 no funcionales.
