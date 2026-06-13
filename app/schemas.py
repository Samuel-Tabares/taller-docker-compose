from pydantic import BaseModel


class TareaIn(BaseModel):
    titulo: str
    completada: bool = False


class TareaOut(BaseModel):
    id: int
    titulo: str
    completada: bool

    model_config = {"from_attributes": True}
