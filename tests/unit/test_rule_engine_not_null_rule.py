"""Tests for the NotNullRule and SimpleRuleEngine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from udvoe.application.services.rule_engine import SimpleRuleEngine
from udvoe.domain.abstractions.data_batch import DataBatch
from udvoe.domain.abstractions.validation_result import ValidationResult
from udvoe.domain.abstractions.validation_rule import ValidationRule
from udvoe.infrastructure.adapters.in_memory_data_source import InMemoryDataSource


@dataclass(frozen=True)
class InMemoryValidationResult(ValidationResult):
    """Simple validation result for testing."""

    _rule_id: str
    _batch_id: str
    _passed: bool
    _message: str | None

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @property
    def batch_id(self) -> str:
        return self._batch_id

    @property
    def passed(self) -> bool:
        return self._passed

    @property
    def message(self) -> str | None:
        return self._message

    def metadata(self) -> Mapping[str, str]:
        return {}


class NotNullRule(ValidationRule):
    """Rule that asserts a field is not null in any record."""

    def __init__(self, *, field: str, rule_id: str = "not-null") -> None:
        self._field = field
        self._rule_id = rule_id

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @property
    def description(self) -> str:
        return f"Field '{self._field}' must not be null."

    def applies_to(self, batch: DataBatch) -> bool:
        return True

    def validate(self, *, batch: DataBatch) -> Iterable[ValidationResult]:
        passed = all(record.get(self._field) is not None for record in batch.records())
        message = None if passed else f"Nulls found for '{self._field}'."
        return [
            InMemoryValidationResult(
                _rule_id=self.rule_id,
                _batch_id=batch.batch_id,
                _passed=passed,
                _message=message,
            )
        ]

    def metadata(self) -> Mapping[str, str]:
        return {"field": self._field}


def _build_batch(records: list[dict[str, object]]) -> DataBatch:
    source = InMemoryDataSource(
        name="test-source",
        records=records,
        schema={"fields": ["id", "name"]},
    )
    return next(iter(source.fetch_batches()))


def test_not_null_rule_passes_when_field_present() -> None:
    batch = _build_batch([
        {"id": 1, "name": "alpha"},
        {"id": 2, "name": "beta"},
    ])

    rule = NotNullRule(field="name")
    results = list(rule.validate(batch=batch))

    assert len(results) == 1
    assert results[0].passed is True
    assert results[0].message is None


def test_not_null_rule_fails_when_field_missing() -> None:
    batch = _build_batch([
        {"id": 1, "name": None},
        {"id": 2, "name": "beta"},
    ])

    rule = NotNullRule(field="name")
    results = list(rule.validate(batch=batch))

    assert len(results) == 1
    assert results[0].passed is False
    assert results[0].message == "Nulls found for 'name'."


def test_rule_engine_collects_results_for_rules() -> None:
    batch = _build_batch([
        {"id": 1, "name": "alpha"},
        {"id": 2, "name": None},
    ])

    engine = SimpleRuleEngine([NotNullRule(field="name")])
    results = list(engine.validate(batch=batch))

    assert len(results) == 1
    assert results[0].passed is False
