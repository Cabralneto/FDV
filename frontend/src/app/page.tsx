import { getDocuments, getSummary } from "../lib/api";

export default async function HomePage() {
  const [summary, documents] = await Promise.all([getSummary(), getDocuments()]);

  return (
    <main style={{ fontFamily: "Arial", padding: 24 }}>
      <h1>Sistema Técnico de Documentos</h1>
      <section>
        <h2>Dashboard</h2>
        <p><strong>Potência total instalada:</strong> {summary.total_power_kw} kW</p>
        <h3>Potência por área</h3>
        <ul>
          {Object.entries(summary.power_by_area).map(([area, value]) => (
            <li key={area}>{area}: {String(value)} kW</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Documentos ativos</h2>
        <table border={1} cellPadding={8}>
          <thead>
            <tr>
              <th>Código</th>
              <th>Tipo</th>
              <th>Revisão ativa</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc: any) => (
              <tr key={doc.id}>
                <td>{doc.document_code}</td>
                <td>{doc.document_type}</td>
                <td>{doc.active_revision ?? "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
