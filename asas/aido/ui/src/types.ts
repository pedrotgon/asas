export interface SessionSummary {
  id: string;
  status: string;
  title?: string | null;
  updatedAt?: number | null;
  manualPath?: string | null;
  videoPath?: string | null;
}

export interface ConciergeCard {
  sessionId: string;
  status: string;
  manualPath?: string | null;
  transcriptionStatus?: string | null;
  notes?: string | null;
}
