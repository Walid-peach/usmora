# Usmora

Usmora is a privacy-first communication reflection prototype. It helps one person separate a difficult situation into **Facts, Assumptions, Feelings, and Needs**, then offers a calm message draft that the person can edit and copy.

Nothing is sent automatically. The deterministic local engine is a prototype aid, not objective truth.

## Safety and privacy boundary

- Demo input is processed in memory and is not persisted by this prototype.
- Do not use real relationship data in development, tests, screenshots, or demos. All repository examples are synthetic.
- Usmora is communication support, not therapy, diagnosis, emergency support, surveillance, or partner monitoring.
- There is no authentication, database, telemetry, partner account, shared memory, background queue, external AI provider, or deployment in this draft.
- Because there is no authentication and transport security is not configured, this prototype is for isolated local development only.

If someone may be in immediate danger, contact local emergency services or an appropriate crisis resource; do not rely on this prototype.

## Architecture

```text
Next.js web (apps/web)
  -> schema-validated HTTP request
FastAPI modular API (apps/api)
  -> ReflectionProvider protocol
DeterministicReflectionProvider (local, no key, no network)
```

The provider interface keeps model choice independent from application trust boundaries. The API does not log raw situations or drafts; its container disables access logging. See `AGENTS.md` and `docs/architecture.md` for the longer-term boundaries.

## Run with Docker Compose

Prerequisite: Docker with Compose v2.

```bash
cp .env.example .env
docker compose up --build
```

Open http://localhost:3000. API health is at http://localhost:8000/health.

## Vercel and Railway preview settings

The preview remains deterministic, synthetic-data-only, in-memory, and unable to send messages. Do not use real relationship data. Configure the two platforms manually as follows:

Railway API:

- Root Directory: `/apps/api`
- Config-as-code: `apps/api/railway.toml` (Railpack)
- Health check path: `/health`
- Start command: `sh -c 'exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"'`
- Environment variable:

  ```text
  ALLOWED_ORIGINS=https://usmora.vercel.app
  ```

Vercel web:

- Root Directory: `/apps/web`
- Environment variable:

  ```text
  NEXT_PUBLIC_API_URL=https://usmora-production.up.railway.app
  ```

`ALLOWED_ORIGINS` is a comma-separated exact-origin allowlist. It rejects blank entries and wildcard origins; when unset, only `http://localhost:3000` is allowed. The production value above is the exact Vercel origin; do not include a path, trailing slash, wildcard, or blank entry.

Stop with:

```bash
docker compose down
```

## Run directly

API (Python 3.11+):

```bash
cd apps/api
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/uvicorn app.main:app --reload --no-access-log
```

Web (Node.js 22+), in another terminal:

```bash
cd apps/web
npm ci
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## Verification

```bash
# API
cd apps/api
.venv/bin/pytest -q
.venv/bin/ruff check .

# Web
cd ../web
npm test
npm run typecheck
npm run lint
npm run build
npm audit --omit=dev

# Compose
cd ../..
docker compose config -q
docker compose up --build -d
curl --fail http://localhost:8000/health
curl --fail http://localhost:3000
curl --fail -X POST http://localhost:8000/v1/reflections \
  -H 'Content-Type: application/json' \
  --data '{"situation":"My housemate arrived after our agreed cooking time, and I felt frustrated."}'
docker compose down
```

## API

`GET /health` returns `{"status":"ok"}`.

`POST /v1/reflections` accepts:

```json
{"situation":"A synthetic situation between housemates."}
```

`situation` must contain non-whitespace text and be at most 4,000 characters. Responses include `facts`, `assumptions`, `feelings`, `needs`, `draft`, and a prototype disclaimer.

## Known limitations

The deterministic provider uses deliberately small keyword rules, so its output is repetitive and cannot understand nuance. No data is persisted, but browser/API process memory and local infrastructure still require normal device security. Clipboard content is controlled by the operating system after the user explicitly copies it. Production identity, consent, deletion, encryption, abuse handling, model evaluation, and deployment remain deferred.
