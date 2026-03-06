from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.entities import Alerta, CronogramaAtividade, CurvaS, Pendencia


def get_dashboard_data(db: Session):
    atraso = db.query(func.count(CronogramaAtividade.id)).filter(CronogramaAtividade.status == "atrasada").scalar() or 0
    pend_crit = db.query(func.count(Pendencia.id)).filter(Pendencia.criticidade == "alta", Pendencia.status != "fechada").scalar() or 0
    alertas = db.query(func.count(Alerta.id)).filter(Alerta.ativo.is_(True)).scalar() or 0

    curva = db.query(CurvaS).order_by(CurvaS.referencia.asc()).limit(12).all()

    return {
        "kpis": [
            {"label": "Atividades atrasadas", "value": float(atraso), "trend": -2.0},
            {"label": "Pendências críticas", "value": float(pend_crit), "trend": 1.0},
            {"label": "Alertas ativos", "value": float(alertas), "trend": 0.0},
        ],
        "curva_s": curva,
    }
