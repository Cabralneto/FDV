export type KpiItem = { label: string; value: string; trend?: string };

export function KpiGrid({ items }: { items: KpiItem[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
      {items.map((item) => (
        <div key={item.label} className="bg-white rounded-lg p-4 shadow border border-slate-100">
          <div className="text-sm text-slate-500">{item.label}</div>
          <div className="text-2xl font-semibold text-slate-800 mt-1">{item.value}</div>
          {item.trend ? <div className="text-xs text-emerald-600 mt-1">{item.trend}</div> : null}
        </div>
      ))}
    </div>
  );
}
