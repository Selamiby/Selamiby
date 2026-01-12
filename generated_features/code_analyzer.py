#!/usr/bin/env python3
"""Code Analyzer - Kod analizi"""
import ast


class CodeAnalyzer:
    """Kod analiz sistemi"""

    def analyze_file(self, filepath: str) -> dict:
        """Dosya analizi"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            return {
                "functions": len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                ),
                "classes": len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                ),
                "lines": len(open(filepath, "r", encoding="utf-8").readlines()),
            }
        except:
            return {"error": True}
