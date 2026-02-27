from datetime import datetime

from pydantic import BaseModel


class DocumentRevisionOut(BaseModel):
    revision: str
    is_active: bool
    uploaded_at: datetime


class DocumentOut(BaseModel):
    id: int
    document_code: str
    document_type: str
    title: str | None
    active_revision: str | None


class CircuitOut(BaseModel):
    circuit_code: str
    equipment_tag: str | None
    power_kw: float | None
    current_a: float | None
    breaker_a: float | None
    cable_spec: str | None


class SearchResultOut(BaseModel):
    document_code: str
    revision: str
    snippet: str


class SummaryOut(BaseModel):
    total_power_kw: float
    power_by_area: dict[str, float]
    consolidated_materials: list[dict]
