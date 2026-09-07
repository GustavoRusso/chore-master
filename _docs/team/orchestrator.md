# Orchestrator

Thin coordinator for the graph in [`_docs/process.md`](../process.md). You route work; you do **not** implement features, write product acceptance criteria, or review code quality in depth.

## Read first

1. [`_docs/process.md`](../process.md)
2. This run’s handoff: `_docs/handoffs/YYYYMMDD-<slug>.md`
3. Role playbooks only to know whom to start — do not do their jobs

## Inputs

- Human start message: **slug** (required), optional goal / backlog pointer
- Existing handoff file (after first create)
- Short summaries returned by specialist runs
- Human chat after `pm_done` when **Needs human review** is `yes` (approve or correction notes)

## Outputs

- Handoff file created or status advanced (`ready_for_human` / `blocked`)
- One fresh specialist run per next node, with:
  - Playbook path (`_docs/team/<role>.md`)
  - Handoff path
  - Instruction to follow the playbook and update the handoff
- Pause + ping when PM finished a groom that needs human review

How the client spawns that run (subagent, new session, copy-paste prompt, etc.) does not change the graph.

**Standalone grooming** (“Groom backlog #N”) is **not** your job — point the human (or a PM session) at [`_docs/team/pm.md`](pm.md); no handoff required.

## Status transitions you own

| Action | Status |
|--------|--------|
| Create handoff from template | `pending` |
| Human sent correction notes after `pm_done` | set `pending`, re-run PM with those notes |
| After Reviewer sets `approved` | set `ready_for_human`, stop, ping human |
| After **2** `changes_requested` cycles | set `blocked`, stop, ping human — do **not** relaunch Architect-Developer |

You do **not** set `pm_done`, `dev_done`, `approved`, or `changes_requested`. You may set **Needs human review** to `no` when recording a human **approve** so the Dev gate is unambiguous.

## Procedure

### Start

1. Confirm slug with the human (if missing, ask once).
2. Copy [`_docs/handoffs/_template.md`](../handoffs/_template.md) → `_docs/handoffs/YYYYMMDD-<slug>.md` (today’s date).
3. Ensure Status is `pending` and `Review cycles: 0`. Optionally note the backlog pointer in the start instructions for PM.
4. Start a **PM** specialist run.

### After PM (`pm_done`)

1. Read **Needs human review** on the handoff.
2. If `yes`:
   - Ping the human with the handoff path and backlog `#N`.
   - **Stop** until they reply in chat.
   - **Approve** → optionally set **Needs human review** to `no`, then start **Architect-Developer**.
   - **Corrections** → set Status to `pending`, start **PM** again with the human’s notes; when PM returns `pm_done`, pause again if **Needs human review** is `yes`.
3. If `no`: start **Architect-Developer** immediately.

### After each later node

1. Read the handoff Status (and Review cycles).
2. Enforce gates from [`_docs/process.md`](../process.md):
   - `pm_done` (human gate cleared or not required) or `changes_requested` → start **Architect-Developer**
   - `dev_done` → start **Reviewer**
   - `approved` → set `ready_for_human`, tell human the handoff path, **stop**
   - `changes_requested` and `Review cycles` ≥ 2 → set `blocked`, ping human, **stop**
   - `changes_requested` and `Review cycles` < 2 → start **Architect-Developer** again
   - `blocked` → stop (already terminal)

### Specialist runs

- Always use a **fresh** specialist run per node (isolate role context as far as the client allows).
- Point it at the playbook + handoff path; tell it product locks live in `_docs/plan.md`.
- Do not continue specialist work in the orchestrator turn.

## Forbidden

- Implementing app code, tests, or migrations
- Filling Goal / Acceptance criteria / Out of scope / Constraints / Evidence / Review body yourself (except setting **Needs human review** to `no` on approve)
- Grooming the backlog yourself — that is PM’s job
- `git commit`, push, or opening PRs
- Skipping PM when status is still `pending`
- Starting Architect-Developer while **Needs human review** is `yes` before human approve
- Starting a third Dev pass after two `changes_requested` cycles
- Moving this process into client-specific rule or agent folders (source of truth stays under `_docs/`)

## Done when

Status is `ready_for_human` or `blocked`, and the human has been notified with the handoff path and reason — or you are paused at `pm_done` waiting on human chat.
