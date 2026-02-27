# Arquitetura proposta

## 1. Objetivo
Sistema interno para ingestão contínua de documentação técnica de obras industriais, com histórico de revisões, busca textual e consolidação de dados de engenharia.

## 2. Componentes

### 2.1 Backend (FastAPI)
- Recebe upload de PDF
- Identifica código do documento e revisão por regex
- Mantém histórico de revisões e revisão ativa
- Extrai texto (pdfplumber/PyMuPDF)
- Estrutura entidades técnicas (circuitos, materiais, cabos)
- Indexa texto em PostgreSQL FTS

### 2.2 Banco (PostgreSQL)
- Modelo relacional normalizado
- Controle de versões por documento
- Tabelas técnicas e relacionamento por revisão
- Índices para performance (GIN + btree)

### 2.3 Frontend (Next.js)
- Tela de upload
- Listagem de documentos e revisões
- Busca textual
- Dashboard técnico (potência total, potência por área, materiais)

## 3. Pipeline
1. **Upload**: usuário envia PDF
2. **Identificação**: regex identifica `document_code` e `revision`
3. **Versionamento**: revisão anterior ativa é desativada
4. **Extração**: conteúdo textual bruto do PDF
5. **Indexação**: `tsvector` atualizado para busca
6. **Estruturação**: parser extrai circuitos, potência, disjuntor, cabo e materiais
7. **Armazenamento**: persiste metadados + entidades técnicas

## 4. Escalabilidade e evolução
- Estrutura preparada para múltiplas obras (`projects`)
- Upload incremental sem sobrescrita histórica
- Evolução de parser por tipo de documento (DE/LI/LM)
- Possibilidade de fila assíncrona para alto volume
