from __future__ import annotations

import json
import re
from typing import Any, Dict

from ..json_utils import parse_json_object
from ..llm import get_model, llm_completion
from ..state import AgentState, PolicyVerdict


HIGH_RISK_PATTERNS = [
    r"\bwire transfer\b",
    r"\bfinancial transaction\b",
    r"\btransfer\s+\$?\d",
    r"\bsend\s+(money|funds|payment)\b",
    r"\bpay\s+(?:a|the)?\s*(?:vendor|invoice|bill)\b",
    r"\bdelete\b.*\b(database|table|records?|data)\b",
    r"\bdrop\s+(database|table)\b",
    r"\berase\b.*\b(data|records?)\b",
    r"\b(sign|execute)\b.*\b(contract|legal)\b",
    r"\bchange\b.*\b(password|credentials?|permissions?|access)\b",
    r"\bgrant\b.*\b(admin|root)\b",
    r"\bdeploy\b.*\bproduction\b",
]


def _is_deterministically_high_risk(intent: str) -> bool:
    text = intent.lower()
    return any(re.search(pattern, text) for pattern in HIGH_RISK_PATTERNS)


def _safe_verdict(reason: str) -> PolicyVerdict:
    return PolicyVerdict(
        risk_tier="HIGH",
        approved=False,
        requires_human=True,
        justification=reason,
    )


def maryada_node(state: AgentState) -> Dict[str, Any]:
    print("[MARYADA] Applying governance policies...")
    intent = (state.get("intent") or "").strip()
    plan_dict = state.get("plan") or {}
    risk_dict = state.get("risk_report") or {}
    errors = state.get("errors", [])

    # Deterministic guardrail. Never allow an LLM to approve these classes.
    if _is_deterministically_high_risk(intent):
        verdict = _safe_verdict(
            "Blocked by deterministic MARYADA policy: the requested action is high-risk and requires human approval."
        )
        return {"current_agent": "MARYADA", "policy_verdict": verdict.model_dump()}

    # Fail closed if an upstream agent failed.
    if errors:
        verdict = _safe_verdict(
            f"Upstream agent errors detected: {'; '.join(errors)}"
        )
        return {"current_agent": "MARYADA", "policy_verdict": verdict.model_dump()}

    # Never allow a high/critical MURPHY result to auto-approve.
    if str(risk_dict.get("risk_level", "")).upper() in {"HIGH", "CRITICAL"}:
        verdict = _safe_verdict(
            "MURPHY identified HIGH/CRITICAL risk; human approval is required."
        )
        return {"current_agent": "MARYADA", "policy_verdict": verdict.model_dump()}

    system_prompt = """
You are MARYADA, the governance and policy gate of BRAHMA COS.
Apply the proposed plan and MURPHY risk report against a conservative policy.

Return ONLY a valid JSON object with exactly:
{
  "risk_tier": "LOW|MEDIUM|HIGH|CRITICAL",
  "approved": true,
  "requires_human": false,
  "justification": "short reason"
}

Policy:
- Financial transfers, destructive database/data actions, credential/access changes,
  legal commitments, production deployments, or similarly consequential actions require human approval.
- HIGH or CRITICAL risk can never be auto-approved.
- If uncertain, require human approval.
- Never return a JSON schema.
- No markdown, commentary, or chain-of-thought.
""".strip()

    user_prompt = (
        f"Intent: {intent}\n\n"
        f"Proposed Plan:\n{json.dumps(plan_dict, indent=2)}\n\n"
        f"Risk Report:\n{json.dumps(risk_dict, indent=2)}"
    )

    try:
        print(f"[MARYADA] Using model: {get_model()}")
        response = llm_completion(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            json_mode=True,
        )
        parsed = parse_json_object(response.choices[0].message.content)

        if "properties" in parsed and "risk_tier" not in parsed:
            raise ValueError("MARYADA returned the JSON schema instead of a policy verdict")

        verdict = PolicyVerdict.model_validate(parsed)
        verdict.risk_tier = verdict.risk_tier.upper()

        # Final deterministic override.
        if verdict.risk_tier in {"HIGH", "CRITICAL"}:
            verdict.approved = False
            verdict.requires_human = True
            verdict.justification += " MARYADA override: high-risk tiers require human approval."

        if verdict.requires_human:
            verdict.approved = False

        return {"current_agent": "MARYADA", "policy_verdict": verdict.model_dump()}

    except Exception as exc:
        message = f"MARYADA Error: {exc}"
        print(f"[MARYADA] {message}")
        verdict = _safe_verdict("Policy evaluation failed due to a system error; execution is blocked.")
        return {
            "current_agent": "MARYADA",
            "policy_verdict": verdict.model_dump(),
            "errors": state.get("errors", []) + [message],
        }
