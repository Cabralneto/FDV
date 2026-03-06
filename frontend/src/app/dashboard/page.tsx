"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const curvaData = [
  { mes: "Jan", previsto: 8, realizado: 7 },
  { mes: "Fev", previsto: 16, realizado: 14 },
  { mes: "Mar", previsto: 24, realizado: 20 },
  { mes: "Abr", previsto: 34, realizado: 28 },
  { mes: "Mai", previsto: 45, realizado: 39 },
  { mes: "Jun", previsto: 58, realizado: 53 },
];

const desvios = [
  { area: "Civil", desvio: 3.2 },
  { area: "Mecânica", desvio: 5.1 },
  { area: "Elétrica", desvio: 2.6 },
  { area: "Tubulação", desvio: 4.4 },
];

const rows = [
  { frente: "Casa de bombas", status: "Atrasada", marco: "Comissionamento", prazo: "2026-04-10", impacto: "Alto" },
  { frente: "Subestação", status: "Atenção", marco: "Energização", prazo: "2026-04-22", impacto: "Médio" },
  { frente: "Utilidades", status: "No prazo", marco: "Teste funcional", prazo: "2026-05-05", impacto: "Baixo" },
];

export default function DashboardPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Dashboard executivo</h2>
      <FilterBar filters={["Período", "Área", "Disciplina", "Fornecedor"]} />
      <KpiGrid
        items={[
          { label: "Avanço físico", value: "53%", trend: "+4.2% vs mês anterior" },
          { label: "Avanço financeiro", value: "R$ 9,6 MM", trend: "+R$ 0,8 MM no mês" },
          { label: "Marcos críticos", value: "7", trend: "2 em atraso" },
          { label: "Pendências críticas", value: "18", trend: "-3 em 15 dias" },
        ]}
      />

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 mt-4">
        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80">
          <h3 className="font-semibold mb-2">Curva de evolução física</h3>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={curvaData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="previsto" stroke="#0284c7" strokeWidth={3} />
              <Line type="monotone" dataKey="realizado" stroke="#16a34a" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80">
          <h3 className="font-semibold mb-2">Desvio por área (%)</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={desvios}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="area" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="desvio" fill="#f97316" radius={4} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-4">
        <DataTable rows={rows} />
      </div>
    </PageShell>
  );
}
