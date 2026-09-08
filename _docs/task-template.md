# Task template

**Post-groom** shape for a backlog item and for the matching sections in a handoff. PM fills every section before implementation.

Anything that does **not** meet this specification is **pre-groom** (not ready to implement). There is no separate pre-groom template.

## Status

Set on the backlog item when it meets this specification (or is shipped):

| Value | Meaning |
|-------|---------|
| `post-groom` | Meets this specification; ready for an implementation run |
| `done` | Shipped in the repo (keep the groomed body) |

Omit **Status** (or leave the body incomplete) while the item is still pre-groom. Do **not** track grooming or delivery in a shared blurb at the top of [`backlog.md`](backlog.md).

Handoffs copy the four sections below (not Status).

## Goal

One or two sentences on what should be true when this is done.

## Acceptance criteria

- [ ] A statement you can check by looking at the result
- [ ] One line per case, including the awkward ones

## Out of scope

- Something that does not belong in this task, moved to #N

## Constraints

- Files this should stay inside
- Libraries to use
- Guidelines to follow
