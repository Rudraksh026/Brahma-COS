import type { Decision } from "@/lib/types";

import { tasks } from "@/lib/mock-data/tasks";

const diligenceTask = tasks[0];

export const decisions: Decision[] = [
  {
    id: 1,
    title: diligenceTask.title,
    prompt: diligenceTask.prompt,
    status: diligenceTask.status,
    risk_level: diligenceTask.risk_level,
    current_agent: diligenceTask.current_agent,
    created_at: diligenceTask.created_at,
    updated_at: "2026-08-13T03:44:00Z",

    plan: diligenceTask.plan,

    risk_report: diligenceTask.risk_report,

    policy_verdict: diligenceTask.policy_verdict,

    execution_result: diligenceTask.execution_result,

    errors: diligenceTask.errors,

    trace: diligenceTask.trace,

    approvalStatus: "pending",
  },

  {
    id: 2,
    title: "Validate hiring plan assumptions",
    prompt:
      "Compare proposed team expansion assumptions against operating priorities and runway guardrails.",
    status: "BLOCKED",
    risk_level: "CRITICAL",
    current_agent: "KOSH",
    created_at: "2026-08-12T11:05:00Z",
    updated_at: "2026-08-12T11:46:00Z",

    plan: {
      summary:
        "Resolve memory conflicts before generating hiring plan validation.",
      steps: [
        "Show conflicting runway memories to the Founder.",
        "Select the canonical constraint set.",
        "Run a fresh plan validation using only approved context.",
      ],
      tools_needed: [],
      assumptions: [
        "Budget and runway guidance may have changed.",
        "Deprecated memory should not be used for final recommendations.",
      ],
    },

    risk_report: {
      risk_level: "CRITICAL",
      failure_modes: [
        "Hiring recommendation could exceed runway guardrails.",
        "Deprecated constraints could override founder intent.",
      ],
      security_concerns: [
        "Compensation and runway data should remain access restricted.",
      ],
      recommendation:
        "Block automated planning until Founder selects the canonical finance memory.",
    },

    policy_verdict: {
      risk_tier: "CRITICAL",
      approved: false,
      requires_human: true,
      justification:
        "The task must pause until the Founder confirms which runway and hiring constraints are canonical.",
    },

    errors: [
      "Runway model memory is marked deprecated.",
      "Latest hiring constraints require founder confirmation.",
    ],

    trace: [
      {
        agent: "KARMA",
        status: "COMPLETED",
        description:
          "Converted hiring plan prompt into structured review criteria.",
        timestamp: "2026-08-12T11:08:00Z",
      },
      {
        agent: "KOSH / SMRITI",
        status: "BLOCKED",
        description:
          "Found conflicting memory for runway and hiring constraints.",
        timestamp: "2026-08-12T11:42:00Z",
      },
      {
        agent: "PRAGYA",
        status: "PENDING",
        description:
          "Waiting for canonical memory confirmation.",
        timestamp: "2026-08-12T11:42:00Z",
      },
      {
        agent: "MURPHY",
        status: "PENDING",
        description:
          "Risk analysis pending plan generation.",
        timestamp: "2026-08-12T11:42:00Z",
      },
      {
        agent: "MARYADA",
        status: "PENDING",
        description:
          "Policy review pending risk analysis.",
        timestamp: "2026-08-12T11:42:00Z",
      },
      {
        agent: "RACHIT",
        status: "PENDING",
        description:
          "Delivery paused while context is blocked.",
        timestamp: "2026-08-12T11:42:00Z",
      },
    ],

    approvalStatus: "pending",
  },
];