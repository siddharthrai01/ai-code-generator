"""Abstract definition of a validation rule engine."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Mapping


class RuleEngine(ABC):
    """Coordinates execution of validation rules over data batches."""

    @abstractmethod
    def register_rules(self, rules: Iterable["ValidationRule"]) -> None:
        """Register validation rules with the engine."""

    @abstractmethod
    def validate(
        self, *, batch: "DataBatch"
    ) -> Iterable["ValidationResult"]:
        """Execute validation rules for a batch and yield results."""

    @abstractmethod
    def metadata(self) -> Mapping[str, str]:
        """Return metadata about the engine configuration."""
