#!/usr/bin/env python3
"""Data Validator - Veri doğrulama modülü"""
from typing import Any, Dict, List


class DataValidator:
    """Veri doğrulama sistemi"""

    @staticmethod
    def validate_dict(data: Dict, required_keys: List[str]) -> bool:
        """Dictionary doğrula"""
        return all(key in data for key in required_keys)

    @staticmethod
    def validate_type(data: Any, expected_type: type) -> bool:
        """Tip doğrula"""
        return isinstance(data, expected_type)

    @staticmethod
    def validate_range(value: int, min_val: int, max_val: int) -> bool:
        """Aralık doğrula"""
        return min_val <= value <= max_val
