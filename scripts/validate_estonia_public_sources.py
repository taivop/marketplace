#!/usr/bin/env python3
"""Validate the Estonia public-sources routing catalog and source recipes."""

from __future__ import annotations

import ast
from pathlib import Path
import re
import sys

from skill_metadata import read_frontmatter, repo_root


SOURCE_REF_RE = re.compile(r"`sources/([a-z0-9-]+)`")
COUNT_CLAIM_RE = re.compile(
    r"\b\d+\s+(?:available\s+)?(?:data\s+)?sources\b", re.IGNORECASE
)


def main() -> int:
    root = repo_root()
    package = root / "skills" / ".curated" / "estonia-public-sources"
    source_root = package / "sources"
    map_path = package / "SOURCE_MAP.md"
    smoke_path = root / "scripts" / "smoke_estonia_public_sources.py"
    errors: list[str] = []

    if not map_path.is_file():
        print(f"ERROR: missing canonical source catalog: {map_path}")
        return 1

    map_text = map_path.read_text(encoding="utf-8")
    catalog_sources = set(SOURCE_REF_RE.findall(map_text))
    source_paths = sorted(source_root.glob("*/SKILL.md"))
    recipe_sources = {path.parent.name for path in source_paths}

    for missing in sorted(catalog_sources - recipe_sources):
        errors.append(f"catalog references missing recipe: sources/{missing}")
    for unlisted in sorted(recipe_sources - catalog_sources):
        errors.append(f"source recipe is absent from SOURCE_MAP.md: sources/{unlisted}")

    if not smoke_path.is_file():
        errors.append(f"missing source smoke checks: {smoke_path}")
        smoke_sources: set[str] = set()
    else:
        smoke_tree = ast.parse(smoke_path.read_text(encoding="utf-8"))
        smoke_sources = set()
        for node in smoke_tree.body:
            if not isinstance(node, ast.AnnAssign):
                continue
            if not isinstance(node.target, ast.Name) or node.target.id != "CHECKS":
                continue
            if isinstance(node.value, ast.Dict):
                smoke_sources = {
                    key.value
                    for key in node.value.keys
                    if isinstance(key, ast.Constant) and isinstance(key.value, str)
                }
            break
        if not smoke_sources:
            errors.append(f"could not read CHECKS mapping: {smoke_path}")

    for missing in sorted(recipe_sources - smoke_sources):
        errors.append(f"source recipe has no smoke check: sources/{missing}")
    for stale in sorted(smoke_sources - recipe_sources):
        errors.append(f"smoke check has no source recipe: sources/{stale}")

    for path in source_paths:
        try:
            frontmatter = read_frontmatter(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"frontmatter parse failed: {path}: {exc}")
            continue

        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if name != path.parent.name:
            errors.append(
                f"source name/path mismatch: {path.parent.name} has name={name!r}"
            )
        if not isinstance(description, str) or not description.strip():
            errors.append(f"source description is missing: {path}")

    entry_points = [
        package / "SKILL.md",
        package / "skills" / "query" / "SKILL.md",
    ]
    for path in entry_points:
        text = path.read_text(encoding="utf-8")
        if "SOURCE_MAP.md" not in text:
            errors.append(f"entry point does not route through SOURCE_MAP.md: {path}")
        if COUNT_CLAIM_RE.search(text):
            errors.append(f"entry point contains a hard-coded source count: {path}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"failed with {len(errors)} error(s)")
        return 1

    print(
        f"ok: validated {len(recipe_sources)} source recipes and "
        f"{len(catalog_sources)} catalog entries"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
