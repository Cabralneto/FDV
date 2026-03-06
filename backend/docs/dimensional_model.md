# Modelo de dados analítico (fatos e dimensões)

Este modelo foi criado para consultas gerenciais de alto desempenho, com granularidade por período e rastreabilidade da origem.

## Dimensões

- **dim_tempo**: calendário analítico (dia, mês, ano e semana) para cortes temporais de todos os fatos.
- **dim_obra**: contexto da obra para análises multiobra.
- **dim_area**: área física/funcional da obra.
- **dim_disciplina**: disciplina técnica (civil, mecânica, elétrica etc.).
- **dim_fornecedor**: fornecedor associado aos eventos financeiros/operacionais.
- **dim_pacote**: pacote de trabalho/contrato para agrupamento de custos, medição e suprimentos.
- **dim_documento**: identificação do documento (número, tipo, revisão) para LD e SIGEM.
- **dim_status**: domínio de status por categoria (documento, PT, requisição, pendência etc.).
- **dim_origem_arquivo**: proveniência dos dados ingeridos (pasta, nome e caminho do arquivo de origem).

## Fatos

- **fato_cronograma**: métricas de planejamento (qtd atividades, avanço previsto e real) por período/área/disciplina/pacote.
- **fato_documentos**: volume e aging documental por período e dimensões de documento/status.
- **fato_sigem**: eventos e movimentações SIGEM por documento e status.
- **fato_medicao**: valores de medição (período e acumulado) por fornecedor/pacote.
- **fato_efetivo**: quantitativo de pessoas e horas trabalhadas por área/disciplina e período.
- **fato_pt**: quantidade de permissões de trabalho por status/área/período.
- **fato_suprimentos**: requisições e lead time por fornecedor/pacote/status/período.
- **fato_rdo**: ocorrências e horas improdutivas registradas no RDO.
- **fato_apontamentos_manuais**: apontamentos internos por tipo, status e recortes organizacionais.

## Relacionamentos principais

- Todas as tabelas de fato possuem `tempo_id -> dim_tempo.id`.
- As tabelas de fato se relacionam com dimensões de contexto (`dim_obra`, `dim_area`, `dim_disciplina`, `dim_fornecedor`, `dim_pacote`) conforme o domínio.
- Fatos de documentos/SIGEM usam `documento_id -> dim_documento.id` e `status_id -> dim_status.id`.
- Todas as tabelas de fato podem manter `origem_arquivo_id -> dim_origem_arquivo.id` para rastreabilidade da ingestão read-only.

## Observação de arquitetura

O modelo dimensional é destinado à camada analítica e não substitui as tabelas transacionais já existentes. A estratégia recomendada é carregar dimensões e fatos via ETL/ELT interno após a ingestão read-only do SharePoint.
