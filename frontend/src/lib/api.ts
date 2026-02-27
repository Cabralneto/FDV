const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export async function getSummary() {
  const res = await fetch(`${API_BASE}/summary`, { cache: "no-store" });
  if (!res.ok) throw new Error("Falha ao carregar resumo");
  return res.json();
}

export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents`, { cache: "no-store" });
  if (!res.ok) throw new Error("Falha ao carregar documentos");
  return res.json();
}

export async function searchText(q: string) {
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Falha na busca");
  return res.json();
}
