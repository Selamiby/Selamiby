#!/usr/bin/env python3
"""Smart Logger - Akıllı loglama sistemi"""
import logging
from datetime import datetime


class SmartLogger:
    """Akıllı log sistemi"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def log(self, level: str, message: str):
        """Log mesajı"""
        timestamp = datetime.now().isoformat()
        self.logger.log(getattr(logging, level.upper()), f"[{timestamp}] {message}")

    def info(self, msg: str):
        self.log("info", msg)

    def error(self, msg: str):
        self.log("error", msg)
