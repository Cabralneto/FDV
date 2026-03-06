export function FilterBar({ filters }: { filters: string[] }) {
  return (
    <div className="bg-white rounded-lg p-4 shadow border border-slate-100 mb-4">
      <div className="text-sm font-medium text-slate-700 mb-3">Filtros</div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {filters.map((label) => (
          <label key={label} className="text-xs text-slate-500">
            {label}
            <select className="mt-1 w-full border rounded px-2 py-2 text-sm text-slate-700">
              <option>Todos</option>
              <option>Crítico</option>
              <option>Atenção</option>
              <option>Normal</option>
            </select>
          </label>
        ))}
      </div>
    </div>
  );
}
