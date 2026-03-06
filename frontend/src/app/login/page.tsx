export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-200">
      <div className="bg-white w-full max-w-md rounded-xl p-8 shadow">
        <h1 className="text-2xl font-bold mb-6">Portal da Obra</h1>
        <input className="w-full border rounded p-2 mb-3" placeholder="E-mail" defaultValue="admin@portalobra.local" />
        <input className="w-full border rounded p-2 mb-4" placeholder="Senha" type="password" defaultValue="admin123" />
        <button className="w-full bg-accent text-white rounded p-2">Entrar</button>
      </div>
    </div>
  );
}
