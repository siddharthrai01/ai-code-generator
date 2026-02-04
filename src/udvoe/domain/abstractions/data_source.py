"""Abstract definition of a data source for validation workflows."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Optional


class DataSource(ABC):
    """Represents a logical source of data batches for validation.

    Implementations provide access to raw or structured data, encapsulating
    connection details, authentication, and retrieval semantics.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a human-readable identifier for the data source."""

    @abstractmethod
    def fetch_batches(
        self, *, limit: Optional[int] = None
    ) -> Iterable["DataBatch"]:
        """Yield data batches available for validation.

        Args:
            limit: Optional maximum number of batches to return.
        """

    @abstractmethod
    def metadata(self) -> Mapping[str, str]:
        """Return descriptive metadata about the source."""
