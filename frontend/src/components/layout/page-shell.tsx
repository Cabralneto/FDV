import { ReactNode } from "react";
import { Header } from "./header";
import { Sidebar } from "./sidebar";

export function PageShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 min-h-screen">
        <Header />
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
}
