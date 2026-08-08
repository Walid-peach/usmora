# Architecture

## Goal

Build a narrow, privacy-first single-user prototype that supports reflective communication while preserving human control.

## System shape

```text
Next.js web application
        |
        v
FastAPI modular monolith
  |-- identity and authorization
  |-- private relationship context
  |-- reflection workflow
  |-- message drafting
  |-- explicit approval boundaries
  |-- consent and audit ledger
  |-- export and deletion
        |
        v
PostgreSQL
```

The AI layer is an adapter behind application services. It must not own authorization, consent transitions, deletion, or message sending.

## Initial runtime flow

```text
User describes a situation
-> application authorizes private context
-> structured extraction: facts, assumptions, feelings, needs
-> optional private-context retrieval
-> clarification response
-> optional message draft
-> user edits and approves
-> copy or discard
```

There is no automatic partner delivery in the first version.

## Data scopes

Every record carrying relationship context has an explicit owner and scope. The initial prototype supports only private scope. A later partner-connection phase may add shared records through a deterministic transition:

1. owner selects an item;
2. exact shared representation is shown;
3. owner explicitly approves;
4. application creates an attributed shared record;
5. consent event is appended;
6. revocation and deletion remain available.

No model response can mutate a record's scope.

## Deployment direction

- Develop on the existing VPS in `/home/walid/server/projects/usmora`.
- Keep Donna and Benjamin logically isolated through separate Hermes profiles.
- Use containers or a separate Linux identity before handling sensitive data.
- Use a separate production environment before inviting external users.
- A future hybrid deployment may use managed Postgres/auth/storage while keeping application services on a VPS. Vendor selection is intentionally deferred.

## Deferred until validated

- partner accounts and invitations;
- shared-memory promotion;
- reminders and scheduling;
- pgvector retrieval;
- background queues;
- multi-agent orchestration;
- production deployment.
