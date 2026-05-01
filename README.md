# multi-domain-support-triage-challenge
Terminal-based multi-domain support triage agent that processes tickets across HackerRank, Claude, and Visa ecosystems. It classifies intent, risk, and domain, retrieves relevant corpus-based documentation using semantic search, and decides whether to respond or escalate. Ensures safe, grounded, and explainable outputs.

# Multi-Domain Support Triage Agent

This project is a terminal-based support triage system that processes customer support tickets across three domains:
	HackerRank
	Claude
	Visa
The system reads each ticket, understands the issue, retrieves relevant support information, and decides whether to respond automatically or escalate to human support.

## What It Does
For every ticket, the agent:
1. Identifies the request type (FAQ, payment issue, API issue, etc.)
2. Classifies the domain (HackerRank, Claude, Visa)
3. Detects risk level (Low, Medium, High)
4. Retrieves relevant documentation from the provided corpus
5. Decides:
	Respond (safe to answer)
	Safe Respond (answer with caution)
	Escalate (send to human support)
6. Generates a grounded response (no hallucination)

## Key Features
1. Domain-specific retrieval (better accuracy)
2. Semantic search using embeddings (FAISS)
3. Risk-aware decision system
4. No external data usage (strictly corpus-based)
5. Transparent logging for every decision

## Output Format
The system generates a CSV with:
	ticket_id
	request_type
	product_area
	decision (RESPOND / SAFE_RESPOND / ESCALATE)
	response

CSV columns: `issue, subject, company, response, product_area, status, request_type, justification`

- `status`: `replied` | `escalated`
- `request_type`: `product_issue` | `feature_request` | `bug` | `invalid`

## Decision Logic (Important)
	HIGH risk → always escalated
	MEDIUM risk → safe response
	LOW risk → respond if confidence is high
	Low retrieval confidence → escalated

## Constraints Followed
	Uses only provided support corpus
	No hallucinated policies
	Safe handling of sensitive issues
	Clear and explainable decisions

## Notes
This is not a generic chatbot. It is a controlled triage system designed for:
	Accuracy over creativity
	Safety over completeness
	Deterministic behavior over guesswork

## Architecture
- `agent.py` - Main triage agent 
- `generate_predictions.py` - Corpus-grounded predictions generator (no API key needed)

## Architecture Diagram
                ┌────────────────────┐
                │   Input Ticket     │
                └─────────┬──────────┘
                          │
                          ▼
        ┌────────────────────────────────┐
        │ Intent + Risk Classification   │
        │ (LOW / MEDIUM / HIGH)          │
        └─────────┬──────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │ Domain Classification        │
        │ (HackerRank / Claude / Visa) │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │ Domain-Specific Retrieval    │
        │ (FAISS + Embeddings)         │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │ Reranking Layer              │
        │ (Sentence-level scoring)     │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │ Decision Engine              │
        │ RESPOND / SAFE / ESCALATE    │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │ Grounded Response Generator  │
        └─────────┬────────────────────┘
                  │
                  ▼
        ┌──────────────────────────────┐
        │ Output CSV + Logs            │
        └──────────────────────────────┘

## How It Works
1. For each ticket, the agent identifies the company domain.
2. It injects the relevant support corpus (fetched from official sites) into the prompt.
3. It asks Claude to classify, respond or escalate, and justify the decision.


### Key design decisions:
- Corpus grounding: Static corpus built from official support sites (hackerrank.com, support.claude.com, visa.co.in/support.html). No hallucination.
- Escalation logic: Hard rules for billing, fraud, identity theft, security vulns, non-admin account access, score disputes, subscription changes.
- Prompt injection detection: System prompt instructs the model to detect and flag injection attempts (including in non-English text).
- Out-of-scope handling: Invalid/harmful requests are declined politely with `replied` + `invalid`.
   
## Improve Classification Rules
HIGH_RISK = [
    "fraud", "unauthorized", "hacked", "stolen",
    "identity theft", "suspicious activity"
]

MEDIUM_RISK = [
    "charged", "refund", "failed payment",
    "account locked", "cannot access"
]

CRITICAL_DOMAINS = {
    "Visa": ["payment", "card", "transaction"],
    "HackerRank": ["test failed", "submission error"],
    "Claude": ["api error", "rate limit"]
}

## Add rule override:
if domain == "Visa" and risk != "LOW":
    return "ESCALATE"
👉 Why:
Finance domain = zero tolerance for mistakes.

## Running the Agent
```bash
export ANTHROPIC_API_KEY=your_key_here
pip install anthropic
# Full agent run (with live API):
python code/agent.py support_tickets/support_tickets.csv output.csv
# Pre-computed predictions (no API key needed):
python code/generate_predictions.py

