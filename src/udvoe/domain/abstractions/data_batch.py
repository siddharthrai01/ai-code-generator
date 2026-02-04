"""Abstract definition of a batch of data to validate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Mapping


class DataBatch(ABC):
    """Represents a bounded set of data records from a source."""

    @property
    @abstractmethod
    def batch_id(self) -> str:
        """Return a unique identifier for the batch."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the originating data source name."""

    @abstractmethod
    def records(self) -> Iterable[Mapping[str, object]]:
        """Return the data records contained in this batch."""

    @abstractmethod
    def metadata(self) -> Mapping[str, str]:
        """Return metadata describing the batch (e.g., timestamps)."""
