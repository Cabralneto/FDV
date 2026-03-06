from __future__ import annotations

from datetime import date
from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from app.models.entities import (
    ArquivoOrigem,
    CronogramaAtividade,
    DocumentoHistorico,
    DocumentoLD,
    DocumentoSigem,
    Efetivo,
    Medicao,
    PT,
    RDO,
    RequisicaoMaterial,
)


def _load_dataframe(content: bytes) -> pd.DataFrame:
    if not content:
        return pd.DataFrame()
    try:
        df = pd.read_excel(BytesIO(content), engine="openpyxl")
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        return df.fillna("")
    except Exception:
        return pd.DataFrame()


def _value(row: pd.Series, *keys: str, default=None):
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def ingest_cronogramas(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(
            CronogramaAtividade(
                atividade_codigo=f"AUTO-{arquivo.id}",
                descricao=f"Carga automática de {arquivo.nome_arquivo}",
                avanco_previsto=0,
                avanco_real=0,
                status="importado",
            )
        )
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        codigo = str(_value(row, "atividade_codigo", "codigo", default="")).strip()
        if not codigo:
            continue
        db.add(
            CronogramaAtividade(
                atividade_codigo=codigo,
                descricao=str(_value(row, "descricao", "atividade", default="Sem descrição")),
                avanco_previsto=float(_value(row, "avanco_previsto", "previsto", default=0) or 0),
                avanco_real=float(_value(row, "avanco_real", "realizado", default=0) or 0),
                status=str(_value(row, "status", default="aberta")),
            )
        )
        inserted += 1
    return inserted


def ingest_ld_engenharia(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(DocumentoLD(numero=f"LD-{arquivo.id}", revisao="0", status="importado", arquivo_origem_id=arquivo.id))
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        numero = str(_value(row, "numero", "documento", default="")).strip()
        if not numero:
            continue
        db.add(
            DocumentoLD(
                numero=numero,
                revisao=str(_value(row, "revisao", default="0")),
                status=str(_value(row, "status", default="pendente")),
                arquivo_origem_id=arquivo.id,
            )
        )
        inserted += 1
    return inserted


def ingest_sigem_historico(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        numero = f"SIGEM-{arquivo.id}"
        db.add(DocumentoSigem(numero=numero, workflow="importado", status="pendente"))
        db.add(
            DocumentoHistorico(
                documento_tipo="sigem",
                documento_numero=numero,
                evento="ingestao_read_only",
            )
        )
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        numero = str(_value(row, "numero", "documento", default="")).strip()
        if not numero:
            continue
        db.add(
            DocumentoSigem(
                numero=numero,
                workflow=str(_value(row, "workflow", default="sem_workflow")),
                status=str(_value(row, "status", default="pendente")),
            )
        )
        db.add(
            DocumentoHistorico(
                documento_tipo="sigem",
                documento_numero=numero,
                evento=str(_value(row, "evento", default="atualizacao")),
            )
        )
        inserted += 1
    return inserted


def ingest_medicao(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(Medicao(referencia=date.today(), valor=0))
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        valor = float(_value(row, "valor", "valor_medido", default=0) or 0)
        db.add(Medicao(referencia=date.today(), valor=valor))
        inserted += 1
    return inserted


def ingest_pt(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(PT(numero=f"PT-{arquivo.id}", status="importado", data_emissao=date.today()))
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        numero = str(_value(row, "numero", "pt", default="")).strip()
        if not numero:
            continue
        db.add(
            PT(
                numero=numero,
                status=str(_value(row, "status", default="aberta")),
                data_emissao=date.today(),
            )
        )
        inserted += 1
    return inserted


def ingest_efetivo(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(Efetivo(referencia=date.today(), quantidade=0))
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        quantidade = int(float(_value(row, "quantidade", "efetivo", default=0) or 0))
        db.add(Efetivo(referencia=date.today(), quantidade=quantidade))
        inserted += 1
    return inserted


def ingest_requisicoes_materiais(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(
            RequisicaoMaterial(
                codigo=f"RM-{arquivo.id}",
                descricao=f"Importação de {arquivo.nome_arquivo}",
                status="aberta",
                data_necessidade=date.today(),
            )
        )
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        codigo = str(_value(row, "codigo", "rm", default="")).strip()
        if not codigo:
            continue
        db.add(
            RequisicaoMaterial(
                codigo=codigo,
                descricao=str(_value(row, "descricao", default="Material sem descrição")),
                status=str(_value(row, "status", default="aberta")),
                data_necessidade=date.today(),
            )
        )
        inserted += 1
    return inserted


def ingest_rdo(db: Session, arquivo: ArquivoOrigem, content: bytes) -> int:
    df = _load_dataframe(content)
    if df.empty:
        db.add(RDO(data=date.today(), frente="geral", ocorrencias=f"Importação de {arquivo.nome_arquivo}"))
        return 1

    inserted = 0
    for _, row in df.head(200).iterrows():
        db.add(
            RDO(
                data=date.today(),
                frente=str(_value(row, "frente", "area", default="geral")),
                ocorrencias=str(_value(row, "ocorrencias", "descricao", default="sem ocorrências")),
            )
        )
        inserted += 1
    return inserted
