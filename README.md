# Taller — Dockerfile, Docker Compose y Pruebas en Contenedores

API de **lista de tareas** hecha con **FastAPI + PostgreSQL**, contenerizada con
Docker y orquestada con Docker Compose. Las pruebas unitarias se ejecutan dentro
del contenedor.

## Endpoints

| Método | Ruta            | Descripción                  |
|--------|-----------------|------------------------------|
| GET    | `/`             | Estado de la API             |
| POST   | `/tareas`       | Crear una tarea              |
| GET    | `/tareas`       | Listar tareas                |
| GET    | `/tareas/{id}`  | Obtener una tarea por id     |
| DELETE | `/tareas/{id}`  | Eliminar una tarea           |

## Estructura

```
app/            código de la aplicación (FastAPI + SQLAlchemy)
tests/          pruebas unitarias (pytest)
Dockerfile      imagen de la aplicación
docker-compose.yml   servicios app + db
docs/           salidas de los entregables
```

## Uso

```bash
# Construir la imagen (Parte 2)
docker build -t mi-app:v1 .
docker images

# Levantar los servicios (Parte 3)
docker compose up -d
docker compose ps
curl http://localhost:8000/

# Ejecutar las pruebas dentro del contenedor (Parte 4)
docker compose exec app pytest -v
docker compose run --rm app pytest -v

# Reconstruir solo la app sin detener la base (Parte 5)
docker compose up -d --build app
docker compose exec app pytest -v
```

## Variables de entorno (conexión a la base)

`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`. Las define
`docker-compose.yml` para el servicio `app`.

## Entregables

- Código fuente: `app/`, `tests/`
- `Dockerfile`
- `docker-compose.yml`
- Salida de `docker compose ps`: [`docs/compose-ps.txt`](docs/compose-ps.txt)
- Salida de las pruebas en el contenedor: [`docs/pruebas.txt`](docs/pruebas.txt)
