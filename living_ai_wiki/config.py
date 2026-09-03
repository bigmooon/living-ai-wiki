from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when an experiment configuration violates the repository contract."""


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from *path*."""
    if not path.is_file():
        raise ConfigError(f"Config file does not exist: {path}")

    with path.open(encoding="utf-8") as stream:
        payload = yaml.safe_load(stream)

    if not isinstance(payload, dict):
        raise ConfigError(f"Config root must be a mapping: {path}")
    return payload


def validate_experiment_config(path: Path) -> dict[str, Any]:
    """Validate the minimum config-to-result experiment contract."""
    payload = load_yaml(path)
    required = {"schema_version", "experiment_id", "corpus", "dataset", "evaluation", "output"}
    missing = sorted(required.difference(payload))
    if missing:
        raise ConfigError(f"Missing required keys: {', '.join(missing)}")

    output = payload["output"]
    if not isinstance(output, dict) or output.get("overwrite") is not False:
        raise ConfigError("output.overwrite must be false")

    corpus = payload["corpus"]
    if not isinstance(corpus, dict) or corpus.get("directory") != "sources":
        raise ConfigError("corpus.directory must be 'sources'")

    return payload
