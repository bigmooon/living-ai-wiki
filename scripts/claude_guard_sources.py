#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import PurePosixPath
from typing import Any


def find_paths(value: Any) -> list[str]:
    if isinstance(value, dict):
        found: list[str] = []
        for key, child in value.items():
            if key in {"file_path", "path"} and isinstance(child, str):
                found.append(child)
            else:
                found.extend(find_paths(child))
        return found
    if isinstance(value, list):
        return [path for child in value for path in find_paths(child)]
    return []


def is_sources_path(raw_path: str) -> bool:
    normalized = PurePosixPath(raw_path.replace("\\", "/"))
    return "sources" in normalized.parts


def main() -> int:
    raw = os.environ.get("CLAUDE_TOOL_INPUT") or sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print("Unable to parse tool input; refusing write as a safe default", file=sys.stderr)
        return 2

    blocked = [path for path in find_paths(payload) if is_sources_path(path)]
    if blocked:
        print(f"sources/ is read-only: {blocked[0]}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
