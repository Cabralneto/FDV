from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.entities import (
    ArquivoOrigem,
    CronogramaAtividade,
    DimArea,
    DimDisciplina,
    DimDocumento,
    DimObra,
    DimOrigemArquivo,
    DimStatus,
    DimTempo,
    DocumentoLD,
    DocumentoSigem,
    Efetivo,
    FatoApontamentosManuais,
    FatoCronograma,
    FatoDocumentos,
    FatoEfetivo,
    FatoMedicao,
    FatoPt,
    FatoRdo,
    FatoSigem,
    FatoSuprimentos,
    Medicao,
    PT,
    RDO,
    RequisicaoMaterial,
)


def _get_or_create_dim_tempo(db: Session, base_date: date) -> DimTempo:
    row = db.query(DimTempo).filter(DimTempo.data == base_date).first()
    if row:
        return row
    row = DimTempo(
        data=base_date,
        ano=base_date.year,
        mes=base_date.month,
        dia=base_date.day,
        semana_ano=base_date.isocalendar()[1],
    )
    db.add(row)
    db.flush()
    return row


def _get_or_create_dim_obra(db: Session) -> DimObra:
    row = db.query(DimObra).filter(DimObra.nome == "Portal da Obra").first()
    if row:
        return row
    row = DimObra(nome="Portal da Obra")
    db.add(row)
    db.flush()
    return row


def _get_or_create_dim_status(db: Session, categoria: str, status: str) -> DimStatus:
    row = db.query(DimStatus).filter(DimStatus.categoria == categoria, DimStatus.status == status).first()
    if row:
        return row
    row = DimStatus(categoria=categoria, status=status)
    db.add(row)
    db.flush()
    return row


def _get_or_create_dim_origem(db: Session, arquivo: ArquivoOrigem) -> DimOrigemArquivo:
    row = db.query(DimOrigemArquivo).filter(DimOrigemArquivo.arquivo_origem_id == arquivo.id).first()
    if row:
        row.pasta = arquivo.pasta
        row.nome_arquivo = arquivo.nome_arquivo
        row.caminho = arquivo.caminho
        return row

    row = DimOrigemArquivo(
        arquivo_origem_id=arquivo.id,
        pasta=arquivo.pasta,
        nome_arquivo=arquivo.nome_arquivo,
        caminho=arquivo.caminho,
    )
    db.add(row)
    db.flush()
    return row


