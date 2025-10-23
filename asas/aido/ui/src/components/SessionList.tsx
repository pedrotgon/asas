import type { SessionSummary } from "../types";

interface SessionListProps {
  sessions: SessionSummary[];
  selectedSessionId: string | null;
  onSelect: (sessionId: string) => void;
  onRefresh: () => void;
  loading: boolean;
  error: string | null;
}

export function SessionList({
  sessions,
  selectedSessionId,
  onSelect,
  onRefresh,
  loading,
  error,
}: SessionListProps) {
  return (
    <aside className="w-72 border-r border-slate-200 bg-white flex flex-col">
      <div className="p-4 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
            Sessoes
          </h2>
          <button
            onClick={onRefresh}
            className="text-xs text-bosch-blue hover:text-bosch-dark"
            aria-label="Atualizar sessoes"
          >
            Atualizar
          </button>
        </div>
        {loading && <p className="mt-3 text-xs text-slate-500">Carregando...</p>}
        {error && <p className="mt-3 text-xs text-red-600">{error}</p>}
      </div>
      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 && !loading ? (
          <p className="p-4 text-xs text-slate-500">
            Nenhuma sessao encontrada. Inicie uma conversa com o AIDO.
          </p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {sessions.map((session) => {
              const isActive = session.id === selectedSessionId;
              const buttonClasses = [
                "w-full text-left px-4 py-3 text-sm transition-colors border-l-2",
                isActive
                  ? "bg-bosch-blue/10 border-bosch-blue text-bosch-blue"
                  : "border-transparent text-slate-700 hover:bg-slate-50",
              ].join(" ");

              return (
                <li key={session.id}>
                  <button onClick={() => onSelect(session.id)} className={buttonClasses}>
                    <p className="font-semibold text-slate-800 truncate">
                      {session.title ?? "Sessao sem titulo"}
                    </p>
                    <p className="text-xs text-slate-500">
                      Status: <span className="font-medium">{session.status}</span>
                    </p>
                    {session.updatedAt && (
                      <p className="text-[11px] text-slate-400 mt-1">
                        Atualizado em {new Date(session.updatedAt * 1000).toLocaleString()}
                      </p>
                    )}
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </aside>
  );
}
