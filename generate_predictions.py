# Multi-Domain Support Triage Agent

## Overview
Terminal-based support triage agent for HackerRank, Claude (Anthropic), and Visa support tickets.

## Architecture
- `agent.py` — Main triage agent (requires ANTHROPIC_API_KEY)
- `generate_predictions.py` — Corpus-grounded predictions generator (no API key needed)

## How It Works
1. For each ticket, the agent identifies the company domain.
2. It injects the relevant support corpus (fetched from official sites) into the prompt.
3. It asks Claude to classify, respond or escalate, and justify the decision.

### Key design decisions:
- **Corpus grounding**: Static corpus built from official support sites (hackerrank.com, support.claude.com, visa.co.in/support.html). No hallucination.
- **Escalation logic**: Hard rules for billing, fraud, identity theft, security vulns, non-admin account access, score disputes, subscription changes.
- **Prompt injection detection**: System prompt instructs the model to detect and flag injection attempts (including in non-English text).
- **Out-of-scope handling**: Invalid/harmful requests are declined politely with `replied` + `invalid`.

## Running the Agent

```bash
export ANTHROPIC_API_KEY=your_key_here
pip install anthropic

# Full agent run (with live API):
python code/agent.py support_tickets/support_tickets.csv output.csv

# Pre-computed predictions (no API key needed):
python code/generate_predictions.py
```

## Output Format
CSV columns: `issue, subject, company, response, product_area, status, request_type, justification`

- `status`: `replied` | `escalated`
- `request_type`: `product_issue` | `feature_request` | `bug` | `invalid`
