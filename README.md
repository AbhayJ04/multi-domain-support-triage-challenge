# multi-domain-support-triage-challenge
Terminal-based multi-domain support triage agent that processes tickets across HackerRank, Claude, and Visa ecosystems. It classifies intent, risk, and domain, retrieves relevant corpus-based documentation using semantic search, and decides whether to respond or escalate. Ensures safe, grounded, and explainable outputs.

# Multi-Domain Support Triage Agent

This project is a terminal-based support triage system that processes customer support tickets across three domains:
	HackerRank
	Claude
	Visa
The system reads each ticket, understands the issue, retrieves relevant support information, and decides whether to respond automatically or escalate to human support.

# What It Does
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

# Key Features
1. Domain-specific retrieval (better accuracy)
2. Semantic search using embeddings (FAISS)
3. Risk-aware decision system
4. No external data usage (strictly corpus-based)
5. Transparent logging for every decision
