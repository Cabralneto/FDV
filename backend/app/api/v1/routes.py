from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ingestion.pipeline import run_ingestion
from app.models.entities import Alerta, ApontamentoManual, CronogramaAtividade, LogProcessamento, Pendencia, Usuario
from app.schemas.apontamento import ApontamentoCreate, ApontamentoOut
from app.schemas.auth import LoginInput, TokenOutput
from app.services.dashboard_service import get_dashboard_data
from app.services.search_service import global_search
from app.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/auth/login", response_model=TokenOutput)
def login(payload: LoginInput, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if not user or not verify_password(payload.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return TokenOutput(access_token=create_access_token(user.email))


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard_data(db)


@router.get("/planejamento")
def planejamento(db: Session = Depends(get_db)):
    items = db.query(CronogramaAtividade).order_by(CronogramaAtividade.data_fim.asc()).limit(200).all()
    return {"items": items}


@router.get("/engenharia")
def engenharia(db: Session = Depends(get_db)):
    pendencias = db.query(Pendencia).limit(100).all()
    return {"pendencias": pendencias}


@router.get("/orcamento")
def orcamento(db: Session = Depends(get_db)):
    return {
        "custo_previsto": 12800000,
        "custo_realizado": 9650000,
        "desvio": -3150000,
        "saldo_contratual": 4950000,
    }


@router.get("/medicao")
def medicao():
    return {"acumulado": 7400000, "periodo": 380000}


@router.get("/suprimentos")
def suprimentos():
    return {"requisicoes_abertas": 28, "criticos": 6, "lead_time_medio_dias": 21}


@router.get("/campo")
def campo():
    return {"efetivo_total": 412, "pt_abertas": 14, "rdo_hoje": 3}


@router.get("/pendencias")
def pendencias(db: Session = Depends(get_db)):
    data = db.query(Pendencia).limit(200).all()
    return {"items": data}


@router.get("/documentos")
def documentos():
    return {"ld_total": 1462, "sigem_total": 1398, "pendentes": 94}


@router.get("/busca")
def busca(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    return global_search(db, q)


@router.get("/alertas")
def alertas(db: Session = Depends(get_db)):
    data = db.query(Alerta).order_by(Alerta.criado_em.desc()).limit(50).all()
    return {"items": data}


@router.get("/admin/status")
def admin_status(db: Session = Depends(get_db)):
    logs = db.query(LogProcessamento).order_by(LogProcessamento.data_evento.desc()).limit(20).all()
    return {"logs": logs}


@router.post("/admin/run-ingestion")
def admin_run_ingestion(db: Session = Depends(get_db)):
    return run_ingestion(db)


@router.post("/apontamentos", response_model=ApontamentoOut)
def create_apontamento(payload: ApontamentoCreate, db: Session = Depends(get_db)):
    obj = ApontamentoManual(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
