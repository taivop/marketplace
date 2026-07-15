# Project Agent Notes

The package must work through both its Codex entry point (`SKILL.md`) and Claude command (`skills/query/SKILL.md`). Both route through `SOURCE_MAP.md`, which is the canonical source catalog.

## Source Inclusion Criteria

Include a new source skill only when it meets all of these:

1. Official and authoritative.
2. Publicly accessible in practice (API, direct download, or stable UI flow with reproducible steps).
3. Governance-relevant records (operations, decisions, spending, enforcement, registries, oversight, or service delivery).
4. Repeatable workflow that an LLM can execute reliably.
5. Non-duplicate coverage versus existing source skills (extend existing skills instead of creating duplicates).

Exclude by default:

1. News/PR pages without durable records.
2. Sources where useful data is mostly non-public.
3. Highly unstable sources with low reuse value.
4. Very narrow one-off topics with low expected reuse.
5. Pages that only describe a system but do not provide practical public data access.

## Recipe Standard

Every `sources/<slug>/SKILL.md` must give a fresh agent the shortest reliable path to a real public record. Include only what changes retrieval:

1. Exact API, download, or public browser endpoint.
2. Required parameters, headers, session steps, or UI inputs.
3. Expected response type and identifying fields.
4. Source-specific coverage, access, pagination, or interpretation limits.
5. A semantic check in `scripts/smoke_estonia_public_sources.py` that proves useful records were returned.

Do not add generic Inputs, Outputs, Access Reality, or Human Setup sections merely to make a recipe look complete. Merge recipes that share an interface when one focused recipe can route both topics.

## Removal / Rejection Rule

Drop (or do not add) a source skill when it fails the practical-access test:

1. The source only provides narrative/context pages and no repeatable way to extract governance-relevant records.
2. The workflow cannot be executed reliably by an LLM, even with human-guided clicks.
3. The same coverage is already provided by another source with better practical access.

When dropping a source, remove its references from `SOURCE_MAP.md`. Do not add source indexes or numeric source claims to `README.md`, root `SKILL.md`, or the Claude command.
