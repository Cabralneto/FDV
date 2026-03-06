from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Obra(Base):
    __tablename__ = "obras"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), unique=True)


class Area(Base):
    __tablename__ = "areas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)


class Disciplina(Base):
    __tablename__ = "disciplinas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)


class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), index=True)


class Responsavel(Base):
    __tablename__ = "responsaveis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), index=True)


class Pacote(Base):
    __tablename__ = "pacotes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), index=True)
    descricao: Mapped[str] = mapped_column(String(255))


class EAP(Base):
    __tablename__ = "eap"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), index=True)
    descricao: Mapped[str] = mapped_column(String(255))


class CronogramaAtividade(Base):
    __tablename__ = "cronograma_atividades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atividade_codigo: Mapped[str] = mapped_column(String(50), index=True)
    descricao: Mapped[str] = mapped_column(String(255))
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("disciplinas.id"))
    data_inicio: Mapped[date | None] = mapped_column(Date)
    data_fim: Mapped[date | None] = mapped_column(Date)
    avanco_previsto: Mapped[float] = mapped_column(Float, default=0)
    avanco_real: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(50), default="aberta")


class CronogramaMarco(Base):
    __tablename__ = "cronograma_marcos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    data_planejada: Mapped[date | None] = mapped_column(Date)
    data_real: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="pendente")


class CronogramaHistorico(Base):
    __tablename__ = "cronograma_historico"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atividade_codigo: Mapped[str] = mapped_column(String(50), index=True)
    referencia: Mapped[date] = mapped_column(Date)
    avanco_previsto: Mapped[float] = mapped_column(Float)
    avanco_real: Mapped[float] = mapped_column(Float)


class CurvaS(Base):
    __tablename__ = "curva_s"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referencia: Mapped[date] = mapped_column(Date, index=True)
    previsto_fisico: Mapped[float] = mapped_column(Float)
    realizado_fisico: Mapped[float] = mapped_column(Float)
    previsto_financeiro: Mapped[float] = mapped_column(Float)
    realizado_financeiro: Mapped[float] = mapped_column(Float)


class DocumentoLD(Base):
    __tablename__ = "documentos_ld"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[str] = mapped_column(String(100), index=True)
    revisao: Mapped[str] = mapped_column(String(10), default="0")
    status: Mapped[str] = mapped_column(String(50), default="pendente")
    arquivo_origem_id: Mapped[int | None] = mapped_column(ForeignKey("arquivos_origem.id"))


class DocumentoSigem(Base):
    __tablename__ = "documentos_sigem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[str] = mapped_column(String(100), index=True)
    workflow: Mapped[str] = mapped_column(String(50), default="sem_workflow")
    status: Mapped[str] = mapped_column(String(50), default="pendente")


class DocumentoHistorico(Base):
    __tablename__ = "documentos_historico"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    documento_tipo: Mapped[str] = mapped_column(String(20))
    documento_numero: Mapped[str] = mapped_column(String(100), index=True)
    evento: Mapped[str] = mapped_column(String(100))
    data_evento: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ArquivoOrigem(Base):
    __tablename__ = "arquivos_origem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    biblioteca: Mapped[str] = mapped_column(String(100), default="SharePoint")
    pasta: Mapped[str] = mapped_column(String(255), index=True)
    nome_arquivo: Mapped[str] = mapped_column(String(255), index=True)
    caminho: Mapped[str] = mapped_column(String(1000))
    hash_arquivo: Mapped[str] = mapped_column(String(128), index=True)
    data_modificacao_origem: Mapped[datetime] = mapped_column(DateTime)
    data_ingestao: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status_processamento: Mapped[str] = mapped_column(String(50), default="novo")


class Medicao(Base):
    __tablename__ = "medicoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referencia: Mapped[date] = mapped_column(Date, index=True)
    fornecedor_id: Mapped[int | None] = mapped_column(ForeignKey("fornecedores.id"))
    valor: Mapped[float] = mapped_column(Float)


class Orcamento(Base):
    __tablename__ = "orcamentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pacote_id: Mapped[int | None] = mapped_column(ForeignKey("pacotes.id"))
    custo_base: Mapped[float] = mapped_column(Float)
    custo_atualizado: Mapped[float] = mapped_column(Float)


class CustoRealizado(Base):
    __tablename__ = "custos_realizados"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referencia: Mapped[date] = mapped_column(Date, index=True)
    pacote_id: Mapped[int | None] = mapped_column(ForeignKey("pacotes.id"))
    valor: Mapped[float] = mapped_column(Float)


class RequisicaoMaterial(Base):
    __tablename__ = "requisicoes_materiais"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), index=True)
    descricao: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), index=True)
    data_necessidade: Mapped[date | None] = mapped_column(Date)


