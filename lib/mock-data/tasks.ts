import type { Task } from "@/lib/types";

const commonTrace: NonNullable<Task["trace"]> = [
  {
    agent: "KARMA",
    status: "COMPLETED",
    description:
      "Captured founder intent and normalized the task envelope.",
    timestamp: "2026-08-13T03:20:00Z",
  },
  {
    agent: "KOSH / SMRITI",
    status: "COMPLETED",
    description:
      "Retrieved relevant operating memory and prior execution context.",
    timestamp: "2026-08-13T03:24:00Z",
  },
  {
    agent: "PRAGYA",
    status: "COMPLETED",
    description:
      "Drafted an execution plan with assumptions and expected outcomes.",
    timestamp: "2026-08-13T03:31:00Z",
  },
  {
    agent: "MURPHY",
    status: "COMPLETED",
    description:
      "Reviewed operational, policy, and failure mode risk.",
    timestamp: "2026-08-13T03:38:00Z",
  },
  {
    agent: "MARYADA",
    status: "PENDING",
    description:
      "Flagged the task for Founder approval before execution.",
    timestamp: "2026-08-13T03:42:00Z",
  },
  {
    agent: "RACHIT",
    status: "PENDING",
    description:
      "Awaiting approval gate before delivery orchestration.",
    timestamp: "2026-08-13T03:42:00Z",
  },
];

