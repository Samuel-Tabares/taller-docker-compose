import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import Tarea

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Tarea).delete()
    db.commit()
    db.close()
    yield


def test_crear_tarea():
    resp = client.post("/tareas", json={"titulo": "Comprar pan"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["titulo"] == "Comprar pan"
    assert body["completada"] is False
    assert isinstance(body["id"], int)


def test_listar_tareas():
    client.post("/tareas", json={"titulo": "Tarea 1"})
    client.post("/tareas", json={"titulo": "Tarea 2"})
    resp = client.get("/tareas")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_eliminar_tarea():
    creada = client.post("/tareas", json={"titulo": "Borrar"}).json()
    resp = client.delete(f"/tareas/{creada['id']}")
    assert resp.status_code == 204
    assert client.get("/tareas").json() == []


def test_obtener_tarea_por_id():
    creada = client.post("/tareas", json={"titulo": "Leer libro"}).json()
    resp = client.get(f"/tareas/{creada['id']}")
    assert resp.status_code == 200
    assert resp.json()["titulo"] == "Leer libro"
    assert client.get("/tareas/99999").status_code == 404
