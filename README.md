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

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## MVP scope

- Sign up / log in; create or join a household via invite code
- Assign tasks; inbox with accept / decline / send back
- Week board with S/M/L blocks + weekend overflow
- Completion points and weekly scoreboard with silly titles

More detail lives in [`_docs/plan.md`](_docs/plan.md).