export const tasks: Task[] = [
  {
    id: 1,
    title: "Prepare investor diligence workspace",
    prompt:
      "Create a structured diligence package outline using current metrics, founder notes, and prior board questions.",
    status: "BLOCKED",
    current_agent: "MARYADA",
    risk_level: "HIGH",
    created_at: "2026-08-13T03:12:00Z",
    updated_at: "2026-08-13T03:42:00Z",

    plan: {
      summary:
        "Assemble a diligence workspace, identify sensitive materials, and route high-risk disclosures for approval.",
      steps: [
        "Map requested diligence categories to existing source material.",
        "Draft a clean workspace index and access policy.",
        "Mark financial and customer references that need founder review.",
        "Prepare the delivery checklist for RACHIT after approval.",
      ],
      tools_needed: [],
      assumptions: [
        "Founder approval is required for sensitive financial disclosures.",
        "No documents are sent externally until policy clearance is complete.",
      ],
    },

    risk_report: {
      risk_level: "HIGH",
      failure_modes: [
        "Draft package may include unapproved financial assumptions.",
        "External recipients may receive customer references too early.",
      ],
      security_concerns: [
        "Investor workspace should use least-privilege access.",
        "Customer names and revenue data need explicit clearance.",
      ],
      recommendation:
        "Proceed only after Founder confirms disclosure scope and recipient access policy.",
    },

    policy_verdict: {
      risk_tier: "HIGH",
      approved: false,
      requires_human: true,
      justification:
        "The task touches sensitive commercial and financial material, so execution must wait for founder approval.",
    },

    errors: [],
    trace: commonTrace,
  },

  {
    id: 2,
    title: "Summarize product telemetry anomalies",
    prompt:
      "Review the latest telemetry digest and summarize anomalies that may affect enterprise onboarding.",
    status: "RUNNING",
    current_agent: "MURPHY",
    risk_level: "MEDIUM",
    created_at: "2026-08-13T02:48:00Z",
    updated_at: "2026-08-13T03:30:00Z",

    plan: {
      summary:
        "Identify anomalous usage patterns and convert them into a concise operational risk summary.",
      steps: [
        "Group anomalies by customer segment.",
        "Separate noise from repeated operational signals.",
        "Draft mitigation options for onboarding owners.",
      ],
      tools_needed: [],
      assumptions: [
        "Telemetry has already been scrubbed of private user content.",
        "This phase is summarization only, not remediation.",
      ],
    },

    risk_report: {
      risk_level: "MEDIUM",
      failure_modes: [
        "Anomalies may be over-attributed without enough historical comparison.",
        "Medium-priority signals may crowd out urgent onboarding blockers.",
      ],
      security_concerns: [
        "Telemetry summaries should avoid raw identifiers.",
      ],
      recommendation:
        "Keep the report scoped to aggregate patterns and include confidence notes.",
    },

    policy_verdict: {
      risk_tier: "MEDIUM",
      approved: true,
      requires_human: false,
      justification:
        "Aggregated operational telemetry is allowed for internal review when identifiers remain excluded.",
    },

    errors: [],

    trace: [
      {
        agent: "KARMA",
        status: "COMPLETED",
        description:
          "Captured request and converted it into analysis criteria.",
        timestamp: "2026-08-13T02:50:00Z",
      },
      {
        agent: "KOSH / SMRITI",
        status: "COMPLETED",
        description:
          "Retrieved prior onboarding anomaly patterns.",
        timestamp: "2026-08-13T03:00:00Z",
      },
      {
        agent: "PRAGYA",
        status: "COMPLETED",
        description:
          "Prepared the analysis plan and output structure.",
        timestamp: "2026-08-13T03:12:00Z",
      },
      {
        agent: "MURPHY",
        status: "RUNNING",
        description:
          "Evaluating false positive risk and security exposure.",
        timestamp: "2026-08-13T03:30:00Z",
      },
      {
        agent: "MARYADA",
        status: "PENDING",
        description:
          "Policy verdict pending risk review completion.",
        timestamp: "2026-08-13T03:30:00Z",
      },
      {
        agent: "RACHIT",
        status: "PENDING",
        description:
          "Waiting for finalized internal summary.",
        timestamp: "2026-08-13T03:30:00Z",
      },
    ],
  },

  {
    id: 3,
    title: "Draft customer renewal briefing",
    prompt:
      "Create a short renewal briefing for a strategic account using approved memory and recent account activity.",
    status: "COMPLETED",
    current_agent: "RACHIT",
    risk_level: "LOW",
    created_at: "2026-08-12T15:10:00Z",
    updated_at: "2026-08-12T16:05:00Z",

    plan: {
      summary:
        "Create a concise renewal briefing using approved account information.",
      steps: [
        "Review approved account milestones.",
        "Identify recent account activity.",
        "Summarize open risks and opportunities.",
        "Prepare recommended next steps.",
      ],
      tools_needed: [],
      assumptions: [
        "Only approved account memory is used.",
        "No sensitive information is disclosed externally.",
      ],
    },

    risk_report: {
      risk_level: "LOW",
      failure_modes: [
        "Briefing may omit a relevant account milestone.",
      ],
      security_concerns: [],
      recommendation:
        "Proceed using approved account information and review the final briefing before delivery.",
    },

    policy_verdict: {
      risk_tier: "LOW",
      approved: true,
      requires_human: false,
      justification:
        "Internal account briefing generation is low risk when based on approved information.",
    },

    execution_result: {
      status: "COMPLETED",
      message:
        "Renewal briefing prepared with approved milestones, open risks, and recommended next steps.",
      executed_steps: 4,
    },

    errors: [],

    trace: [
      {
        agent: "KARMA",
        status: "COMPLETED",
        description:
          "Captured briefing objective and audience.",
        timestamp: "2026-08-12T15:13:00Z",
      },
      {
        agent: "KOSH / SMRITI",
        status: "COMPLETED",
        description:
          "Retrieved approved account milestones and recent notes.",
        timestamp: "2026-08-12T15:24:00Z",
      },
      {
        agent: "PRAGYA",
        status: "COMPLETED",
        description:
          "Built a briefing outline and renewal narrative.",
        timestamp: "2026-08-12T15:36:00Z",
      },
      {
        agent: "MURPHY",
        status: "COMPLETED",
        description:
          "Confirmed low risk and no sensitive financial exposure.",
        timestamp: "2026-08-12T15:44:00Z",
      },
      {
        agent: "MARYADA",
        status: "COMPLETED",
        description:
          "Approved internal account briefing generation.",
        timestamp: "2026-08-12T15:48:00Z",
      },
      {
        agent: "RACHIT",
        status: "COMPLETED",
        description:
          "Generated and packaged the final briefing.",
        timestamp: "2026-08-12T16:05:00Z",
      },
    ],
  },

  {
    id: 4,
    title: "Validate hiring plan assumptions",
    prompt:
      "Compare proposed team expansion assumptions against operating priorities and runway guardrails.",
    status: "BLOCKED",
    current_agent: "KOSH",
    risk_level: "CRITICAL",
    created_at: "2026-08-12T11:05:00Z",
    updated_at: "2026-08-12T11:42:00Z",

    plan: {
      summary:
        "Validate hiring assumptions against canonical operating memory and current runway constraints.",
      steps: [
        "Retrieve the latest approved runway assumptions.",
        "Compare hiring requirements against operating priorities.",
        "Identify conflicts between current and deprecated memory.",
        "Request Founder confirmation where required.",
      ],
      tools_needed: [],
      assumptions: [
        "Canonical runway data must be confirmed before execution.",
        "Deprecated memory must not be used for financial decisions.",
      ],
    },

    risk_report: {
      risk_level: "CRITICAL",
      failure_modes: [
        "Deprecated runway assumptions may result in incorrect hiring decisions.",
        "Conflicting memory may cause the wrong staffing plan to be approved.",
      ],
      security_concerns: [
        "Financial planning information should remain restricted to authorized users.",
      ],
      recommendation:
        "Block execution until the latest runway and hiring constraints are confirmed by the Founder.",
    },

    policy_verdict: {
      risk_tier: "CRITICAL",
      approved: false,
      requires_human: true,
      justification:
        "Conflicting financial planning memory requires Founder confirmation before execution.",
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
  },
];