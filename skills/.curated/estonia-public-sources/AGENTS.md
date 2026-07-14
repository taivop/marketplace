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

## Mandatory SKILL.md Quality Standard

Every `sources/<slug>/SKILL.md` must contain enough detail for a fresh agent to actually retrieve data, not just describe it.

Required minimum content:

1. **Access reality statement**
   - Explicitly state whether access is `API`, `download files`, `UI export`, `UI copy-only`, or `no public machine-readable data`.
2. **Primary endpoints**
   - Include concrete, currently reachable URLs (not just homepages).
3. **Retrieval workflow with reproducible steps**
   - Step-by-step actions including filters/inputs needed to obtain records.
4. **Request/query contract (when applicable)**
   - Required parameters, accepted values, required headers, auth/session constraints, and expected response format.
5. **Output schema expectations**
   - List key fields the extractor should return (with exact source naming when possible).
6. **Limits and caveats**
   - Language constraints, anti-bot/session behavior, pagination, stale coverage windows, and auth boundaries.
7. **Verification hooks**
   - At least one concrete check (example file name, response type, update date field, record count sanity check, etc.).

## Removal / Rejection Rule

Drop (or do not add) a source skill when it fails the practical-access test:

1. The source only provides narrative/context pages and no repeatable way to extract governance-relevant records.
2. The workflow cannot be executed reliably by an LLM, even with human-guided clicks.
3. The same coverage is already provided by another source with better practical access.

When dropping a source, remove its references from `SOURCE_MAP.md`. Do not add source indexes or numeric source claims to `README.md`, root `SKILL.md`, or the Claude command.
