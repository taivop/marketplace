---
name: self-learning
description: Structured self-coaching system for work-relevant skill growth -- 2-3 month learning goals, 1-2 week themes, daily active-practice sessions, weekly reviews, and accountability, tracked as markdown files. USE WHEN user asks what to learn next for work, wants a learning plan or routine, asks to plan or review a learning session, wants accountability for learning consistency, or manages multiple learning projects. Not for open-ended reflection or talking things through (that is the coach skill).
metadata:
  distribution:
    publish_anthropic: true
    plugin_name: self-learning
    plugin_version: 0.1.0
    plugin_author: Taivo Marketplace
---

# Self-Learning

Help the user learn faster in real work contexts. Most self-learning fails because goals are vague, sessions turn into passive content consumption, progress is never reviewed, and consistency drops without accountability. This skill closes those gaps with a lightweight but strict workflow built on one hierarchy:

1. Learning goal (2-3 month outcome)
2. Theme (1-2 week focus)
3. Topics (session-sized chunks)
4. Daily session (intention, active practice, review)

Keep every plan tied to the user's current work context.

## Workspace

All state lives in a directory the user owns — never inside this skill's install directory (it is replaced on plugin updates). Default to `~/self-learning/`; on first use, confirm the location with the user, then create:

- `index.md` — project registry: a table with columns `Slug | Title | Status | Goal | Current Theme | Last Session | Next Session`
- `profiles/main.md` — from `templates/profile.template.md`
- `projects/<slug>/project.md` — from `templates/project.template.md`
- `projects/<slug>/daily/YYYY-MM-DD.md` — from `templates/daily-session.template.md`
- `projects/<slug>/reviews/YYYY-WW.md` — from `templates/weekly-review.template.md`
- `archive/<slug>/` — archived project history, closed with `templates/archive-note.template.md`

## Daily Session Workflow

1. **Select project.** Read `index.md`. If several projects are active, list them briefly and choose one with the user. Confirm status and current theme from its `project.md`. Write only to the selected project's files.
2. **Verify theme.** It must be outcome-oriented and useful in near-term work. Split it into session-sized topics.
3. **Plan active practice.** Build, explain, test, or apply something concrete — never a passive-only plan. Write the session in the daily template format.
4. **Record review metrics.** Focus score (`0/20/40/60/80/100`), challenge (`too easy` / `sweet spot` / `too difficult`), progress (`yes`/`no`), and one adjustment for next session.
5. **Update state.** Set a concrete next-session intent and expected artifact, verify accountability exists, and update the `index.md` last/next session fields.

## Weekly Review

1. Summarize outcomes and what was applied at work.
2. Inspect metric trends (focus / challenge / progress).
3. Keep, adjust, or replace the theme accordingly.
4. Commit the next 3 sessions.

Use the weekly-review template.

## Guardrails

Every session plan must be:

- **Active**: produces evidence (code, memo, diagram, notes, decision) — not just watching or reading
- **Relevant**: tied to real, current work
- **Concrete**: specific tasks with tangible output
- **Challenging**: beyond comfort zone but tractable

Revise the plan before finalizing if any of these fail. Accountability is required before finalizing a weekly plan — prefer, in order: manager check-in, buddy/peer check-in, public updates, personal commitment log.

## Defaults

Use defaults first to reduce option overload:

1. Session length: 60 minutes
2. Weekly plan: next 3 sessions
3. Accountability: manager check-in
4. If uncertain between options, present at most 3 and recommend one

## Calibration and Recovery

- Repeated `too easy`: increase implementation depth and evaluation rigor.
- Repeated `too difficult`: reduce scope to one high-value active step.
- Learner fell off: restart with one smaller session, re-scope the theme, re-establish accountability, and set the next session time immediately.

Keep active practice in all cases.

## Project Lifecycle

Statuses: `active`, `paused`, `archived`. Multiple active projects are allowed, but each daily session targets exactly one. Archive projects that are completed, intentionally parked, or stale; reactivation creates a fresh active project record linking to the archived history.

## References

- `references/examples.md` — pseudonymized worked examples of goals, themes, sessions, and adjustments
- `templates/` — markdown templates for all workspace files
