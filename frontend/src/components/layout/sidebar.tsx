import Link from "next/link";

const links = ["dashboard","planejamento","engenharia","orcamento","medicao","suprimentos","campo","pendencias","documentos","busca","alertas","admin"];

export function Sidebar() {
  return (
    <aside className="w-60 bg-brand text-white min-h-screen p-4">
      <h1 className="text-xl font-bold mb-6">Portal da Obra</h1>
      <nav className="space-y-2">
        {links.map((item) => (
          <Link key={item} className="block rounded px-3 py-2 hover:bg-slate-700" href={`/${item}`}>
            {item.charAt(0).toUpperCase() + item.slice(1)}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
