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
- SQLite (dev) or Postgres
- [uv](https://docs.astral.sh/uv/) for dependencies (inside the Dev Container)

## Setup

**Host prerequisites:** Docker (e.g. Docker Desktop) and a Dev Containers–capable editor (Cursor or VS Code). Do not install Python, `uv`, or project deps on the host.

1. Open this folder in the editor.
2. Reopen in Container (Dev Containers). On first create, the container runs `uv sync` and applies migrations.
3. Start the app:

```bash
uv run python manage.py runserver 0.0.0.0:8000
```

4. Open http://127.0.0.1:8000/

## MVP scope

- Sign up / log in; create or join a household via invite code
- Assign tasks; inbox with accept / decline / send back
- Week board with S/M/L blocks + weekend overflow
- Completion points and weekly scoreboard with silly titles

More detail lives in [`_docs/plan.md`](_docs/plan.md).
