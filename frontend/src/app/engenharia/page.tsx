"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

const statusDocs = [
  { name: "Aprovado", value: 740 },
  { name: "Em análise", value: 228 },
  { name: "Comentado", value: 160 },
  { name: "Pendente", value: 94 },
];

const COLORS = ["#16a34a", "#2563eb", "#f59e0b", "#dc2626"];

const rows = [
  { documento: "LD-001-EL-230", revisao: "3", ld: "Emitido", sigem: "Comentado", disciplina: "Elétrica", aging: 12 },
  { documento: "LD-112-MC-010", revisao: "1", ld: "Em análise", sigem: "Em análise", disciplina: "Mecânica", aging: 7 },
  { documento: "LD-090-CV-005", revisao: "0", ld: "Pendente", sigem: "Sem workflow", disciplina: "Civil", aging: 25 },
];

export default function EngenhariaPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Engenharia e documentação</h2>
      <FilterBar filters={["Disciplina", "Área", "Fornecedor", "Pacote", "Status"]} />
      <KpiGrid
        items={[
          { label: "Documentos LD", value: "1.462" },
          { label: "Documentos SIGEM", value: "1.398" },
          { label: "Pendentes", value: "94", trend: "-8 na semana" },
          { label: "Duplicados", value: "13" },
        ]}
      />
      <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80 mt-4">
        <h3 className="font-semibold mb-2">Status documental consolidado</h3>
        <ResponsiveContainer width="100%" height="90%">
          <PieChart>
            <Pie data={statusDocs} dataKey="value" nameKey="name" outerRadius={100} label>
              {statusDocs.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
