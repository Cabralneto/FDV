import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";

const rows = [
  { modulo: "alertas", indicador: "Exemplo 1", valor: 123 },
  { modulo: "alertas", indicador: "Exemplo 2", valor: 456 },
  { modulo: "alertas", indicador: "Exemplo 3", valor: 789 },
];

export default function Page() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4 capitalize">alertas</h2>
      <DataTable rows={rows} />
    </PageShell>
  );
}
