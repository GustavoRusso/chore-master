# AGENTS

This repo uses a **graph engineering** process for multi-agent work. It is **client-agnostic**: any agentic client that can read these files and run role playbooks may follow it.

- **Process (graph, gates, statuses):** [`_docs/process.md`](_docs/process.md)
- **Role playbooks:** [`_docs/team/`](_docs/team/)
- **Handoff template:** [`_docs/handoffs/_template.md`](_docs/handoffs/_template.md)
- **Product / scope locks:** [`_docs/plan.md`](_docs/plan.md), [`_docs/backlog.md`](_docs/backlog.md)

Keep this process under `_docs/` (and this pointer file). Do **not** relocate it into client-specific rule or agent folders — the on-disk playbooks and handoffs are the source of truth for every client.
