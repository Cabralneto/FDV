from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Area(Base):
    __tablename__ = "areas"
    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_area_project_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (UniqueConstraint("project_id", "document_code", name="uq_document_project_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    document_code: Mapped[str] = mapped_column(String(80))
    document_type: Mapped[str] = mapped_column(String(10))
    title: Mapped[str | None] = mapped_column(String(255))
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    equipment_tag: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    revisions = relationship("DocumentRevision", back_populates="document")


class DocumentRevision(Base):
    __tablename__ = "document_revisions"
    __table_args__ = (UniqueConstraint("document_id", "revision", name="uq_document_revision"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    revision: Mapped[str] = mapped_column(String(16))
    revision_order: Mapped[int]
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(Text)
    checksum_sha256: Mapped[str | None] = mapped_column(String(64))
    extracted_text: Mapped[str | None] = mapped_column(Text)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    document = relationship("Document", back_populates="revisions")


class Circuit(Base):
    __tablename__ = "circuits"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("document_revisions.id", ondelete="CASCADE"))
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    circuit_code: Mapped[str] = mapped_column(String(100))
    equipment_tag: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    power_kw: Mapped[float | None] = mapped_column(Numeric(12, 3))
    current_a: Mapped[float | None] = mapped_column(Numeric(12, 3))
    breaker_a: Mapped[float | None] = mapped_column(Numeric(12, 3))
    cable_spec: Mapped[str | None] = mapped_column(String(120))


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("document_revisions.id", ondelete="CASCADE"))
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    material_code: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(20))
    quantity: Mapped[float] = mapped_column(Numeric(14, 3), default=0)
    discipline: Mapped[str | None] = mapped_column(String(20))
