"""Concrete rule engine for executing validation rules."""

from __future__ import annotations

from typing import Iterable, List

from udvoe.domain.abstractions.data_batch import DataBatch
from udvoe.domain.abstractions.rule_engine import RuleEngine
from udvoe.domain.abstractions.validation_result import ValidationResult
from udvoe.domain.abstractions.validation_rule import ValidationRule


class SimpleRuleEngine(RuleEngine):
    """Executes a collection of validation rules against data batches."""

    def __init__(self, rules: Iterable[ValidationRule]) -> None:
        self._rules: List[ValidationRule] = list(rules)

    def register_rules(self, rules: Iterable[ValidationRule]) -> None:
        self._rules.extend(rules)

    def validate(self, *, batch: DataBatch) -> Iterable[ValidationResult]:
        results: List[ValidationResult] = []
        for rule in self._rules:
            if rule.applies_to(batch):
                results.extend(rule.validate(batch=batch))
        return results

    def metadata(self) -> dict[str, str]:
        return {"rule_count": str(len(self._rules))}
