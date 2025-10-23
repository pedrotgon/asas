import { useEffect, useState } from "react";
import { useCopilotReadable } from "@copilotkit/react-core";

export function useSessionSharedState() {
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);

  useEffect(() => {
    if (selectedSessionId) {
      localStorage.setItem("aido:lastSession", selectedSessionId);
    }
  }, [selectedSessionId]);

  useEffect(() => {
    const stored = localStorage.getItem("aido:lastSession");
    if (stored) {
      setSelectedSessionId(stored);
    }
  }, []);

  useCopilotReadable({
    description: "Identificador da sessão selecionada atualmente na UI",
    value: selectedSessionId ?? "",
    name: "selected_session_id"
  });

  return { selectedSessionId, setSelectedSessionId } as const;
}
