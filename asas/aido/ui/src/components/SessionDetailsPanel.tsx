import { useState } from "react";
import { useCopilotAction } from "@copilotkit/react-core";
import { z } from "zod";
import type { ConciergeCard } from "../types";

interface SessionDetailsPanelProps {
  enabled?: boolean;
}

export function SessionDetailsPanel({ enabled = true }: SessionDetailsPanelProps) {
  if (!enabled) {
    return (
      <aside className="w-96 border-l border-slate-200 bg-slate-50 flex items-center justify-center">
        <p className="text-xs text-slate-500 px-6 text-center">
          Painel dinamico indisponivel neste modo. Ative o CopilotKit para visualizar cartoes gerados
          pelo agente.
        </p>
      </aside>
    );
  }

  const [cards, setCards] = useState<ConciergeCard[]>([]);

  useCopilotAction({
    name: "render_session_card",
    description:
      "Renderiza informacoes resumidas sobre uma sessao do AIDO, incluindo status e artefatos.",
    parameters: z.object({
      sessionId: z.string(),
      status: z.string(),
      manualPath: z.string().optional(),
      transcriptionStatus: z.string().optional(),
      notes: z.string().optional(),
    }),
    handler: ({ sessionId, status, manualPath, transcriptionStatus, notes }) => {
      setCards((previous) => [
        ...previous,
        {
          sessionId,
          status,
          manualPath: manualPath ?? null,
          transcriptionStatus: transcriptionStatus ?? null,
          notes: notes ?? null,
        },
      ]);
    },
  });

  return (
    <aside className="w-96 border-l border-slate-200 bg-slate-50 flex flex-col">
      <div className="p-4 border-b border-slate-200">
        <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
          Painel dinamico
        </h2>
        <p className="mt-2 text-xs text-slate-500">
          O AIDO pode gerar cartoes com diagnosticos, lembretes e referencias de arquivos.
        </p>
      </div>
      <div className="flex-1 overflow-y-auto space-y-3 p-4">
        {cards.length === 0 ? (
          <p className="text-xs text-slate-500">
            Ainda nao ha cartoes gerados. Solicite ao AIDO detalhes sobre uma sessao.
          </p>
        ) : (
          cards.map((card, index) => (
            <article
              key={`${card.sessionId}-${index}`}
              className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
            >
              <header className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500 uppercase">Sessao</span>
                <span className="text-xs text-slate-400">#{card.sessionId.slice(0, 8)}</span>
              </header>
              <h3 className="mt-2 text-lg font-semibold text-slate-800">Status: {card.status}</h3>
              {card.transcriptionStatus && (
                <p className="text-sm text-slate-600 mt-1">
                  Transcricao: <span className="font-medium">{card.transcriptionStatus}</span>
                </p>
              )}
              {card.manualPath && (
                <p className="text-sm text-slate-600 mt-1">
                  Manual gerado em: <span className="underline text-bosch-blue">{card.manualPath}</span>
                </p>
              )}
              {card.notes && (
                <p className="text-sm text-slate-600 mt-2 whitespace-pre-wrap">{card.notes}</p>
              )}
            </article>
          ))
        )}
      </div>
    </aside>
  );
}
