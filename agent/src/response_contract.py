"""Structured support output; the evaluator checks its business semantics."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference: str
    title: str


class SupportResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str
    decision: Literal[
        "recalled", "no_recall", "needs_batch", "unknown", "compatible",
        "incompatible", "recommendation", "eligible", "ineligible", "needs_order",
        "escalation", "refusal", "unavailable", "remembered", "forgotten",
        "preference",
    ]
    product_id: str | None
    batch: str | None
    citations: list[Citation]
    synthetic: Literal[True]
