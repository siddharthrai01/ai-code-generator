"""Abstract definition of a validation result."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping, Optional


class ValidationResult(ABC):
    """Represents the outcome of applying a validation rule."""

    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Return the identifier of the rule that produced this result."""

    @property
    @abstractmethod
    def batch_id(self) -> str:
        """Return the batch identifier associated with this result."""

    @property
    @abstractmethod
    def passed(self) -> bool:
        """Return whether the validation passed."""

    @property
    @abstractmethod
    def message(self) -> Optional[str]:
        """Return an optional human-readable message."""

    @abstractmethod
    def metadata(self) -> Mapping[str, str]:
        """Return structured metadata for observability and reporting."""
