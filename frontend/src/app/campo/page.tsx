"use client";

import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const efetivo = [
  { dia: "Seg", qtd: 398 },
  { dia: "Ter", qtd: 405 },
  { dia: "Qua", qtd: 412 },
  { dia: "Qui", qtd: 401 },
  { dia: "Sex", qtd: 420 },
];

const produtividade = [
  { semana: "S1", indice: 0.84 },
  { semana: "S2", indice: 0.88 },
  { semana: "S3", indice: 0.86 },
  { semana: "S4", indice: 0.91 },
];

const rows = [
  { data: "2026-03-10", frente: "Montagem mecânica", efetivo: 88, pt_abertas: 4, rdo: "Sem incidentes" },
  { data: "2026-03-10", frente: "Elétrica", efetivo: 72, pt_abertas: 3, rdo: "Parada por chuva 1h" },
  { data: "2026-03-10", frente: "Civil", efetivo: 96, pt_abertas: 5, rdo: "Concretagem normal" },
];

export default function CampoPage() {
  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Produção / campo</h2>
      <FilterBar filters={["Período", "Área", "Frente", "Turno"]} />
      <KpiGrid
        items={[
          { label: "Efetivo total", value: "412" },
          { label: "PT abertas", value: "14" },
          { label: "RDO do dia", value: "3" },
          { label: "Produtividade", value: "0,91", trend: "+0,05 vs semana anterior" },
        ]}
      />
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 mt-4">
        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80">
          <h3 className="font-semibold mb-2">Efetivo diário</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={efetivo}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="dia" /><YAxis /><Tooltip /><Bar dataKey="qtd" fill="#0891b2" /></BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-80">
          <h3 className="font-semibold mb-2">Índice de produtividade</h3>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={produtividade}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="semana" /><YAxis /><Tooltip /><Line dataKey="indice" stroke="#16a34a" strokeWidth={3} /></LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
