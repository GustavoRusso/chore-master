# Chore Master

A family chore planner built with Django and HTMX. Assign chores to each other, Tetris-fit them into your week, finish them for points, and chase the weekly scoreboard — no random chore lottery.

## How it works

1. Anyone can assign a chore (S / M / L) to anyone else.
2. The receiver accepts, declines, or sends it back.
3. Accepted chores go on a personal week board (Mon–Fri); leftovers land in a weekend catch-up pile.
4. Mark done → points (more if someone else assigned it).
5. Household scoreboard + weekly winner with silly titles.

## Stack

- [Django](https://www.djangoproject.com/) (auth, server-rendered templates)
- HTMX for inbox and mark-done interactions
- Small JS for drag-and-drop scheduling
- SQLite for local/dev (Postgres deferred; see [`_docs/plan.md`](_docs/plan.md))
- [uv](https://docs.astral.sh/uv/) for dependencies (inside Docker / the Dev Container)

## Setup

Do not install Python, `uv`, or project deps on the host. Pick one path below.

### For developers (IDE + Dev Containers)

Use an IDE with [Dev Containers](https://containers.dev/) support and Docker (e.g. Docker Desktop).

1. Open this folder in the editor.
2. Reopen in Container. On first create, the container runs `uv sync` and applies migrations.
3. Copy `.env.example` to `.env` (gitignored):

```bash
cp .env.example .env
```

4. Create your own Google OAuth Web client and put the values in `.env` — step-by-step: [`_docs/google-oauth-local-setup.md`](_docs/google-oauth-local-setup.md).
5. Load env vars and start the app:

```bash
set -a && source .env && set +a
uv run python manage.py runserver 0.0.0.0:8000
```

6. Open http://127.0.0.1:8000/

### Auth env vars

| Variable | Purpose |
|----------|---------|
| `GOOGLE_CLIENT_ID` | OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret |

How to create the client and the local redirect URI: [`_docs/google-oauth-local-setup.md`](_docs/google-oauth-local-setup.md).

### Only run the project (Docker Desktop)

Use [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or another Docker engine) from a terminal — no Dev Containers IDE required. From the project root:

```bash
docker build -f .devcontainer/Dockerfile -t chore-master .
docker run --rm -it -p 8000:8000 \
  -e UV_LINK_MODE=copy \
  -e GOOGLE_CLIENT_ID \
  -e GOOGLE_CLIENT_SECRET \
  -v "$PWD":/app -w /app \
  chore-master \
  bash -lc 'uv sync && uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000'
```

Open http://127.0.0.1:8000/

## Multi-agent work

To groom backlog items or start an implementation graph in chat, use the copy-paste lines in [`_docs/human-start.md`](_docs/human-start.md). Full process: [`_docs/process.md`](_docs/process.md).

## MVP scope

Short overview only. Full must-have list, out of scope, and “done” criteria: [`_docs/plan.md`](_docs/plan.md). Build progress: [`_docs/backlog.md`](_docs/backlog.md).

- Sign up / log in; create or join a household via invite code
- Assign tasks; inbox with accept / decline / send back
- Week board with S/M/L blocks + weekend overflow
- Completion points and weekly scoreboard with silly titles
