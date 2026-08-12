"use client";

import Link from "next/link";
import { ArrowLeft, Clock, FileText, Search } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { EmptyState } from "@/components/common/empty-state";
import { PageHeader } from "@/components/common/page-header";
import { RiskBadge } from "@/components/common/risk-badge";
import { RiskReview } from "@/components/common/risk-review";
import { StatusBadge } from "@/components/common/status-badge";
import { AgentTimeline } from "@/components/tasks/agent-timeline";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import type { Task } from "@/lib/types";
import { formatDateTime } from "@/lib/utils";

const storageKey = "brahma-cos-local-tasks";

export function TaskDetailView({
  initialTasks,
  taskId
}: {
  initialTasks: Task[];
  taskId: string;
}) {
  const [localTasks, setLocalTasks] = useState<Task[]>([]);

  useEffect(() => {
    const raw = window.localStorage.getItem(storageKey);
    if (!raw) {
      return;
    }

    try {
      setLocalTasks(JSON.parse(raw) as Task[]);
    } catch {
      setLocalTasks([]);
    }
  }, []);

  const task = useMemo(
    () => [...localTasks, ...initialTasks].find((item) => item.id === taskId),
    [initialTasks, localTasks, taskId]
  );

  if (!task) {
    return (
      <div className="space-y-6">
        <PageHeader
          action={
            <Button asChild variant="outline">
              <Link href="/tasks">
                <ArrowLeft className="h-4 w-4" aria-hidden="true" />
                Back to tasks
              </Link>
            </Button>
          }
          description="This task is not available in mock data or local browser state."
          title="Task not found"
        />
        <EmptyState
          description="Return to the task console and open an existing task."
          icon={Search}
          title="No task detail available"
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        action={
          <Button asChild variant="outline">
            <Link href="/tasks">
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              Back to tasks
            </Link>
          </Button>
        }
        description={task.description}
        title={task.title}
      />

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Agent Execution Timeline</CardTitle>
              <CardDescription>
                Visual representation only. No LangGraph execution is connected.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <AgentTimeline trace={task.trace} />
            </CardContent>
          </Card>

          {task.riskReport ? <RiskReview report={task.riskReport} /> : null}
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Task Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-2">
                <StatusBadge status={task.status} />
                <RiskBadge level={task.riskLevel} />
              </div>
              <InfoRow label="Current agent" value={task.currentAgent} />
              <InfoRow label="Current stage" value={task.currentStage} />
              <InfoRow label="Created" value={formatDateTime(task.createdAt)} />
              <InfoRow label="Updated" value={formatDateTime(task.updatedAt)} />
              {task.executionResult ? (
                <div className="rounded-md border bg-muted/45 p-4">
                  <div className="flex items-center gap-2 text-sm font-medium">
                    <FileText className="h-4 w-4" aria-hidden="true" />
                    Execution result
                  </div>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {task.executionResult}
                  </p>
                </div>
              ) : null}
              {task.errors?.length ? (
                <div className="rounded-md border border-red-200 bg-red-50 p-4">
                  <p className="text-sm font-medium text-red-700">Errors</p>
                  <ul className="mt-2 space-y-1 text-sm text-red-700">
                    {task.errors.map((error) => (
                      <li key={error}>{error}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </CardContent>
          </Card>

          {task.plan ? (
            <Card>
              <CardHeader>
                <CardTitle>PRAGYA Plan</CardTitle>
                <CardDescription>{task.plan.summary}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-xs font-semibold uppercase text-muted-foreground">
                    Steps
                  </p>
                  <ol className="mt-2 space-y-2 text-sm text-muted-foreground">
                    {task.plan.steps.map((step, index) => (
                      <li className="flex gap-2" key={step}>
                        <span className="font-medium text-foreground">
                          {index + 1}.
                        </span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
                <div>
                  <p className="text-xs font-semibold uppercase text-muted-foreground">
                    Assumptions
                  </p>
                  <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                    {task.plan.assumptions.map((assumption) => (
                      <li className="flex gap-2" key={assumption}>
                        <Clock className="mt-0.5 h-4 w-4 shrink-0" />
                        <span>{assumption}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          ) : null}
        </div>
      </div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-muted-foreground">
        {label}
      </p>
      <p className="mt-1 text-sm">{value}</p>
    </div>
  );
}
