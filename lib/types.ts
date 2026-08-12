export type WorkflowStatus =
  | "pending"
  | "running"
  | "completed"
  | "failed"
  | "blocked"
  | "waiting_approval";

export type RiskLevel = "low" | "medium" | "high" | "critical";

export type ApprovalStatus = "pending" | "approved" | "rejected";

export type AgentHealth = "healthy" | "degraded" | "offline";

export type AgentOperationalStatus = "active" | "idle" | "failed";

export type MemoryType = "Working" | "Episodic" | "Semantic" | "Strategic";

export type MemoryStatus = "Candidate" | "Approved" | "Canonical" | "Deprecated";

export type AuditStatus = "success" | "warning" | "failed" | "blocked";

export interface RiskReport {
  riskLevel: RiskLevel;
  category: string;
  failureModes: string[];
  securityConcerns: string[];
  recommendation: string;
}

export interface PolicyVerdict {
  riskTier: RiskLevel;
  approved: boolean;
  humanApprovalRequired: boolean;
  justification: string;
}

export interface PragyaPlan {
  summary: string;
  steps: string[];
  assumptions: string[];
}

export interface AgentTraceStep {
  id: string;
  agentName: string;
  status: WorkflowStatus;
  activity: string;
  timestamp: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: WorkflowStatus;
  currentAgent: string;
  currentStage: string;
  riskLevel: RiskLevel;
  createdAt: string;
  updatedAt: string;
  plan?: PragyaPlan;
  riskReport?: RiskReport;
  policyVerdict?: PolicyVerdict;
  executionResult?: string;
  errors?: string[];
  trace: AgentTraceStep[];
}

export interface Decision {
  id: string;
  taskId: string;
  taskName: string;
  pragyaSummary: string;
  riskLevel: RiskLevel;
  murphyRiskSummary: string;
  maryadaVerdict: PolicyVerdict;
  approvalStatus: ApprovalStatus;
  plan: PragyaPlan;
  riskReport: RiskReport;
  updatedAt: string;
}

export interface MemoryItem {
  id: string;
  title: string;
  type: MemoryType;
  status: MemoryStatus;
  source: string;
  confidence: number;
  createdDate: string;
  reviewDate: string;
  details: string;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  status: AgentOperationalStatus;
  currentTask: string;
  lastActivity: string;
  health: AgentHealth;
  description: string;
  recentActivity: string[];
  recentExecutions: {
    id: string;
    task: string;
    status: WorkflowStatus;
    timestamp: string;
  }[];
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  task: string;
  agent: string;
  action: string;
  status: AuditStatus;
  event: string;
  details: string;
}
