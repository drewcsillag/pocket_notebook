"""Utility functions"""

from typing import IO


def create_output_file(name) -> IO:
    """Create an output file in a way that makes pylint happy"""
    return open(name, "w", encoding="utf-8")
