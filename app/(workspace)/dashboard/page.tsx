"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Activity, AlertTriangle, Bot, ClipboardCheck, ListChecks, Radio, RefreshCw } from "lucide-react";
import api from "@/lib/api";
import { PageHeader } from "@/components/common/page-header";
import { StatCard } from "@/components/common/stat-card";
import { StatusBadge } from "@/components/common/status-badge";
import { RiskBadge } from "@/components/common/risk-badge";
import { EmptyState } from "@/components/common/empty-state";
import { LoadingState } from "@/components/common/loading-state";
import { ErrorState } from "@/components/common/error-state";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { Task, Agent, AuditEvent } from "@/lib/types";
import { formatDateTime } from "@/lib/utils";

function SkeletonRows(){return <>{[1,2,3].map(i=><TableRow key={i}><TableCell colSpan={5}><div className="h-12 animate-pulse rounded-lg bg-muted"/></TableCell></TableRow>)}</>}
export default function DashboardPage(){
 const[tasks,setTasks]=useState<Task[]>([]),[agents,setAgents]=useState<Agent[]>([]),[audit,setAudit]=useState<AuditEvent[]>([]),[loading,setLoading]=useState(true),[error,setError]=useState(""),[tick,setTick]=useState(0); const previous=useRef({a:-1,p:-1,r:-1});
 async function load(){setLoading(true);setError("");try{const[t,a,l]=await Promise.all([api.get("/tasks/"),api.get("/agents/"),api.get("/audit/")]);setTasks(t.data);setAgents(a.data);setAudit(l.data);setTick(x=>x+1);}catch(e){setError("Live connection is unavailable. Check the deployed FastAPI backend.")}finally{setLoading(false)}}
 useEffect(()=>{load();const id=window.setInterval(load,15000);return()=>window.clearInterval(id)},[]);
 const pending=tasks.filter(t=>t.status==="BLOCKED"); const risks=tasks.filter(t=>["HIGH","CRITICAL"].includes(t.risk_level)); const active=tasks.filter(t=>["RUNNING","PENDING","BLOCKED"].includes(t.status)).length; const activeAgents=agents.filter(a=>a.status==="active").length;
 const changed={a:previous.current.a!==-1&&previous.current.a!==active,p:previous.current.p!==-1&&previous.current.p!==pending.length,r:previous.current.r!==-1&&previous.current.r!==risks.length};
 useEffect(()=>{if(!loading) previous.current={a:active,p:pending.length,r:risks.length};},[loading,active,pending.length,risks.length]);
 return <div className="space-y-6">
  <PageHeader title="Founder Command Center" description="Live operating view of tasks, approvals, agents and audit activity." action={<div className="flex items-center gap-2"><span className="hidden sm:flex items-center gap-2 rounded-full border bg-card px-3 py-1.5 text-xs text-muted-foreground"><span className="live-dot h-2 w-2 rounded-full bg-emerald-500"/>Live · 15s</span><Button variant="outline" size="sm" onClick={load} disabled={loading}><RefreshCw className={loading?"mr-2 h-4 w-4 animate-spin":"mr-2 h-4 w-4"}/>Refresh</Button><Button asChild><Link href="/tasks">Create task</Link></Button></div>}/>
  {error&&<ErrorState message={error}/>} 
  <div className="ai-sheen rounded-2xl border p-1"><div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4 rounded-xl bg-background/95 p-1">
   {loading?<>{[1,2,3,4].map(i=><div key={i} className="h-28 animate-pulse rounded-xl bg-muted"/>)}</>:<>
   <StatCard label="Active Tasks" value={active} detail="Running or waiting" icon={ListChecks} tone={active?"warning":"success"} changed={changed.a}/>
   <StatCard label="Pending Decisions" value={pending.length} detail={pending.length?"Founder review queue":"All decisions clear"} icon={ClipboardCheck} tone={pending.length?"warning":"success"} changed={changed.p}/>
   <StatCard label="Active Agents" value={activeAgents} detail={`${agents.length} monitored`} icon={Bot} tone={activeAgents?"success":"neutral"}/>
   <StatCard label="Recent Risks" value={risks.length} detail={risks.length?"High and critical":"No high-risk tasks"} icon={AlertTriangle} tone={risks.some(r=>r.risk_level==="CRITICAL")?"danger":risks.length?"warning":"success"} changed={changed.r}/>
   </>}
  </div></div>
  <div className="grid gap-6 xl:grid-cols-[1.6fr_.9fr]">
   <Card><CardHeader><div className="flex items-center justify-between"><div><CardTitle>Recent Tasks</CardTitle><CardDescription>Live task state from FastAPI.</CardDescription></div><Radio className="h-4 w-4 text-emerald-500"/></div></CardHeader><CardContent>{loading?<LoadingState label="Streaming live task state…"/>:<Table><TableHeader><TableRow><TableHead>Task</TableHead><TableHead>Status</TableHead><TableHead>Agent</TableHead><TableHead>Risk</TableHead><TableHead>Updated</TableHead></TableRow></TableHeader><TableBody>{tasks.length?tasks.slice(0,10).map(t=><TableRow key={t.id} className="transition-colors hover:bg-muted/40"><TableCell><Link className="font-medium hover:underline" href={`/tasks/${t.id}`}>{t.title}</Link><p className="max-w-md truncate text-xs text-muted-foreground">{t.prompt}</p></TableCell><TableCell><StatusBadge status={t.status}/></TableCell><TableCell>{t.current_agent||"—"}</TableCell><TableCell><RiskBadge level={t.risk_level}/></TableCell><TableCell>{formatDateTime(t.updated_at||t.created_at)}</TableCell></TableRow>):<TableRow><TableCell colSpan={5}><EmptyState title="No live tasks yet" description="Create a task to start the agent workflow." icon={ListChecks}/></TableCell></TableRow>}</TableBody></Table>}</CardContent></Card>
   <div className="space-y-6"><Card><CardHeader><CardTitle>Pending Decisions</CardTitle><CardDescription>Tasks waiting for Founder approval.</CardDescription></CardHeader><CardContent className="space-y-3">{loading?<LoadingState label="Checking approval queue…"/>:pending.length?pending.slice(0,5).map(t=><Link key={t.id} href="/decisions" className="block rounded-xl border p-4 transition-all hover:-translate-y-0.5 hover:bg-muted/40 hover:shadow-sm"><div className="flex justify-between gap-3"><span className="font-medium">{t.title}</span><RiskBadge level={t.risk_level}/></div><p className="mt-2 text-sm text-muted-foreground">{t.policy_verdict?.justification||"Human review required."}</p></Link>):<EmptyState title="Approval queue clear" description="No tasks currently require Founder approval." icon={ClipboardCheck}/>}</CardContent></Card>
   <Card><CardHeader><CardTitle>Recent Activity</CardTitle><CardDescription>Latest NIYANTRA audit events.</CardDescription></CardHeader><CardContent className="space-y-4">{loading?<LoadingState label="Loading audit stream…"/>:audit.length?audit.slice(0,5).map(e=><div key={e.id} className="flex gap-3"><div className="mt-1 flex h-8 w-8 items-center justify-center rounded-lg border bg-muted"><Activity className="h-4 w-4"/></div><div><div className="flex gap-2"><b className="text-sm">{e.agent}</b><StatusBadge status={e.status==="success"?"COMPLETED":e.status==="blocked"?"BLOCKED":e.status==="failed"?"FAILED":"RUNNING"}/></div><p className="text-sm text-muted-foreground">{e.event}</p><p className="text-xs text-muted-foreground">{formatDateTime(e.timestamp)}</p></div></div>):<EmptyState title="No activity yet" description="Audit events will appear here as the system runs." icon={Activity}/>}</CardContent></Card></div>
  </div>
  <p className="text-center text-xs text-muted-foreground">Live data connected · refresh cycle {tick}</p>
 </div>
}
