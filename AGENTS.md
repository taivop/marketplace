# Marketplace Agent Guide

This repository is a dual-distribution marketplace for reusable agent plugins:

1. Anthropic Claude Code marketplace plugins.
2. Codex installable skills.

It is not limited to public-data skills. Any useful, reusable agent plugin can live here (for example, future additions such as `skill-self-coaching`).

## Core Layout

```text
.
├── .claude-plugin/marketplace.json
├── skills/
│   └── <plugin-package>/
│       ├── SKILL.md
│       ├── .claude-plugin/plugin.json
│       └── ...
├── scripts/
│   ├── generate_plugin_manifests.py
│   ├── generate_marketplace.py
│   ├── validate_codex_skills.py
│   └── validate_anthropic_plugins.py
└── .github/workflows/validate-distribution.yml
```

## Source Of Truth

For each package, `SKILL.md` frontmatter is authoritative.

Expected frontmatter fields:

1. Required:
   - `name`
   - `description`
2. Distribution metadata (recommended and used by generators):
   - `metadata.distribution.publish_anthropic`: `true`/`false`
   - `metadata.distribution.plugin_name`: Anthropic plugin name
   - `metadata.distribution.plugin_version`: SemVer (`X.Y.Z`)
   - `metadata.distribution.plugin_author`: display author name

Generated files:

1. `<package>/.claude-plugin/plugin.json`
2. `/.claude-plugin/marketplace.json`

Do not hand-edit generated files. Run generators instead.

## Add A New Plugin Package

1. Create the package directory at `skills/<slug>`.
2. Add `SKILL.md` with valid frontmatter.
3. Add any package-specific resources (`agents/`, `scripts/`, `references/`, `assets/`, docs).
4. Set `metadata.distribution.*` values in `SKILL.md`.
5. Run generation + validation:
   - `python3 scripts/generate_plugin_manifests.py`
   - `python3 scripts/generate_marketplace.py`
   - `python3 scripts/validate_codex_skills.py`
   - `python3 scripts/validate_anthropic_plugins.py`
6. Ensure clean generation check:
   - `python3 scripts/generate_plugin_manifests.py --check`
   - `python3 scripts/generate_marketplace.py --check`

## Update Existing Plugin Package

1. Edit package content and/or `SKILL.md`.
2. Regenerate manifests.
3. Re-run validators.
4. Commit package changes together with regenerated manifests.

## CI Expectations

CI runs:

1. Codex structure/frontmatter validation.
2. Anthropic manifest/marketplace validation.
3. Generation drift check (`git diff --exit-code` after generation).

A PR should fail if:

1. `SKILL.md` metadata is invalid.
2. Generated files are stale.
3. Marketplace or plugin JSON is malformed.

## Working Conventions

1. Keep package names and plugin names kebab-case.
2. Keep version increments explicit in `metadata.distribution.plugin_version`.
3. Keep package-specific operational rules inside that package's own docs (`README.md`, `AGENTS.md`).
