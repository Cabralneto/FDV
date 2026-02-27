-- Potência total instalada (somente revisões ativas)
SELECT COALESCE(SUM(c.power_kw), 0) AS total_power_kw
FROM circuits c
JOIN document_revisions dr ON dr.id = c.revision_id
WHERE dr.is_active = TRUE;

-- Potência por área
SELECT a.name AS area, COALESCE(SUM(c.power_kw), 0) AS power_kw
FROM areas a
LEFT JOIN circuits c ON c.area_id = a.id
LEFT JOIN document_revisions dr ON dr.id = c.revision_id
WHERE dr.is_active = TRUE OR dr.id IS NULL
GROUP BY a.name
ORDER BY a.name;

-- Busca por equipamento (documentos ativos)
SELECT d.document_code,
       dr.revision,
       c.equipment_tag,
       c.circuit_code,
       c.power_kw
FROM circuits c
JOIN document_revisions dr ON dr.id = c.revision_id
JOIN documents d ON d.id = dr.document_id
WHERE dr.is_active = TRUE
  AND c.equipment_tag ILIKE '%BOMBA-101%'
ORDER BY d.document_code;

-- Consulta por circuito
SELECT d.document_code,
       dr.revision,
       c.circuit_code,
       c.power_kw,
       c.current_a,
       c.breaker_a,
       c.cable_spec
FROM circuits c
JOIN document_revisions dr ON dr.id = c.revision_id
JOIN documents d ON d.id = dr.document_id
WHERE dr.is_active = TRUE
  AND c.circuit_code = 'CIR-2201';
