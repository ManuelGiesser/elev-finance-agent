import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

const API_BASE = "http://78.46.162.115:8000";

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

type DashboardTasks = {
  needs_ocr: number;
  ready_for_ai_analysis: number;
  proposed_matches: number;
  confirmed_matches: number;
  rejected_matches: number;
};

type DocumentItem = {
  id: number;
  folder: string | null;
  filename: string;
  mime_type: string | null;
  status: string;
  ocr_status: string;
};

type AnalysisItem = {
  id: number;
  document_id: number;
  vendor: string | null;
  invoice_date: string | null;
  invoice_number: string | null;
  total_amount: string | null;
  currency: string | null;
  vat_amount: string | null;
  category: string | null;
  confidence: string | null;
  engine: string;
};

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [tasks, setTasks] = useState<DashboardTasks | null>(null);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [analyses, setAnalyses] = useState<AnalysisItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function loadDashboard() {
    const [summaryRes, tasksRes, documentsRes, analysesRes] =
      await Promise.all([
        fetch(`${API_BASE}/dashboard/summary`),
        fetch(`${API_BASE}/dashboard/tasks`),
        fetch(`${API_BASE}/documents?limit=20`),
        fetch(`${API_BASE}/ai/analyses`),
      ]);

    setSummary(await summaryRes.json());
    setTasks(await tasksRes.json());
    setDocuments(await documentsRes.json());
    setAnalyses(await analysesRes.json());
  }

  async function runDailyWorkflow() {
    setLoading(true);
    setMessage("Tageslauf läuft...");
    await fetch(`${API_BASE}/workflows/daily?limit=3`, { method: "POST" });
    await loadDashboard();
    setMessage("Tageslauf abgeschlossen.");
    setLoading(false);
  }

  async function runOcr(documentId: number) {
    setLoading(true);
    setMessage(`OCR für Dokument ${documentId} läuft...`);
    await fetch(`${API_BASE}/ocr/documents/${documentId}`, { method: "POST" });
    await loadDashboard();
    setMessage(`OCR für Dokument ${documentId} abgeschlossen.`);
    setLoading(false);
  }

  async function runAi(documentId: number) {
    setLoading(true);
    setMessage(`KI-Analyse für Dokument ${documentId} läuft...`);
    await fetch(`${API_BASE}/ai/documents/${documentId}/analyze`, { method: "POST" });
    await loadDashboard();
    setMessage(`KI-Analyse für Dokument ${documentId} abgeschlossen.`);
    setLoading(false);
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <main style={{ fontFamily: "Arial", padding: 32 }}>
      <h1>ELEV Finance Agent</h1>

      <button onClick={runDailyWorkflow} disabled={loading}>
        {loading ? "Bitte warten..." : "Tageslauf starten"}
      </button>

      {message && <p>{message}</p>}

      {!summary || !tasks ? (
        <p>Lade Dashboard...</p>
      ) : (
        <>
          <h2>Dashboard</h2>

          <div style={{ display: "flex", gap: 16, marginTop: 24, flexWrap: "wrap" }}>
            <Card title="Dokumente" value={summary.documents.total} />
            <Card title="Transaktionen" value={summary.transactions_total} />
            <Card title="Matches" value={summary.matches_total} />
            <Card title="OCR offen" value={tasks.needs_ocr} />
            <Card title="KI bereit" value={tasks.ready_for_ai_analysis} />
          </div>

          <h3>Neueste Dokumente</h3>

          <table style={{ borderCollapse: "collapse", width: "100%", marginTop: 16 }}>
            <thead>
              <tr>
                <Th>ID</Th>
                <Th>Dateiname</Th>
                <Th>Ordner</Th>
                <Th>Status</Th>
                <Th>OCR</Th>
                <Th>Aktionen</Th>
              </tr>
            </thead>
            <tbody>
              {documents.map((document) => (
                <tr key={document.id}>
                  <Td>{document.id}</Td>
                  <Td>{document.filename}</Td>
                  <Td>{document.folder}</Td>
                  <Td>{document.status}</Td>
                  <Td>{document.ocr_status}</Td>
                  <Td>
                    <button onClick={() => runOcr(document.id)} disabled={loading}>
                      OCR
                    </button>{" "}
                    <button onClick={() => runAi(document.id)} disabled={loading}>
                      KI
                    </button>
                  </Td>
                </tr>
              ))}
            </tbody>
          </table>

          <h3>KI-Analysen</h3>

          <table style={{ borderCollapse: "collapse", width: "100%", marginTop: 16 }}>
            <thead>
              <tr>
                <Th>ID</Th>
                <Th>Dokument</Th>
                <Th>Lieferant</Th>
                <Th>Datum</Th>
                <Th>Rechnungsnr.</Th>
                <Th>Betrag</Th>
                <Th>Kategorie</Th>
                <Th>Engine</Th>
              </tr>
            </thead>
            <tbody>
              {analyses.map((analysis) => (
                <tr key={analysis.id}>
                  <Td>{analysis.id}</Td>
                  <Td>{analysis.document_id}</Td>
                  <Td>{analysis.vendor || "-"}</Td>
                  <Td>{analysis.invoice_date || "-"}</Td>
                  <Td>{analysis.invoice_number || "-"}</Td>
                  <Td>
                    {analysis.total_amount
                      ? `${analysis.total_amount} ${analysis.currency || ""}`
                      : "-"}
                  </Td>
                  <Td>{analysis.category || "-"}</Td>
                  <Td>{analysis.engine}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </main>
  );
}

function Card(props: { title: string; value: number }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16, minWidth: 140 }}>
      <strong>{props.title}</strong>
      <div style={{ fontSize: 28, marginTop: 8 }}>{props.value}</div>
    </div>
  );
}

function Th(props: { children: React.ReactNode }) {
  return <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>{props.children}</th>;
}

function Td(props: { children: React.ReactNode }) {
  return <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{props.children}</td>;
}

createRoot(document.getElementById("root")!).render(<App />);