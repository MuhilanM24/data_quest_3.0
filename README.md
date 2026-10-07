# PRISM Engine

PRISM is a local-first career planning prototype for students and families. It combines a deterministic career engine, a financial feasibility solver, parent/student conflict analysis, assessments, roadmaps, mentor recommendations, and seeded opportunity data.

## Run locally

```bash
npm install
npm run dev
```

The Next.js app runs at <http://localhost:3000>. The FastAPI API runs at <http://localhost:8000> when started separately:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The frontend includes a deterministic local fallback dataset, so the demo remains functional if the API is not running. Set `NEXT_PUBLIC_API_URL` to point it at another backend.

## Vercel deployment

The root `vercel.json` defines two Vercel services: `backend` (FastAPI) and
`frontend` (Next.js). The backend is public only through `/api/*`; all other
routes go to the frontend. The frontend API client uses same-origin `/api`
requests in Vercel and only needs `NEXT_PUBLIC_API_URL` when running against a
separate local or hosted backend.

Use `vercel dev` from the repository root to run both services together.
Configure `GEMINI_API_KEY`, `SUPABASE_URL`, and `SUPABASE_SERVICE_ROLE_KEY` as
Vercel project environment variables when enabling hosted integrations. No
service binding is required because the frontend calls the public `/api/*`
rewrite from the browser and the backend does not call another service.

## Demo routes and API

The app includes `/assessment`, `/careers`, `/parent`, `/market`, `/roadmap`,
and `/mentor` in addition to the dashboard. Compatibility aliases also include
`/dashboard`, `/career-dna`, `/recommendations`, `/alignment`, `/opportunities`,
`/opportunities/trackers`, `/parent/dashboard`, and `/compare`. The FastAPI service exposes seeded
careers, recommendations and career DNA, student/parent persistence, assessment
submission, conflict analysis, financial feasibility, market signals,
opportunities, career-specific roadmaps, and mentors. All seed data is stored
in `backend/prism.db`; delete that file to recreate the deterministic demo
database. The schema is created by `backend/app/db.py` at startup and is also documented in
`backend/database_schema.sql`; `backend/seed_data.py` can recreate the local
fallback database independently. It includes `careers`, `opportunities`,
`students`, `parents`, and `assessments`.

## Data and configuration

The backend uses SQLite (`backend/prism.db`) by default and seeds itself on startup. For a hosted deployment, configure `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`; the adapter boundary in `backend/app/db.py` is intentionally isolated so Supabase tables can replace SQLite without changing API contracts. Never commit credentials. `GEMINI_API_KEY` is optional: the engine uses safe deterministic templates when it is absent.

## Checks

```bash
npm run typecheck
npm run build
python -m compileall backend/app
```

This is a hackathon prototype: all recommendations are educational guidance, not financial or career advice.