def refresh_analytical_model(db: Session, source_type: str, arquivo: ArquivoOrigem) -> int:
    """Atualiza camada analítica para o arquivo processado (sem tocar na origem)."""
    base_date = arquivo.data_modificacao_origem.date() if isinstance(arquivo.data_modificacao_origem, datetime) else date.today()
    dim_tempo = _get_or_create_dim_tempo(db, base_date)
    dim_obra = _get_or_create_dim_obra(db)
    dim_origem = _get_or_create_dim_origem(db, arquivo)

    affected = 0

    if source_type == "cronogramas":
        db.query(FatoCronograma).filter(FatoCronograma.origem_arquivo_id == dim_origem.id).delete()
        total = db.query(CronogramaAtividade).count()
        avg_prev = db.query(CronogramaAtividade).with_entities(CronogramaAtividade.avanco_previsto).all()
        avg_real = db.query(CronogramaAtividade).with_entities(CronogramaAtividade.avanco_real).all()
        prev = round(sum(x[0] for x in avg_prev) / total, 2) if total else 0
        real = round(sum(x[0] for x in avg_real) / total, 2) if total else 0
        db.add(
            FatoCronograma(
                tempo_id=dim_tempo.id,
                obra_id=dim_obra.id,
                origem_arquivo_id=dim_origem.id,
                atividade_codigo=f"SRC-{arquivo.id}",
                qtd_atividades=total,
                avanco_previsto=prev,
                avanco_real=real,
            )
        )
        affected = 1

    elif source_type == "ld_engenharia":
        status = _get_or_create_dim_status(db, "documento_ld", "processado")
        db.query(FatoDocumentos).filter(FatoDocumentos.origem_arquivo_id == dim_origem.id).delete()
        for doc in db.query(DocumentoLD).filter(DocumentoLD.arquivo_origem_id == arquivo.id).all():
            dim_doc = db.query(DimDocumento).filter(
                DimDocumento.numero_documento == doc.numero,
                DimDocumento.tipo_documento == "ld",
            ).first()
            if not dim_doc:
                dim_doc = DimDocumento(numero_documento=doc.numero, tipo_documento="ld", revisao=doc.revisao)
                db.add(dim_doc)
                db.flush()
            db.add(
                FatoDocumentos(
                    tempo_id=dim_tempo.id,
                    obra_id=dim_obra.id,
                    documento_id=dim_doc.id,
                    status_id=status.id,
                    origem_arquivo_id=dim_origem.id,
                    qtd_documentos=1,
                    aging_dias=0,
                )
            )
            affected += 1

    elif source_type == "sigem_historico":
        status = _get_or_create_dim_status(db, "sigem", "processado")
        db.query(FatoSigem).filter(FatoSigem.origem_arquivo_id == dim_origem.id).delete()
        for doc in db.query(DocumentoSigem).all():
            dim_doc = db.query(DimDocumento).filter(
                DimDocumento.numero_documento == doc.numero,
                DimDocumento.tipo_documento == "sigem",
            ).first()
            if not dim_doc:
                dim_doc = DimDocumento(numero_documento=doc.numero, tipo_documento="sigem", revisao="0")
                db.add(dim_doc)
                db.flush()
            db.add(
                FatoSigem(
                    tempo_id=dim_tempo.id,
                    obra_id=dim_obra.id,
                    documento_id=dim_doc.id,
                    status_id=status.id,
                    origem_arquivo_id=dim_origem.id,
                    qtd_eventos=1,
                )
            )
            affected += 1

    elif source_type == "medicao":
        db.query(FatoMedicao).filter(FatoMedicao.origem_arquivo_id == dim_origem.id).delete()
        valor_total = sum(row.valor for row in db.query(Medicao).all())
        db.add(
            FatoMedicao(
                tempo_id=dim_tempo.id,
                obra_id=dim_obra.id,
                origem_arquivo_id=dim_origem.id,
                valor_medido=valor_total,
                valor_acumulado=valor_total,
            )
        )
        affected = 1

    elif source_type == "pt":
        status = _get_or_create_dim_status(db, "pt", "processado")
        db.query(FatoPt).filter(FatoPt.origem_arquivo_id == dim_origem.id).delete()
        qtd = db.query(PT).count()
        db.add(
            FatoPt(
                tempo_id=dim_tempo.id,
                obra_id=dim_obra.id,
                status_id=status.id,
                origem_arquivo_id=dim_origem.id,
                qtd_pt=qtd,
            )
        )
        affected = 1

    elif source_type == "efetivo":
        db.query(FatoEfetivo).filter(FatoEfetivo.origem_arquivo_id == dim_origem.id).delete()
        qtd = sum(row.quantidade for row in db.query(Efetivo).all())
        db.add(
            FatoEfetivo(
                tempo_id=dim_tempo.id,
                obra_id=dim_obra.id,
                origem_arquivo_id=dim_origem.id,
                qtd_pessoas=qtd,
                horas_trabalhadas=float(qtd) * 8,
            )
        )
        affected = 1

    elif source_type == "requisicoes_materiais":
        status = _get_or_create_dim_status(db, "suprimentos", "processado")
        db.query(FatoSuprimentos).filter(FatoSuprimentos.origem_arquivo_id == dim_origem.id).delete()
        qtd = db.query(RequisicaoMaterial).count()
        db.add(
            FatoSuprimentos(
                tempo_id=dim_tempo.id,
                obra_id=dim_obra.id,
                status_id=status.id,
                origem_arquivo_id=dim_origem.id,
                qtd_requisicoes=qtd,
                lead_time_dias=21,
            )
        )
        affected = 1

    elif source_type == "rdo":
        db.query(FatoRdo).filter(FatoRdo.origem_arquivo_id == dim_origem.id).delete()
        qtd = db.query(RDO).count()
        db.add(
            FatoRdo(
                tempo_id=dim_tempo.id,
                obra_id=dim_obra.id,
                origem_arquivo_id=dim_origem.id,
                qtd_ocorrencias=qtd,
                horas_sem_produtividade=0,
            )
        )
        affected = 1

    # Mantém tabela criada/utilizada no modelo mesmo sem carga direta neste ciclo.
    _ = (DimArea, DimDisciplina, FatoApontamentosManuais)

    return affected
