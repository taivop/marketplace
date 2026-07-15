# Estonian Public Sources

This package routes Estonian public-data questions to acquisition recipes for official APIs, downloads, and public web interfaces.

## Usage

Codex loads the package-level `SKILL.md`. Claude can also use the explicit command:

```
/estonia-public-sources:query millised keskkonnaload on Tallinnale väljastatud?
```

```
/estonia-public-sources:query procurement contracts for IT services in 2025
```

```
/estonia-public-sources:query äriregistri andmed ettevõtte X kohta
```

Both entry points use `SOURCE_MAP.md` as the canonical routing catalog and the same recipes under `sources/`.

## Structure

```text
.
├── AGENTS.md
├── SKILL.md
├── SOURCE_MAP.md
├── skills/
│   └── query/
│       └── SKILL.md        ← slash command entry point
└── sources/
    ├── <source-skill-slug-1>/
    │   └── SKILL.md
    ├── <source-skill-slug-2>/
    │   └── SKILL.md
    └── ...
```

## Inclusion rule

A source stays in the package only when a fresh agent can retrieve a useful public record through its documented workflow. Descriptive pages, inaccessible systems, and duplicate topic wrappers are removed rather than counted as coverage.
