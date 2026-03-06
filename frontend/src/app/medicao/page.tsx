"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const evolucao = [
  { mes: "Jan", medido: 0.8, acumulado: 0.8 },
  { mes: "Fev", medido: 1.1, acumulado: 1.9 },
  { mes: "Mar", medido: 1.4, acumulado: 3.3 },
  { mes: "Abr", medido: 1.0, acumulado: 4.3 },
  { mes: "Mai", medido: 1.6, acumulado: 5.9 },
];

const rows = [
  { periodo: "2026-01", fornecedor: "Fornecedor A", contrato: "CT-100", previsto: "R$ 1,0 MM", realizado: "R$ 0,8 MM", desvio: "-R$ 0,2 MM" },
  { periodo: "2026-02", fornecedor: "Fornecedor B", contrato: "CT-112", previsto: "R$ 1,3 MM", realizado: "R$ 1,1 MM", desvio: "-R$ 0,2 MM" },
  { periodo: "2026-03", fornecedor: "Fornecedor C", contrato: "CT-119", previsto: "R$ 1,5 MM", realizado: "R$ 1,4 MM", desvio: "-R$ 0,1 MM" },
];

export default function MedicaoPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Medição</h2>
      <FilterBar filters={["Período", "Contrato", "Fornecedor", "Disciplina"]} />
      <KpiGrid
        items={[
          { label: "Medição no período", value: "R$ 1,4 MM" },
          { label: "Medição acumulada", value: "R$ 5,9 MM" },
          { label: "Previsto x realizado", value: "92%" },
          { label: "Fornecedores medidos", value: "14" },
        ]}
      />
      <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80 mt-4">
        <h3 className="font-semibold mb-2">Evolução da medição (MM)</h3>
        <ResponsiveContainer width="100%" height="90%">
          <AreaChart data={evolucao}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="mes" /><YAxis /><Tooltip /><Area type="monotone" dataKey="medido" stackId="1" stroke="#0284c7" fill="#7dd3fc" /><Area type="monotone" dataKey="acumulado" stackId="2" stroke="#16a34a" fill="#86efac" /></AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
