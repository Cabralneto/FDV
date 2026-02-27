from __future__ import annotations

import hashlib
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import Area, Circuit, Document, DocumentRevision, Material, Project
from app.services.pdf_service import extract_text_from_pdf
from app.services.technical_parser import parse_circuits, parse_materials
from app.utils.parser import (
    AREA_HINTS,
    detect_document_code,
    detect_revision,
    infer_document_type,
    revision_to_order,
    safe_filename,
)


def _sha256_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ensure_project(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).one_or_none()
    if project:
        return project

    project = Project(id=project_id, code=f"OBRA-{project_id}", name=f"Obra {project_id}")
    db.add(project)
    db.flush()
    return project


def _detect_area_name(text: str) -> str | None:
    lowered = text.lower()
    for area in AREA_HINTS:
        if area.lower() in lowered:
            return area
    return None


def _ensure_area(db: Session, project_id: int, area_name: str | None) -> int | None:
    if not area_name:
        return None
    area = db.query(Area).filter(Area.project_id == project_id, Area.name == area_name).one_or_none()
    if area:
        return area.id
    area = Area(project_id=project_id, name=area_name)
    db.add(area)
    db.flush()
    return area.id


def process_upload(db: Session, upload_bytes: bytes, original_name: str, project_id: int = 1) -> DocumentRevision:
    _ensure_project(db, project_id)

    upload_root = Path(settings.upload_dir)
    upload_root.mkdir(parents=True, exist_ok=True)

    file_name = safe_filename(original_name)
    target = upload_root / file_name
    target.write_bytes(upload_bytes)

    extracted_text = extract_text_from_pdf(str(target))
    document_code = detect_document_code(extracted_text, file_name) or f"UNK-{file_name}"
    revision = detect_revision(extracted_text, file_name)
    area_id = _ensure_area(db, project_id, _detect_area_name(extracted_text))

    doc = (
        db.query(Document)
        .filter(Document.project_id == project_id, Document.document_code == document_code)
        .one_or_none()
    )
    if doc is None:
        doc = Document(
            project_id=project_id,
            document_code=document_code,
            document_type=infer_document_type(document_code),
            title=file_name,
            area_id=area_id,
        )
        db.add(doc)
        db.flush()
    elif area_id and doc.area_id is None:
        doc.area_id = area_id

    same_revision = (
        db.query(DocumentRevision)
        .filter(DocumentRevision.document_id == doc.id, DocumentRevision.revision == revision)
        .one_or_none()
    )

    db.query(DocumentRevision).filter(
        DocumentRevision.document_id == doc.id,
        DocumentRevision.is_active.is_(True),
    ).update({"is_active": False})

    if same_revision:
        same_revision.is_active = True
        same_revision.file_name = file_name
        same_revision.file_path = str(target)
        same_revision.checksum_sha256 = _sha256_file(target)
        same_revision.extracted_text = extracted_text
        rev = same_revision

        db.query(Circuit).filter(Circuit.revision_id == rev.id).delete()
        db.query(Material).filter(Material.revision_id == rev.id).delete()
    else:
        rev = DocumentRevision(
            document_id=doc.id,
            revision=revision,
            revision_order=revision_to_order(revision),
            is_active=True,
            file_name=file_name,
            file_path=str(target),
            checksum_sha256=_sha256_file(target),
            extracted_text=extracted_text,
        )
        db.add(rev)
        db.flush()

    if db.bind and db.bind.dialect.name == "postgresql":
        db.execute(
            text(
                """
                UPDATE document_revisions
                SET search_vector = to_tsvector('portuguese', coalesce(extracted_text, ''))
                WHERE id = :revision_id
                """
            ),
            {"revision_id": rev.id},
        )

    for circuit in parse_circuits(extracted_text):
        db.add(
            Circuit(
                revision_id=rev.id,
                area_id=area_id,
                circuit_code=circuit["circuit_code"],
                power_kw=circuit.get("power_kw"),
                breaker_a=circuit.get("breaker_a"),
            )
        )

    for material in parse_materials(extracted_text):
        db.add(
            Material(
                revision_id=rev.id,
                area_id=area_id,
                material_code=material.get("material_code"),
                description=material["description"],
                quantity=material["quantity"],
                unit=material.get("unit"),
            )
        )

    db.commit()
    db.refresh(rev)
    return rev
