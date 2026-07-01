import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

type DashboardSummary = {
  documents: {
    total: number;
    status: Record<string, number>;
    folder: Record<string, number>;
  };
  transactions_total: number;
  matches_total: number;
  matches_by_status: Record<string, number>;
};

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard/summary")
      .then((response) => response.json())
      .then((data) => setSummary(data));
  }, []);

  return (
    <main style={{ fontFamily: "Arial", padding: 32 }}>
      <h1>ELEV Finance Agent</h1>

      {!summary && <p>Lade Dashboard...</p>}

      {summary && (
        <section>
          <h2>Dashboard</h2>
          <p>Dokumente gesamt: {summary.documents.total}</p>
          <p>Transaktionen: {summary.transactions_total}</p>
          <p>Matches: {summary.matches_total}</p>

          <h3>Dokumentstatus</h3>
          <pre>{JSON.stringify(summary.documents.status, null, 2)}</pre>

          <h3>Ordner</h3>
          <pre>{JSON.stringify(summary.documents.folder, null, 2)}</pre>
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);