class Pendencia(Base):
    __tablename__ = "pendencias"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    criticidade: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(50), index=True)
    responsavel_id: Mapped[int | None] = mapped_column(ForeignKey("responsaveis.id"))
    prazo: Mapped[date | None] = mapped_column(Date)


class PT(Base):
    __tablename__ = "pt"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[str] = mapped_column(String(50))
    data_emissao: Mapped[date | None] = mapped_column(Date)


class Efetivo(Base):
    __tablename__ = "efetivo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referencia: Mapped[date] = mapped_column(Date, index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    quantidade: Mapped[int] = mapped_column(Integer)


class RDO(Base):
    __tablename__ = "rdo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[date] = mapped_column(Date, index=True)
    frente: Mapped[str] = mapped_column(String(100))
    ocorrencias: Mapped[str] = mapped_column(Text)


class ApontamentoManual(Base):
    __tablename__ = "apontamentos_manuais"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(50), index=True)
    titulo: Mapped[str] = mapped_column(String(255))
    descricao: Mapped[str] = mapped_column(Text)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("disciplinas.id"))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FatoGerador(Base):
    __tablename__ = "fatos_geradores"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    impacto: Mapped[str] = mapped_column(String(50))


class PlanoAcao(Base):
    __tablename__ = "planos_acao"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pendencia_id: Mapped[int | None] = mapped_column(ForeignKey("pendencias.id"))
    descricao: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="aberto")


class Alerta(Base):
    __tablename__ = "alertas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    severidade: Mapped[str] = mapped_column(String(20), index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LogProcessamento(Base):
    __tablename__ = "logs_processamento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    processo: Mapped[str] = mapped_column(String(100), index=True)
    nivel: Mapped[str] = mapped_column(String(10), index=True)
    mensagem: Mapped[str] = mapped_column(Text)
    data_evento: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Perfil(Base):
    __tablename__ = "perfis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True)


class Permissao(Base):
    __tablename__ = "permissoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    perfil_id: Mapped[int | None] = mapped_column(ForeignKey("perfis.id"))


Index("idx_arquivo_unico", ArquivoOrigem.caminho, ArquivoOrigem.hash_arquivo)


# =========================
# Modelo dimensional (DW)
# =========================


class DimTempo(Base):
    __tablename__ = "dim_tempo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[date] = mapped_column(Date, unique=True, index=True)
    ano: Mapped[int] = mapped_column(Integer, index=True)
    mes: Mapped[int] = mapped_column(Integer, index=True)
    dia: Mapped[int] = mapped_column(Integer)
    semana_ano: Mapped[int] = mapped_column(Integer)


class DimObra(Base):
    __tablename__ = "dim_obra"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("obras.id"))
    nome: Mapped[str] = mapped_column(String(255), index=True)


class DimArea(Base):
    __tablename__ = "dim_area"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"))
    nome: Mapped[str] = mapped_column(String(100), index=True)


class DimDisciplina(Base):
    __tablename__ = "dim_disciplina"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("disciplinas.id"))
    nome: Mapped[str] = mapped_column(String(100), index=True)


class DimFornecedor(Base):
    __tablename__ = "dim_fornecedor"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fornecedor_id: Mapped[int | None] = mapped_column(ForeignKey("fornecedores.id"))
    nome: Mapped[str] = mapped_column(String(255), index=True)


class DimPacote(Base):
    __tablename__ = "dim_pacote"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pacote_id: Mapped[int | None] = mapped_column(ForeignKey("pacotes.id"))
    codigo: Mapped[str] = mapped_column(String(50), index=True)
    descricao: Mapped[str] = mapped_column(String(255))


class DimDocumento(Base):
    __tablename__ = "dim_documento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_documento: Mapped[str] = mapped_column(String(100), index=True)
    tipo_documento: Mapped[str] = mapped_column(String(30), index=True)
    revisao: Mapped[str] = mapped_column(String(20), default="0")


class DimStatus(Base):
    __tablename__ = "dim_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categoria: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[str] = mapped_column(String(50), index=True)


class DimOrigemArquivo(Base):
    __tablename__ = "dim_origem_arquivo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arquivo_origem_id: Mapped[int | None] = mapped_column(ForeignKey("arquivos_origem.id"))
    pasta: Mapped[str] = mapped_column(String(255), index=True)
    nome_arquivo: Mapped[str] = mapped_column(String(255))
    caminho: Mapped[str] = mapped_column(String(1000))


