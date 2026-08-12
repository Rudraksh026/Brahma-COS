import { Badge } from "@/components/ui/badge";
import type {
  AgentHealth,
  AgentOperationalStatus,
  ApprovalStatus,
  AuditStatus,
  MemoryStatus,
  WorkflowStatus
} from "@/lib/types";

const workflowLabels: Record<WorkflowStatus, string> = {
  pending: "Pending",
  running: "Running",
  completed: "Completed",
  failed: "Failed",
  blocked: "Blocked",
  waiting_approval: "Waiting approval"
};

function variantForStatus(
  status:
    | WorkflowStatus
    | ApprovalStatus
    | MemoryStatus
    | AgentOperationalStatus
    | AgentHealth
    | AuditStatus
) {
  if (
    status === "completed" ||
    status === "approved" ||
    status === "Approved" ||
    status === "Canonical" ||
    status === "active" ||
    status === "healthy" ||
    status === "success"
  ) {
    return "success" as const;
  }

  if (
    status === "running" ||
    status === "waiting_approval" ||
    status === "pending" ||
    status === "Candidate" ||
    status === "idle" ||
    status === "degraded" ||
    status === "warning"
  ) {
    return "warning" as const;
  }

  if (
    status === "failed" ||
    status === "blocked" ||
    status === "rejected" ||
    status === "Deprecated" ||
    status === "offline"
  ) {
    return "danger" as const;
  }

  return "secondary" as const;
}

export function StatusBadge({
  status
}: {
  status:
    | WorkflowStatus
    | ApprovalStatus
    | MemoryStatus
    | AgentOperationalStatus
    | AgentHealth
    | AuditStatus;
}) {
  const label =
    status in workflowLabels
      ? workflowLabels[status as WorkflowStatus]
      : String(status).replace("_", " ");

  return (
    <Badge variant={variantForStatus(status)} className="capitalize">
      {label}
    </Badge>
  );
}
