#!/usr/bin/env python3
"""Config Manager - Konfigürasyon yönetimi"""
import json
from pathlib import Path


class ConfigManager:
    """Konfigürasyon yönetim sistemi"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self.load()

    def load(self) -> dict:
        """Konfigürasyon yükle"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        """Konfigürasyon kaydet"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default=None):
        """Değer al"""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Değer ayarla"""
        self.config[key] = value
        self.save()
