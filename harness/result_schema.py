from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class RunMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    config_path: str
    git_commit: str
    corpus_tag: str
    repetition: int = Field(ge=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    models: dict[str, str]


class QuestionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str
    question_type: Literal["pinpoint", "synthesis", "multihop"]
    answerable: bool
    retrieved_source_ids: list[str]
    metrics: dict[str, float | int | None]
    answer: str | None = None
    provenance: list[dict[str, Any]] = Field(default_factory=list)


class ExperimentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metadata: RunMetadata
    results: list[QuestionResult]
    aggregate: dict[str, Any]
