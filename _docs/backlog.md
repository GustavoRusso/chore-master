# Chore Master — MVP backlog

Ordered tasks for building the Django + HTMX app from [`plan.md`](plan.md). Each task delivers something you can use as soon as it lands; later tasks assume earlier ones exist.

Each item that is ready or shipped has **Status** (`post-groom` | `done`) per [`task-template.md`](task-template.md). Anything that does not meet the post-groom specification is pre-groom. Implementation needs **Status:** `post-groom` (or already `done`) — see [`process.md`](process.md).

---

## 1. Project bootstrap

**Status:** `done`

**Goal:** Run the empty Django app inside the Dev Container with no host Python.

**User can:** Open the folder in a Dev Container, run `uv run python manage.py runserver 0.0.0.0:8000`, hit the app (admin at `/admin/`).

**Build:** `.devcontainer/` (Python + `uv`), `pyproject.toml` + lockfile, Django project `chore_master`, SQLite, port 8000, `postCreateCommand` sync + migrate.

**Depends on:** nothing.

---

## 2. Accounts

**Status:** `post-groom`

**Goal:** Family members sign in with Google so every later action is tied to a real user account (themselves).

## Acceptance criteria

- [ ] A visitor can open a login page that offers **Sign in with Google**
- [ ] Completing Google Sign-In for a **new** Google account creates a Django user and starts a logged-in session
- [ ] Completing Google Sign-In for a **returning** Google account logs into the same Django user (no second account for the same Google identity)
- [ ] Cancelled or failed Google Sign-In leaves the visitor logged out and shows a clear return to the login page (or a visible error)
- [ ] A logged-in user can log out and then cannot open a login-required page without signing in again
- [ ] At least one simple logged-in home (or redirect target) is protected with `LoginRequiredMixin` / `@login_required`
- [ ] Google OAuth client id and secret come from environment (or Dev Container env); they are not hard-coded in the repo
- [ ] Automated tests cover login-required redirect and logout (in-app only)

## Out of scope

- Household create/join and invite codes — backlog #3
- Username/password registration or login (replaced by Google for MVP per [`plan.md`](plan.md))
- Email confirmation and password-reset email flows
- Protecting chore / household pages beyond the simple login-required home in this task
- Linking multiple Google identities to one user, or account deletion / “disconnect Google”
- Automated tests of the external identity-provider boundary (live calls or mocks of systems this project does not own) — see [`software-engineer.md`](team/software-engineer.md) **Mandatory test depth**

## Constraints

- Stay inside the existing `chore_master` Django project; add a small `accounts` app (or equivalent) for views/templates/urls
- Use a maintained Django Google OAuth stack (prefer **django-allauth** with Google provider) and Django **session** auth after OAuth
- Dev Container / local run must document the required env vars (e.g. in README or `.env.example`); secrets stay out of git
- Honor [`plan.md`](plan.md): Google Sign-In only for MVP accounts; one shared household comes in #3
- Tests: Django test client for in-app auth behavior only; no browser e2e; honor [`software-engineer.md`](team/software-engineer.md) **Mandatory test depth** (no live external systems; no mocks of systems this project does not own)

---

## 3. Household + invite code


**Goal:** One shared household per family.

**User can:** Create a household (get an invite code) or join with a code; see who is in the household.

**Build:** `Household` + membership models; create/join flows; simple household home listing members. User is always themselves — no “switch person.”

**Depends on:** 2.

---

## 4. Assign chores


**Goal:** Anyone can send a chore to anyone in the household (including self).

**User can:** Create a chore with a normal name, size S/M/L, and assignee; see sent/received offers (status `offered`).

**Build:** `Task` model (name, size, assigner, assignee, status, planned day unset); create/assign form scoped to household members; list of outgoing and incoming offers.

**Depends on:** 3.

---

## 5. Inbox actions


**Goal:** Receiver controls the handshake — no forced chores.

**User can:** Accept, decline, or send back an offered chore (`accepted` / `declined` / `returned`).

**Build:** Inbox view for the assignee; HTMX (or form posts) for the three actions; update status; assigner sees declined/returned feedback.

**Depends on:** 4.

---

## 6. Week board + schedule


**Goal:** Tetris-fit accepted chores into the week; leftovers go to weekend.

**User can:** See Mon–Fri columns + weekend overflow; drag accepted S/M/L blocks onto a day; household can see when someone planned a chore.

**Build:** Personal week board template; small JS (HTML5 drag or tiny library) posting planned day (`mon`…`fri` / `weekend` / none); capacity by size is visual Tetris — overflow lands in weekend, no shame penalty.

**Depends on:** 5.

---

## 7. Complete + points


**Goal:** Finishing earns points; more if someone else assigned it.

**User can:** Mark a scheduled (or accepted) chore done; see points from a clear ledger (e.g. self-assign 1×, other-assign 2×).

**Build:** Status → `done`; `PointsLedger` (or equivalent) per completion with multiplier; HTMX “mark done”; simple personal points total for the current week.

**Depends on:** 6.

---

## 8. Weekly scoreboard


**Goal:** The joke reward — weekly winner and silly titles, not spendable treats.

**User can:** Open a household scoreboard for the current week (keyed by week start date); see ranking, weekly winner, and a few silly titles from rank/points.

**Build:** Aggregate ledger by member for the week; scoreboard page; title rules (static list from rank/points); leftover weekend pile can roll forward later without changing this MVP surface.

**Depends on:** 7.

---

## 9. Playful polish


**Goal:** Tone matches the product without new domain rules.

**User can:** Enjoy playful colors/stickers; optional tiny sound when marking complete. Chore names stay normal.

**Build:** Shared CSS, light sticker/decoration assets; optional complete sound hook on the mark-done UI.

**Depends on:** 8 (can start earlier visually, but finish after the scoreboard loop exists).

---

## Out of scope

Do not pull global MVP exclusions into this backlog. Canonical list: [`plan.md`](plan.md) — **Explicitly out of scope** (and locked decisions such as SQLite for local/dev).

---

## Done when

MVP completion criteria live in [`plan.md`](plan.md) — **What “done” looks like**. Per-task delivery is **Status:** `done` on each numbered item above.
