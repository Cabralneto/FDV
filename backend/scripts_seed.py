from datetime import date, timedelta

from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import (
    Alerta,
    Area,
    CronogramaAtividade,
    CurvaS,
    Disciplina,
    Fornecedor,
    Pendencia,
    Perfil,
    RequisicaoMaterial,
    Responsavel,
    Usuario,
)


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Usuario).first():
        print("Seed já aplicada")
        return

    perfil_admin = Perfil(nome="administrador")
    db.add(perfil_admin)

    area = Area(nome="Utilidades")
    disc = Disciplina(nome="Mecânica")
    forn = Fornecedor(nome="Metal Forte")
    resp = Responsavel(nome="Ana Planejamento")
    db.add_all([area, disc, forn, resp])
    db.flush()

    for i in range(1, 13):
        d = date.today().replace(day=1) - timedelta(days=(12 - i) * 30)
        db.add(CurvaS(referencia=d, previsto_fisico=i * 7.5, realizado_fisico=i * 6.8, previsto_financeiro=i * 800000, realizado_financeiro=i * 720000))

    db.add_all(
        [
            CronogramaAtividade(atividade_codigo="ATV-001", descricao="Montagem de tubulação", area_id=area.id, disciplina_id=disc.id, avanco_previsto=65, avanco_real=52, status="atrasada"),
            CronogramaAtividade(atividade_codigo="ATV-002", descricao="Comissionamento elétrico", area_id=area.id, disciplina_id=disc.id, avanco_previsto=40, avanco_real=43, status="em_dia"),
        ]
    )

    db.add_all(
        [
            Pendencia(titulo="Aprovação de revisão P&ID", criticidade="alta", status="aberta", responsavel_id=resp.id),
            Pendencia(titulo="Entrega de cabos especiais", criticidade="media", status="em_andamento", responsavel_id=resp.id),
        ]
    )

    db.add_all([
        RequisicaoMaterial(codigo="REQ-1001", descricao="Válvula de bloqueio", status="aberta"),
        RequisicaoMaterial(codigo="REQ-1002", descricao="Cabos instrumentação", status="em_andamento"),
    ])

    db.add_all([
        Alerta(titulo="Marco de energização em risco", severidade="alta", ativo=True),
        Alerta(titulo="Desvio de custo em instrumentação", severidade="media", ativo=True),
    ])

    db.add(Usuario(nome="Admin", email="admin@portalobra.local", senha_hash=get_password_hash("admin123"), perfil_id=1))
    db.commit()
    print("Seed aplicada")


if __name__ == "__main__":
    run()
