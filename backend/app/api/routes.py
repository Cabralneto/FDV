from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Area, Circuit, Document, DocumentRevision, Material
from app.schemas.document import CircuitOut, DocumentOut, SearchResultOut, SummaryOut
from app.services.ingestion_service import process_upload

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos")

    payload = await file.read()
    revision = process_upload(db, payload, file.filename)
    return {
        "revision_id": revision.id,
        "document_id": revision.document_id,
        "revision": revision.revision,
        "is_active": revision.is_active,
    }


@router.get("/documents", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Document.id,
            Document.document_code,
            Document.document_type,
            Document.title,
            DocumentRevision.revision.label("active_revision"),
        )
        .outerjoin(DocumentRevision, (DocumentRevision.document_id == Document.id) & (DocumentRevision.is_active.is_(True)))
        .order_by(Document.document_code)
        .all()
    )
    return [DocumentOut(**row._asdict()) for row in rows]


@router.get("/circuits", response_model=list[CircuitOut])
def list_circuits(
    area: str | None = Query(default=None),
    circuit: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Circuit).join(DocumentRevision, Circuit.revision_id == DocumentRevision.id).filter(DocumentRevision.is_active.is_(True))

    if circuit:
        query = query.filter(Circuit.circuit_code.ilike(f"%{circuit}%"))
    if area:
        query = query.join(Area, Circuit.area_id == Area.id).filter(Area.name == area)

    circuits = query.order_by(Circuit.circuit_code).all()
    return [
        CircuitOut(
            circuit_code=item.circuit_code,
            equipment_tag=item.equipment_tag,
            power_kw=float(item.power_kw) if item.power_kw is not None else None,
            current_a=float(item.current_a) if item.current_a is not None else None,
            breaker_a=float(item.breaker_a) if item.breaker_a is not None else None,
            cable_spec=item.cable_spec,
        )
        for item in circuits
    ]


@router.get("/search", response_model=list[SearchResultOut])
def search_textual(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    sql = text(
        """
        SELECT d.document_code,
               dr.revision,
               ts_headline('portuguese', dr.extracted_text, plainto_tsquery('portuguese', :q)) AS snippet
        FROM document_revisions dr
        JOIN documents d ON d.id = dr.document_id
        WHERE dr.is_active = TRUE
          AND dr.search_vector @@ plainto_tsquery('portuguese', :q)
        ORDER BY d.document_code
        LIMIT 50
        """
    )
    rows = db.execute(sql, {"q": q}).mappings().all()
    return [SearchResultOut(**dict(row)) for row in rows]


@router.get("/summary", response_model=SummaryOut)
def summary(db: Session = Depends(get_db)):
    total_power = (
        db.query(func.coalesce(func.sum(Circuit.power_kw), 0))
        .join(DocumentRevision, Circuit.revision_id == DocumentRevision.id)
        .filter(DocumentRevision.is_active.is_(True))
        .scalar()
    )

    area_rows = (
        db.query(Area.name, func.coalesce(func.sum(Circuit.power_kw), 0).label("power_kw"))
        .outerjoin(Circuit, Circuit.area_id == Area.id)
        .outerjoin(DocumentRevision, Circuit.revision_id == DocumentRevision.id)
        .filter((DocumentRevision.is_active.is_(True)) | (DocumentRevision.id.is_(None)))
        .group_by(Area.name)
        .all()
    )

    material_rows = (
        db.query(Material.material_code, Material.description, Material.unit, func.sum(Material.quantity).label("quantity"))
        .join(DocumentRevision, Material.revision_id == DocumentRevision.id)
        .filter(DocumentRevision.is_active.is_(True))
        .group_by(Material.material_code, Material.description, Material.unit)
        .order_by(Material.description)
        .all()
    )

    return SummaryOut(
        total_power_kw=float(total_power or 0),
        power_by_area={name: float(power or 0) for name, power in area_rows},
        consolidated_materials=[
            {
                "material_code": row.material_code,
                "description": row.description,
                "unit": row.unit,
                "quantity": float(row.quantity or 0),
            }
            for row in material_rows
        ],
    )
