# Usmora

Usmora is a private AI relationship copilot that helps people turn emotional reactions into thoughtful, user-approved conversations.

## Current phase

This repository is an isolated development scaffold for a narrow, single-user prototype. Product validation is still in progress. Scaffolding does not authorize production deployment or the use of real relationship data.

## Initial wedge

A controlled workflow:

1. A user describes a situation.
2. The application separates facts, assumptions, feelings, and needs.
3. It retrieves only authorized private context.
4. It helps clarify the user's intent.
5. It optionally drafts a message.
6. The user edits and explicitly approves it.
7. The user copies or discards the draft. Usmora never sends it autonomously.

## Planned stack

- Web: Next.js
- API: FastAPI
- Data: PostgreSQL
- Semantic retrieval: pgvector only when justified
- Local deployment: Docker Compose
- Edge/TLS: Caddy
- AI: provider-independent adapter
- Evaluation: deterministic privacy/leakage tests and qualitative communication checks

## Repository layout

```text
apps/web/        Next.js user interface
apps/api/        FastAPI application and domain services
packages/ai/     Provider adapter, prompts, structured outputs, evaluations
tests/evals/     Privacy, leakage, consent, and communication evaluations
docs/            Architecture, decisions, and trust model
```

## Development control plane

Donna coordinates work through the `usmora` Hermes Kanban board. Benjamin is the assigned engineering profile. External GitHub creation, pushes, deployments, and production credentials require Walid's explicit approval.

See `AGENTS.md` and `docs/architecture.md` before implementation.
