#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "HEAD^"
    changed = set(git("diff", "--name-only", f"{base}...HEAD").splitlines())
    source_changes = sorted(path for path in changed if path.startswith("sources/"))
    if source_changes:
        print("sources/ changes are forbidden after the corpus snapshot:", file=sys.stderr)
        print("\n".join(source_changes), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
