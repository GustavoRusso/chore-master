# Graph engineering process

Static multi-agent pipeline for Chore Master. Works with **any agentic client**: the Orchestrator starts a **fresh specialist run per node** (subagent, separate session, or that client’s equivalent isolation). Shared state lives on disk in a handoff file. Agents **never** `git commit`; the human commits/PRs after `ready_for_human`.

## Nodes

| Role | Playbook |
|------|----------|
| Orchestrator | [`_docs/team/orchestrator.md`](team/orchestrator.md) |
| Product Manager (PM) | [`_docs/team/product-manager.md`](team/product-manager.md) |
| Software Engineer | [`_docs/team/software-engineer.md`](team/software-engineer.md) |
| QA Engineer | [`_docs/team/qa-engineer.md`](team/qa-engineer.md) |

## Roles (summary)

- **PM** — grooms a task before anyone implements it; follows [`_docs/team/product-manager.md`](team/product-manager.md). May run **standalone** (human: “Groom backlog #N”) or as the **first node** of an implementation run.
- **Orchestrator** — creates the handoff, enforces gates, pauses for human when PM set **Needs human review: yes**.
- **Software Engineer** — implements from the groomed handoff with classic TDD.
- **QA Engineer** — checks finished work against acceptance criteria (and locks/scope); writes PASS/FAIL in **Review**.

## Grooming vs implementation

**Grooming** makes a backlog item precise enough that an engineer who never spoke to the PM could implement it.

### Backlog shapes

| Shape | When allowed | Sections |
|-------|--------------|----------|
| **Pre-groom** | Ungroomed ideas and ordered MVP stubs in [`_docs/backlog.md`](backlog.md) | Goal, User can, Build, Depends on |
| **Post-groom** | Required after PM finishes (standalone or graph); required before Software Engineer | Goal, Acceptance criteria, Out of scope, Constraints — see [`_docs/task-template.md`](task-template.md) |

- **Standalone:** Human asks the PM to groom. PM rewrites (or adds) a numbered item in [`_docs/backlog.md`](backlog.md) **in place** to **post-groom**. No handoff. Human reviews the backlog entry.
- **Implementation graph:** Orchestrator creates a handoff, then PM runs first. If the backlog item is still **pre-groom** (or incomplete post-groom), PM grooms it to post-groom (and may add a new backlog item for ad-hoc work). PM copies the four post-groom sections into the handoff. Handoff always records **Backlog: #N**.
- **Dev gate:** Do not start Software Engineer until the handoff four sections are filled **and** backlog `#N` is **post-groom** (groomed earlier, or groomed this turn).

Catch misunderstandings while the issue is still a paragraph — correcting grooming is cheap; correcting after implementation is a rewrite.

## Graph

```mermaid
flowchart LR
  human[Human_start] --> orch[Orchestrator]
  orch --> pm[PM]
  pm -->|Needs_human_review_yes| humanGate[Human_chat_approve]
  humanGate -->|approve| orchResume[Orchestrator]
  humanGate -->|corrections| pm
  orchResume --> dev[SoftwareEngineer]
  pm -->|Needs_human_review_no| dev
  dev --> rev[QAEngineer]
  rev -->|approved| orch2[Orchestrator]
  orch2 --> ready[ready_for_human]
  rev -->|changes_requested| dev
  rev -->|2_cycles| blocked[blocked]
```

**Default path:** Orchestrator → PM → (human gate if PM groomed this turn) → Software Engineer → QA Engineer → Orchestrator sets `ready_for_human` → human.

**Cycles:**

- Human corrections after `pm_done` → Orchestrator re-runs **PM** with notes; pause again at `pm_done`.
- QA Engineer → Software Engineer when status is `changes_requested`.

**Cap:** Review-cycle stop limit is defined only under **Review cycles** below (not in role playbooks). Orchestrator enforces it via the **Stop / ping human** gate.

## How to start an implementation run

1. Human gives a **slug** and optional goal / backlog pointer (`#N`). Work may be a groomed backlog item or something not yet in the backlog (PM will add and groom it).
2. Orchestrator copies [`_docs/handoffs/_template.md`](handoffs/_template.md) to:

   `_docs/handoffs/YYYYMMDD-<slug>.md`

   Use the current date (`YYYYMMDD`) and the human’s slug (lowercase, hyphenated).
3. Status starts as `pending`.
4. Orchestrator starts **PM**, then follows gates below. Do **not** start Software Engineer while **Needs human review** is `yes` until the human approves in chat.

## How to groom only

1. Human asks to groom (e.g. “Groom backlog #4” or describes new work).
2. Agent follows [`_docs/team/product-manager.md`](team/product-manager.md) **standalone** mode — no Orchestrator handoff required.
3. Human reviews the **post-groom** backlog entry. Later implementation runs can skip the human gate when PM only copies an already **post-groom** item (`Needs human review: no`).

## Fresh specialist

Each graph node is a **new specialist run** (subagent, separate session, or the client’s isolation equivalent):

- Must re-read its playbook and this run’s handoff from disk at start.
- Must not rely on prior role conversation, Orchestrator tool state, or another specialist’s memory.
- Isolate role context as far as the client allows.

## Specialist invocation contract

How the client spawns the run is out of scope. Every specialist start must carry the same contract.

**Required inputs (Orchestrator provides):**

1. Playbook path (`_docs/team/<role>.md`)
2. Handoff path (`_docs/handoffs/YYYYMMDD-<slug>.md`) — omit only for PM **standalone** groom
3. Instruction: follow the playbook; read [`plan.md`](plan.md) / [`backlog.md`](backlog.md) from disk as needed; update only allowed handoff/backlog fields

**Required outputs (specialist returns to Orchestrator):**

1. Short summary of what it did
2. Resulting Status (and **Needs human review** / **Review cycles** / **Backlog** when that role changes them)
3. Which handoff or backlog sections it changed

Orchestrator must not implement features. Specialists must not skip gates.

## Specialist run rule

Each node run is a fresh specialist (see above) that must:

1. Read its playbook under `_docs/team/`.
2. Read the handoff file for this run (graph mode).
3. Read [`_docs/plan.md`](plan.md) and [`_docs/backlog.md`](backlog.md) as needed — not from conversation memory alone.
4. Update only the handoff / backlog sections and statuses it is allowed to change.
5. Return the invocation-contract outputs to the Orchestrator when done.

Client adapters stay irrelevant to the graph: gates, statuses, and handoff files stay the same everywhere.

## Handoff file

**Path:** `_docs/handoffs/YYYYMMDD-<slug>.md`  
**Template:** [`_docs/handoffs/_template.md`](handoffs/_template.md)  
**Groomed shape:** [`_docs/task-template.md`](task-template.md)

### Required sections

1. **Status** (includes `Review cycles`, **Backlog**, **Needs human review**)
2. **Goal**
3. **Acceptance criteria**
4. **Out of scope**
5. **Constraints**
6. **Evidence**
7. **Review**

### Status values

| Status | Meaning |
|--------|---------|
| `pending` | Handoff created; PM not done |
| `pm_done` | Four groomed sections filled; if **Needs human review** is `yes`, Orchestrator pauses until human says go in chat; if `no`, ready for Software Engineer |
| `dev_done` | Implementation + Evidence complete; ready for QA Engineer |
| `changes_requested` | QA Engineer rejected (FAIL); Software Engineer must rework |
| `approved` | QA Engineer accepted (PASS); Orchestrator must finalize |
| `blocked` | Stopped (e.g. 2 failed review cycles); human must intervene |
| `ready_for_human` | Graph finished; human may commit/PR |

### Who may set which status

| From | To | Who |
|------|----|-----|
| (new file) | `pending` | Orchestrator |
| `pending` | `pm_done` | PM |
| `pm_done` → `pending` (re-groom) | Orchestrator (on human correction notes), then PM → `pm_done` again |
| `pm_done` or `changes_requested` | `dev_done` | Software Engineer |
| `dev_done` | `approved` | QA Engineer |
| `dev_done` | `changes_requested` | QA Engineer (also increments `Review cycles`) |
| `approved` | `ready_for_human` | Orchestrator |
| any (when `Review cycles` is `2` after `changes_requested`) | `blocked` | Orchestrator |

### Gates (Orchestrator enforces)

| Next node | Required status | Required content |
|-----------|-----------------|------------------|
| PM | `pending` | Handoff file exists from template |
| Human (chat) | `pm_done` and **Needs human review:** `yes` | Ping human with handoff path; wait for approve or correction notes |
| Software Engineer | `pm_done` with **Needs human review:** `no`, or `pm_done` after human approve, or `changes_requested` | Goal + Acceptance criteria + Out of scope + Constraints filled; **Backlog** `#N` set and **post-groom** in [`backlog.md`](backlog.md); if rework, Review explains what failed |
| QA Engineer | `dev_done` | Status `dev_done` (QA re-runs tests; Evidence may be incomplete) |
| Orchestrator finalize | `approved` | Review records `## QA: PASS` |
| Stop / ping human | `changes_requested` with `Review cycles: 2`, or explicit `blocked` | Orchestrator sets `blocked`; do not start Software Engineer |

### Gate checklist (yes/no)

Use this before each spawn or finalize. It is the **Gates** table as checks — do not invent extra rules.

**Before PM**

- [ ] Status is `pending`
- [ ] Handoff file exists (from template)

**Before Human (chat) pause**

- [ ] Status is `pm_done`
- [ ] **Needs human review** is `yes`
- [ ] Human has been pinged with handoff path (and backlog `#N` when set)

**Before Software Engineer**

- [ ] Stop / ping human gate does **not** match
- [ ] Status is `pm_done` with **Needs human review:** `no`, or `pm_done` after human approve, or `changes_requested`
- [ ] Goal, Acceptance criteria, Out of scope, Constraints are filled
- [ ] **Backlog** `#N` is set and that item is **post-groom** in `backlog.md`
- [ ] If `changes_requested`: Review explains what failed

**Before QA Engineer**

- [ ] Status is `dev_done`

**Before Orchestrator finalize**

- [ ] Status is `approved`
- [ ] Review starts with `## QA: PASS`

**Before Stop / ping human**

- [ ] `changes_requested` with `Review cycles: 2`, or Status is already `blocked` / must become `blocked`
- [ ] Do **not** start Software Engineer; set `blocked` if needed; ping human

### Human gate after PM

- Status stays **`pm_done`** while paused (no separate status).
- Human replies in **chat** (not by editing the handoff).
- **Approve** → Orchestrator starts Software Engineer (may set **Needs human review** to `no` when recording the go-ahead).
- **Corrections** → Orchestrator sets Status back to `pending`, re-runs PM with the notes; PM updates backlog + handoff, sets `pm_done` with **Needs human review: yes** again; Orchestrator pauses again.

### Review cycles

- Field lives under **Status** in the handoff: `Review cycles: N` (starts at `0`).
- QA Engineer increments by **1** each time it sets `changes_requested`. QA does not apply the stop limit; it always records FAIL when criteria fail.
- **Cap (defined only here):** After QA sets `changes_requested` and `Review cycles` becomes `2`, Orchestrator sets `blocked` and does **not** start another Software Engineer run. Orchestrator alone sets `blocked`. Do not restate this number in role playbooks.

## Software Engineer

Classic **red → green → refactor** TDD is required. Full rules, mandatory test depth, and **Evidence** commands live only in [`_docs/team/software-engineer.md`](team/software-engineer.md). Stay inside handoff **Constraints** and **Out of scope**.

## Exit

- **`ready_for_human`:** Orchestrator tells the human the handoff path; human commits/PRs. Agents must **not** run `git commit` / push / open PRs unless the human explicitly asks outside this graph.
- **`blocked`:** Orchestrator stops and pings the human with why (usually review-cycle cap).

## Product context

Do not duplicate product locks here. Agents read [`_docs/plan.md`](plan.md) and [`_docs/backlog.md`](backlog.md) as needed.
