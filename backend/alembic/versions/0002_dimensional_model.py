"""add dimensional model for analytics

Revision ID: 0002_dimensional_model
Revises: 0001_initial
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_dimensional_model"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dim_tempo",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("data", sa.Date(), nullable=False, unique=True),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("semana_ano", sa.Integer(), nullable=False),
    )
    op.create_index("ix_dim_tempo_data", "dim_tempo", ["data"])
    op.create_index("ix_dim_tempo_ano", "dim_tempo", ["ano"])
    op.create_index("ix_dim_tempo_mes", "dim_tempo", ["mes"])

    op.create_table(
        "dim_obra",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("obras.id")),
        sa.Column("nome", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_dim_obra_nome", "dim_obra", ["nome"])

    op.create_table(
        "dim_area",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("areas.id")),
        sa.Column("nome", sa.String(length=100), nullable=False),
    )
    op.create_index("ix_dim_area_nome", "dim_area", ["nome"])

    op.create_table(
        "dim_disciplina",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("disciplina_id", sa.Integer(), sa.ForeignKey("disciplinas.id")),
        sa.Column("nome", sa.String(length=100), nullable=False),
    )
    op.create_index("ix_dim_disciplina_nome", "dim_disciplina", ["nome"])

    op.create_table(
        "dim_fornecedor",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("fornecedor_id", sa.Integer(), sa.ForeignKey("fornecedores.id")),
        sa.Column("nome", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_dim_fornecedor_nome", "dim_fornecedor", ["nome"])

    op.create_table(
        "dim_pacote",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pacote_id", sa.Integer(), sa.ForeignKey("pacotes.id")),
        sa.Column("codigo", sa.String(length=50), nullable=False),
        sa.Column("descricao", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_dim_pacote_codigo", "dim_pacote", ["codigo"])

    op.create_table(
        "dim_documento",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("numero_documento", sa.String(length=100), nullable=False),
        sa.Column("tipo_documento", sa.String(length=30), nullable=False),
        sa.Column("revisao", sa.String(length=20), nullable=False, server_default="0"),
    )
    op.create_index("ix_dim_documento_numero_documento", "dim_documento", ["numero_documento"])
    op.create_index("ix_dim_documento_tipo_documento", "dim_documento", ["tipo_documento"])
    op.create_index("idx_dim_documento_numero_tipo", "dim_documento", ["numero_documento", "tipo_documento"])

    op.create_table(
        "dim_status",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("categoria", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
    )
    op.create_index("ix_dim_status_categoria", "dim_status", ["categoria"])
    op.create_index("ix_dim_status_status", "dim_status", ["status"])

    op.create_table(
        "dim_origem_arquivo",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("arquivo_origem_id", sa.Integer(), sa.ForeignKey("arquivos_origem.id")),
        sa.Column("pasta", sa.String(length=255), nullable=False),
        sa.Column("nome_arquivo", sa.String(length=255), nullable=False),
        sa.Column("caminho", sa.String(length=1000), nullable=False),
    )
    op.create_index("ix_dim_origem_arquivo_pasta", "dim_origem_arquivo", ["pasta"])

    op.create_table(
        "fato_cronograma",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("dim_area.id")),
        sa.Column("disciplina_id", sa.Integer(), sa.ForeignKey("dim_disciplina.id")),
        sa.Column("pacote_id", sa.Integer(), sa.ForeignKey("dim_pacote.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("atividade_codigo", sa.String(length=50), nullable=False),
        sa.Column("qtd_atividades", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("avanco_previsto", sa.Float(), nullable=False, server_default="0"),
        sa.Column("avanco_real", sa.Float(), nullable=False, server_default="0"),
    )
    op.create_index("ix_fato_cronograma_tempo_id", "fato_cronograma", ["tempo_id"])
    op.create_index("idx_fato_cronograma_periodo", "fato_cronograma", ["tempo_id", "area_id", "disciplina_id"])

    op.create_table(
        "fato_documentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("dim_area.id")),
        sa.Column("disciplina_id", sa.Integer(), sa.ForeignKey("dim_disciplina.id")),
        sa.Column("fornecedor_id", sa.Integer(), sa.ForeignKey("dim_fornecedor.id")),
        sa.Column("documento_id", sa.Integer(), sa.ForeignKey("dim_documento.id"), nullable=False),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("dim_status.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("qtd_documentos", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("aging_dias", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_fato_documentos_tempo_id", "fato_documentos", ["tempo_id"])
    op.create_index("idx_fato_documentos_periodo", "fato_documentos", ["tempo_id", "documento_id", "status_id"])

    op.create_table(
        "fato_sigem",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("documento_id", sa.Integer(), sa.ForeignKey("dim_documento.id"), nullable=False),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("dim_status.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("qtd_eventos", sa.Integer(), nullable=False, server_default="1"),
    )

    op.create_table(
        "fato_medicao",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("fornecedor_id", sa.Integer(), sa.ForeignKey("dim_fornecedor.id")),
        sa.Column("pacote_id", sa.Integer(), sa.ForeignKey("dim_pacote.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("valor_medido", sa.Float(), nullable=False, server_default="0"),
        sa.Column("valor_acumulado", sa.Float(), nullable=False, server_default="0"),
    )
    op.create_index("ix_fato_medicao_tempo_id", "fato_medicao", ["tempo_id"])
    op.create_index("idx_fato_medicao_periodo", "fato_medicao", ["tempo_id", "fornecedor_id", "pacote_id"])

    op.create_table(
        "fato_efetivo",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("dim_area.id")),
        sa.Column("disciplina_id", sa.Integer(), sa.ForeignKey("dim_disciplina.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("qtd_pessoas", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("horas_trabalhadas", sa.Float(), nullable=False, server_default="0"),
    )
    op.create_index("ix_fato_efetivo_tempo_id", "fato_efetivo", ["tempo_id"])
    op.create_index("idx_fato_efetivo_periodo", "fato_efetivo", ["tempo_id", "area_id", "disciplina_id"])

    op.create_table(
        "fato_pt",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("dim_area.id")),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("dim_status.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("qtd_pt", sa.Integer(), nullable=False, server_default="1"),
    )

    op.create_table(
        "fato_suprimentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("fornecedor_id", sa.Integer(), sa.ForeignKey("dim_fornecedor.id")),
        sa.Column("pacote_id", sa.Integer(), sa.ForeignKey("dim_pacote.id")),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("dim_status.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("qtd_requisicoes", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("lead_time_dias", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_fato_suprimentos_tempo_id", "fato_suprimentos", ["tempo_id"])
    op.create_index(
        "idx_fato_suprimentos_periodo",
        "fato_suprimentos",
        ["tempo_id", "fornecedor_id", "status_id"],
    )

    op.create_table(
        "fato_rdo",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("dim_area.id")),
        sa.Column("disciplina_id", sa.Integer(), sa.ForeignKey("dim_disciplina.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("qtd_ocorrencias", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("horas_sem_produtividade", sa.Float(), nullable=False, server_default="0"),
    )

    op.create_table(
        "fato_apontamentos_manuais",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tempo_id", sa.Integer(), sa.ForeignKey("dim_tempo.id"), nullable=False),
        sa.Column("obra_id", sa.Integer(), sa.ForeignKey("dim_obra.id")),
        sa.Column("area_id", sa.Integer(), sa.ForeignKey("dim_area.id")),
        sa.Column("disciplina_id", sa.Integer(), sa.ForeignKey("dim_disciplina.id")),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("dim_status.id")),
        sa.Column("origem_arquivo_id", sa.Integer(), sa.ForeignKey("dim_origem_arquivo.id")),
        sa.Column("tipo_apontamento", sa.String(length=50), nullable=False),
        sa.Column("qtd_apontamentos", sa.Integer(), nullable=False, server_default="1"),
    )


def downgrade() -> None:
    op.drop_table("fato_apontamentos_manuais")
    op.drop_table("fato_rdo")
    op.drop_index("idx_fato_suprimentos_periodo", table_name="fato_suprimentos")
    op.drop_index("ix_fato_suprimentos_tempo_id", table_name="fato_suprimentos")
    op.drop_table("fato_suprimentos")
    op.drop_table("fato_pt")
    op.drop_index("idx_fato_efetivo_periodo", table_name="fato_efetivo")
    op.drop_index("ix_fato_efetivo_tempo_id", table_name="fato_efetivo")
    op.drop_table("fato_efetivo")
    op.drop_index("idx_fato_medicao_periodo", table_name="fato_medicao")
    op.drop_index("ix_fato_medicao_tempo_id", table_name="fato_medicao")
    op.drop_table("fato_medicao")
    op.drop_table("fato_sigem")
    op.drop_index("idx_fato_documentos_periodo", table_name="fato_documentos")
    op.drop_index("ix_fato_documentos_tempo_id", table_name="fato_documentos")
    op.drop_table("fato_documentos")
    op.drop_index("idx_fato_cronograma_periodo", table_name="fato_cronograma")
    op.drop_index("ix_fato_cronograma_tempo_id", table_name="fato_cronograma")
    op.drop_table("fato_cronograma")

    op.drop_index("ix_dim_origem_arquivo_pasta", table_name="dim_origem_arquivo")
    op.drop_table("dim_origem_arquivo")
    op.drop_index("ix_dim_status_status", table_name="dim_status")
    op.drop_index("ix_dim_status_categoria", table_name="dim_status")
    op.drop_table("dim_status")
    op.drop_index("idx_dim_documento_numero_tipo", table_name="dim_documento")
    op.drop_index("ix_dim_documento_tipo_documento", table_name="dim_documento")
    op.drop_index("ix_dim_documento_numero_documento", table_name="dim_documento")
    op.drop_table("dim_documento")
    op.drop_index("ix_dim_pacote_codigo", table_name="dim_pacote")
    op.drop_table("dim_pacote")
    op.drop_index("ix_dim_fornecedor_nome", table_name="dim_fornecedor")
    op.drop_table("dim_fornecedor")
    op.drop_index("ix_dim_disciplina_nome", table_name="dim_disciplina")
    op.drop_table("dim_disciplina")
    op.drop_index("ix_dim_area_nome", table_name="dim_area")
    op.drop_table("dim_area")
    op.drop_index("ix_dim_obra_nome", table_name="dim_obra")
    op.drop_table("dim_obra")
    op.drop_index("ix_dim_tempo_mes", table_name="dim_tempo")
    op.drop_index("ix_dim_tempo_ano", table_name="dim_tempo")
    op.drop_index("ix_dim_tempo_data", table_name="dim_tempo")
    op.drop_table("dim_tempo")
