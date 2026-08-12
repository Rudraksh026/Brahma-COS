import Link from "next/link";
import {
  Activity,
  AlertTriangle,
  Bot,
  ClipboardCheck,
  ListChecks
} from "lucide-react";

import { PageHeader } from "@/components/common/page-header";
import { RiskBadge } from "@/components/common/risk-badge";
import { StatCard } from "@/components/common/stat-card";
import { StatusBadge } from "@/components/common/status-badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { agents, auditEvents, decisions, tasks } from "@/lib/mock-data";
import { formatDateTime } from "@/lib/utils";

export default function DashboardPage() {
  const activeTasks = tasks.filter((task) =>
    ["running", "pending", "waiting_approval", "blocked"].includes(task.status)
  );
  const pendingDecisions = decisions.filter(
    (decision) => decision.approvalStatus === "pending"
  );
  const activeAgents = agents.filter((agent) => agent.status === "active");
  const recentRisks = tasks.filter((task) =>
    ["high", "critical"].includes(task.riskLevel)
  );

  return (
    <div className="space-y-6">
      <PageHeader
        action={
          <Button asChild>
            <Link href="/tasks">Create task</Link>
          </Button>
        }
        description="A compact operating view for tasks, agent state, approvals, and recent risk signals."
        title="Founder Command Center"
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          detail={`${activeTasks.length} active or waiting`}
          icon={ListChecks}
          label="Active Tasks"
          value={activeTasks.length}
        />
        <StatCard
          detail="Founder review queue"
          icon={ClipboardCheck}
          label="Pending Decisions"
          value={pendingDecisions.length}
        />
        <StatCard
          detail={`${agents.length} configured agents`}
          icon={Bot}
          label="Active Agents"
          value={activeAgents.length}
        />
        <StatCard
          detail="High and critical items"
          icon={AlertTriangle}
          label="Recent Risks"
          value={recentRisks.length}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1.6fr)_minmax(320px,0.9fr)]">
        <Card>
          <CardHeader>
            <CardTitle>Recent Tasks</CardTitle>
            <CardDescription>
              Current agent, stage, and risk posture across the MVP workflow.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Task</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Agent</TableHead>
                  <TableHead>Risk</TableHead>
                  <TableHead>Updated</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tasks.map((task) => (
                  <TableRow key={task.id}>
                    <TableCell>
                      <Link
                        className="font-medium hover:underline"
                        href={`/tasks/${task.id}`}
                      >
                        {task.title}
                      </Link>
                      <p className="mt-1 text-xs text-muted-foreground">
                        {task.currentStage}
                      </p>
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={task.status} />
                    </TableCell>
                    <TableCell>{task.currentAgent}</TableCell>
                    <TableCell>
                      <RiskBadge level={task.riskLevel} />
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {formatDateTime(task.updatedAt)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Pending Decisions</CardTitle>
              <CardDescription>
                Tasks waiting for Founder approval.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {pendingDecisions.map((decision) => (
                <Link
                  className="block rounded-lg border p-4 transition-colors hover:bg-muted/40"
                  href="/decisions"
                  key={decision.id}
                >
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-medium">{decision.taskName}</p>
                    <RiskBadge level={decision.riskLevel} />
                  </div>
                  <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">
                    {decision.murphyRiskSummary}
                  </p>
                </Link>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Latest agent and system events from the audit ledger.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {auditEvents.slice(0, 4).map((event) => (
                <div className="flex gap-3" key={event.id}>
                  <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-md border bg-muted text-muted-foreground">
                    <Activity className="h-4 w-4" aria-hidden="true" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="text-sm font-medium">{event.agent}</p>
                      <StatusBadge status={event.status} />
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {event.event}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {formatDateTime(event.timestamp)}
                    </p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