class FatoCronograma(Base):
    __tablename__ = "fato_cronograma"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("dim_area.id"), index=True)
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("dim_disciplina.id"), index=True)
    pacote_id: Mapped[int | None] = mapped_column(ForeignKey("dim_pacote.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    atividade_codigo: Mapped[str] = mapped_column(String(50), index=True)
    qtd_atividades: Mapped[int] = mapped_column(Integer, default=0)
    avanco_previsto: Mapped[float] = mapped_column(Float, default=0)
    avanco_real: Mapped[float] = mapped_column(Float, default=0)


class FatoDocumentos(Base):
    __tablename__ = "fato_documentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("dim_area.id"), index=True)
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("dim_disciplina.id"), index=True)
    fornecedor_id: Mapped[int | None] = mapped_column(ForeignKey("dim_fornecedor.id"), index=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("dim_documento.id"), index=True)
    status_id: Mapped[int | None] = mapped_column(ForeignKey("dim_status.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    qtd_documentos: Mapped[int] = mapped_column(Integer, default=1)
    aging_dias: Mapped[int] = mapped_column(Integer, default=0)


class FatoSigem(Base):
    __tablename__ = "fato_sigem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("dim_documento.id"), index=True)
    status_id: Mapped[int | None] = mapped_column(ForeignKey("dim_status.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    qtd_eventos: Mapped[int] = mapped_column(Integer, default=1)


class FatoMedicao(Base):
    __tablename__ = "fato_medicao"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    fornecedor_id: Mapped[int | None] = mapped_column(ForeignKey("dim_fornecedor.id"), index=True)
    pacote_id: Mapped[int | None] = mapped_column(ForeignKey("dim_pacote.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    valor_medido: Mapped[float] = mapped_column(Float, default=0)
    valor_acumulado: Mapped[float] = mapped_column(Float, default=0)


class FatoEfetivo(Base):
    __tablename__ = "fato_efetivo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("dim_area.id"), index=True)
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("dim_disciplina.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    qtd_pessoas: Mapped[int] = mapped_column(Integer, default=0)
    horas_trabalhadas: Mapped[float] = mapped_column(Float, default=0)


class FatoPt(Base):
    __tablename__ = "fato_pt"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("dim_area.id"), index=True)
    status_id: Mapped[int | None] = mapped_column(ForeignKey("dim_status.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    qtd_pt: Mapped[int] = mapped_column(Integer, default=1)


class FatoSuprimentos(Base):
    __tablename__ = "fato_suprimentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    fornecedor_id: Mapped[int | None] = mapped_column(ForeignKey("dim_fornecedor.id"), index=True)
    pacote_id: Mapped[int | None] = mapped_column(ForeignKey("dim_pacote.id"), index=True)
    status_id: Mapped[int | None] = mapped_column(ForeignKey("dim_status.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    qtd_requisicoes: Mapped[int] = mapped_column(Integer, default=1)
    lead_time_dias: Mapped[int] = mapped_column(Integer, default=0)


class FatoRdo(Base):
    __tablename__ = "fato_rdo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("dim_area.id"), index=True)
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("dim_disciplina.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    qtd_ocorrencias: Mapped[int] = mapped_column(Integer, default=0)
    horas_sem_produtividade: Mapped[float] = mapped_column(Float, default=0)


class FatoApontamentosManuais(Base):
    __tablename__ = "fato_apontamentos_manuais"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tempo_id: Mapped[int] = mapped_column(ForeignKey("dim_tempo.id"), index=True)
    obra_id: Mapped[int | None] = mapped_column(ForeignKey("dim_obra.id"), index=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("dim_area.id"), index=True)
    disciplina_id: Mapped[int | None] = mapped_column(ForeignKey("dim_disciplina.id"), index=True)
    status_id: Mapped[int | None] = mapped_column(ForeignKey("dim_status.id"), index=True)
    origem_arquivo_id: Mapped[int | None] = mapped_column(ForeignKey("dim_origem_arquivo.id"))
    tipo_apontamento: Mapped[str] = mapped_column(String(50), index=True)
    qtd_apontamentos: Mapped[int] = mapped_column(Integer, default=1)


Index("idx_dim_documento_numero_tipo", DimDocumento.numero_documento, DimDocumento.tipo_documento)
Index("idx_fato_cronograma_periodo", FatoCronograma.tempo_id, FatoCronograma.area_id, FatoCronograma.disciplina_id)
Index("idx_fato_documentos_periodo", FatoDocumentos.tempo_id, FatoDocumentos.documento_id, FatoDocumentos.status_id)
Index("idx_fato_medicao_periodo", FatoMedicao.tempo_id, FatoMedicao.fornecedor_id, FatoMedicao.pacote_id)
Index("idx_fato_efetivo_periodo", FatoEfetivo.tempo_id, FatoEfetivo.area_id, FatoEfetivo.disciplina_id)
Index("idx_fato_suprimentos_periodo", FatoSuprimentos.tempo_id, FatoSuprimentos.fornecedor_id, FatoSuprimentos.status_id)
