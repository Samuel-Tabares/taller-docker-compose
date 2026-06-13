from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Tarea
from app.schemas import TareaIn, TareaOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de Tareas", lifespan=lifespan)


@app.get("/")
def raiz() -> dict[str, str]:
    return {"mensaje": "API de Tareas funcionando"}


@app.post("/tareas", response_model=TareaOut, status_code=201)
def crear_tarea(tarea: TareaIn, db: Session = Depends(get_db)) -> Tarea:
    nueva = Tarea(titulo=tarea.titulo, completada=tarea.completada)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/tareas", response_model=list[TareaOut])
def listar_tareas(db: Session = Depends(get_db)) -> list[Tarea]:
    return db.query(Tarea).all()


@app.get("/tareas/{tarea_id}", response_model=TareaOut)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db)) -> Tarea:
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)) -> None:
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
