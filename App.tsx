import { useCallback, useEffect, useMemo, useState } from "react";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { SessionList } from "./components/SessionList";
import { SessionDetailsPanel } from "./components/SessionDetailsPanel";
import { useSessionSharedState } from "./hooks/useSessionSharedState";
import type { SessionSummary } from "./types";

const RUNTIME_URL = import.meta.env.VITE_COPILOTKIT_RUNTIME_URL ?? "/api/copilotkit";
const DEFAULT_USER_ID = import.meta.env.VITE_AIDO_USER_ID ?? "local-user";

function normalizeTimestamp(value: unknown): number | null {
  if (typeof value === "number") {
    return value;
  }
  if (typeof value === "string") {
    const parsed = Date.parse(value);
    return Number.isNaN(parsed) ? null : Math.floor(parsed / 1000);
  }
  return null;
}

export default function App() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { selectedSessionId, setSelectedSessionId } = useSessionSharedState();

  const loadSessions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `/api/sessions?user_id=${encodeURIComponent(DEFAULT_USER_ID)}`
      );
      if (!response.ok) {
        throw new Error(`Falha ao buscar sessoes (status ${response.status})`);
      }
      const payload = await response.json();
      const list: SessionSummary[] = (payload.sessions ?? []).map((item: any) => {
        const updatedAt = normalizeTimestamp(item.updated_at ?? item.updatedAt ?? null);
        return {
          id: String(item.id),
          status: item.status ?? "desconhecido",
          title:
            item.structured_title ??
            item.video_path ??
            (item.id ? `Sessao ${String(item.id).slice(0, 6)}` : "Sessao"),
          updatedAt,
          manualPath: item.generated_docx_path ?? null,
          videoPath: item.video_path ?? null,
        };
      });
      setSessions(list);
      if (!selectedSessionId && list.length > 0) {
        setSelectedSessionId(list[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado ao listar sessoes");
    } finally {
      setLoading(false);
    }
  }, [selectedSessionId, setSelectedSessionId]);

  useEffect(() => {
    void loadSessions();
  }, [loadSessions]);

  const sortedSessions = useMemo(
    () => [...sessions].sort((a, b) => (b.updatedAt ?? 0) - (a.updatedAt ?? 0)),
    [sessions]
  );

  const handleSelect = (sessionId: string) => {
    setSelectedSessionId(sessionId);
  };

  const copilotKey = selectedSessionId ?? "default";

  return (
    <CopilotKit
      key={copilotKey}
      runtimeUrl={RUNTIME_URL}
      initialSessionId={selectedSessionId ?? undefined}
    >
      <div className="h-screen flex bg-slate-50">
        <SessionList
          sessions={sortedSessions}
          selectedSessionId={selectedSessionId}
          onSelect={handleSelect}
          onRefresh={loadSessions}
          loading={loading}
          error={error}
        />
        <main className="flex-1 flex flex-col bg-[#f6f8fb]">
          <header className="px-6 py-4 border-b border-slate-200 bg-white shadow-sm">
            <h1 className="text-xl font-semibold text-slate-800">AIDO Control Center</h1>
            <p className="text-sm text-slate-500 mt-1">
              Converse com o AIDO no painel central. O painel direito exibe cartoes dinamicos
              produzidos pelo agente.
            </p>
          </header>
          <div className="flex-1 overflow-hidden flex">
            <div className="flex-1 border-r border-slate-200 bg-white">
              <CopilotChat
                className="h-full"
                instructions="Voce esta interagindo com o AIDO, agente especializado em criar e atualizar manuais."
              />
            </div>
            <SessionDetailsPanel />
          </div>
        </main>
      </div>
    </CopilotKit>
  );
}
