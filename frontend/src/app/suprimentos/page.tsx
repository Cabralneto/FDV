"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const leadTime = [
  { fornecedor: "Fornecedor A", dias: 18 },
  { fornecedor: "Fornecedor B", dias: 26 },
  { fornecedor: "Fornecedor C", dias: 21 },
  { fornecedor: "Fornecedor D", dias: 33 },
];

const rows = [
  { requisicao: "RM-24031", material: "Válvula 4\"", status: "Aberta", fornecedor: "Fornecedor A", impacto: "Alto", necessidade: "2026-03-18" },
  { requisicao: "RM-24045", material: "Cabo 15kV", status: "Em cotação", fornecedor: "Fornecedor B", impacto: "Médio", necessidade: "2026-03-20" },
  { requisicao: "RM-24060", material: "Tubo inox", status: "Em compra", fornecedor: "Fornecedor C", impacto: "Baixo", necessidade: "2026-03-28" },
];

export default function SuprimentosPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Suprimentos</h2>
      <FilterBar filters={["Período", "Fornecedor", "Status", "Pacote"]} />
      <KpiGrid
        items={[
          { label: "Requisições abertas", value: "28" },
          { label: "Materiais críticos", value: "6", trend: "+2 na semana" },
          { label: "Lead time médio", value: "21 dias" },
          { label: "Impacto no cronograma", value: "11 atividades" },
        ]}
      />
      <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80 mt-4">
        <h3 className="font-semibold mb-2">Lead time por fornecedor</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={leadTime}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="fornecedor" /><YAxis /><Tooltip /><Bar dataKey="dias" fill="#7c3aed" /></BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
