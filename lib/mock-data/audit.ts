import type { AuditEvent } from "@/lib/types";

export const auditEvents: AuditEvent[] = [
  {
    id: 1,
    timestamp: "2026-08-13T03:45:00Z",
    task: "Prepare investor diligence workspace",
    agent: "MARYADA",
    action: "approval_required",
    status: "blocked",
    event: "Human approval required for high-risk external disclosure.",
    details:
      "MARYADA classified the task as high risk because customer and financial material may be externally shared.",
  },
  {
    id: 2,
    timestamp: "2026-08-13T03:38:00Z",
    task: "Prepare investor diligence workspace",
    agent: "MURPHY",
    action: "risk_reported",
    status: "warning",
    event: "Sensitive disclosure risk identified.",
    details:
      "MURPHY recommended least-privilege investor access and founder confirmation before package delivery.",
  },
  {
    id: 3,
    timestamp: "2026-08-13T03:30:00Z",
    task: "Summarize product telemetry anomalies",
    agent: "MURPHY",
    action: "risk_review_started",
    status: "warning",
    event: "Aggregate telemetry risk review in progress.",
    details:
      "The review is checking false-positive risk and removing raw identifiers from summaries.",
  },
  {
    id: 4,
    timestamp: "2026-08-12T16:05:00Z",
    task: "Draft customer renewal briefing",
    agent: "RACHIT",
    action: "output_delivered",
    status: "success",
    event: "Renewal briefing delivered internally.",
    details:
      "RACHIT packaged the approved renewal briefing with milestones, risks, and suggested next actions.",
  },
  {
    id: 5,
    timestamp: "2026-08-12T11:42:00Z",
    task: "Validate hiring plan assumptions",
    agent: "KOSH",
    action: "context_blocked",
    status: "blocked",
    event: "Conflicting runway memory blocked planning.",
    details:
      "KOSH found deprecated and current runway references and paused the workflow until founder confirmation.",
  },
  {
    id: 6,
    timestamp: "2026-08-13T03:10:00Z",
    task: "Founder approval digest",
    agent: "LISA",
    action: "notification_failed",
    status: "failed",
    event: "Notification digest could not be generated.",
    details:
      "The digest remained local to the UI prototype because no notification service is integrated in this phase.",
  },
];