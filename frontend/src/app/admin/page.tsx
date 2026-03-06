"use client";

import { useState } from "react";
import { PageShell } from "@/components/layout/page-shell";
import { DataTable } from "@/components/tables/data-table";
import { FilterBar } from "@/components/ui/filter-bar";
import { KpiGrid } from "@/components/ui/kpi-grid";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const tipos = [
  { tipo: "Justificativa", qtd: 16 },
  { tipo: "Fato gerador", qtd: 11 },
  { tipo: "Plano de ação", qtd: 23 },
  { tipo: "Risco", qtd: 9 },
];

const rows = [
  { tipo: "Justificativa", titulo: "Atraso de entrega", area: "Suprimentos", disciplina: "Mecânica", status: "Aberto", criado_em: "2026-03-10" },
  { tipo: "Plano de ação", titulo: "Recuperar caminho crítico", area: "Planejamento", disciplina: "Civil", status: "Em andamento", criado_em: "2026-03-09" },
  { tipo: "Risco", titulo: "Janela climática", area: "Campo", disciplina: "Montagem", status: "Monitorado", criado_em: "2026-03-08" },
];

export default function AdminPage() {
  const [draft, setDraft] = useState({ tipo: "Justificativa", titulo: "", descricao: "" });

  return (
    <PageShell>
      <h2 className="text-2xl font-bold mb-4">Administração de apontamentos manuais</h2>
      <FilterBar filters={["Tipo", "Área", "Disciplina", "Status"]} />
      <KpiGrid
        items={[
          { label: "Apontamentos no mês", value: "59" },
          { label: "Abertos", value: "21" },
          { label: "Em andamento", value: "26" },
          { label: "Concluídos", value: "12" },
        ]}
      />

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 mt-4">
        <div className="bg-white rounded-lg p-4 shadow border border-slate-100">
          <h3 className="font-semibold mb-3">Novo apontamento manual</h3>
          <div className="space-y-3">
            <label className="block text-sm text-slate-600">Tipo
              <select
                className="mt-1 w-full border rounded px-3 py-2"
                value={draft.tipo}
                onChange={(e) => setDraft((old) => ({ ...old, tipo: e.target.value }))}
              >
                <option>Justificativa</option>
                <option>Fato gerador</option>
                <option>Plano de ação</option>
                <option>Risco</option>
              </select>
            </label>
            <label className="block text-sm text-slate-600">Título
              <input className="mt-1 w-full border rounded px-3 py-2" value={draft.titulo} onChange={(e) => setDraft((old) => ({ ...old, titulo: e.target.value }))} />
            </label>
            <label className="block text-sm text-slate-600">Descrição
              <textarea className="mt-1 w-full border rounded px-3 py-2" rows={4} value={draft.descricao} onChange={(e) => setDraft((old) => ({ ...old, descricao: e.target.value }))} />
            </label>
            <button className="bg-accent text-white px-4 py-2 rounded">Salvar apontamento</button>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow border border-slate-100 h-96">
          <h3 className="font-semibold mb-2">Distribuição por tipo</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={tipos}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="tipo" /><YAxis /><Tooltip /><Bar dataKey="qtd" fill="#f97316" /></BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-4"><DataTable rows={rows} /></div>
    </PageShell>
  );
}
