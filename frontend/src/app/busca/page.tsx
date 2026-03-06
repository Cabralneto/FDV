import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";

const rows = [
  { modulo: "busca", indicador: "Exemplo 1", valor: 123 },
  { modulo: "busca", indicador: "Exemplo 2", valor: 456 },
  { modulo: "busca", indicador: "Exemplo 3", valor: 789 },
];

export default function Page() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4 capitalize">busca</h2>
      <DataTable rows={rows} />
    </PageShell>
  );
}
