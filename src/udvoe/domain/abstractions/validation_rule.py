"""Abstract definition of a validation rule."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Mapping


class ValidationRule(ABC):
    """Defines a single validation rule for a data batch or record."""

    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Return a unique identifier for the rule."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a human-readable summary of the rule."""

    @abstractmethod
    def applies_to(self, batch: "DataBatch") -> bool:
        """Return whether the rule should run for the provided batch."""

    @abstractmethod
    def validate(
        self, *, batch: "DataBatch"
    ) -> Iterable["ValidationResult"]:
        """Validate a batch and yield validation results."""

    @abstractmethod
    def metadata(self) -> Mapping[str, str]:
        """Return metadata describing the rule (e.g., severity)."""
