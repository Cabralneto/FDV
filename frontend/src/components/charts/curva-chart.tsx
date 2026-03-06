"use client";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function CurvaChart({ data }: { data: Array<{ referencia: string; previsto_fisico: number; realizado_fisico: number }> }) {
  return (
    <div className="h-72 bg-white rounded-lg p-4 shadow">
      <h3 className="font-semibold mb-2">Curva S Física</h3>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <XAxis dataKey="referencia" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="previsto_fisico" stroke="#0369a1" strokeWidth={3} />
          <Line type="monotone" dataKey="realizado_fisico" stroke="#16a34a" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
