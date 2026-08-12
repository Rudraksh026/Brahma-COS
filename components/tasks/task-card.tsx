import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { RiskBadge } from "@/components/common/risk-badge";
import { StatusBadge } from "@/components/common/status-badge";
import { Card, CardContent } from "@/components/ui/card";
import type { Task } from "@/lib/types";
import { formatDateTime } from "@/lib/utils";

export function TaskCard({ task }: { task: Task }) {
  return (
    <Card className="transition-colors hover:border-slate-300">
      <CardContent className="p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="truncate text-base font-semibold">{task.title}</h3>
              <StatusBadge status={task.status} />
              <RiskBadge level={task.riskLevel} />
            </div>
            <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">
              {task.description}
            </p>
            <div className="mt-3 flex flex-wrap gap-x-5 gap-y-1 text-xs text-muted-foreground">
              <span>Agent: {task.currentAgent}</span>
              <span>Stage: {task.currentStage}</span>
              <span>{formatDateTime(task.updatedAt)}</span>
            </div>
          </div>
          <Link
            className="inline-flex items-center gap-2 rounded-md border px-3 py-2 text-sm font-medium hover:bg-muted"
            href={`/tasks/${task.id}`}
          >
            Open
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
