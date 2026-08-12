"use client";

import { useEffect, useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";

import { EmptyState } from "@/components/common/empty-state";
import { ErrorState } from "@/components/common/error-state";
import { PageHeader } from "@/components/common/page-header";
import { RiskBadge } from "@/components/common/risk-badge";
import { StatusBadge } from "@/components/common/status-badge";
import { TaskCard } from "@/components/tasks/task-card";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import type { Task } from "@/lib/types";
import { formatDateTime } from "@/lib/utils";

const storageKey = "brahma-cos-local-tasks";

export function TaskSubmitPanel({ initialTasks }: { initialTasks: Task[] }) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const raw = window.localStorage.getItem(storageKey);
    if (raw) {
      try {
        const saved = JSON.parse(raw) as Task[];
        setTasks([...saved, ...initialTasks]);
      } catch {
        setTasks(initialTasks);
      }
    }
  }, [initialTasks]);

  const filteredTasks = useMemo(() => {
    const normalized = search.trim().toLowerCase();
    if (!normalized) {
      return tasks;
    }

    return tasks.filter((task) =>
      [task.title, task.description, task.currentAgent, task.currentStage]
        .join(" ")
        .toLowerCase()
        .includes(normalized)
    );
  }, [search, tasks]);

  function submitTask(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!description.trim()) {
      setError("Add a task description before submitting.");
      return;
    }

    setLoading(true);

    window.setTimeout(() => {
      const now = new Date().toISOString();
      const newTask: Task = {
        id: `local-${Date.now()}`,
        title: title.trim() || "Untitled Founder task",
        description: description.trim(),
        status: "pending",
        currentAgent: "KARMA",
        currentStage: "Task intake",
        riskLevel: "medium",
        createdAt: now,
        updatedAt: now,
        trace: [
          {
            id: "karma",
            agentName: "KARMA",
            status: "pending",
            activity: "Local prototype task queued for intake.",
            timestamp: now
          },
          {
            id: "kosh-smriti",
            agentName: "KOSH / SMRITI",
            status: "pending",
            activity: "Context retrieval has not started.",
            timestamp: now
          },
          {
            id: "pragya",
            agentName: "PRAGYA",
            status: "pending",
            activity: "Plan generation has not started.",
            timestamp: now
          },
          {
            id: "murphy",
            agentName: "MURPHY",
            status: "pending",
            activity: "Risk review has not started.",
            timestamp: now
          },
          {
            id: "maryada",
            agentName: "MARYADA",
            status: "pending",
            activity: "Policy review has not started.",
            timestamp: now
          },
          {
            id: "rachit",
            agentName: "RACHIT",
            status: "pending",
            activity: "Delivery has not started.",
            timestamp: now
          }
        ]
      };

      const savedTasks = [newTask, ...tasks.filter((task) => task.id.startsWith("local-"))];
      window.localStorage.setItem(storageKey, JSON.stringify(savedTasks));
      setTasks((current) => [newTask, ...current]);
      setTitle("");
      setDescription("");
      setSuccess("Task submitted locally and queued for KARMA.");
      setLoading(false);
    }, 500);
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Task Console"
        description="Submit and inspect Founder tasks using mock workflow state. This prototype does not execute agents."
      />

      <div className="grid gap-6 xl:grid-cols-[minmax(0,0.95fr)_minmax(0,1.4fr)]">
        <Card>
          <CardHeader>
            <CardTitle>Submit Task</CardTitle>
            <CardDescription>
              Add a task title and detailed instruction for the local prototype.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={submitTask}>
              {error ? <ErrorState message={error} /> : null}
              {success ? (
                <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
                  {success}
                </div>
              ) : null}
              <div className="space-y-2">
                <Label htmlFor="task-title">Optional title</Label>
                <Input
                  disabled={loading}
                  id="task-title"
                  onChange={(event) => setTitle(event.target.value)}
                  placeholder="Prepare board update narrative"
                  value={title}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="task-description">Task</Label>
                <Textarea
                  disabled={loading}
                  id="task-description"
                  onChange={(event) => setDescription(event.target.value)}
                  placeholder="Describe the desired outcome, constraints, and any approval sensitivity."
                  value={description}
                />
              </div>
              <Button disabled={loading || !description.trim()} type="submit">
                <Plus className="h-4 w-4" aria-hidden="true" />
                {loading ? "Submitting" : "Submit task"}
              </Button>
            </form>
          </CardContent>
        </Card>

        <section className="space-y-4">
          <div className="flex flex-col gap-4 rounded-lg border bg-card p-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-base font-semibold">Recent Tasks</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                Local submissions appear at the top of the queue.
              </p>
            </div>
            <div className="relative w-full sm:w-72">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                className="pl-9"
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search tasks"
                value={search}
              />
            </div>
          </div>
          <div className="space-y-3">
            {filteredTasks.length ? (
              filteredTasks.map((task) => <TaskCard key={task.id} task={task} />)
            ) : (
              <EmptyState
                description="Adjust search terms or submit a new local task."
                icon={Search}
                title="No tasks found"
              />
            )}
          </div>
        </section>
      </div>

      <div className="rounded-lg border bg-card p-5">
        <div className="grid gap-4 md:grid-cols-4">
          {tasks.slice(0, 4).map((task) => (
            <div className="min-w-0" key={task.id}>
              <p className="truncate text-sm font-medium">{task.title}</p>
              <div className="mt-2 flex flex-wrap gap-2">
                <StatusBadge status={task.status} />
                <RiskBadge level={task.riskLevel} />
              </div>
              <p className="mt-2 text-xs text-muted-foreground">
                {formatDateTime(task.updatedAt)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
