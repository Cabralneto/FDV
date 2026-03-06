from datetime import datetime

from pydantic import BaseModel


class ApontamentoCreate(BaseModel):
    tipo: str
    titulo: str
    descricao: str
    area_id: int | None = None
    disciplina_id: int | None = None


class ApontamentoOut(ApontamentoCreate):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
