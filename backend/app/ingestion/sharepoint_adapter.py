from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from app.core.config import settings


@dataclass
class SourceFile:
    pasta: str
    nome_arquivo: str
    caminho: str
    data_modificacao: datetime
    hash_arquivo: str


class SharePointReadOnlyAdapter:
    """Adapter estritamente somente leitura para integração SharePoint.

    Regras de segurança:
    - Não cria, altera, renomeia, move ou remove arquivos na origem.
    - Apenas lista metadados e lê conteúdo para ingestão interna.
    """

    MONITORED_FOLDERS = [
        "1. CRONOGRAMAS",
        "26. LD ENGENHARIA",
        "27. SIGEM_HISTÓRICO",
        "5. MEDIÇÃO",
        "21. PT",
        "25. EFETIVO",
        "31. REQUISIÇÃO DE MATERIAIS",
        "35. RDO_HISTÓRICO",
    ]

    def list_files(self) -> list[SourceFile]:
        if settings.sharepoint_mode == "mock":
            return self._list_files_mock()
        return self._list_files_from_local_mirror()

    def read_file_bytes(self, source_file: SourceFile) -> bytes:
        """Retorna bytes do arquivo em modo somente leitura."""
        if settings.sharepoint_mode == "mock":
            return b""

        file_path = Path(source_file.caminho)
        if not file_path.exists() or not file_path.is_file():
            return b""
        return file_path.read_bytes()

    def _list_files_mock(self) -> list[SourceFile]:
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        items: list[SourceFile] = []

        for idx, folder in enumerate(self.MONITORED_FOLDERS, start=1):
            name = f"fonte_{idx:02d}.xlsx"
            path = f"/sharepoint/{folder}/{name}"
            items.append(
                SourceFile(
                    pasta=folder,
                    nome_arquivo=name,
                    caminho=path,
                    data_modificacao=now,
                    hash_arquivo=sha256(path.encode("utf-8")).hexdigest(),
                )
            )

        return items

    def _list_files_from_local_mirror(self) -> list[SourceFile]:
        """Modo de desenvolvimento para leitura a partir de espelho local read-only."""
        root = Path(settings.sharepoint_site_url or ".")
        if not root.exists():
            return []

        files: list[SourceFile] = []
        for folder in self.MONITORED_FOLDERS:
            folder_path = root / folder
            if not folder_path.exists() or not folder_path.is_dir():
                continue

            for candidate in folder_path.glob("**/*"):
                if not candidate.is_file():
                    continue
                if candidate.suffix.lower() not in {".xlsx", ".xlsm", ".xls"}:
                    continue

                stat = candidate.stat()
                hash_value = sha256(f"{candidate}:{stat.st_mtime_ns}:{stat.st_size}".encode("utf-8")).hexdigest()
                files.append(
                    SourceFile(
                        pasta=folder,
                        nome_arquivo=candidate.name,
                        caminho=str(candidate),
                        data_modificacao=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                        hash_arquivo=hash_value,
                    )
                )

        return files
