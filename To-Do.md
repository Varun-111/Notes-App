# Notes App — PRD and Learning Plan
 
## 1. Goal
Build an async Notes API with FastAPI and PostgreSQL, a minimal React UI, tests, and auto-generated OpenAPI docs. The real goal is to *understand* FastAPI, coming from Django/DRF.
 
Resume line: "Developed an async notes API with FastAPI and PostgreSQL with auto-generated OpenAPI docs."
 
## 2. Stack (confirmed, with one decision)
| Layer | Choice | Why |
|---|---|---|
| API | FastAPI | the thing to learn |
| Validation | Pydantic v2 | DRF serializers equivalent |
| ORM | SQLAlchemy 2.0 async (not SQLModel) | see note below |
| Migrations | Alembic | Django migrations equivalent, but more manual |
| DB driver | asyncpg | has Python 3.14 Windows wheels |
| DB | PostgreSQL (local, pgAdmin) | already installed |
| Tests | pytest + pytest-asyncio + httpx | async test client |
| UI | React (Vite), plain CSS | minimal, no Tailwind |
| Containers | Docker (added late, Session 5) | local Postgres until then; use host port 5433 for the container to avoid clashing with local 5432 |
 
**Why not SQLModel:** it merges the DB model and the Pydantic schema into one class. That's convenient, but it hides exactly the two things you want to learn separately (ORM vs validation). Plain SQLAlchemy + Pydantic is also what most real FastAPI jobs use.
 
## 3. Python 3.14 check
- asyncpg 0.32.0: cp314 win_amd64 wheel exists (verified on PyPI)
- Pydantic: 3.14 support since 2.12 (use 2.12+)
- SQLAlchemy: use 2.0.45+ on 3.14
- FastAPI: running on 3.14 in real projects
- Not yet verified: pytest-asyncio, httpx, Alembic. We confirm at install time with `pip install` and a smoke test.
- Fallback if something breaks: a 3.13 venv.
## 4. Scope
### Core (must be done)
- Create, read (list + single), update, delete notes
- Tags: add/remove tags on a note, filter notes by tag (many-to-many)
- Search: by text in title/body (case-insensitive `ILIKE`)
- Pagination on the list endpoint
- Swagger docs at `/docs`
- Alembic migrations, `.env` config, tests for every endpoint
- Minimal React UI: list, create, edit, delete, tag filter, search box
### Out of scope for core
- Auth/users (notes are global in core; see optional phase below)
- Styling, deployment
### Optional phase after core: Auth
- Users + JWT login, `Depends(get_current_user)`, notes owned per user
- **Learn:** the best real use of dependency injection; compare with DRF permissions
### Stretch (only after core is done)
- Markdown rendering
- Share a note via a public link (random token + public read-only endpoint)
## 5. Definition of "done" for the core
1. All core endpoints work and appear in Swagger
2. `pytest` passes, using a separate test database
3. Fresh clone + README steps gets the app running
4. UI can do the full create/edit/delete/tag/search loop
5. Pushed to GitHub with README, screenshots, `.env.example`, `.gitignore`
## 6. Sessions and to-do list
 
### Session 1 — Foundations
- [ ] Project folder in `D:\Varun\Projects\notes-app`, venv, install packages
- [ ] Git init, `.gitignore`, `.env`, `.env.example`
- [ ] Hello-world FastAPI app, run with `fastapi dev`, open `/docs`
- [ ] Config with `pydantic-settings`
- [ ] Pydantic schemas: `NoteCreate`, `NoteUpdate`, `NoteRead`
- [ ] In-memory CRUD (no DB yet) so you see routing + validation first
- [ ] First test with `TestClient`/httpx
- **Learn:** path operations, request/response models, how validation errors become 422
### Session 2 — Database, async, migrations
- [ ] Async engine + session, `get_db` dependency
- [ ] `Note` SQLAlchemy model (2.0 `Mapped` style)
- [ ] Alembic setup (async `env.py`), first migration
- [ ] Swap in-memory CRUD for DB CRUD
- [ ] Test DB fixture, rewrite tests against it
- **Learn:** `async def` endpoints, sessions, dependency injection (vs Django middleware/ORM manager), migrations
### Session 3 — Tags and search
- [ ] `Tag` model + association table, second migration
- [ ] Tag endpoints, attach/detach on a note
- [ ] Filter by tag, search by text, pagination
- [ ] Tests for each, including edge cases (404s, duplicate tags)
- **Learn:** relationships, N+1 and eager loading (`selectinload`), query params
### Session 4 — React UI
- [ ] CORS setup
- [ ] Vite React app: list, create/edit form, delete, tag filter, search
- [ ] Plain CSS only
- **Learn:** how the OpenAPI schema maps to the frontend calls
### Session 5 — Polish and ship
- [ ] Consistent error responses, input limits
- [ ] Containerize: `docker-compose.yml` for Postgres, then a `Dockerfile` for the API so `docker compose up` runs everything
- [ ] README with setup steps and screenshots
- [ ] Tests green, GitHub push
- [ ] LinkedIn post
- [ ] Stretch goals if time remains
## 7. Concept checklist (tick when you can explain it in your own words)
- [ ] What runs first on a request: routing → dependencies → validation → handler → response model
- [ ] Why `async def` helps, and what blocks the event loop
- [ ] Dependency injection with `Depends`
- [ ] Pydantic model vs SQLAlchemy model, and why they're separate
- [ ] What `autogenerate` in Alembic can and can't detect
- [ ] How FastAPI builds `/docs` from type hints
- [ ] Test DB isolation
## 8. After this project
RAG question-answering service: FastAPI + Postgres/pgvector + local LLM.