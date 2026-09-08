# EXAMPLE — not a live handoff

Agents: copy structure from this file mentally. Do **not** treat this path as an active run. Live handoffs are `YYYYMMDD-<slug>.md` created from [`_template.md`](_template.md).

# Handoff: 20260908-accounts-auth

## Status

- **Status:** `approved`
- **Review cycles:** 0
- **Backlog:** #2
- **Needs human review:** no
- **Pending question:**

## Goal

Household members can sign up, log in, and log out with Django auth so every later action is tied to a real user account.

## Acceptance criteria

- [x] A visitor can create an account with a username and password from a register page
- [x] A duplicate username shows a visible error and does not create a second account
- [x] A registered user can log in and reach a logged-in home (or redirect target)
- [x] A logged-in user can log out and can no longer open a login-required page without signing in again
- [x] No Google login and no email confirmation flow

## Out of scope

- Household create/join and invite codes — backlog #3
- Protecting chore pages beyond a simple login-required example home
- Password-reset email flows

## Constraints

- Stay inside Django auth views/templates (or thin wrappers) under the existing `chore_master` project
- Use session auth from Django; no new auth libraries
- Honor [`plan.md`](../plan.md): real logins, one shared household later — this task is accounts only
- Tests: Django test client for views; no browser e2e

## Evidence

### Tests

```text
$ uv run python manage.py test
Found 12 test(s).
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 12 tests in 0.84s

OK
```

### Migrate check

```text
$ uv run python manage.py migrate --check
System check identified no issues (0 silenced).
```

## Review

## QA: PASS

- [x] A visitor can create an account with a username and password from a register page - PASS
- [x] A duplicate username shows a visible error and does not create a second account - PASS
- [x] A registered user can log in and reach a logged-in home (or redirect target) - PASS
- [x] A logged-in user can log out and can no longer open a login-required page without signing in again - PASS
- [x] No Google login and no email confirmation flow - PASS

Tests: `uv run python manage.py test`, 12 passed, 0 failed

Migrate check: `uv run python manage.py migrate --check`, ok
