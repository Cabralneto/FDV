"use client";
import { useState } from "react";

export function DataTable({ rows }: { rows: Array<Record<string, string | number>> }) {
  const [filter, setFilter] = useState("");
  const filtered = rows.filter((row) => JSON.stringify(row).toLowerCase().includes(filter.toLowerCase()));
  const headers = rows[0] ? Object.keys(rows[0]) : [];

  return (
    <div className="bg-white rounded-lg p-4 shadow">
      <div className="flex justify-between mb-4">
        <input className="border rounded px-3 py-2 w-72" placeholder="Filtrar..." value={filter} onChange={(e) => setFilter(e.target.value)} />
        <button className="bg-accent text-white px-3 py-2 rounded">Exportar CSV</button>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b">{headers.map((h) => <th key={h} className="p-2">{h}</th>)}</tr>
        </thead>
        <tbody>
          {filtered.map((row, idx) => (
            <tr key={idx} className="border-b">{headers.map((h) => <td key={h} className="p-2">{String(row[h])}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
