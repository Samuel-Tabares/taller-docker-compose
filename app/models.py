from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    completada = Column(Boolean, default=False, nullable=False)
