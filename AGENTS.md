# Agent Instructions

## Product boundary

Usmora is a communication-support product, not a therapist, surveillance tool, or autonomous relationship agent. The first implementation is a single-user prototype using synthetic data only.

## Non-negotiable trust rules

- Never impersonate a partner.
- Never send a sensitive message or take a consequential action without explicit user approval.
- Never reveal one partner's private memory to another.
- Shared memory must be explicit, reviewable, attributed, revocable, exportable, and deletable.
- Do not infer consent from model output, relationship status, or conversational context.
- Do not diagnose mental-health conditions or claim therapeutic authority.
- Do not build monitoring, coercion, location tracking, or partner-surveillance features.

## Data model invariant

Keep these scopes technically distinct:

1. Partner A private data
2. Partner B private data
3. Mutually approved shared data

A model may suggest sharing. Only deterministic application code may perform a scope transition after an explicit review and approval action. Record the transition in a consent ledger.

## Engineering workflow

- Read this file and relevant docs before changing code.
- Translate every task into testable acceptance criteria.
- Prefer a modular monolith and a provider-independent AI adapter.
- Add no Redis, queue, graph orchestrator, multi-agent runtime, or pgvector dependency without demonstrated need and approval.
- Use synthetic fixtures. Never place real relationship data in source, tests, logs, prompts, screenshots, or issue text.
- Add deterministic authorization and privacy tests before relying on model evaluations.
- Keep prompts versioned and structured outputs schema-validated.
- Avoid logging raw private reflections or generated sensitive drafts.

## Git and external actions

- Work on task-specific branches or Hermes worktrees.
- Do not push, merge to `main`, create a remote repository, deploy, provision services, or modify production credentials without Walid's explicit approval.
- Local commits are allowed only when requested by the task.

## Completion evidence

A task is complete only when the relevant tests/checks have run successfully. Report:

- files changed;
- commands and actual results;
- acceptance criteria covered;
- assumptions and remaining risks;
- any action still awaiting approval.
