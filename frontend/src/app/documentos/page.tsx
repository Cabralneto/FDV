import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";

const rows = [
  { modulo: "documentos", indicador: "Exemplo 1", valor: 123 },
  { modulo: "documentos", indicador: "Exemplo 2", valor: 456 },
  { modulo: "documentos", indicador: "Exemplo 3", valor: 789 },
];

export default function Page() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4 capitalize">documentos</h2>
      <DataTable rows={rows} />
    </PageShell>
  );
}
