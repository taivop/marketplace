#!/usr/bin/env python3
"""Helpers for reading package metadata from SKILL.md frontmatter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---(?:\n|$)", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^( *)([A-Za-z0-9_-]+):(.*)$")
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9-]+$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class DistributionSettings:
    publish_anthropic: bool
    plugin_name: str
    plugin_version: str
    plugin_author: str | None


@dataclass
class SkillPackage:
    path: Path
    rel_path: Path
    folder_name: str
    skill_name: str
    description: str
    distribution: DistributionSettings


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if value == "":
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_frontmatter_block(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = KEY_VALUE_RE.match(line)
        if not match:
            raise ValueError(f"Unsupported frontmatter line {line_no}: {line}")
        indent = len(match.group(1))
        if indent % 2 != 0:
            raise ValueError(f"Invalid indentation at line {line_no}: {line}")

        key = match.group(2)
        raw_value = match.group(3).lstrip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"Invalid frontmatter structure near line {line_no}")
        parent = stack[-1][1]

        if raw_value == "":
            nested: dict[str, Any] = {}
            parent[key] = nested
            stack.append((indent, nested))
        else:
            parent[key] = parse_scalar(raw_value)

    return root


def read_frontmatter(skill_md_path: Path) -> dict[str, Any]:
    content = skill_md_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"No frontmatter found in {skill_md_path}")
    return parse_frontmatter_block(match.group(1))


def _as_str(value: Any, default: str | None = None) -> str | None:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False
    if isinstance(value, int):
        return value != 0
    return default


def _distribution_settings(
    folder_name: str, metadata: dict[str, Any]
) -> DistributionSettings:
    distribution = metadata.get("distribution", {})
    if not isinstance(distribution, dict):
        distribution = {}

    plugin_name = _as_str(distribution.get("plugin_name"), folder_name) or folder_name
    if not PLUGIN_NAME_RE.match(plugin_name):
        raise ValueError(
            f"Invalid plugin_name '{plugin_name}' in {folder_name}; expected [a-z0-9-]+"
        )

    plugin_version = (
        _as_str(distribution.get("plugin_version"), "1.0.0") or "1.0.0"
    )
    if not VERSION_RE.match(plugin_version):
        raise ValueError(
            f"Invalid plugin_version '{plugin_version}' in {folder_name}; expected X.Y.Z"
        )

    publish_anthropic = _as_bool(distribution.get("publish_anthropic"), True)
    plugin_author = _as_str(distribution.get("plugin_author"))

    return DistributionSettings(
        publish_anthropic=publish_anthropic,
        plugin_name=plugin_name,
        plugin_version=plugin_version,
        plugin_author=plugin_author or None,
    )


def iter_skill_packages(root: Path | None = None) -> list[SkillPackage]:
    repo = root or repo_root()
    packages: list[SkillPackage] = []
    skills_dir = repo / "skills"

    if not skills_dir.is_dir():
        return packages

    package_dirs = sorted(
        path
        for path in skills_dir.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    for child in package_dirs:
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue

        fm = read_frontmatter(skill_md)
        skill_name = _as_str(fm.get("name"), "") or ""
        description = _as_str(fm.get("description"), "") or ""
        if not skill_name:
            raise ValueError(f"Missing frontmatter name in {skill_md}")
        if not description:
            raise ValueError(f"Missing frontmatter description in {skill_md}")

        metadata = fm.get("metadata", {})
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise ValueError(
                f"metadata must be a mapping in {skill_md}, got {type(metadata)}"
            )

        settings = _distribution_settings(child.name, metadata)

        packages.append(
            SkillPackage(
                path=child,
                rel_path=child.relative_to(repo),
                folder_name=child.name,
                skill_name=skill_name,
                description=description,
                distribution=settings,
            )
        )

    return packages
