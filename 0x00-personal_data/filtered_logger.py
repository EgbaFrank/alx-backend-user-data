#!/usr/bin/env python3
"""
replace a string with a given redaction string
"""
import re
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """obfuscated log messages"""
    for field in fields:
        message = re.sub(
            f"{field}=[^{separator}]*", f"{field}={redaction}", message)
    return message
