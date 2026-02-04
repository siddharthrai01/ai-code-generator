"""YAML rule specification loader and validator.

This module intentionally implements a minimal YAML reader without external
libraries. It supports a constrained subset of YAML needed for rule specs:
- Top-level mappings with scalar values.
- A `validations` key containing a list of mappings.
- Indentation with two spaces for list items and nested mappings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


class RuleSpecError(ValueError):
    """Base error for rule specification parsing and validation."""


class RuleSpecParseError(RuleSpecError):
    """Raised when the YAML cannot be parsed into a rule specification."""


class RuleSpecValidationError(RuleSpecError):
    """Raised when the rule specification fails validation."""


@dataclass(frozen=True)
class RuleSpec:
    """Normalized representation of a rule specification."""

    version: str
    data_source: str
    validations: List[Mapping[str, Any]]
    metadata: Mapping[str, Any]


def load_rule_spec(path: str) -> RuleSpec:
    """Load a rule specification from a YAML file path.

    Args:
        path: Path to a YAML rule specification file.

    Raises:
        RuleSpecParseError: If the YAML cannot be parsed.
        RuleSpecValidationError: If required fields are missing or invalid.
    """

    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read()

    payload = parse_yaml(content)
    return validate_rule_spec(payload)


def parse_yaml(content: str) -> Mapping[str, Any]:
    """Parse a limited YAML subset into a Python mapping."""

    lines = _strip_empty_and_comment_lines(content.splitlines())
    if not lines:
        raise RuleSpecParseError("YAML content is empty.")

    index = 0
    result: Dict[str, Any] = {}

    while index < len(lines):
        line = lines[index]
        if line.startswith("-"):
            raise RuleSpecParseError("Top-level YAML must be a mapping.")

        key, value, indent = _parse_mapping_line(line)
        if indent != 0:
            raise RuleSpecParseError("Top-level keys must not be indented.")

        if value is None:
            if key == "validations":
                items, index = _parse_list(lines, index + 1, indent + 2)
                result[key] = items
            else:
                mapping, index = _parse_nested_mapping(lines, index + 1, indent + 2)
                result[key] = mapping
        else:
            result[key] = value
            index += 1

    return result


def validate_rule_spec(payload: Mapping[str, Any]) -> RuleSpec:
    """Validate and normalize a rule specification mapping."""

    required = ("version", "data_source", "validations")
    missing = [field for field in required if field not in payload]
    if missing:
        raise RuleSpecValidationError(
            f"Missing required field(s): {', '.join(sorted(missing))}."
        )

    version = _require_string(payload, "version")
    data_source = _require_string(payload, "data_source")
    validations = _require_list(payload, "validations")

    if not validations:
        raise RuleSpecValidationError("The validations list must not be empty.")

    for index, validation in enumerate(validations):
        if not isinstance(validation, Mapping):
            raise RuleSpecValidationError(
                f"Validation entry at index {index} must be a mapping."
            )

    metadata = {
        key: value
        for key, value in payload.items()
        if key not in required
    }

    return RuleSpec(
        version=version,
        data_source=data_source,
        validations=list(validations),
        metadata=metadata,
    )


def _strip_empty_and_comment_lines(lines: Iterable[str]) -> List[str]:
    stripped: List[str] = []
    for line in lines:
        raw = line.rstrip()
        if not raw:
            continue
        if raw.lstrip().startswith("#"):
            continue
        stripped.append(raw)
    return stripped


def _parse_mapping_line(line: str) -> tuple[str, Optional[str], int]:
    if ":" not in line:
        raise RuleSpecParseError(f"Invalid mapping line: '{line}'.")

    indent = len(line) - len(line.lstrip(" "))
    key, remainder = line.split(":", 1)
    key = key.strip()
    remainder = remainder.strip()

    if not key:
        raise RuleSpecParseError(f"Empty key in line: '{line}'.")

    if remainder == "":
        return key, None, indent
    return key, _parse_scalar(remainder), indent


def _parse_list(lines: List[str], start: int, indent: int) -> tuple[List[Any], int]:
    items: List[Any] = []
    index = start

    while index < len(lines):
        line = lines[index]
        if len(line) - len(line.lstrip(" ")) < indent:
            break

        if not line.lstrip().startswith("-"):
            break

        item_content = line[indent - 2 :].lstrip()[1:].strip()
        if item_content:
            items.append(_parse_scalar(item_content))
            index += 1
            continue

        mapping, index = _parse_nested_mapping(lines, index + 1, indent + 2)
        items.append(mapping)

    if not items:
        raise RuleSpecParseError("Expected at least one list item.")

    return items, index


def _parse_nested_mapping(
    lines: List[str], start: int, indent: int
) -> tuple[Dict[str, Any], int]:
    mapping: Dict[str, Any] = {}
    index = start

    while index < len(lines):
        line = lines[index]
        line_indent = len(line) - len(line.lstrip(" "))
        if line_indent < indent:
            break

        if line_indent != indent:
            raise RuleSpecParseError(
                f"Unexpected indentation at line: '{line}'."
            )

        key, value, _ = _parse_mapping_line(line)
        if value is None:
            nested_mapping, index = _parse_nested_mapping(
                lines, index + 1, indent + 2
            )
            mapping[key] = nested_mapping
        else:
            mapping[key] = value
            index += 1

    if not mapping:
        raise RuleSpecParseError("Expected a mapping block but found none.")

    return mapping, index


def _parse_scalar(value: str) -> str:
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _require_string(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise RuleSpecValidationError(f"Field '{key}' must be a non-empty string.")
    return value


def _require_list(payload: Mapping[str, Any], key: str) -> List[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise RuleSpecValidationError(f"Field '{key}' must be a list.")
    return value
