<!--
Repository-specific Copilot instructions. Keep short and actionable.
Designed for AI coding agents to be immediately productive in this repo.
-->

# Copilot instructions for this repo

Quick orientation
- This is a tiny FastAPI app in `src/app.py` (the app object is named `app`). Static UI lives in `src/static/` (HTML/JS/CSS). The app mounts the static folder and redirects `/` to `/static/index.html`.
- Data is an in-memory `activities` dict in `src/app.py`. Entries use the activity name as the key and contain a `participants` list. Changes are not persisted across restarts.

Run & debug (explicit commands)
- Install dependencies: `pip install -r requirements.txt` (or `pip install fastapi uvicorn`).
- Run locally with uvicorn (recommended):

  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

- The app serves:
  - API docs: `http://localhost:8000/docs` (OpenAPI)
  - Static UI: `http://localhost:8000/static/index.html`

Key code patterns and what to watch for
- In-memory store: `activities` in `src/app.py`. Expect code that directly mutates `activities[<name>]["participants"]` (no dedupe, no capacity checks). Example: POST `/activities/{activity_name}/signup` simply appends the provided `email`.
- Static assets are under `src/static/`. When editing the UI, update `src/static/index.html`, `src/static/app.js`, and `src/static/styles.css` together — the repository's exercises expect coordinated UI + JS changes (see `.github/steps/3-copilot-edits.md`).
- Naming conventions: activities are identified by their human-readable name (space‑sensitive). Use exact string matches when referencing activity keys.

Tests & CI
- There are no unit tests in the repo. CI/workflows exist under `.github/workflows/` and the learning steps under `.github/steps/` — these are exercise scaffolding rather than production CI.

Safe edit rules for agents (concrete)
- Avoid adding persistent storage without a small migration plan. The codebase expects in-memory state for the exercises.
- When adding API behavior, prefer additive changes (new endpoints or optional query params) to avoid breaking the exercise flow.
- When changing `signup` behavior, preserve the current signature (POST `/activities/{activity_name}/signup?email=...`) unless the change is accompanied by updates to the static UI and exercise docs in `.github/steps/`.

Examples to reference in edits
- Show participants list in the UI: modify `src/static/app.js` + `src/static/index.html`. The Edit Mode lesson explicitly mentions these files.
- To list activities from the API, call GET `/activities` (returns the `activities` dict).

Where to look for more context
- Primary app: `src/app.py` (business logic and in-memory model)
- Static UI: `src/static/index.html`, `src/static/app.js`, `src/static/styles.css`
- Dependency hints: `requirements.txt`
- Exercise/agent guidance: `.github/steps/` (contains Copilot Edit/Agent step documents) and `.github/workflows/` for exercise automation.

If you need clarification
- Ask for which files should be included in context for an Edit Mode request (common selection: `src/app.py` + any `src/static/*` files touched).
- If you plan to introduce persistence, propose a minimal migration (file + small runbook) before implementing.

---
Please review these instructions and tell me if any section needs more detail or examples from specific files.
