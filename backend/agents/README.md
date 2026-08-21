# BRAHMA COS Agents

Production-oriented:

KARMA → PRAGYA → MURPHY → MARYADA → RACHIT

## Production environment

For Render/OpenRouter:

```env
LLM_MODEL=openrouter/free
OPENROUTER_API_KEY=...
LLM_TIMEOUT=60
LLM_TEMPERATURE=0
```

Keep the API key only in Render Environment Variables. Never commit it.

## Local Ollama

```env
LLM_MODEL=ollama/llama3.2:3b
OLLAMA_API_BASE=http://localhost:11434
```

## Important fixes in this version

- LLM model is read from `LLM_MODEL`; no production Ollama hardcoding.
- OpenRouter API key is passed explicitly.
- `openrouter/free` does not force `response_format`, because the free router can select models with different structured-output support.
- PRAGYA, MURPHY, and MARYADA explicitly reject JSON schemas returned by smaller models.
- Defensive JSON parsing handles markdown fences and safe single-quote fallback.
- Pydantic validates the final data object.
- MARYADA has deterministic high-risk guardrails and fails closed.
- RACHIT executes only after explicit MARYADA approval.
- HIGH/CRITICAL risk is never automatically approved.

## Test locally

From the directory containing the `agents` package:

```bash
python -m agents.test_run
```

Expected:
- LOW-RISK test can complete when OpenRouter is available.
- HIGH-RISK test is blocked by MARYADA even if the LLM is unavailable.
