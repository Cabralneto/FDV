"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const criticidade = [
  { faixa: "Crítica", qtd: 18 },
  { faixa: "Alta", qtd: 26 },
  { faixa: "Média", qtd: 41 },
  { faixa: "Baixa", qtd: 33 },
];

const rows = [
  { id: "PEN-1002", titulo: "Interferência de layout", responsavel: "Engenharia", prazo: "2026-03-14", aging: 22, status: "Aberta" },
  { id: "PEN-1020", titulo: "Aprovação de desenho", responsavel: "Cliente", prazo: "2026-03-16", aging: 14, status: "Plano de ação" },
  { id: "PEN-1045", titulo: "Entrega de spool", responsavel: "Fornecedor", prazo: "2026-03-20", aging: 11, status: "Em tratamento" },
];

export default function PendenciasPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Pendências e restrições</h2>
      <FilterBar filters={["Criticidade", "Responsável", "Prazo", "Status"]} />
      <KpiGrid
        items={[
          { label: "Pendências abertas", value: "118" },
          { label: "Críticas", value: "18", trend: "+2 na semana" },
          { label: "Aging médio", value: "17 dias" },
          { label: "Planos de ação ativos", value: "36" },
        ]}
      />
      <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80 mt-4">
        <h3 className="font-semibold mb-2">Pendências por criticidade</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={criticidade}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="faixa" /><YAxis /><Tooltip /><Bar dataKey="qtd" fill="#ef4444" /></BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
