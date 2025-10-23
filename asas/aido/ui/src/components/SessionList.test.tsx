import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { SessionList } from "./SessionList";

const sessions = [
  { id: "1", status: "completed", title: "Sessao 1", updatedAt: 1 },
  { id: "2", status: "pending", title: "Sessao 2", updatedAt: 2 }
];

describe("SessionList", () => {
  it("exibe sessoes", () => {
    render(
      <SessionList
        sessions={sessions}
        selectedSessionId={"1"}
        onSelect={() => undefined}
        onRefresh={() => undefined}
        loading={false}
        error={null}
      />
    );

    expect(screen.getByText("Sessao 1")).toBeInTheDocument();
    expect(screen.getByText("Sessao 2")).toBeInTheDocument();
  });
});
