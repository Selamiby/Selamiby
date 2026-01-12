#!/usr/bin/env python3
"""Data Validator - Input validation"""

from typing import Any, Dict, List


class DataValidator:
    """Validate data types and formats"""

    def __init__(self):
        self.rules: Dict = {}

    def add_rule(self, field: str, rules: Dict):
        self.rules[field] = rules

    def validate(self, data: Dict) -> tuple:
        errors = []

        for field, rules in self.rules.items():
            if field not in data:
                if rules.get("required"):
                    errors.append(f"Missing required field: {field}")
                continue

            value = data[field]

            # Type check
            if "type" in rules:
                if not isinstance(value, rules["type"]):
                    errors.append(f"Field {field} must be {rules['type'].__name__}")

            # Length check
            if "min_length" in rules and len(str(value)) < rules["min_length"]:
                errors.append(f"Field {field} too short")

            if "max_length" in rules and len(str(value)) > rules["max_length"]:
                errors.append(f"Field {field} too long")

        return len(errors) == 0, errors
