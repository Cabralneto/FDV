from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.ingestion.analytics_refresher import refresh_analytical_model
from app.ingestion.domain_ingestors import (
    ingest_cronogramas,
    ingest_efetivo,
    ingest_ld_engenharia,
    ingest_medicao,
    ingest_pt,
    ingest_rdo,
    ingest_requisicoes_materiais,
    ingest_sigem_historico,
)
from app.ingestion.sharepoint_adapter import SharePointReadOnlyAdapter, SourceFile
from app.models.entities import ArquivoOrigem, LogProcessamento


def _source_key(folder_name: str) -> str:
    normalized = folder_name.upper()
    if "CRONOGRAMA" in normalized:
        return "cronogramas"
    if "LD ENGENHARIA" in normalized:
        return "ld_engenharia"
    if "SIGEM" in normalized:
        return "sigem_historico"
    if "MEDI" in normalized:
        return "medicao"
    if normalized.strip().endswith("PT") or " PT" in normalized:
        return "pt"
    if "EFETIVO" in normalized:
        return "efetivo"
    if "REQUISI" in normalized:
        return "requisicoes_materiais"
    if "RDO" in normalized:
        return "rdo"
    return "desconhecido"


def _needs_reprocess(db: Session, source_file: SourceFile) -> bool:
    latest = (
        db.query(ArquivoOrigem)
        .filter(ArquivoOrigem.caminho == source_file.caminho)
        .order_by(ArquivoOrigem.data_modificacao_origem.desc(), ArquivoOrigem.id.desc())
        .first()
    )
    if not latest:
        return True

    if source_file.data_modificacao > latest.data_modificacao_origem:
        return True

    if source_file.data_modificacao == latest.data_modificacao_origem and source_file.hash_arquivo != latest.hash_arquivo:
        return True

    return False


def run_ingestion(db: Session) -> dict:
    adapter = SharePointReadOnlyAdapter()
    files = adapter.list_files()

    processed_files = 0
    inserted_rows = 0
    refreshed_analytics = 0
    skipped = 0
    errors = 0

    ingestors = {
        "cronogramas": ingest_cronogramas,
        "ld_engenharia": ingest_ld_engenharia,
        "sigem_historico": ingest_sigem_historico,
        "medicao": ingest_medicao,
        "pt": ingest_pt,
        "efetivo": ingest_efetivo,
        "requisicoes_materiais": ingest_requisicoes_materiais,
        "rdo": ingest_rdo,
    }

    for source_file in files:
        source_type = _source_key(source_file.pasta)
        if source_type == "desconhecido":
            skipped += 1
            continue

        if not _needs_reprocess(db, source_file):
            skipped += 1
            continue

        arquivo = ArquivoOrigem(
            pasta=source_file.pasta,
            nome_arquivo=source_file.nome_arquivo,
            caminho=source_file.caminho,
            hash_arquivo=source_file.hash_arquivo,
            data_modificacao_origem=source_file.data_modificacao,
            data_ingestao=datetime.utcnow(),
            status_processamento="processando",
        )
        db.add(arquivo)
        db.flush()

        try:
            content = adapter.read_file_bytes(source_file)
            inserted = ingestors[source_type](db, arquivo, content)
            refreshed = refresh_analytical_model(db, source_type, arquivo)
            arquivo.status_processamento = "processado"
            processed_files += 1
            inserted_rows += inserted
            refreshed_analytics += refreshed
        except Exception as exc:  # noqa: BLE001
            arquivo.status_processamento = "erro"
            errors += 1
            db.add(
                LogProcessamento(
                    processo="ingestao_sharepoint_read_only",
                    nivel="ERROR",
                    mensagem=f"Falha ao processar {source_file.caminho} ({source_type}): {exc}",
                )
            )

    db.add(
        LogProcessamento(
            processo="ingestao_sharepoint_read_only",
            nivel="INFO",
            mensagem=(
                "Execução read-only incremental finalizada: "
                f"{processed_files} arquivo(s) reprocessado(s), {inserted_rows} registro(s) transacionais inserido(s), "
                f"{refreshed_analytics} registro(s) analítico(s) atualizado(s), "
                f"{skipped} arquivo(s) não alterado(s)/ignorado(s), {errors} erro(s)."
            ),
        )
    )
    db.commit()
    return {
        "mode": "read_only",
        "found": len(files),
        "processed_files": processed_files,
        "inserted_rows": inserted_rows,
        "refreshed_analytics": refreshed_analytics,
        "skipped": skipped,
        "errors": errors,
    }
