"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity,
  AlertTriangle,
  Bot,
  ClipboardCheck,
  ListChecks,
} from "lucide-react";
import api from "@/lib/api";
import { PageHeader } from "@/components/common/page-header";
import { StatCard } from "@/components/common/stat-card";
import { StatusBadge } from "@/components/common/status-badge";
import { RiskBadge } from "@/components/common/risk-badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Task, Agent, AuditEvent } from "@/lib/types";
import { formatDateTime } from "@/lib/utils";
export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]),
    [agents, setAgents] = useState<Agent[]>([]),
    [audit, setAudit] = useState<AuditEvent[]>([]),
    [error, setError] = useState("");
  useEffect(() => {
    Promise.all([api.get("/tasks/"), api.get("/agents/"), api.get("/audit/")])
      .then(([t, a, l]) => {
        setTasks(t.data);
        setAgents(a.data);
        setAudit(l.data);
      })
      .catch(() =>
        setError(
          "Backend is unavailable. Start FastAPI to load live dashboard data.",
        ),
      );
  }, []);
  const pending = tasks.filter((t) => t.status === "BLOCKED");
  const risks = tasks.filter((t) =>
    ["HIGH", "CRITICAL"].includes(t.risk_level),
  );
  return (
    <div className="space-y-6">
      <PageHeader
        title="Founder Command Center"
        description="Live operating view of tasks, approvals, agents and audit activity."
        action={
          <Button asChild>
            <Link href="/tasks">Create task</Link>
          </Button>
        }
      />
      {error && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          {error}
        </div>
      )}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Active Tasks"
          value={
            tasks.filter((t) =>
              ["RUNNING", "PENDING", "BLOCKED"].includes(t.status),
            ).length
          }
          detail="Running or waiting"
          icon={ListChecks}
        />
        <StatCard
          label="Pending Decisions"
          value={pending.length}
          detail="Founder review queue"
          icon={ClipboardCheck}
        />
        <StatCard
          label="Active Agents"
          value={agents.filter((a) => a.status === "active").length}
          detail={`${agents.length} monitored`}
          icon={Bot}
        />
        <StatCard
          label="Recent Risks"
          value={risks.length}
          detail="High and critical"
          icon={AlertTriangle}
        />
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.6fr_.9fr]">
        <Card>
          <CardHeader>
            <CardTitle>Recent Tasks</CardTitle>
            <CardDescription>Live task state from FastAPI.</CardDescription>
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
                {tasks.slice(0, 10).map((t) => (
                  <TableRow key={t.id}>
                    <TableCell>
                      <Link
                        className="font-medium hover:underline"
                        href={`/tasks/${t.id}`}
                      >
                        {t.title}
                      </Link>
                      <p className="text-xs text-muted-foreground">
                        {t.prompt}
                      </p>
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={t.status} />
                    </TableCell>
                    <TableCell>{t.current_agent || "-"}</TableCell>
                    <TableCell>
                      <RiskBadge level={t.risk_level} />
                    </TableCell>
                    <TableCell>
                      {formatDateTime(t.updated_at || t.created_at)}
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
              {pending.length ? (
                pending.slice(0, 5).map((t) => (
                  <Link
                    key={t.id}
                    href="/decisions"
                    className="block rounded-lg border p-4 hover:bg-muted/40"
                  >
                    <div className="flex justify-between gap-3">
                      <span className="font-medium">{t.title}</span>
                      <RiskBadge level={t.risk_level} />
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {t.policy_verdict?.justification}
                    </p>
                  </Link>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  No pending decisions.
                </p>
              )}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Latest NIYANTRA audit events.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {audit.slice(0, 5).map((e) => (
                <div key={e.id} className="flex gap-3">
                  <div className="mt-1 flex h-8 w-8 items-center justify-center rounded-md border bg-muted">
                    <Activity className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="flex gap-2">
                      <b className="text-sm">{e.agent}</b>
                      <StatusBadge
                        status={
                          e.status === "success"
                            ? "COMPLETED"
                            : e.status === "blocked"
                              ? "BLOCKED"
                              : e.status === "failed"
                                ? "FAILED"
                                : "RUNNING"
                        }
                      />
                    </div>
                    <p className="text-sm text-muted-foreground">{e.event}</p>
                    <p className="text-xs text-muted-foreground">
                      {formatDateTime(e.timestamp)}
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
