# Human start card — graph engineering

Short copy-paste lines for a human developer. Full rules, gates, and statuses: [`process.md`](process.md). Agents read playbooks under [`team/`](team/).

Replace `#N` and `<slug>` before you send. Do not hard-code a backlog number into this file.

## Groom only (no handoff)

```text
Groom backlog #N
```

```text
Follow _docs/team/product-manager.md. Groom this idea into a post-groom backlog item: <description>
```

Then review the **post-groom** item in [`backlog.md`](backlog.md) (Goal, Acceptance criteria, Out of scope, Constraints).

## Start an implementation run

```text
Act as Orchestrator per _docs/team/orchestrator.md and _docs/process.md.
Start an implementation run.
Slug: <slug>
Backlog: #N
```

Omit `Backlog: #N` if the work is not in the backlog yet. PM will add and groom it. Use a lowercase hyphenated slug (example: `accounts-auth`).

## After PM (human gate)

When the Orchestrator pauses with **Needs human review: yes**:

```text
Approve — continue to Software Engineer
```

```text
Corrections: <your notes for PM>
```

Reply in **chat**. The Orchestrator already gave the handoff path — you do not need to paste it to approve. Do **not** edit the handoff (including Status) to approve or correct; chat only.

## Resume a run

```text
Resume Orchestrator for handoff _docs/handoffs/YYYYMMDD-<slug>.md
```

## When you commit or open a PR

Wait until Status is `ready_for_human` on the handoff. Agents must not commit unless you ask outside the graph. If Status is `blocked`, fix the cause (often review-cycle cap), then resume or start a new run.

## What to review

| Moment | You review |
|--------|------------|
| After standalone groom | Post-groom backlog `#N` |
| After PM in a graph run | Handoff Goal / Acceptance criteria / Out of scope / Constraints (and backlog `#N`) |
| After `ready_for_human` | Diff + Evidence / Review on the handoff; then you commit/PR |

Product locks: [`plan.md`](plan.md). Ordered work: [`backlog.md`](backlog.md).
