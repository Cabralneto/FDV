from datetime import date, datetime

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class KPI(BaseModel):
    label: str
    value: float
    trend: float


class CurvaSItem(BaseModel):
    referencia: date
    previsto_fisico: float
    realizado_fisico: float


class LogItem(BaseModel):
    processo: str
    nivel: str
    mensagem: str
    data_evento: datetime
