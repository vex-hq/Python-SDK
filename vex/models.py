from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, model_validator


class ThresholdConfig(BaseModel):
    pass_threshold: float = 0.8
    flag_threshold: float = 0.5
    block_threshold: float = 0.3

    @model_validator(mode="after")
    def validate_threshold_order(self) -> ThresholdConfig:
        if not (self.block_threshold < self.flag_threshold < self.pass_threshold):
            raise ValueError(
                "Thresholds must satisfy: block < flag < pass. "
                f"Got block={self.block_threshold}, flag={self.flag_threshold}, "
                f"pass={self.pass_threshold}"
            )
        return self


class ConversationTurn(BaseModel):
    """A single turn in a multi-turn conversation.

    Used by Session to accumulate conversation history for cross-turn
    verification (hallucination, drift, coherence).
    """

    sequence_number: int
    input: Any = None
    output: Any = None
    task: str | None = None


class StepRecord(BaseModel):
    step_type: str  # "tool_call", "llm", "custom"
    name: str
    input: Any = None
    output: Any = None
    duration_ms: float | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExecutionEvent(BaseModel):
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str | None = None
    parent_execution_id: str | None = None
    sequence_number: int | None = None
    agent_id: str
    task: str | None = None
    input: Any
    output: Any
    steps: list[StepRecord] = Field(default_factory=list)
    token_count: int | None = None
    cost_estimate: float | None = None
    latency_ms: float | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ground_truth: Any = None
    schema_definition: dict[str, Any] | None = None
    conversation_history: list[ConversationTurn] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    experiment_id: str | None = None
    variant: str | None = None


class VexResult(BaseModel):
    output: Any
    confidence: float | None = None
    action: str = "pass"  # "pass" | "flag" | "block"
    corrections: list[dict[str, Any]] | None = None
    execution_id: str
    verification: dict[str, Any] | None = None
    corrected: bool = False
    original_output: Any | None = None
