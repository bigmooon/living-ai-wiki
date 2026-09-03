from pathlib import Path

import pytest

from living_ai_wiki.config import ConfigError, validate_experiment_config


def test_b0_config_respects_append_only_contract() -> None:
    payload = validate_experiment_config(Path("config/experiments/b0.yaml"))

    assert payload["experiment_id"] == "b0-full-context"
    assert payload["output"]["overwrite"] is False


def test_invalid_output_contract_is_rejected(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text(
        """
schema_version: 1
experiment_id: invalid
corpus: {directory: sources}
dataset: {path: evals/questions.jsonl}
evaluation: {repetitions: 1}
output: {directory: evals/results, overwrite: true}
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="overwrite"):
        validate_experiment_config(config_path)
