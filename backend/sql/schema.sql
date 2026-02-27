-- Extensões úteis
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Projetos/obras
CREATE TABLE IF NOT EXISTS projects (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Áreas físicas
CREATE TABLE IF NOT EXISTS areas (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    UNIQUE(project_id, name)
);

-- Documento lógico (sem revisão)
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    document_code VARCHAR(80) NOT NULL,
    document_type VARCHAR(10) NOT NULL,
    title VARCHAR(255),
    area_id BIGINT REFERENCES areas(id),
    equipment_tag VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(project_id, document_code)
);

-- Revisões de documento
CREATE TABLE IF NOT EXISTS document_revisions (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    revision VARCHAR(16) NOT NULL,
    revision_order INT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    checksum_sha256 VARCHAR(64),
    extracted_text TEXT,
    search_vector tsvector,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, revision)
);

CREATE INDEX IF NOT EXISTS idx_document_revisions_document_id ON document_revisions(document_id);
CREATE INDEX IF NOT EXISTS idx_document_revisions_active ON document_revisions(document_id, is_active);
CREATE INDEX IF NOT EXISTS idx_document_revisions_search_vector ON document_revisions USING GIN(search_vector);

-- Circuitos
CREATE TABLE IF NOT EXISTS circuits (
    id BIGSERIAL PRIMARY KEY,
    revision_id BIGINT NOT NULL REFERENCES document_revisions(id) ON DELETE CASCADE,
    area_id BIGINT REFERENCES areas(id),
    circuit_code VARCHAR(100) NOT NULL,
    equipment_tag VARCHAR(100),
    description TEXT,
    power_kw NUMERIC(12,3),
    current_a NUMERIC(12,3),
    breaker_a NUMERIC(12,3),
    cable_spec VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_circuits_revision_id ON circuits(revision_id);
CREATE INDEX IF NOT EXISTS idx_circuits_area_id ON circuits(area_id);
CREATE INDEX IF NOT EXISTS idx_circuits_code ON circuits(circuit_code);

-- Materiais
CREATE TABLE IF NOT EXISTS materials (
    id BIGSERIAL PRIMARY KEY,
    revision_id BIGINT NOT NULL REFERENCES document_revisions(id) ON DELETE CASCADE,
    area_id BIGINT REFERENCES areas(id),
    material_code VARCHAR(100),
    description TEXT NOT NULL,
    unit VARCHAR(20),
    quantity NUMERIC(14,3) NOT NULL DEFAULT 0,
    discipline VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_materials_revision_id ON materials(revision_id);
CREATE INDEX IF NOT EXISTS idx_materials_area_id ON materials(area_id);
CREATE INDEX IF NOT EXISTS idx_materials_code ON materials(material_code);

-- DE/PARA
CREATE TABLE IF NOT EXISTS de_para_mappings (
    id BIGSERIAL PRIMARY KEY,
    revision_id BIGINT NOT NULL REFERENCES document_revisions(id) ON DELETE CASCADE,
    origin_tag VARCHAR(100) NOT NULL,
    destination_tag VARCHAR(100) NOT NULL,
    signal_type VARCHAR(50),
    notes TEXT
);

-- Consulta útil: somente revisão ativa
CREATE OR REPLACE VIEW v_active_document_revisions AS
SELECT dr.*
FROM document_revisions dr
WHERE dr.is_active = TRUE;
