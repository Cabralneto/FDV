"use client";

import { FormEvent, useState } from "react";
import { searchText } from "../../lib/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const data = await searchText(query);
    setResults(data);
  }

  return (
    <main style={{ fontFamily: "Arial", padding: 24 }}>
      <h1>Busca textual</h1>
      <form onSubmit={onSubmit}>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ex: motor M-102" />
        <button type="submit">Buscar</button>
      </form>
      <ul>
        {results.map((item, idx) => (
          <li key={`${item.document_code}-${idx}`}>
            <strong>{item.document_code} REV {item.revision}:</strong> {item.snippet}
          </li>
        ))}
      </ul>
    </main>
  );
}
