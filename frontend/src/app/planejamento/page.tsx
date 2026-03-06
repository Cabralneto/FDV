"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const atraso = [
  { disciplina: "Civil", dias: 12 },
  { disciplina: "Mecânica", dias: 18 },
  { disciplina: "Elétrica", dias: 9 },
  { disciplina: "Instrumentação", dias: 14 },
];

const lookahead = [
  { semana: "S1", atividades: 24 },
  { semana: "S2", atividades: 31 },
  { semana: "S3", atividades: 28 },
  { semana: "S4", atividades: 35 },
];

const rows = [
  { atividade: "Montagem de estrutura", area: "Pátio", responsavel: "Planejamento", baseline: "2026-03-12", atual: "2026-03-26", status: "Atrasada" },
  { atividade: "Lançamento de cabos", area: "Subestação", responsavel: "Campo", baseline: "2026-03-18", atual: "2026-03-20", status: "Atenção" },
  { atividade: "Teste hidráulico", area: "Utilidades", responsavel: "Qualidade", baseline: "2026-03-22", atual: "2026-03-22", status: "No prazo" },
];

export default function PlanejamentoPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Planejamento</h2>
      <FilterBar filters={["Período", "Área", "Disciplina", "Pacote", "Responsável"]} />
      <KpiGrid
        items={[
          { label: "Atividades em aberto", value: "214" },
          { label: "Atividades atrasadas", value: "47", trend: "+6 na semana" },
          { label: "Marcos no mês", value: "12" },
          { label: "Lookahead 4 semanas", value: "118" },
        ]}
      />
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 mt-4">
        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80">
          <h3 className="font-semibold mb-2">Ranking de atraso por disciplina</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={atraso}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="disciplina" /><YAxis /><Tooltip /><Bar dataKey="dias" fill="#dc2626" /></BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80">
          <h3 className="font-semibold mb-2">Lookahead semanal</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={lookahead}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="semana" /><YAxis /><Tooltip /><Bar dataKey="atividades" fill="#2563eb" /></BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
