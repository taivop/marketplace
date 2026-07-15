#!/usr/bin/env python3
"""Validate Codex skill package structure and SKILL frontmatter."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from skill_metadata import VERSION_RE, iter_skill_packages, read_frontmatter, repo_root


def _check(cond: bool, message: str, errors: list[str]) -> None:
    if not cond:
        errors.append(message)


def main() -> int:
    root = repo_root()
    errors: list[str] = []
    checked_dirs = 0
    skills_dir = root / "skills"

    _check(skills_dir.is_dir(), f"missing skills directory: {skills_dir}", errors)
    package_dirs = (
        sorted(
            child
            for child in skills_dir.iterdir()
            if child.is_dir() and not child.name.startswith(".")
        )
        if skills_dir.is_dir()
        else []
    )

    for child in package_dirs:
        checked_dirs += 1
        skill_md = child / "SKILL.md"
        _check(skill_md.is_file(), f"missing SKILL.md: {child}", errors)
        if not skill_md.is_file():
            continue

        try:
            fm = read_frontmatter(skill_md)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"frontmatter parse failed: {skill_md}: {exc}")
            continue

        name = fm.get("name")
        desc = fm.get("description")
        _check(
            isinstance(name, str) and bool(name.strip()),
            f"invalid frontmatter name in {skill_md}",
            errors,
        )
        _check(
            isinstance(desc, str) and bool(desc.strip()),
            f"invalid frontmatter description in {skill_md}",
            errors,
        )

        metadata = fm.get("metadata", {})
        if metadata is None:
            metadata = {}
        _check(
            isinstance(metadata, dict),
            f"metadata must be mapping in {skill_md}",
            errors,
        )
        if not isinstance(metadata, dict):
            continue

        distribution = metadata.get("distribution", {})
        if distribution is None:
            distribution = {}
        _check(
            isinstance(distribution, dict),
            f"metadata.distribution must be mapping in {skill_md}",
            errors,
        )
        if not isinstance(distribution, dict):
            continue

        plugin_name = distribution.get("plugin_name")
        if plugin_name is not None:
            _check(
                isinstance(plugin_name, str)
                and re.fullmatch(r"[a-z0-9-]+", plugin_name) is not None,
                f"invalid metadata.distribution.plugin_name in {skill_md}",
                errors,
            )

        plugin_version = distribution.get("plugin_version")
        if plugin_version is not None:
            _check(
                isinstance(plugin_version, str)
                and VERSION_RE.fullmatch(plugin_version) is not None,
                f"invalid metadata.distribution.plugin_version in {skill_md}; expected X.Y.Z",
                errors,
            )

    packages = iter_skill_packages(root)
    _check(
        len(packages) > 0,
        "no installable packages found under skills/",
        errors,
    )

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        print(f"failed with {len(errors)} error(s)")
        return 1

    print(f"ok: validated {checked_dirs} package directories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
