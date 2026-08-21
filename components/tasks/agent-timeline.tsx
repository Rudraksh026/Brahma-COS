import {
  CheckCircle2,
  Circle,
  Clock,
  Loader2,
  OctagonAlert,
  XCircle
} from "lucide-react";

import { StatusBadge } from "@/components/common/status-badge";
import type { AgentTraceStep, WorkflowStatus } from "@/lib/types";
import { cn, formatDateTime } from "@/lib/utils";

const statusIcons: Record<WorkflowStatus, typeof Circle> = {
  PENDING: Circle,
  RUNNING: Loader2,
  COMPLETED: CheckCircle2,
  FAILED: XCircle,
  BLOCKED: OctagonAlert
};

const iconTone: Record<WorkflowStatus, string> = {
  PENDING: "border-muted bg-background text-muted-foreground",
  RUNNING: "border-amber-200 bg-amber-50 text-amber-700",
  COMPLETED: "border-emerald-200 bg-emerald-50 text-emerald-700",
  FAILED: "border-red-200 bg-red-50 text-red-700",
  BLOCKED: "border-red-200 bg-red-50 text-red-700"
};

export function AgentTimeline({ trace }: { trace: AgentTraceStep[] }) {
  return (
    <div className="space-y-0">
      {trace.map((step, index) => {
        const Icon = statusIcons[step.status as WorkflowStatus];
        const isLast = index === trace.length - 1;

        return (
          <div className="relative flex gap-4 pb-6 last:pb-0" key={`${step.agent}-${index}`}>
            {!isLast ? (
              <div className="absolute left-5 top-10 h-[calc(100%-2.5rem)] w-px bg-border" />
            ) : null}
            <div
              className={cn(
                "z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border",
                iconTone[step.status as WorkflowStatus]
              )}
            >
              <Icon
                className={cn("h-5 w-5", step.status === "RUNNING" && "animate-spin")}
                aria-hidden="true"
              />
            </div>
            <div className="min-w-0 flex-1 rounded-lg border bg-card p-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold">{step.agent}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {step.description}
                  </p>
                </div>
                <StatusBadge status={step.status as WorkflowStatus} />
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                {formatDateTime(step.timestamp)}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
