export type WorkflowStatus="PENDING"|"RUNNING"|"COMPLETED"|"FAILED"|"BLOCKED";
export type RiskLevel="LOW"|"MEDIUM"|"HIGH"|"CRITICAL";
export interface PragyaPlan{summary:string;steps:string[];tools_needed:string[];assumptions:string[]}
export interface RiskReport{risk_level:RiskLevel;failure_modes:string[];security_concerns:string[];recommendation:string}
export interface PolicyVerdict{risk_tier:RiskLevel;approved:boolean;requires_human:boolean;justification:string}
export interface ExecutionResult{status:string;message:string;executed_steps:number}
export interface AgentTraceStep{agent:string;status:string;description:string;timestamp?:string}
export interface Task{id:number;title:string;prompt:string;status:WorkflowStatus;risk_level:RiskLevel;current_agent?:string;created_at:string;updated_at?:string;plan?:PragyaPlan;risk_report?:RiskReport;policy_verdict?:PolicyVerdict;execution_result?:ExecutionResult;errors?:string[];trace?:AgentTraceStep[]}
export type ApprovalStatus="pending"|"approved"|"rejected";
export interface Decision extends Task{approvalStatus:ApprovalStatus}
export interface MemoryItem{id:number;content:string;source:string;approved:string;created_at:string}
export type MemoryStatus="PENDING"|"APPROVED"; export type MemoryType="Working"|"Episodic"|"Semantic"|"Strategic";
export type AuditStatus="success"|"warning"|"failed"|"blocked";
export interface AuditEvent{id:number;task_id?:number;task:string;agent:string;action:string;status:AuditStatus;event:string;details:string;timestamp:string}
export type AgentOperationalStatus="active"|"idle"|"failed";
export interface Agent{ name:string; role:string; status:AgentOperationalStatus; current_task?:string|null; last_activity?:string|null; health:string }
export interface KnowledgeDocument{title:string}
