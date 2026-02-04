"""In-memory data source for testing and examples."""

from __future__ import annotations

from typing import Iterable, List, Mapping, Sequence

from udvoe.domain.abstractions.data_batch import DataBatch
from udvoe.domain.abstractions.data_source import DataSource


class InMemoryDataBatch(DataBatch):
    """Simple data batch backed by in-memory records."""

    def __init__(
        self,
        *,
        batch_id: str,
        source_name: str,
        records: Sequence[Mapping[str, object]],
        schema: Mapping[str, object],
    ) -> None:
        self._batch_id = batch_id
        self._source_name = source_name
        self._records = list(records)
        self._schema = dict(schema)

    @property
    def batch_id(self) -> str:
        return self._batch_id

    @property
    def source_name(self) -> str:
        return self._source_name

    def records(self) -> Iterable[Mapping[str, object]]:
        return list(self._records)

    def metadata(self) -> Mapping[str, str]:
        return {"record_count": str(len(self._records))}

    @property
    def schema(self) -> Mapping[str, object]:
        """Return the schema associated with the batch."""
        return dict(self._schema)


class InMemoryDataSource(DataSource):
    """Data source that serves a single in-memory batch for testing."""

    def __init__(
        self,
        *,
        name: str,
        records: Sequence[Mapping[str, object]],
        schema: Mapping[str, object],
        batch_id: str = "in-memory-batch",
    ) -> None:
        self._name = name
        self._records = list(records)
        self._schema = dict(schema)
        self._batch_id = batch_id

    @property
    def name(self) -> str:
        return self._name

    def fetch_batches(self, *, limit: int | None = None) -> Iterable[DataBatch]:
        batch = InMemoryDataBatch(
            batch_id=self._batch_id,
            source_name=self._name,
            records=self._records,
            schema=self._schema,
        )
        batches: List[DataBatch] = [batch]
        if limit is None:
            return batches
        return batches[:limit]

    def metadata(self) -> Mapping[str, str]:
        return {"batch_id": self._batch_id}
