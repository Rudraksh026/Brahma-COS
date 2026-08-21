# BRAHMA COS Agents

Production-oriented KARMA → PRAGYA → MURPHY → MARYADA → RACHIT agent graph.

## Production environment

Set:

```env
LLM_MODEL=openrouter/free
OPENROUTER_API_KEY=...
LLM_TIMEOUT=60
LLM_TEMPERATURE=0
```

`OPENROUTER_API_KEY` must be kept in the hosting provider's secret/environment-variable store and must not be committed to Git.

## Local Ollama

```env
LLM_MODEL=ollama/llama3.2:3b
OLLAMA_API_BASE=http://localhost:11434
```

## Behavior

- PRAGYA validates an actual plan, not a JSON schema.
- MURPHY fails closed to HIGH risk if analysis fails.
- MARYADA has deterministic high-risk guardrails and never auto-approves HIGH/CRITICAL risk.
- RACHIT executes only when MARYADA explicitly approves and does not require human approval.
- LLM calls are provider-aware and support OpenRouter and Ollama.
- Structured responses are parsed defensively, including accidental Markdown fences.

## Test

From the package's parent directory:

```bash
python -m agents.test_run
```

The low-risk test requires a working LLM. The high-risk test is blocked by deterministic MARYADA policy even if an LLM is unavailable.
