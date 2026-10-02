"""Scenario DSL v0.1: validate (JSON Schema + semantics against a model's data) and apply to a base model.

See ``SPEC.md`` in this directory for the grammar and the worked examples.
"""
from .validate import SCHEMA, ValidationError, validate_scenario, validate_syntax  # noqa: F401
from .apply import apply_data_changes, apply_scenario, scenario_hash  # noqa: F401
